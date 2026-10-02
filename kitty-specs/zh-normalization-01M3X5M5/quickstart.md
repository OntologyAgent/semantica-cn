# Quickstart: 中文规范化上手

**Mission**: zh-normalization-01M3X5M5

## 1. 环境

```bash
cd /Users/luofisher/ToolsChain/semantica-cn
source .venv/bin/activate
git checkout feature/zh-normalization   # mission 分支
```

## 2. 五分钟用起来

```python
from semantica.normalize import CJKSpacingNormalizer, ZhDateParser, DateNormalizer

# CJK 空格
CJKSpacingNormalizer().normalize("Semantica知识图谱，AI驱动决策")
# -> "Semantica 知识图谱，AI 驱动决策"

# 中文日期
ZhDateParser().parse("2026年10月2日 14:30")["value"]
# -> datetime(2026, 10, 2, 14, 30)

# 既有入口直接吃中文
DateNormalizer().normalize_date("2026年10月2日")
```

## 3. 验证

```bash
uv run --frozen pytest tests/normalize/test_cjk_spacing.py tests/normalize/test_zh_date_parser.py -q
bash tools/nightly/run_gate.sh   # 门禁：失败数 ≤ 基线 51
```

## 4. 边界行为速查

- 纯英文文本零改动；`2月30日` 拒绝；农历/民国纪年原样保留并计数
- policy="remove" 是反向操作（`Semantica 知识图谱` → `Semantica知识图谱`）
