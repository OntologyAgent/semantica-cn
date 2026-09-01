# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

本文件用中文维护，供在此仓库工作的 Claude Code 实例阅读。

## 项目概述

Semantica 是知识图谱(Knowledge Graph)基础设施，充当 LLM 应用底下的确定性基础设施层——它把分散的原始数据加工成一张可查询、可审计的图，全程不需要 LLM 参与构建、推理和溯源。

数据处理流水线是理解整个代码库的主线，每个阶段对应 `semantica/` 下的一个同名子模块：

```
原始数据 → ingest 摄取 → parse 解析 → normalize 规范化 → split 分块
        → semantic_extract 语义抽取（NER/关系/事件）
        → conflicts 冲突检测 → deduplication 去重
        → kg 知识图谱构建
        → ontology 本体 / reasoning 推理 / provenance 溯源 / context 决策智能
        → vector_store / graph_store / triplet_store 多后端存储
        → export 导出 / visualization 可视化
```

对外有五种入口：Python 库、CLI（`semantica`）、REST API（`semantica-server`）、MCP 服务器（`semantica-mcp`）、Knowledge Explorer 面板（`semantica-explorer`）。

## 与上游同步（本仓库的 HEAD 约束）

这是上游 `semantica-agi/semantica` 的 fork：`origin` 指向 Guji-AnaSora/semantica，`upstream` 指向官方仓库。定期执行：

```bash
git fetch upstream && git merge upstream/main && git push origin main
```

因此本地改动必须遵守一条纪律：**开闭原则——只扩展，不侵入**。

- 新功能用新增文件、新增模块、子类、适配器落地，尽量不修改上游既有代码。侵入越少，合并 upstream 时的冲突越少。
- 国际化和翻译工作另起炉灶：中文文档放进独立目录（如 `docs/zh/`），不覆盖英文原文；界面文案优先走新增的语言资源文件，不改上游字符串的原文。
- `projects/` 是本地自建项目的数据目录，不提交，也不要把要提交的代码放进去。

## 技术栈

- **后端**：Python 3.8+（CI 用 3.11）。核心依赖 numpy/pandas/scikit-learn/spacy/transformers/torch、rdflib（RDF）、networkx、faiss、pydantic、click + rich（CLI）、loguru/structlog（日志）。
- **可选依赖**：所有外部后端都是 `pyproject.toml` 里的 extra——图库（Neo4j/FalkorDB/Apache AGE/Neptune）、向量库（FAISS/Qdrant/Weaviate/Milvus/Pinecone/pgvector/sqlite-vec）、LLM 提供商（OpenAI/Anthropic/Gemini/Groq/Ollama 等）、数据平台连接器（Snowflake/Databricks）、Explorer 服务端（FastAPI + uvicorn）。
- **前端**：Explorer 用 React 19 + TypeScript + Vite + Sigma.js，构建产物打进 `semantica/static/` 随 wheel 分发，终端用户不需要 Node.js。
- **工程化**：setuptools、哈希锁文件 `requirements-ci.txt`、pre-commit、GitHub Actions、Docker、checkov。本地环境统一用 **uv** 管理（虚拟环境、装包、跑测试），不用 pip。

## 工程结构

```
semantica/        Python 包，子模块按流水线阶段命名（见概述）
explorer/         Knowledge Explorer 前端（React 19 + Vite + Sigma.js）
integrations/     智能体框架适配：agno/crewai/langchain/openclaw
mcp/              MCP 服务器实现
tests/            与包结构镜像的测试目录
docs/             Mintlify 文档（英文，上游维护；中文翻译另建目录）
docs/zh/          中文文档镜像：译文 + glossary 术语表 + README 翻译规范
tools/i18n/       zh_status.py，中文译文过期追踪（git blob sha 基准）
cookbook/         教程笔记本
plugins/          编辑器插件、agents、hooks、skills
deploy/           k8s/helm/gcp/azure/fly/railway/render 部署配置
projects/         本地数据，不提交
```

完整流水线图见 `ARCHITECTURE.md`。

## 编码风格

- Black 行宽 88；isort 用 black profile；flake8 参数 `--max-line-length=88 --extend-ignore=E203,W503`；mypy 做类型检查。
- Google 风格 docstring（Args/Returns/Raises/Example）。
- Conventional Commits：`feat(kg): ...`、`fix(parse): ...`；类型限 feat/fix/docs/test/refactor/perf/style/chore。
- 分支名 `fix/xxx` 或 `feature/xxx`；测试文件必须叫 `test_*.py`。

### 容易踩的坑

- **惰性加载**：`semantica/__init__.py` 用 `_ModuleProxy` 延迟导入子模块。不要在包顶层加 eager import，会拖慢整个包的导入。
- **可选依赖必须守护**：import 可选后端时用 `try/except ImportError`，保证最小安装也能导入。写法参考 `semantica/graph_store/neo4j_store.py`。
- **溯源不可断**：图数据带 W3C PROV-O 溯源，决策是一等对象（`ContextGraph.record_decision()`）。改图数据的代码必须保持溯源链完整。
- **先冲突检测再合并**：冲突事实要经 `conflicts` 标记、`deduplication` 去重后才进 KG，禁止静默覆盖。
- **进度条**：只在交互式 TTY 渲染，新 CLI 输出要尊重 `SEMANTICA_DISABLE_PROGRESS` / `SEMANTICA_FORCE_PROGRESS`。
- `crewai` extra 因 chromadb CVE 被刻意排除在 `all` 之外，不要加回去。

## 常用命令

```bash
# ── 环境 ──
uv venv --python 3.11 .venv                 # 系统没装 3.11 时 uv 会自动下载
source .venv/bin/activate
uv pip install -e ".[dev]"
pre-commit install
cd explorer && npm ci                       # 前端依赖，Node 18+ / npm 9+
semantica doctor                            # 验证安装

# ── 测试 ──
pytest                                      # 全量
pytest tests/test_cli_commands.py           # 单文件
pytest tests/kg/test_x.py::TestX::test_y    # 单测试
pytest -m "not integration"                 # 跳过依赖外部服务/API key 的测试
pytest --cov=semantica                      # 覆盖率，目标 80%，核心模块 90%+

# ── Lint / 格式化 ──
black semantica/ tests/ && isort semantica/ tests/ && flake8 semantica/ tests/
mypy semantica/
pre-commit run --all-files

# ── Explorer 前端（在 explorer/ 下）──
npm run dev                                 # Vite 开发服务器
npm run build                               # tsc -b && vite build
npm run lint
npm run test:graph-store                    # 另有 graph-workspace / plugin-registry / deterministic-e2e

# ── 文档 ──
python docs_check.py                        # docs/ 一致性检查，文档 PR 前必跑
python tools/i18n/zh_status.py              # 中文译文过期状态
```

## CI 与锁文件的坑

- **CI 不跑全量 Python 测试**。`.github/workflows/ci.yml` 只跑 Explorer 前端测试、一个确定性 e2e（`tests/explorer/test_explorer_deterministic_rendering_e2e.py`）、锁文件过期检查和 wheel 构建。CI 绿 ≠ 测试全过，提交前本地跑 pytest。
- **全量 `pytest` 有跨测试状态污染**（native 层线程互斥崩溃 `recursive_mutex lock failed`），会大面积误报失败。改了哪个模块就按模块跑：`pytest tests/<module>`。
- **本机代理会击穿网络类测试**：SSRF 守护（`semantica/ingest/ssrf.py`）拒绝经代理的请求，且 macOS 上 requests 会从系统网络配置读代理、仅 `env -u` 无效。跑 ingest 等测试前缀 `NO_PROXY='*' no_proxy='*'`；个别测试仍会真实访问外网（如 `example.com`），网络不通时失败属正常。
- 部分测试依赖未进 extras 的可选包（如 `sqlalchemy`），报 `ModuleNotFoundError` 时 `uv pip install` 补上即可。
- **`requirements-ci.txt` 是 CI/发布专用的哈希锁文件**，绝不能装进本地开发环境。改了 `pyproject.toml` 依赖后必须重新生成，否则 CI 过期检查失败。本仓库没有 `uv.lock`：本地环境用 uv 的临时解析安装（`uv pip install`），CI 安装仍是 pip + 锁文件（上游配置，不要改）：

  ```bash
  pip install uv==0.12.1    # uv 版本须与 CI 一致
  uv pip compile pyproject.toml --python-version 3.11 --extra all --generate-hashes -o requirements-ci.txt
  ```

- Explorer 后端 extra 按 Python 版本分别钉版（`.github/requirements/explorer-extra-py311.txt` 等），不能跨版本共用。

## 中文文档翻译

- 翻译规范单一事实源：`docs/zh/README.md`；术语统一查 `docs/zh/glossary.md`。
- 上游同步（`git merge upstream/main`）之后先跑 `python tools/i18n/zh_status.py`，按 stale 清单逐篇重译并刷新 `source_version`。
- 翻译流程入口：`.claude/skills/docs-zh-translation`（编排层，细节一律链接 README）。
- 零侵入：只增改 `docs/zh/`、`tools/i18n/` 与该 Skill 目录，不动上游既有文件。
