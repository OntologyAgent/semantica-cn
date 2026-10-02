# Quickstart: 提示词入口

**Mission**: llm-extractor-family-01M3X5J7

```bash
cd /Users/luofisher/ToolsChain/semantica-cn && source .venv/bin/activate
git checkout feature/llm-extractor-family
```

## 五分钟用起来

```python
from semantica.semantic_extract import NERExtractor, resolve_aliases_llm

ner = NERExtractor(method="llm_prompt", provider="deepseek", llm_model="deepseek-flash",
                   api_key=KEY, prompt="只抽取医药政策里的公司全称与政策编号，输出宁缺毋滥")
entities = ner.extract("……")

resolved = resolve_aliases_llm(text, provider="deepseek", api_key=KEY)
```

## 验证

```bash
uv run --frozen pytest tests/semantic_extract/test_prompt_entry.py tests/semantic_extract/test_coref_llm.py -q
bash tools/nightly/run_gate.sh
```

## 边界速查

- 未传 prompt = 官方默认行为，零变化
- prompt 里自带输出要求即可；框架的 schema 守卫尾兜底解析
- resolve_aliases_llm 的 min_confidence 默认 0.85，防幻觉映射
