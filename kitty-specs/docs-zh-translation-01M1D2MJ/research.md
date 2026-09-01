# Research: Semantica 中文文档翻译

**Mission**: docs-zh-translation-01M1D2MJ | **Date**: 2026-08-31

所有关键未知项在规划前调研（对话确认 + 仓库勘察）中已解决，本文记录决策与理由。无遗留 NEEDS CLARIFICATION。

## D1: 过期追踪机制 — git blob sha（而非内容 hash / mtime / 人工记录）

- **Decision**: 译文 frontmatter 记录翻译时的英文源文件 git blob sha，工具比对当前 sha 判定过期
- **Rationale**: blob sha 由 git 计算，内容不变则 sha 不变（无假阳性）；`git log --follow` 可追踪英文文件改名；无需额外状态文件，状态即 git 对象
- **Alternatives considered**:
  - 内容 hash（sha256sum）——需自建 hash 记录与更新逻辑，重复造 git 已有的轮子
  - mtime 比较——clone/checkout 会重置 mtime，完全不可靠
  - 记录 commit 号而非 blob sha——英文文件在两次 commit 间未变时产生假阳性（文件没变但 commit 前进了）

## D2: 目录策略 — docs/zh/ 1:1 镜像（而非平行仓库 / 独立命名）

- **Decision**: `docs/zh/quickstart.md` 严格对应 `docs/quickstart.md`
- **Rationale**: 同步逻辑零映射表；读者 URL 规律可循；`docs_check.py` 的递归 glob 会卷入 zh 文件，但其检查项（JSX 平衡、stale URL、代码块 3.8 语法）对合规译文是合理约束而非阻碍（已逐一核对检查函数）
- **Alternatives considered**:
  - 独立 `i18n/` 顶层目录——脱离 Mintlify 站点上下文，未来接入 Mintlify `navigation.languages` 时需整体搬迁
  - 改 docs_check.py 排除 zh——侵入上游脚本，违反 C-001

## D3: 分层策略 — P0/P1/P2/P3 四层（而非全量直翻）

- **Decision**: P0 门面 9 篇精翻 → P1 高频 4 篇起步 → P2 reference 29 篇后期批量 → P3 社区类 5 篇与 changelog 不翻
- **Rationale**: 83 篇/16 万词全量直翻交付周期长且大部分页面低频访问；changelog 持续变动，翻译维护成本无穷大
- **Alternatives considered**: 全量翻译——维护负担与价值不成比例

## D4: Mintlify i18n 接入 — 现阶段不改 docs.json

- **Decision**: 译文不进上游 `docs.json` 导航；中文站部署留待第三期独立决策
- **Rationale**: `docs.json` 是上游高频改动文件，任何修改都制造合并冲突；Mintlify 构建不感知未注册页面，`docs_check.py` 的 nav 检查不受影响
- **Alternatives considered**: 立即给上游提 PR 启用 `navigation.languages`——超出本 Mission 范围，且应先有稳定译文再谈上游贡献

## D5: 验收门 — docs_check.py 全绿（而非新造检查器）

- **Decision**: 译文合规性复用上游 `python docs_check.py`，不新增 CI 门
- **Rationale**: 该脚本已覆盖 JSX 平衡、死链、stale URL 等译文同样需要满足的约束；自建 workflow 属第二期增量
- **Alternatives considered**: 自建 zh 专用检查 workflow——第二期再评估，首期以本地工具跑通为先

## D6: 复用封装 — 项目级 Claude Skill

- **Decision**: 规范/工具/流程封装为 `.claude/skills/docs-zh-translation/SKILL.md`，单一事实源仍是 `docs/zh/README.md` 与本 Mission 产物
- **Rationale**: 用户要求可反复使用；Skill 只做"流程编排 + 指路"，规范细节不复制进 Skill，避免双源漂移
- **Alternatives considered**: 把规范全文写进 SKILL.md——两处维护必然漂移
