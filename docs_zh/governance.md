---
title: 治理
description: 项目治理模式：角色、决策流程、发布节奏与代码评审准则。
source: governance.md
source_version: 8fa78d0a0b094bdef855b9e7241384109e7b2091
icon: "scale-balanced"
---

> Semantica 由 Semantica 团队在开放治理模式下维护，并接受社区贡献。


## 角色

- **维护者(Maintainers)**：Semantica 团队。评审并合并 PR，管理发布与代码质量，决定项目方向和社区规范。
- **贡献者(Contributors)**：提交代码、文档和缺陷报告，协助处理 issue 与评审。名字会收录进 [CONTRIBUTORS.md](https://github.com/semantica-agi/semantica/blob/main/CONTRIBUTORS.md)。
- **社区成员**：使用 Semantica、提供反馈、分享使用案例，并参与 GitHub Discussions 和 Discord。


## 决策流程

### 代码变更

<Steps>
  <Step title="提案">开一个 GitHub Issue，描述这项变更。</Step>
  <Step title="讨论">社区就技术方案和范围展开讨论。</Step>
  <Step title="实现">提交包含该变更的 pull request。</Step>
  <Step title="评审">至少一名维护者评审该 PR。</Step>
  <Step title="合并">CI 通过且维护者批准后合并。</Step>
</Steps>

### 重大决策

- 在 GitHub Issues 中发布 RFC
- 社区讨论期至少一周
- 维护者根据社区反馈和技术可行性做出决定


## 发布

Semantica 遵循**语义化版本**(Semantic Versioning)（`MAJOR.MINOR.PATCH`）：

| 级别 | 触发条件 | 节奏 |
| :------- | :--------- | :--------- |
| MAJOR | 破坏性变更 | 每季度或按需 |
| MINOR | 新功能（向后兼容） | 每月或就绪即发 |
| PATCH | 缺陷修复（向后兼容） | 修完即发 |


## 代码评审

**评审标准：** 功能性、代码质量、测试、文档、性能、安全性。

**时间线：** 首次评审在 48 小时内给出；后续跟进在 7 天内完成。

**对评审者的要求：** 保持建设性、说明理由、给出替代方案。

**对贡献者的要求：** 及时回应评论、有疑问就问、乐于接受反馈。


## 沟通渠道

- **GitHub Issues**：缺陷报告、功能请求和提问
- **GitHub PRs**：代码贡献
- **GitHub Discussions**：社区交流
- **安全公告**：[私下报告安全问题](https://github.com/semantica-agi/semantica/security/advisories/new)


## 项目目标

- **易用**：默认配置合理、文档清晰、流程精简，好用也好懂。
- **可靠**：生产级质量，在多种 Python 版本、平台和真实负载下经过测试。
- **性能**：从单机 notebook 到企业级图数据库(Graph Database)都高效、可扩展。
- **可扩展**：通过 `PluginRegistry` 模式即可轻松接入插件和自定义模块。
- **社区**：友好且包容。任何背景、任何经验水平的人都能贡献并获得认可。


## 许可证

MIT 许可证：详见 [LICENSE](https://github.com/semantica-agi/semantica/blob/main/LICENSE) 和[许可证页面](./project-license.md)。


## 延伸阅读

- [贡献指南](./contributing-guide.md)：如何提交变更。
- [社区](./community.md)：社区准则与沟通渠道。
