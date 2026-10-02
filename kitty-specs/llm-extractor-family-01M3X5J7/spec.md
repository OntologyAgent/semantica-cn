# Specification: LLM 抽取器家族（中文增强）

**Mission**: `llm-extractor-family-01M3X5J7` · software-dev · single_branch
**Branch contract**: 规划与实现均在 `feature/llm-extractor-family`，mission merge 时回 `main`
**Date**: 2026-10-02
**Status**: backlog（specify 完成待启动 plan/tasks；本文为路线图待办的规格化记录）

## Overview

semantica 的语义抽取层（`semantica/semantic_extract/`）当前以规则/统计抽取器为主，LLM 参与有限且不可定制。本 mission 为五类抽取能力建立统一的 LLM 驱动实现，全部面向中文场景优化，并共享一套「自定义提示词 + 提取约束」骨架：

1. **指代消解**（Coreference Resolution）——LLM + 提示词实现，支持中文人称/指示代词链
2. **实体抽取**（NER）——约束主题方向（domain steering）与实体类型白名单
3. **关系抽取**（RE）——约束主题方向与关系类型集合（本体对齐）
4. **事件探查**（Event Extraction）——约束主题方向与事件类型体系
5. **三元组抽取**（Triple Extraction）——约束头尾实体类型与谓词集合

统一能力（用户 2026-10-02 澄清：**只留提示词入口，不做分项约束体系**）：

- **自定义提示词入口**：每个 LLM 抽取器接受一个 `prompt`/`instructions` 参数，整体替换默认提示词——抽取目的、方法、few-shot 例子、主题方向、类型约束、输出要求全部由用户在提示词里自由表达，框架不拆分、不额外建模
- 默认提示词保持中文场景开箱可用；未传 prompt 时行为与现状一致
- 输出仍走既有的结构化解析（generate_structured / 现有 schema），不新增校验层

复用现有 `semantica/llms/` 的 provider 抽象（OpenAI/DeepSeek/Qwen 等已接入），不新建 provider 层。

附属任务：**MinerU 4.0.10 支持说明**——fork 已完成 MinerU 4 双代 API 适配（v4 SDK + v2 回退，`parse-mineru` extra 装 `mineru[torch]>=4.0,<5`，backend→tier 映射），需在 `docs_zh/integrations/mineru.md` 与 README.zh-CN 补充说明（fork 支持最新版 4.0.10，官方 semantica 仍钉 2.x）。

## User Scenarios & Testing

### 主流程（以实体抽取为例）

用户在金融文档上运行 `NERExtractor(engine=llm, topic="金融", entity_types=["公司","产品","人名"])` → 只返回约束类型内的实体，附带置信度与来源 span → 更换 `prompt_template` 自定义提示词后抽取口径随之变化。

### 中文场景

中文文本中的指代（「该公司」「其子公司」）被正确链回先行词；三元组抽取输出中文谓词并遵守声明的关系类型集合。

### 异常路径

- LLM 输出不符合 schema：重试一次后仍失败则按配置降级（丢弃并告警 / 返回部分结果），绝不静默注入非法结构
- 约束类型白名单为空：拒绝启动并给出明确错误（不允许「不限」语义混入空列表）

## Requirements

### Functional Requirements

| ID | Requirement | Status |
| --- | --- | --- |
| FR-001 | 公共入口：五类抽取器统一接受 `prompt` 参数（整体替换默认提示词，承载目的/方法/例子/输出要求），不建分项约束配置 | Clear |
| FR-002 | 指代消解：LLM 驱动，输入篇章文本，输出代词—先行词链；支持约束消解范围（实体类型/人称类） | Clear |
| FR-003 | 实体抽取：LLM 模式，自定义提示词 + 主题方向 + 实体类型白名单；与现有规则 NER 并存可切换 | Clear |
| FR-004 | 关系抽取：LLM 模式，约束关系类型集合；输出对齐本体谓词 | Clear |
| FR-005 | 事件探查：LLM 模式，约束事件类型体系（触发词/论元角色） | Clear |
| FR-006 | 三元组抽取：LLM 模式，约束头尾实体类型与谓词集合 | Clear |
| FR-007 | MinerU 4.0.10 支持说明补充至 docs_zh/integrations/mineru.md 与 README.zh-CN | Clear |

### Non-goals

- 不新建 LLM provider 层（复用 `semantica/llms/`）
- 不做模型微调/本地推理优化（纯提示词工程）
- 英文语种的专项优化不在本期（骨架天然语言无关，英文提示词模板由后续按需补）

## Work Packages（草案，最终以 /spec-kitty.tasks 产出为准）

- WP01 公共骨架（FR-001）+ MinerU 文档说明（FR-007）
- WP02 指代消解（FR-002）
- WP03 实体抽取（FR-003）
- WP04 关系抽取（FR-004）
- WP05 事件探查（FR-005）
- WP06 三元组抽取（FR-006）

## 决策记录

- 2026-10-02 用户提出 7 项路线图待办（本 mission 覆盖其中 ③–⑦ 与 ①），要求统一「自定义提示词 + 约束主题方向/类型」能力
- 2026-10-02 用户澄清（提供 DeepSeek notebook 后）：抽取约束不做分项体系，**只要提示词入口**——目的、方法、例子、输出要求等全部经一个 prompt 参数灌入；FR-001 已按此改写
- 2026-10-02 **用户执行开闭原则裁决**：初版直接修改了上游 extract_*_llm / 三个 Extractor / CoreferenceResolver 源码，被否决。重构为纯扩展：`semantica/semantic_extract/prompt_extraction.py` 经官方 method_registry 注册 `"llm_prompt"` 方法 + provider 包装注入提示词 + 委托期旁路上游缓存（其键不含 prompt）；`resolve_aliases_llm` 为模块级函数。上游六文件零改动（测试守卫固化）。zh 侧同理：`ZhDateNormalizer` 组合扩展替代 DateNormalizer 路由改写
