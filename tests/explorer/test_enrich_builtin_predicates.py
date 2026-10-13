"""Builtin predicate support in the fallback reasoner (fork fix).

The reasoning playground's fallback reasoner matched antecedents only
against facts, so builtin predicates like ``not_equal(?x, Y)`` and
``ge(?v, 50)`` silently dropped every rule that used them — numeric rules
from the sinopharm rule library never fired. Builtin predicates evaluate
against the accumulated bindings instead: pass (keep the bindings) or fail
(drop them); unresolvable or non-numeric arguments fail the antecedent.
"""

from semantica.explorer.routes.enrich import _run_fallback_reasoner


class TestBuiltinComparisonPredicates:
    def test_ge_fires_only_above_threshold(self):
        inferred = _run_fallback_reasoner(
            facts=["amount(az:doc1, 120)", "amount(az:doc2, 30)"],
            rules=["IF amount(?doc, ?v) AND ge(?v, 50) THEN high_value(?doc)"],
        )
        assert inferred == ["high_value(az:doc1)"]

    def test_gt_le_lt_comparisons(self):
        assert _run_fallback_reasoner(
            ["v(a, 10)", "v(b, 10)"],
            ["IF v(?x, ?n) AND gt(?n, 9) THEN gt_hit(?x)"],
        ) == ["gt_hit(a)", "gt_hit(b)"]
        assert _run_fallback_reasoner(
            ["v(a, 10)"],
            ["IF v(?x, ?n) AND le(?n, 10) THEN le_hit(?x)"],
        ) == ["le_hit(a)"]
        assert _run_fallback_reasoner(
            ["v(a, 10)"],
            ["IF v(?x, ?n) AND lt(?n, 10) THEN lt_hit(?x)"],
        ) == []

    def test_not_equal_passes_only_when_bindings_differ(self):
        inferred = _run_fallback_reasoner(
            facts=["party(az:doc1, Foo)", "party(az:doc2, AzRenZheng)"],
            rules=["IF party(?doc, ?p) AND not_equal(?p, AzRenZheng) THEN external_party(?doc)"],
        )
        assert inferred == ["external_party(az:doc1)"]

    def test_non_numeric_argument_fails_the_antecedent(self):
        assert _run_fallback_reasoner(
            ["v(a, ten)"],
            ["IF v(?x, ?n) AND ge(?n, 5) THEN hit(?x)"],
        ) == []

    def test_unbound_variable_fails_the_antecedent(self):
        assert _run_fallback_reasoner(
            ["v(a, 1)"],
            ["IF v(?x, ?n) AND ge(?m, 5) THEN hit(?x)"],
        ) == []

    def test_regular_fact_matching_still_works(self):
        inferred = _run_fallback_reasoner(
            facts=["parent(alice, bob)"],
            rules=["IF parent(?x, ?y) THEN ancestor(?x, ?y)"],
        )
        assert inferred == ["ancestor(alice, bob)"]
