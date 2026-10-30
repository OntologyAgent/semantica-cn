"""Convert OMG Commons Ontology Library RDF/XML files to Turtle with Chinese labels.

Run from repo root:
    python tools/nightly/convert_commons_to_ttl.py
"""
from __future__ import annotations

import os
from pathlib import Path

from rdflib import Graph, Namespace, RDF, RDFS, OWL, SKOS, Literal, URIRef

BASE_DIR = Path("ontology_models/Commons/20250801")
CMNS = "https://www.omg.org/spec/Commons/"

# File-level Chinese labels/comments for every Commons module
MODULE_META: dict[str, tuple[str, str]] = {
    "AboutCommons": (
        "关于 Commons 本体库（About the Commons Ontology Library）",
        "方便用户一次性加载全部 Commons 本体的入口文件。",
    ),
    "AnnotationVocabulary": (
        "Commons 标注词汇表（Commons Annotation Vocabulary）",
        "提供文档标注常用的属性，如摘要、定义、解释、版权、同义词等，并梳理 SKOS 与 Dublin Core 标注属性之间的关系。",
    ),
    "BusinessAuthorizations": (
        "Commons 业务授权本体（Commons Business Authorizations Ontology）",
        "定义业务授权、许可及其相关角色和关系。",
    ),
    "Classifiers": (
        "Commons 分类器本体（Commons Classifiers Ontology）",
        "定义用于对事物进行分类、分面或归类的通用概念。",
    ),
    "CodesAndCodeSets": (
        "Commons 代码与代码集本体（Commons Codes and Code Sets Ontology）",
        "定义代码、代码集、编码方案及其标识方式。",
    ),
    "Collections": (
        "Commons 集合本体（Commons Collections Ontology）",
        "定义集合、成员关系及集合操作的基础概念。",
    ),
    "ContextualDesignators": (
        "Commons 上下文指称本体（Commons Contextual Designators Ontology）",
        "定义在特定上下文中有意义的指称、名称和标识符。",
    ),
    "ContextualIdentifiers": (
        "Commons 上下文标识符本体（Commons Contextual Identifiers Ontology）",
        "定义在特定上下文或情境中使用的标识符。",
    ),
    "DatesAndTimes": (
        "Commons 日期与时间本体（Commons Dates and Times Ontology）",
        "定义日期、时间、时间段及其表示方式。",
    ),
    "Designators": (
        "Commons 指称本体（Commons Designators Ontology）",
        "定义名称、标识符等指称事物的通用概念。",
    ),
    "Documents": (
        "Commons 文档本体（Commons Documents Ontology）",
        "定义文档、记录及其组成部分的通用概念。",
    ),
    "Identifiers": (
        "Commons 标识符本体（Commons Identifiers Ontology）",
        "定义标识符及其发布、管理与解析的基础概念。",
    ),
    "Languages": (
        "Commons 语言本体（Commons Languages Ontology）",
        "定义语言、语言标签及其相关概念。",
    ),
    "Locations": (
        "Commons 位置本体（Commons Locations Ontology）",
        "定义地址、地理区域、位置及其关系。",
    ),
    "Organizations": (
        "Commons 组织本体（Commons Organizations Ontology）",
        "定义组织、组织单元及其标识和关系。",
    ),
    "PartiesAndSituations": (
        "Commons 参与方与情境本体（Commons Parties and Situations Ontology）",
        "定义参与方、角色、情境以及它们之间关系的高层概念，是 FIBO 等多领域的上层本体。",
    ),
    "QuantitiesAndUnits": (
        "Commons 量与单位本体（Commons Quantities and Units Ontology）",
        "定义数量、度量单位、量纲及其转换。",
    ),
    "RegistrationAuthorities": (
        "Commons 注册机构本体（Commons Registration Authorities Ontology）",
        "定义注册机构、注册标识符及其管理。",
    ),
    "RegulatoryAgencies": (
        "Commons 监管机构本体（Commons Regulatory Agencies Ontology）",
        "定义监管机构、监管角色及其关系。",
    ),
    "RolesAndCompositions": (
        "Commons 角色与组合本体（Commons Roles and Compositions Ontology）",
        "定义角色、组合及其扮演/组成关系的基础本体。",
    ),
    "SitesAndFacilities": (
        "Commons 场所与设施本体（Commons Sites and Facilities Ontology）",
        "定义场所、设施、地址及其关系。",
    ),
    "StructuredCollections": (
        "Commons 结构化集合本体（Commons Structured Collections Ontology）",
        "定义具有特定结构或模式的集合，如序列、层次结构等。",
    ),
    "TextDatatype": (
        "Commons 文本数据类型本体（Commons Text Datatype Ontology）",
        "定义文本、字符串及其数据类型的基础概念。",
    ),
}

# Chinese labels for terms in the three core modules used directly by FIBO Agreements
TERM_LABELS: dict[str, str] = {
    # PartiesAndSituations classes
    f"{CMNS}PartiesAndSituations/Actor": "行为者（actor）",
    f"{CMNS}PartiesAndSituations/Agent": "智能体（agent）",
    f"{CMNS}PartiesAndSituations/AgentRole": "智能体角色（agent role）",
    f"{CMNS}PartiesAndSituations/Party": "参与方（party）",
    f"{CMNS}PartiesAndSituations/PartyRole": "参与方角色（party role）",
    f"{CMNS}PartiesAndSituations/Situation": "情境（situation）",
    f"{CMNS}PartiesAndSituations/SoftwareAgent": "软件智能体（software agent）",
    f"{CMNS}PartiesAndSituations/Undergoer": "承受者（undergoer）",
    # PartiesAndSituations object properties
    f"{CMNS}PartiesAndSituations/actsIn": "在…中行动（acts in）",
    f"{CMNS}PartiesAndSituations/actsOn": "对…采取行动（acts on）",
    f"{CMNS}PartiesAndSituations/directlyAffects": "直接影响（directly affects）",
    f"{CMNS}PartiesAndSituations/experiences": "经历（experiences）",
    f"{CMNS}PartiesAndSituations/experiencesDirectly": "直接经历（experiences directly）",
    f"{CMNS}PartiesAndSituations/experiencesWith": "与…共同经历（experiences with）",
    f"{CMNS}PartiesAndSituations/hasActiveParty": "具有主动参与方（has active party）",
    f"{CMNS}PartiesAndSituations/hasActiveRole": "具有主动角色（has active role）",
    f"{CMNS}PartiesAndSituations/hasActor": "具有行为者（has actor）",
    f"{CMNS}PartiesAndSituations/hasObjectRole": "具有客体角色（has object role）",
    f"{CMNS}PartiesAndSituations/hasParty": "具有参与方（has party）",
    f"{CMNS}PartiesAndSituations/hasPartyRole": "具有参与方角色（has party role）",
    f"{CMNS}PartiesAndSituations/hasRelatedPartyRole": "具有相关参与方角色（has related party role）",
    f"{CMNS}PartiesAndSituations/hasSubjectRole": "具有主体角色（has subject role）",
    f"{CMNS}PartiesAndSituations/hasUndergoer": "具有承受者（has undergoer）",
    f"{CMNS}PartiesAndSituations/holdsDuring": "在…期间保持（holds during）",
    f"{CMNS}PartiesAndSituations/isAPartyTo": "是…的参与方（is a party to）",
    f"{CMNS}PartiesAndSituations/isAffectedBy": "受…影响（is affected by）",
    f"{CMNS}PartiesAndSituations/isDirectlyAffectedBy": "直接受…影响（is directly affected by）",
    f"{CMNS}PartiesAndSituations/isExperiencedBy": "被…经历（is experienced by）",
    f"{CMNS}PartiesAndSituations/isObjectRoleIn": "是…中的客体角色（is object role in）",
    f"{CMNS}PartiesAndSituations/isRealizedIn": "在…中实现（is realized in）",
    f"{CMNS}PartiesAndSituations/isSubjectRoleIn": "是…中的主体角色（is subject role in）",
    f"{CMNS}PartiesAndSituations/playsActivePartyIn": "在…中扮演主动参与方（plays active party in）",
    f"{CMNS}PartiesAndSituations/playsActiveRoleIn": "在…中扮演主动角色（plays active role in）",
    f"{CMNS}PartiesAndSituations/playsActiveRoleThatAffects": "扮演影响…的主动角色（plays active role that affects）",
    f"{CMNS}PartiesAndSituations/playsActiveRoleThatDirectlyAffects": "扮演直接影响…的主动角色（plays active role that directly affects）",
    f"{CMNS}PartiesAndSituations/realizes": "实现（realizes）",
    f"{CMNS}PartiesAndSituations/undergoes": "承受（undergoes）",
    # RolesAndCompositions classes
    f"{CMNS}RolesAndCompositions/Composition": "组合（composition）",
    f"{CMNS}RolesAndCompositions/FunctionalRole": "功能角色（functional role）",
    f"{CMNS}RolesAndCompositions/ProcessRole": "过程角色（process role）",
    f"{CMNS}RolesAndCompositions/Role": "角色（role）",
    f"{CMNS}RolesAndCompositions/StructuralRole": "结构角色（structural role）",
    # RolesAndCompositions object properties
    f"{CMNS}RolesAndCompositions/hasRole": "具有角色（has role）",
    f"{CMNS}RolesAndCompositions/isManifestedIn": "体现在…中（is manifested in）",
    f"{CMNS}RolesAndCompositions/isPlayedBy": "由…扮演（is played by）",
    f"{CMNS}RolesAndCompositions/isRoleIn": "是…中的角色（is role in）",
    f"{CMNS}RolesAndCompositions/manifests": "体现（manifests）",
    f"{CMNS}RolesAndCompositions/playsRole": "扮演角色（plays role）",
}

TERM_COMMENTS: dict[str, str] = {
    # PartiesAndSituations classes
    f"{CMNS}PartiesAndSituations/Actor": "参与方之间关系中的主要执行者，即做出某事、导致某事发生或以其他方式在关系中扮演施事角色的参与方。",
    f"{CMNS}PartiesAndSituations/Agent": "能够适应环境并与之交互的自主事物。",
    f"{CMNS}PartiesAndSituations/AgentRole": "任何智能体所扮演的角色。",
    f"{CMNS}PartiesAndSituations/Party": "个人或组织。",
    f"{CMNS}PartiesAndSituations/PartyRole": "由组织或个人扮演的、可能具有时间边界的角色。",
    f"{CMNS}PartiesAndSituations/Situation": "在一段时间内相对稳定的场景、状态或关系。",
    f"{CMNS}PartiesAndSituations/SoftwareAgent": "感知环境并采取行动以最大化实现其目标的数字实体。",
    f"{CMNS}PartiesAndSituations/Undergoer": "在情境中扮演客体或接受者角色的事物（或参与方），即被情境影响的对象，或扮演被动接受者/受事角色的实体。",
    # PartiesAndSituations object properties
    f"{CMNS}PartiesAndSituations/actsIn": "指出行为者扮演主要角色的情境。",
    f"{CMNS}PartiesAndSituations/actsOn": "将情境中的行为者与其在特定情形下影响的承受者关联起来。",
    f"{CMNS}PartiesAndSituations/directlyAffects": "将情境中的行为者与其在特定情形下直接影响的事物（或参与方）关联起来。",
    f"{CMNS}PartiesAndSituations/experiences": "将某事物与以某种方式影响它的情境关联起来。",
    f"{CMNS}PartiesAndSituations/experiencesDirectly": "将某事物直接关联到驱动涉及该事物的情境的参与方。",
    f"{CMNS}PartiesAndSituations/experiencesWith": "将某事物关联到驱动涉及该事物的情境的行为者。",
    f"{CMNS}PartiesAndSituations/hasActiveParty": "将情境关联到以主要（施事）角色行动的个人或组织。",
    f"{CMNS}PartiesAndSituations/hasActiveRole": "将情境关联到以主要（施事）角色行动的事物。",
    f"{CMNS}PartiesAndSituations/hasActor": "识别在特定情境中扮演特定角色并起主要作用的参与方。",
    f"{CMNS}PartiesAndSituations/hasObjectRole": "识别被特定关系或情境影响，或在该关系中充当次要参数的人或事物。",
    f"{CMNS}PartiesAndSituations/hasParty": "识别与协议、合同、政策、规章、情境或其他安排相关联的参与方。",
    f"{CMNS}PartiesAndSituations/hasPartyRole": "识别某个人或组织在与情境、协议、合同、政策、规章、活动或其他关系相关的方面所扮演的具体角色。",
    f"{CMNS}PartiesAndSituations/hasRelatedPartyRole": "将扮演某一具体角色的参与方直接关联到扮演相同或另一角色的另一参与方。",
    f"{CMNS}PartiesAndSituations/hasSubjectRole": "识别在特定情境中是讨论、描述、处理对象或主要主题的人或事物。",
    f"{CMNS}PartiesAndSituations/hasUndergoer": "识别给定情境中作为经历者、被动或其他客体角色的实体。",
    f"{CMNS}PartiesAndSituations/holdsDuring": "指示某事物为真的日期时间段。",
    f"{CMNS}PartiesAndSituations/isAPartyTo": "识别参与方所关联的协议、合同、政策、规章、情境或其他安排。",
    f"{CMNS}PartiesAndSituations/isAffectedBy": "将情境中的承受者关联到在特定情形下对其产生影响的行为者。",
    f"{CMNS}PartiesAndSituations/isDirectlyAffectedBy": "将情境中的承受者关联到在特定情形下对其产生直接影响的人或组织。",
    f"{CMNS}PartiesAndSituations/isExperiencedBy": "将情境关联到直接参与或受其影响的事物。",
    f"{CMNS}PartiesAndSituations/isObjectRoleIn": "指示该角色为次要角色的情境，例如经历者或被动参与者。",
    f"{CMNS}PartiesAndSituations/isRealizedIn": "将情境或组成关联到被特定关系或情境影响或作为其次要参数的事物。",
    f"{CMNS}PartiesAndSituations/isSubjectRoleIn": "指示该角色为主要主题的情境。",
    f"{CMNS}PartiesAndSituations/playsActivePartyIn": "将个人或组织关联到其直接参与的情境。",
    f"{CMNS}PartiesAndSituations/playsActiveRoleIn": "将某事物关联到其直接参与的情境。",
    f"{CMNS}PartiesAndSituations/playsActiveRoleThatAffects": "将个人或组织关联到其在特定情形下产生影响的承受者。",
    f"{CMNS}PartiesAndSituations/playsActiveRoleThatDirectlyAffects": "将个人或组织关联到其在特定情形下直接影响的事物。",
    f"{CMNS}PartiesAndSituations/realizes": "将某事物关联到其扮演的角色为次要角色的情境或组成，例如经历者或被动参与者。",
    f"{CMNS}PartiesAndSituations/undergoes": "指示承受者所经历的情境。",
    # RolesAndCompositions classes
    f"{CMNS}RolesAndCompositions/Composition": "为特定目的将其他事物（可能以特定角色）组合在一起而形成的特定产物。",
    f"{CMNS}RolesAndCompositions/FunctionalRole": "表示某人、组织、过程或服务预期执行或提供的底层功能的角色。",
    f"{CMNS}RolesAndCompositions/ProcessRole": "将资源和参与者关联到为特定目的设计并组织的一组涉及多个企业实体的结构化活动的角色。",
    f"{CMNS}RolesAndCompositions/Role": "某事物在特定情境中参与的命名具体行为。",
    f"{CMNS}RolesAndCompositions/StructuralRole": "以能力意义指定实体之间关系的角色，通常反映组织或结构关系（层级）。",
    # RolesAndCompositions object properties
    f"{CMNS}RolesAndCompositions/hasRole": "识别在某事物（例如组合）中扮演部分的角色。",
    f"{CMNS}RolesAndCompositions/isManifestedIn": "指示角色在其中实现、出现或发生的事物。",
    f"{CMNS}RolesAndCompositions/isPlayedBy": "指示填充该角色的人、组织或其他事物。",
    f"{CMNS}RolesAndCompositions/isRoleIn": "识别涉及该角色的某事物，例如组合、情境或合同。",
    f"{CMNS}RolesAndCompositions/manifests": "指示在某种情境中实现、展示或显示某事物的角色。",
    f"{CMNS}RolesAndCompositions/playsRole": "指示某人或某事物在某种情境下所扮演的部分。",
}

# Annotation properties in Commons AnnotationVocabulary (Chinese labels only)
AV_LABELS: dict[str, str] = {
    "http://purl.org/dc/terms/abstract": "摘要（abstract）",
    "http://purl.org/dc/terms/contributor": "贡献者（contributor）",
    "http://purl.org/dc/terms/creator": "创建者（creator）",
    "http://purl.org/dc/terms/description": "描述（description）",
    "http://purl.org/dc/terms/issued": "发布日期（issued）",
    "http://purl.org/dc/terms/license": "许可证（license）",
    "http://purl.org/dc/terms/modified": "修改日期（modified）",
    "http://purl.org/dc/terms/publisher": "发布者（publisher）",
    "http://purl.org/dc/terms/references": "引用（references）",
    "http://purl.org/dc/terms/rights": "权利（rights）",
    "http://purl.org/dc/terms/source": "来源（source）",
    "http://purl.org/dc/terms/title": "标题（title）",
    "http://www.w3.org/2004/02/skos/core#altLabel": "替代标签（altLabel）",
    "http://www.w3.org/2004/02/skos/core#changeNote": "变更说明（changeNote）",
    "http://www.w3.org/2004/02/skos/core#definition": "定义（definition）",
    "http://www.w3.org/2004/02/skos/core#editorialNote": "编辑注记（editorialNote）",
    "http://www.w3.org/2004/02/skos/core#example": "示例（example）",
    "http://www.w3.org/2004/02/skos/core#historyNote": "历史说明（historyNote）",
    "http://www.w3.org/2004/02/skos/core#note": "注记（note）",
    "http://www.w3.org/2004/02/skos/core#prefLabel": "首选标签（prefLabel）",
    "http://www.w3.org/2004/02/skos/core#scopeNote": "范围说明（scopeNote）",
    f"{CMNS}AnnotationVocabulary/abbreviation": "缩写（abbreviation）",
    f"{CMNS}AnnotationVocabulary/acronym": "首字母缩写（acronym）",
    f"{CMNS}AnnotationVocabulary/adaptedFrom": "改编自（adaptedFrom）",
    f"{CMNS}AnnotationVocabulary/copyright": "版权（copyright）",
    f"{CMNS}AnnotationVocabulary/directSource": "直接来源（directSource）",
    f"{CMNS}AnnotationVocabulary/explanatoryNote": "解释性说明（explanatoryNote）",
    f"{CMNS}AnnotationVocabulary/logicalDefinition": "逻辑定义（logicalDefinition）",
    f"{CMNS}AnnotationVocabulary/symbol": "符号（symbol）",
    f"{CMNS}AnnotationVocabulary/synonym": "同义词（synonym）",
    f"{CMNS}AnnotationVocabulary/usageNote": "使用说明（usageNote）",
}


def bind_prefixes(g: Graph) -> None:
    g.bind("owl", Namespace("http://www.w3.org/2002/07/owl#"))
    g.bind("rdf", Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"))
    g.bind("rdfs", Namespace("http://www.w3.org/2000/01/rdf-schema#"))
    g.bind("xsd", Namespace("http://www.w3.org/2001/XMLSchema#"))
    g.bind("skos", Namespace("http://www.w3.org/2004/02/skos/core#"))
    g.bind("dct", Namespace("http://purl.org/dc/terms/"))
    g.bind("cmns-av", Namespace(f"{CMNS}AnnotationVocabulary/"))
    g.bind("cmns-pts", Namespace(f"{CMNS}PartiesAndSituations/"))
    g.bind("cmns-rlcmp", Namespace(f"{CMNS}RolesAndCompositions/"))


def add_chinese_labels(g: Graph, module_name: str) -> None:
    # Ontology-level metadata
    ontologies = list(g.subjects(RDF.type, OWL.Ontology))
    if ontologies:
        ont = ontologies[0]
        label, comment = MODULE_META.get(module_name, (f"Commons {module_name} 本体", ""))
        g.add((ont, RDFS.label, Literal(label, lang="zh")))
        if comment:
            g.add((ont, RDFS.comment, Literal(comment, lang="zh")))

    # Term-level labels/comments
    for term in set(g.subjects(RDF.type, OWL.Class)) | set(g.subjects(RDF.type, OWL.ObjectProperty)) | set(g.subjects(RDF.type, OWL.DatatypeProperty)):
        if not isinstance(term, URIRef):
            continue
        uri = str(term)
        lbl = TERM_LABELS.get(uri)
        cmt = TERM_COMMENTS.get(uri)
        if lbl:
            g.add((term, RDFS.label, Literal(lbl, lang="zh")))
        if cmt:
            g.add((term, RDFS.comment, Literal(cmt, lang="zh")))

    # AnnotationVocabulary annotation properties
    if module_name == "AnnotationVocabulary":
        for term in g.subjects(RDF.type, OWL.AnnotationProperty):
            if not isinstance(term, URIRef):
                continue
            lbl = AV_LABELS.get(str(term))
            if lbl:
                g.add((term, RDFS.label, Literal(lbl, lang="zh")))


def convert_module(module_dir: Path) -> None:
    rdf_file = module_dir / f"{module_dir.name}.rdf"
    ttl_file = module_dir / f"{module_dir.name}.ttl"
    if not rdf_file.exists():
        return
    g = Graph()
    g.parse(str(rdf_file), format="xml")
    bind_prefixes(g)
    add_chinese_labels(g, module_dir.name)
    g.serialize(str(ttl_file), format="turtle")
    print(f"Wrote {ttl_file}")


def main() -> None:
    for module_dir in sorted(BASE_DIR.iterdir()):
        if module_dir.is_dir():
            convert_module(module_dir)


if __name__ == "__main__":
    main()
