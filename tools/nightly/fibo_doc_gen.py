"""Generate Chinese Turtle + structure diagram + markdown doc for a single FIBO RDF file.

Usage:
    python tools/nightly/fibo_doc_gen.py <path/to/File.rdf>

Translations are read from ontology_models/fibo_translations.json. If any local term
is missing a Chinese translation, the script prints the missing terms as JSON and
exits with code 3 without writing outputs.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

from rdflib import Graph, Namespace, RDF, RDFS, OWL, SKOS, DCTERMS, Literal, URIRef, BNode

TRANSLATIONS_PATH = Path(__file__).resolve().parents[2] / "ontology_models" / "fibo_translations.json"
SUMMARIES_PATH = Path(__file__).resolve().parents[2] / "ontology_models" / "fibo_module_summaries.json"
FIBO_PREFIX = "https://spec.edmcouncil.org/fibo/ontology/"


def load_translations() -> dict:
    if TRANSLATIONS_PATH.exists():
        return json.loads(TRANSLATIONS_PATH.read_text(encoding="utf-8"))
    return {"by_label": {}, "by_uri": {}}


def load_summaries() -> dict:
    if SUMMARIES_PATH.exists():
        return json.loads(SUMMARIES_PATH.read_text(encoding="utf-8"))
    return {}


def get_ontology_ns(g: Graph) -> str:
    onts = list(g.subjects(RDF.type, OWL.Ontology))
    if onts:
        return str(onts[0])
    return ""


def english_label(g: Graph, term: URIRef) -> str:
    for lbl in g.objects(term, RDFS.label):
        if isinstance(lbl, Literal) and (lbl.language is None or lbl.language == "en"):
            return str(lbl)
    return str(term).split("/")[-1]


def english_definition(g: Graph, term: URIRef) -> str:
    for d in g.objects(term, SKOS.definition):
        if isinstance(d, Literal) and (d.language is None or d.language == "en"):
            return str(d)
    return ""


def local_terms(g: Graph, ns: str) -> dict[str, dict]:
    terms = {}
    for rdf_type, kind in [
        (OWL.Class, "class"),
        (OWL.ObjectProperty, "object_property"),
        (OWL.DatatypeProperty, "datatype_property"),
        (OWL.AnnotationProperty, "annotation_property"),
    ]:
        for t in g.subjects(RDF.type, rdf_type):
            if not isinstance(t, URIRef) or (ns and not str(t).startswith(ns)):
                continue
            terms[str(t)] = {
                "uri": str(t),
                "kind": kind,
                "label_en": english_label(g, t),
                "definition_en": english_definition(g, t),
            }
    return terms


def find_translation(trans: dict, uri: str, label_en: str) -> dict | None:
    if uri in trans.get("by_uri", {}):
        return trans["by_uri"][uri]
    if label_en in trans.get("by_label", {}):
        return trans["by_label"][label_en]
    return None


def display_label(g: Graph, trans: dict, uri) -> str:
    """Chinese (English) label for any URI, falling back to short URI."""
    if uri is None:
        return ""
    s = str(uri)
    # 1. zh label already in graph
    for l in g.objects(URIRef(s), RDFS.label):
        if isinstance(l, Literal) and l.language == "zh":
            return str(l)
    # 2. display label map (covers imported Commons/FIBO terms)
    if s in trans.get("display_labels", {}):
        return trans["display_labels"][s]
    # 3. English label -> translation
    en = english_label(g, URIRef(s))
    tr = find_translation(trans, s, en)
    if tr:
        return tr["label_zh"]
    # 4. try URI fragment as English label
    frag = s.split("/")[-1].split("#")[-1]
    tr = find_translation(trans, s, frag)
    if tr:
        return tr["label_zh"]
    return short_uri(g, URIRef(s))


def restriction_text(g: Graph, trans: dict, bnode: BNode) -> str:
    on_prop = g.value(bnode, OWL.onProperty)
    on_class = g.value(bnode, OWL.onClass)
    svf = g.value(bnode, OWL.someValuesFrom)
    avf = g.value(bnode, OWL.allValuesFrom)
    min_q = g.value(bnode, OWL.minQualifiedCardinality)
    max_q = g.value(bnode, OWL.maxQualifiedCardinality)
    q = g.value(bnode, OWL.qualifiedCardinality)
    min_c = g.value(bnode, OWL.minCardinality)
    max_c = g.value(bnode, OWL.maxCardinality)
    card = None
    for val, sym in [(q, "="), (min_q, "≥"), (max_q, "≤"), (min_c, "min"), (max_c, "max")]:
        if val is not None:
            card = f"{sym}{val}"
            break
    prop = display_label(g, trans, on_prop) if on_prop else "?"
    if on_class:
        target = display_label(g, trans, on_class)
        return f"{prop} {target} {card}" if card else f"{prop} {target}"
    if svf:
        if isinstance(svf, BNode):
            inner = restriction_text(g, trans, svf)
            return f"{prop} some（{inner}）"
        return f"{prop} some {display_label(g, trans, svf)}"
    if avf:
        return f"{prop} only {display_label(g, trans, avf)}"
    return "restriction"


def short_uri(g: Graph, uri) -> str:
    if uri is None:
        return ""
    s = str(uri)
    for prefix, ns in g.namespace_manager.namespaces():
        ns = str(ns)
        if s.startswith(ns):
            return f"{prefix}:{s[len(ns):]}"
    return s.split("/")[-1] if "/" in s else s


def add_chinese(g: Graph, terms: dict[str, dict], trans: dict) -> None:
    for uri, info in terms.items():
        t = URIRef(uri)
        tr = find_translation(trans, uri, info["label_en"])
        if not tr:
            continue
        g.add((t, RDFS.label, Literal(tr["label_zh"], lang="zh")))
        if tr.get("comment_zh"):
            g.add((t, RDFS.comment, Literal(tr["comment_zh"], lang="zh")))


def add_ontology_chinese(g: Graph, trans: dict) -> None:
    for ont in g.subjects(RDF.type, OWL.Ontology):
        label_en = english_label(g, ont)
        abstract_en = ""
        for a in g.objects(ont, DCTERMS.abstract):
            if isinstance(a, Literal) and (a.language is None or a.language == "en"):
                abstract_en = str(a)
                break
        tr = find_translation(trans, str(ont), label_en)
        if tr:
            g.add((ont, RDFS.label, Literal(tr["label_zh"], lang="zh")))
            if tr.get("comment_zh"):
                g.add((ont, RDFS.comment, Literal(tr["comment_zh"], lang="zh")))


def generate_diagram(g: Graph, terms: dict[str, dict], trans: dict, out_base: Path) -> None:
    try:
        from graphviz import Digraph
    except ImportError:
        return
    dot = Digraph(format="png")
    dot.attr(rankdir="TB", fontname="PingFang SC", fontsize="14", bgcolor="white")
    dot.attr("node", shape="ellipse", style="filled", fontname="PingFang SC", fontsize="10", margin="0.12,0.06")
    dot.attr("edge", fontname="PingFang SC", fontsize="8", arrowsize="0.7")

    def node_id(uri: str) -> str:
        return uri.replace(":", "_").replace("/", "_").replace("#", "_")

    # local classes
    classes = [u for u, i in terms.items() if i["kind"] == "class"]
    for uri in classes:
        dot.node(node_id(uri), display_label(g, trans, URIRef(uri)), fillcolor="#a6cee3")

    # external superclasses referenced by local classes
    for uri in classes:
        for sup in g.objects(URIRef(uri), RDFS.subClassOf):
            if isinstance(sup, URIRef) and str(sup) not in terms:
                dot.node(node_id(str(sup)), display_label(g, trans, sup), fillcolor="#cccccc")

    # subclass edges
    for uri in classes:
        for sup in g.objects(URIRef(uri), RDFS.subClassOf):
            if isinstance(sup, URIRef):
                dot.edge(node_id(uri), node_id(str(sup)), color="#1f77b4")

    # object properties between local classes (domain/range)
    props = [u for u, i in terms.items() if i["kind"] == "object_property"]
    for uri in props:
        dom = g.value(URIRef(uri), RDFS.domain)
        rng = g.value(URIRef(uri), RDFS.range)
        label = display_label(g, trans, URIRef(uri))
        if dom and rng and str(dom) in terms and str(rng) in terms:
            dot.edge(node_id(str(dom)), node_id(str(rng)), label=label, color="#2ca02c")

    # restrictions: edge to target with label
    for uri in classes:
        for sco in g.objects(URIRef(uri), RDFS.subClassOf):
            if isinstance(sco, BNode):
                target = g.value(sco, OWL.onClass)
                if target is None:
                    svf = g.value(sco, OWL.someValuesFrom)
                    target = g.value(svf, OWL.onClass) if isinstance(svf, BNode) else svf
                if isinstance(target, URIRef) and str(target) in terms:
                    dot.edge(node_id(uri), node_id(str(target)), label=restriction_text(g, trans, sco), style="dashed", color="#d62728", fontcolor="#d62728")

    dot.render(str(out_base), cleanup=True)
    dot.format = "svg"
    dot.render(str(out_base), cleanup=True)


def own_summary_entry(summaries: dict, rdf_path: Path) -> dict:
    if not summaries:
        return {}
    root = rdf_path
    while root.name != "master_2026Q3" and root.parent != root:
        root = root.parent
    try:
        return summaries.get(str(rdf_path.with_suffix("").relative_to(root)), {})
    except ValueError:
        return {}


def generate_markdown(g: Graph, terms: dict[str, dict], trans: dict, rdf_path: Path, out_path: Path,
                      summaries: dict | None = None) -> None:
    ns = get_ontology_ns(g)
    ont = next(iter(g.subjects(RDF.type, OWL.Ontology)), None)
    ont_label_en = english_label(g, ont) if ont else rdf_path.stem
    ont_label_zh = ont_label_en
    ont_comment_zh = ""
    if ont:
        for l in g.objects(ont, RDFS.label):
            if isinstance(l, Literal) and l.language == "zh":
                ont_label_zh = str(l)
                break
        for c in g.objects(ont, RDFS.comment):
            if isinstance(c, Literal) and c.language == "zh":
                ont_comment_zh = str(c)
                break

    classes = [i for i in terms.values() if i["kind"] == "class"]
    obj_props = [i for i in terms.values() if i["kind"] == "object_property"]
    dt_props = [i for i in terms.values() if i["kind"] == "datatype_property"]

    def zh_label(uri: str) -> str:
        return display_label(g, trans, URIRef(uri))

    def zh_comment(uri: str) -> str:
        for c in g.objects(URIRef(uri), RDFS.comment):
            if isinstance(c, Literal) and c.language == "zh":
                return str(c)
        return english_definition(g, URIRef(uri))

    own = own_summary_entry(summaries, rdf_path)
    overview_zh = own.get("overview_zh", "")
    if own.get("name_zh"):
        ont_label_zh = own["name_zh"]

    title = ont_label_zh if "本体" in ont_label_zh else f"{ont_label_zh}本体"
    lines = [
        f"# {title}结构与公理说明",
        "",
        f"本文档对应 `{rdf_path.name}` / `{rdf_path.with_suffix('.ttl').name}`，说明该本体的类、继承关系、属性和公理约定。结构图见 `{rdf_path.stem}-structure.png`（`{rdf_path.stem}-structure.svg` 为可缩放版本）。",
        "",
        f"![{ont_label_zh}本体结构图]({rdf_path.stem}-structure.png)",
        "",
        "## 1. 本体概述",
        "",
        overview_zh or ont_comment_zh or "（暂无中文概述）",
        "",
    ]

    if classes:
        lines += ["## 2. 类（Class）", "", "| 类（Class） | 定义（Definition） |", "|---|---|"]
        for info in sorted(classes, key=lambda x: x["label_en"]):
            uri = info["uri"]
            lines.append(f"| {zh_label(uri)} | {zh_comment(uri) or '—'} |")
        lines.append("")

        lines += ["### 2.1 继承关系（Inheritance）", ""]
        for info in sorted(classes, key=lambda x: x["label_en"]):
            uri = info["uri"]
            for sup in g.objects(URIRef(uri), RDFS.subClassOf):
                if isinstance(sup, URIRef):
                    lines.append(f"- {zh_label(uri)} ⊑ {zh_label(str(sup))}")
        lines.append("")

    if obj_props:
        lines += ["## 3. 对象属性（Object Property）", "", "| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |", "|---|---|---|---|"]
        for info in sorted(obj_props, key=lambda x: x["label_en"]):
            uri = info["uri"]
            dom = g.value(URIRef(uri), RDFS.domain)
            rng = g.value(URIRef(uri), RDFS.range)
            inv = g.value(URIRef(uri), OWL.inverseOf)
            subp = g.value(URIRef(uri), RDFS.subPropertyOf)
            notes = []
            if dom:
                notes.append(f"定义域（domain）：{zh_label(str(dom))}")
            if rng:
                notes.append(f"值域（range）：{zh_label(str(rng))}")
            if inv:
                notes.append(f"逆属性（inverseOf）：{zh_label(str(inv))}")
            if subp:
                notes.append(f"子属性（subPropertyOf）：{zh_label(str(subp))}")
            lines.append(f"| {short_uri(g, URIRef(uri))} | {zh_label(uri)} | {zh_comment(uri) or '—'} | {'；'.join(notes) if notes else '—'} |")
        lines.append("")

    if dt_props:
        lines += ["## 4. 数据属性（Datatype Property）", "", "| 属性（Property） | 中文（English） | 定义（Definition） |", "|---|---|---|"]
        for info in sorted(dt_props, key=lambda x: x["label_en"]):
            uri = info["uri"]
            lines.append(f"| {short_uri(g, URIRef(uri))} | {zh_label(uri)} | {zh_comment(uri) or '—'} |")
        lines.append("")

    # axioms
    restriction_lines = []
    for info in sorted(classes, key=lambda x: x["label_en"]):
        uri = info["uri"]
        for sco in g.objects(URIRef(uri), RDFS.subClassOf):
            if isinstance(sco, BNode):
                restriction_lines.append(f"- {zh_label(uri)}：{restriction_text(g, trans, sco)}")
        for dw in g.objects(URIRef(uri), OWL.disjointWith):
            if isinstance(dw, URIRef):
                restriction_lines.append(f"- {zh_label(uri)} 与 {zh_label(str(dw))} 互斥（disjointWith）")
    if restriction_lines:
        lines += ["## 5. 公理约定（Axioms）", ""] + restriction_lines + [""]

    imports_uris = [str(i) for i in g.objects(ont, OWL.imports)] if ont else []
    if imports_uris:
        if summaries:
            lines += [
                f"## 6. 依赖（owl:imports，{len(imports_uris)} 个）",
                "",
                "本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：",
                "",
                "| 导入本体 | 中文名称 | 简介 |",
                "|---|---|---|",
            ]
            for u in imports_uris:
                i = aggregate_module_info(summaries, u, rdf_path)
                lines.append(f"| `{i['rel']}` | {i['name_zh']} | {i['summary_zh']} |")
            lines.append("")
        else:
            imports = [short_uri(g, URIRef(i)) for i in imports_uris]
            lines += ["## 6. 依赖", ""] + [f"- {i}" for i in imports] + [""]

    lines += [
        "## 7. 文件",
        "",
        f"- 官方 RDF/XML：`{rdf_path.name}`",
        f"- 中文 Turtle：`{rdf_path.with_suffix('.ttl').name}`",
        f"- 结构图：`{rdf_path.stem}-structure.png` / `{rdf_path.stem}-structure.svg`",
    ]

    out_path.write_text("\n".join(lines), encoding="utf-8")


def aggregate_module_info(summaries: dict, uri: str, rdf_path: Path) -> dict:
    """Resolve one owl:imports URI to display info and its kind (local/external/missing)."""
    if uri.startswith(FIBO_PREFIX):
        rel = uri[len(FIBO_PREFIX):].rstrip("/")
        root = rdf_path
        while root.name != "master_2026Q3" and root.parent != root:
            root = root.parent
        local_file = root / (rel + ".rdf")
        if not local_file.exists() and "/" in rel:
            # dct:hasPart may point at a Module/Domain individual inside a metadata file
            parent_rel = rel.rsplit("/", 1)[0]
            if (root / (parent_rel + ".rdf")).exists():
                rel = parent_rel
                local_file = root / (rel + ".rdf")
        if local_file.exists():
            info = summaries.get(rel, {})
            return {"kind": "local", "rel": rel + ".rdf",
                    "name_zh": info.get("name_zh", rel.split("/")[-1]),
                    "summary_zh": info.get("summary_zh", "")}
        info = summaries.get("_missing", {}).get(rel, {})
        return {"kind": "missing", "rel": rel,
                "name_zh": info.get("name_zh", rel.split("/")[-1]),
                "summary_zh": info.get("summary_zh", "FIBO 上游声明引用，但本版本仓库未包含对应文件。")}
    ext = summaries.get("_external", {}).get(uri)
    if ext:
        return {"kind": "external", "rel": uri, "name_zh": ext["name_zh"], "summary_zh": ext["summary_zh"]}
    m = re.search(r"ISO3166-2-SubdivisionCodes-([A-Z]{2})/?$", uri)
    if m:
        cc = m.group(1)
        cc_name = summaries.get("_lcc_countries", {}).get(cc, cc)
        pat = summaries.get("_external_pattern", {}).get("ISO3166-2-SubdivisionCodes-", {})
        return {"kind": "external", "rel": uri,
                "name_zh": pat.get("name_zh", "{cc}").format(cc=cc, cc_name=cc_name),
                "summary_zh": pat.get("summary_zh", "").format(cc=cc, cc_name=cc_name)}
    return {"kind": "external", "rel": uri, "name_zh": uri, "summary_zh": ""}


def generate_aggregate_diagram(imports: list[dict], ont_label: str, out_base: Path) -> None:
    try:
        from graphviz import Digraph
    except ImportError:
        return
    dot = Digraph(format="png")
    dot.attr(rankdir="TB", fontname="PingFang SC", fontsize="14", bgcolor="white")
    dot.attr("node", shape="ellipse", style="filled", fontname="PingFang SC", fontsize="10", margin="0.12,0.06")
    dot.attr("edge", fontname="PingFang SC", fontsize="8", arrowsize="0.7")
    dot.node("AGG", ont_label, shape="box", fillcolor="#fdbf6f")
    for i, imp in enumerate(imports):
        nid = f"M{i}"
        color = "#a6cee3" if imp["kind"] == "local" else "#cccccc"
        dot.node(nid, imp["name_zh"], fillcolor=color)
        dot.edge("AGG", nid, label="导入（imports）", color="#1f77b4")
    dot.render(str(out_base), cleanup=True)
    dot.format = "svg"
    dot.render(str(out_base), cleanup=True)


def generate_aggregate_markdown(g: Graph, trans: dict, summaries: dict,
                                rdf_path: Path, out_path: Path) -> None:
    ont = next(iter(g.subjects(RDF.type, OWL.Ontology)), None)
    stem = str(rdf_path.with_suffix(""))
    root = rdf_path
    while root.name != "master_2026Q3" and root.parent != root:
        root = root.parent
    own_rel = str(rdf_path.with_suffix("").relative_to(root))
    own = summaries.get(own_rel, {})
    name_zh = own.get("name_zh", rdf_path.stem)
    summary_zh = own.get("summary_zh", "")

    imports_uris = [str(i) for i in g.objects(ont, OWL.imports)] if ont else []
    imports = [aggregate_module_info(summaries, u, rdf_path) for u in imports_uris]
    local = [i for i in imports if i["kind"] == "local"]
    external = [i for i in imports if i["kind"] == "external"]
    missing = [i for i in imports if i["kind"] == "missing"]

    has_diagram = (rdf_path.with_name(rdf_path.stem + "-structure.png")).exists()
    lines = [
        f"# {name_zh}聚合说明",
        "",
        f"本文档对应 `{rdf_path.name}` / `{rdf_path.with_suffix('.ttl').name}`。",
        "",
    ]
    if has_diagram:
        lines += [f"![{name_zh}聚合结构图]({rdf_path.stem}-structure.png)", ""]
    lines += [
        "## 1. 本文件是什么",
        "",
        summary_zh,
        "",
        "从机制上说，这是一个聚合入口（load-all）文件：它本身不定义任何新的类或属性，"
        "只通过 `owl:imports` 把一组本体打包在一起。应用只要导入这一个文件，"
        "推理机就会把它列出的所有本体一次性加载进来，免去逐个声明的麻烦。"
        "因此它的价值不在「内容」，而在「组合」——组合方式本身就表达了发布方的意图"
        "（例如按域打包、按区域扩展打包、按是否含参考数据打包）。",
        "",
        f"## 2. 聚合的本地本体（{len(local)} 个）",
        "",
        "以下本体均可在本目录结构中找到同名 `.rdf` 文件及配套中文文档：",
        "",
        "| 导入本体 | 中文名称 | 简介 |",
        "|---|---|---|",
    ]
    for i in local:
        lines.append(f"| `{i['rel']}` | {i['name_zh']} | {i['summary_zh']} |")
    lines.append("")

    if external:
        lines += [
            f"## 3. 外部依赖（{len(external)} 个，不在 FIBO 仓库内）",
            "",
            "以下导入来自 OMG 的外部本体库，不在 FIBO 仓库中，加载时需从 spec.edmcouncil.org / omg.org 获取：",
            "",
            "| 外部本体 | 中文名称 | 简介 |",
            "|---|---|---|",
        ]
        for i in external:
            lines.append(f"| `{i['rel']}` | {i['name_zh']} | {i['summary_zh']} |")
        lines.append("")

    if missing:
        sec = len(external) + 3
        lines += [
            f"## {sec}. 上游缺失引用（{len(missing)} 个）",
            "",
        ]
        for i in missing:
            lines.append(f"- `{i['rel']}`：{i['name_zh']} —— {i['summary_zh']}")
        lines.append("")

    n = (3 if external else 2) + (1 if missing else 0)
    lines += [
        f"## {n + 1}. 文件",
        "",
        f"- 官方 RDF/XML：`{rdf_path.name}`",
        f"- 中文 Turtle：`{rdf_path.with_suffix('.ttl').name}`",
    ]
    if has_diagram:
        lines.append(f"- 结构图：`{rdf_path.stem}-structure.png` / `{rdf_path.stem}-structure.svg`")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def generate_metadata_markdown(g: Graph, trans: dict, summaries: dict,
                               rdf_path: Path, out_path: Path) -> None:
    """Doc for Metadata*.rdf manifest files (dct:hasPart composition declarations)."""
    ont = next(iter(g.subjects(RDF.type, OWL.Ontology)), None)
    root = rdf_path
    while root.name != "master_2026Q3" and root.parent != root:
        root = root.parent
    own = summaries.get(str(rdf_path.with_suffix("").relative_to(root)), {})
    name_zh = own.get("name_zh", rdf_path.stem)
    summary_zh = own.get("summary_zh", "")

    parts = [aggregate_module_info(summaries, str(p), rdf_path)
             for p in sorted(set(g.objects(None, DCTERMS.hasPart)), key=str)]
    imports = [aggregate_module_info(summaries, str(i), rdf_path)
               for i in (g.objects(ont, OWL.imports) if ont else [])]

    has_diagram = (rdf_path.with_name(rdf_path.stem + "-structure.png")).exists()
    lines = [
        f"# {name_zh}说明",
        "",
        f"本文档对应 `{rdf_path.name}` / `{rdf_path.with_suffix('.ttl').name}`。",
        "",
    ]
    if has_diagram:
        lines += [f"![{name_zh}结构图]({rdf_path.stem}-structure.png)", ""]
    lines += [
        "## 1. 本文件是什么",
        "",
        summary_zh,
        "",
        "从机制上说，这是一个元数据清单（metadata manifest）文件：它本身不定义任何类或属性，"
        "而是通过 `dct:hasPart` 声明一个域或模块由哪些本体构成，并携带版本 IRI、版权、"
        "许可与成熟度等发布管理信息。它回答的问题是「这个域/模块包含什么、当前是什么版本」，"
        "供发布工具和文档系统按模块组织内容；它的 `owl:imports` 只引入标注词汇表，"
        "不是用来加载业务本体的入口（加载入口是 `All*` 与 `About*` 聚合文件）。",
        "",
        f"## 2. 声明的构成（dct:hasPart，{len(parts)} 个）",
        "",
        "| 构成项 | 中文名称 | 简介 |",
        "|---|---|---|",
    ]
    for i in parts:
        lines.append(f"| `{i['rel']}` | {i['name_zh']} | {i['summary_zh']} |")
    lines += [
        "",
        f"## 3. 标注依赖（owl:imports，{len(imports)} 个）",
        "",
        "以下导入仅用于支撑元数据标注本身（如成熟度等级、概念映射），不属于业务内容：",
        "",
        "| 导入本体 | 中文名称 | 简介 |",
        "|---|---|---|",
    ]
    for i in imports:
        lines.append(f"| `{i['rel']}` | {i['name_zh']} | {i['summary_zh']} |")
    lines += [
        "",
        "## 4. 文件",
        "",
        f"- 官方 RDF/XML：`{rdf_path.name}`",
        f"- 中文 Turtle：`{rdf_path.with_suffix('.ttl').name}`",
    ]
    if has_diagram:
        lines.append(f"- 结构图：`{rdf_path.stem}-structure.png` / `{rdf_path.stem}-structure.svg`")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def generate_individuals_markdown(g: Graph, trans: dict, summaries: dict,
                                  individuals: list, rdf_path: Path, out_path: Path) -> None:
    """Doc for reference-data / example files whose content is named individuals."""
    ont = next(iter(g.subjects(RDF.type, OWL.Ontology)), None)
    root = rdf_path
    while root.name != "master_2026Q3" and root.parent != root:
        root = root.parent
    own = summaries.get(str(rdf_path.with_suffix("").relative_to(root)), {})
    name_zh = own.get("name_zh", rdf_path.stem)
    summary_zh = own.get("summary_zh", "")

    imports = [aggregate_module_info(summaries, str(i), rdf_path)
               for i in (g.objects(ont, OWL.imports) if ont else [])]

    type_counts: dict[str, int] = {}
    for ind in individuals:
        for t in g.objects(ind, RDF.type):
            if isinstance(t, URIRef) and t != OWL.NamedIndividual:
                type_counts[str(t)] = type_counts.get(str(t), 0) + 1

    has_diagram = (rdf_path.with_name(rdf_path.stem + "-structure.png")).exists()
    lines = [
        f"# {name_zh}说明",
        "",
        f"本文档对应 `{rdf_path.name}` / `{rdf_path.with_suffix('.ttl').name}`。",
        "",
    ]
    if has_diagram:
        lines += [f"![{name_zh}结构图]({rdf_path.stem}-structure.png)", ""]
    lines += [
        "## 1. 本文件是什么",
        "",
        summary_zh,
        "",
        "从机制上说，这是一个个体（individuals）文件：它本身不定义任何新的类或属性，"
        "装的全是命名个体（owl:NamedIndividual）——也就是一条条真实存在的实例数据"
        "（如具体的货币、市场、监管机构、法域）。它的 `owl:imports` 引入的是这些个体"
        "所属的类定义所在的本体。应用需要实例级参考数据时加载这类文件。",
        "",
        f"## 2. 个体构成（共 {len(individuals)} 个）",
        "",
        "按个体所属类型统计（类型名为中文（English）对照）：",
        "",
        "| 类型（Class） | 个体数量 |",
        "|---|---|",
    ]
    def type_label(t_uri: str) -> str:
        zh = display_label(g, trans, URIRef(t_uri))
        frag = t_uri.split("/")[-1].split("#")[-1]
        return f"{zh}（{frag}）" if zh != frag else frag

    for t, n in sorted(type_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {type_label(t)} | {n} |")
    lines.append("")

    def ind_label(ind) -> str:
        en = english_label(g, ind)
        s = str(ind)
        if s in trans.get("display_labels", {}):
            return f"{trans['display_labels'][s]}（{en}）" if en and trans["display_labels"][s] != en else trans["display_labels"][s]
        return en or s.split("/")[-1]

    def ind_types(ind) -> str:
        return "、".join(type_label(str(t)) for t in g.objects(ind, RDF.type)
                         if isinstance(t, URIRef) and t != OWL.NamedIndividual)

    if len(individuals) <= 20:
        lines += [
            "个体数量较少，全部列出：",
            "",
            "| 个体 | 类型 |",
            "|---|---|",
        ]
        for ind in sorted(individuals, key=lambda x: english_label(g, x)):
            lines.append(f"| {ind_label(ind)} | {ind_types(ind)} |")
        lines.append("")
    else:
        lines += [
            "个体数量较多，仅举前 10 个示例，完整清单见同名 `.ttl` 文件：",
            "",
            "| 个体（示例） | 类型 |",
            "|---|---|",
        ]
        for ind in sorted(individuals, key=lambda x: english_label(g, x))[:10]:
            lines.append(f"| {ind_label(ind)} | {ind_types(ind)} |")
        lines.append("")

    lines += [
        f"## 3. 依赖的本体（owl:imports，{len(imports)} 个）",
        "",
        "以下导入提供个体所属的类定义与相关参考数据：",
        "",
        "| 导入本体 | 中文名称 | 简介 |",
        "|---|---|---|",
    ]
    for i in imports:
        lines.append(f"| `{i['rel']}` | {i['name_zh']} | {i['summary_zh']} |")
    lines += [
        "",
        "## 4. 文件",
        "",
        f"- 官方 RDF/XML：`{rdf_path.name}`",
        f"- 中文 Turtle：`{rdf_path.with_suffix('.ttl').name}`",
    ]
    if has_diagram:
        lines.append(f"- 结构图：`{rdf_path.stem}-structure.png` / `{rdf_path.stem}-structure.svg`")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: fibo_doc_gen.py <file.rdf>", file=sys.stderr)
        return 1
    rdf_path = Path(sys.argv[1])
    if not rdf_path.exists():
        print(f"File not found: {rdf_path}", file=sys.stderr)
        return 1

    g = Graph()
    g.parse(str(rdf_path), format="xml")
    ns = get_ontology_ns(g)
    terms = local_terms(g, ns)
    trans = load_translations()

    ont = next(iter(g.subjects(RDF.type, OWL.Ontology)), None)
    is_aggregate = not terms and ont is not None and any(g.objects(ont, OWL.imports))
    if is_aggregate:
        summaries = load_summaries()
        root = rdf_path
        while root.name != "master_2026Q3" and root.parent != root:
            root = root.parent
        own_rel = str(rdf_path.with_suffix("").relative_to(root))
        own = summaries.get(own_rel, {})
        if own.get("name_zh"):
            g.add((ont, RDFS.label, Literal(own["name_zh"], lang="zh")))
        if own.get("summary_zh"):
            g.add((ont, RDFS.comment, Literal(own["summary_zh"], lang="zh")))
        ttl_path = rdf_path.with_suffix(".ttl")
        g.serialize(str(ttl_path), format="turtle")
        imports_uris = [str(i) for i in g.objects(ont, OWL.imports)]
        out_base = rdf_path.with_name(rdf_path.stem + "-structure")
        if len(imports_uris) <= 40:
            infos = [aggregate_module_info(summaries, u, rdf_path) for u in imports_uris]
            generate_aggregate_diagram(infos, own.get("name_zh", rdf_path.stem), out_base)
        else:
            for ext in ("png", "svg"):
                stale = rdf_path.with_name(f"{rdf_path.stem}-structure.{ext}")
                if stale.exists():
                    stale.unlink()
        individuals = sorted(
            {s for s in g.subjects(RDF.type, None)
             if isinstance(s, URIRef) and s != ont and (not ns or str(s).startswith(ns))},
            key=str)
        has_part = any(True for _ in g.subjects(DCTERMS.hasPart, None))
        md_path = rdf_path.with_suffix(".md")
        if has_part:
            generate_metadata_markdown(g, trans, summaries, rdf_path, md_path)
            flavor = "metadata"
        elif individuals:
            generate_individuals_markdown(g, trans, summaries, individuals, rdf_path, md_path)
            flavor = "individuals"
        else:
            generate_aggregate_markdown(g, trans, summaries, rdf_path, md_path)
            flavor = "aggregate"
        print(f"OK({flavor}) {rdf_path} -> {ttl_path.name}, {md_path.name}")
        return 0

    missing = []
    for uri, info in terms.items():
        if not find_translation(trans, uri, info["label_en"]):
            missing.append(info)

    if missing:
        print(json.dumps({"file": str(rdf_path), "missing": missing}, ensure_ascii=False, indent=2))
        return 3

    add_ontology_chinese(g, trans)
    add_chinese(g, terms, trans)

    summaries = load_summaries()
    own = own_summary_entry(summaries, rdf_path)
    if ont is not None and own.get("name_zh"):
        g.add((ont, RDFS.label, Literal(own["name_zh"], lang="zh")))
        if own.get("summary_zh") and not any(
                isinstance(c, Literal) and c.language == "zh" for c in g.objects(ont, RDFS.comment)):
            g.add((ont, RDFS.comment, Literal(own["summary_zh"], lang="zh")))

    ttl_path = rdf_path.with_suffix(".ttl")
    g.serialize(str(ttl_path), format="turtle")

    out_base = rdf_path.with_name(rdf_path.stem + "-structure")
    generate_diagram(g, terms, trans, out_base)

    md_path = rdf_path.with_suffix(".md")
    generate_markdown(g, terms, trans, rdf_path, md_path, load_summaries())

    print(f"OK {rdf_path} -> {ttl_path.name}, {md_path.name}, {out_base.name}.png/.svg")
    return 0


if __name__ == "__main__":
    sys.exit(main())
