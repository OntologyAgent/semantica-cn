---
title: 安装
description: 一分钟内装好 Semantica。
source: installation.md
source_version: 5e434d894d25771912509a751cacf594dde6b809
icon: "download"
---

<Check>
  **已上架 PyPI**：`pip install semantica`，装完即用。
</Check>

<Note>
  需要 Python 3.10 或更高版本（支持 3.10–3.13），推荐 Python 3.11+。
</Note>

## 系统要求

| 组件 | 最低要求 | 推荐配置 |
| :--------- | :------- | :----------- |
| Python | 3.10 | 3.11+ |
| 操作系统 | Windows / Linux / Mac | Linux / Mac |
| 内存 | 4 GB | 16 GB+ |
| 存储 | 2 GB | 20 GB+（模型和数据） |


## 基础安装

```bash
pip install semantica
```

安装全部可选依赖：

```bash
pip install semantica[all]
```

<Note>
  **社区中文包 `semantica-cn`**：本站所属的 fork [OntologyAgent/semantica-cn](https://github.com/OntologyAgent/semantica-cn) 发布了同源构建的 `semantica-cn` 包，版本跟随上游同步。中文用户可以直接安装：

  ```bash
  pip install semantica-cn          # 基础安装
  pip install semantica-cn[all]     # 全部可选依赖
  ```

  安装后的 import 名和命令行工具仍然是 `semantica`（如 `import semantica`、`semantica-explorer`）。两种发行名对应同一个代码库，请在同一环境中二选一，不要同时安装。
</Note>

### 验证

```bash
python -c "import semantica; print(semantica.__version__)"
```


## 虚拟环境（推荐）

<Tabs>
  <Tab title="venv">
    ```bash
    python -m venv venv
    source venv/bin/activate   # Linux / Mac
    venv\Scripts\activate      # Windows
    pip install semantica
    ```
  </Tab>
  <Tab title="conda">
    ```bash
    conda create -n semantica python=3.11
    conda activate semantica
    pip install semantica
    ```
  </Tab>
</Tabs>


## 可选依赖

只装需要的部分：

<Tabs>
  <Tab title="GPU">
    ```bash
    pip install semantica[gpu]
    ```
    包含带 CUDA 的 PyTorch、FAISS GPU 和 CuPy。
  </Tab>
  <Tab title="可视化">
    ```bash
    pip install semantica[viz]
    ```
    包含 PyVis、Graphviz 和 UMAP。
  </Tab>
  <Tab title="LLM 提供商">
    ```bash
    pip install semantica[llm-all]       # all providers
    pip install semantica[llm-openai]    # OpenAI
    pip install semantica[llm-anthropic] # Anthropic
    pip install semantica[llm-gemini]    # Google Gemini
    pip install semantica[llm-groq]      # Groq
    pip install semantica[llm-ollama]    # Ollama (local)
    ```
  </Tab>
  <Tab title="云存储">
    ```bash
    pip install semantica[cloud]
    ```
    包含 AWS S3、Azure Blob 和 Google Cloud Storage。
  </Tab>
</Tabs>


## 从源码安装

想用最新的开发版，或想参与贡献时：

```bash
git clone https://github.com/semantica-agi/semantica.git
cd semantica

pip install -e .         # core only
pip install -e ".[all]"  # all extras
pip install -e . --group dev  # dev tools (pytest, black, etc.); needs pip 25.1+, or use `uv sync`
```

PyPI 发行版有问题时，可直接从 main 分支安装：

```bash
pip install git+https://github.com/semantica-agi/semantica.git@main
```


## 故障排查

<AccordionGroup>

<Accordion title="ModuleNotFoundError: No module named 'semantica'" icon="circle-xmark">

确认你处在正确的虚拟环境里：

```bash
pip list | grep semantica
pip install --upgrade semantica
```

</Accordion>

<Accordion title="安装时依赖报错" icon="triangle-exclamation">

```bash
pip install --upgrade pip
pip install build wheel
pip install semantica --no-deps  # install core first, then add extras
```

</Accordion>

<Accordion title="GPU 依赖安装失败" icon="bolt">

先装 CPU 版，再叠加 GPU 支持：

```bash
pip install semantica
pip install semantica[gpu]
```

</Accordion>

<Accordion title="权限被拒绝" icon="lock">

```bash
pip install --user semantica  # or use a virtual environment
```

</Accordion>

<Accordion title="Windows 上 [all] 安装失败" icon="windows">

**v0.5.0** 已修复。升级到最新版：

```bash
pip install --upgrade semantica
```

</Accordion>

<Accordion title="Windows 启动时 PyTorch DLL 报错" icon="windows">

安装 [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)。这是 Windows 系统依赖，不是 Semantica 的缺陷。

</Accordion>

</AccordionGroup>


## 下一步

- [入门指南](./getting-started.md) — 先弄清 Semantica 能做什么，再动手构建。
- [搭建流水线](./quickstart.md) — 跟着带代码的端到端流程走一遍。
- [浏览示例](cookbook.md) — 按用例分类的笔记本示例。
