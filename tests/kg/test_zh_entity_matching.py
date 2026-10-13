"""Chinese-language support in core utilities (fork extensions).

Three long-standing gaps, one per test class:
- NamingConventions.normalize_class_name reduced CJK names to the "Entity"
  placeholder because _to_pascal_case only harvested ASCII word characters.
- split_by_sentences' regex fallback ignored CJK terminal punctuation
  (。！？；), so Chinese paragraphs never split without whitespace.
- EntityResolver._detect_duplicate_groups keyed names verbatim, so
  "华跃控股北京有限公司" and "华跃控股北京" stayed separate entities.
"""

import re

import pytest

from semantica.kg.entity_resolver import EntityResolver
from semantica.ontology.naming_conventions import NamingConventions
from semantica.split.methods import _split_sentences_regex, split_by_sentences


class TestNormalizeClassNameKeepsCjk:
    def test_pure_cjk_name_returns_itself(self):
        assert NamingConventions().normalize_class_name("政策") == "政策"

    def test_mixed_cjk_name_preserved(self):
        assert NamingConventions().normalize_class_name("合同管理") == "合同管理"

    def test_ascii_behaviour_unchanged(self):
        nc = NamingConventions()
        assert nc.normalize_class_name("Policy") == "Policy"
        assert nc.normalize_class_name("contract_item") == "ContractItem"

    def test_empty_still_falls_back(self):
        assert NamingConventions().normalize_class_name("!!!") == "Entity"


class TestSentenceSplitCjkPunctuation:
    TEXT = "华跃控股成立于2018年。其主要业务为医药流通。营收超过百亿！现状如何？另有分号；也算一句。"

    def test_regex_splits_on_cjk_punctuation(self):
        sentences = _split_sentences_regex(self.TEXT)
        assert len(sentences) == 6
        assert sentences[0].endswith("。")
        assert sentences[2].endswith("！")
        assert sentences[4].endswith("；")

    def test_ascii_sentences_unchanged(self):
        text = "First sentence. Second one! Third?"
        assert _split_sentences_regex(text) == ["First sentence.", "Second one!", "Third?"]

    def test_decimal_numbers_not_split(self):
        assert _split_sentences_regex("增长了3.14个百分点") == ["增长了3.14个百分点"]

    def test_split_by_sentences_chunking_cjk(self):
        chunks = split_by_sentences(self.TEXT, chunk_size=30)
        assert len(chunks) >= 2
        rejoined = "".join(chunk.text for chunk in chunks)
        assert re.sub(r"\s+", "", rejoined) == re.sub(r"\s+", "", self.TEXT)


class TestEntityResolverCjkSuffixes:
    def _entities(self, *names):
        return [
            {"id": f"e{i}", "type": "company", "name": name}
            for i, name in enumerate(names)
        ]

    def test_company_suffix_stripped_for_grouping(self):
        resolver = EntityResolver()
        merged = resolver.merge_duplicates(
            self._entities("华跃控股北京有限公司", "华跃控股北京")
        )
        assert len(merged) == 1

    def test_distinct_names_stay_distinct(self):
        resolver = EntityResolver()
        merged = resolver.merge_duplicates(
            self._entities("华跃控股北京有限公司", "杭州岭川制药有限公司")
        )
        assert len(merged) == 2

    def test_english_suffix_still_supported(self):
        resolver = EntityResolver()
        merged = resolver.merge_duplicates(
            self._entities("Acme Corp", "Acme")
        )
        assert len(merged) == 1
