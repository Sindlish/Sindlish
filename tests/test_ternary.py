"""Tests for the ternary conditional expression (x agar shart warna y).

SEP #46: Sindlish-only ternary, sits below `ya` (or) and above assignment,
left-associative, both arms mandatory. Compiles to the same
JUMP_IF_FALSE / JUMP_ABSOLUTE back-patching as the `agar` statement, leaving
exactly one value on the stack.
"""

import pytest

from interpreter.errors import LikhaiJeGhalti
from tests.conftest import get_variable_value, run


class TestTernaryBasic:
    def test_true_arm_value(self):
        vm, _ = run('x = "haan" agar 1 > 0 warna "na"')
        assert get_variable_value(vm, "x") == "haan"

    def test_false_arm_value(self):
        vm, _ = run('x = "haan" agar 0 > 1 warna "na"')
        assert get_variable_value(vm, "x") == "na"

    def test_statement_position_discards_value(self):
        _, out = run('likh("yes") agar sach warna likh("no")')
        assert out.strip() == "yes"

    def test_statement_position_false_discards_value(self):
        _, out = run('likh("yes") agar koorh warna likh("no")')
        assert out.strip() == "no"

    def test_arms_can_be_any_expression(self):
        vm, _ = run("x = 2 + 3 agar 1 > 0 warna 10 + 10")
        assert get_variable_value(vm, "x") == 5

    def test_false_arm_any_expression(self):
        vm, _ = run("x = 2 + 3 agar 0 > 1 warna 10 + 10")
        assert get_variable_value(vm, "x") == 20


class TestTernaryShortCircuit:
    def test_unused_arm_not_evaluated(self):
        vm, out = run('x = "kept" agar sach warna likh("else-arm-ran")')
        assert out.strip() == ""
        assert get_variable_value(vm, "x") == "kept"

    def test_true_arm_evaluated_when_true(self):
        vm, out = run('x = likh("if-arm-ran") agar sach warna "kept"')
        assert out.strip() == "if-arm-ran"
        assert get_variable_value(vm, "x") is None  # likh() returns khali

    def test_no_side_effects_in_untaken_arm(self):
        code = """
kaam side() {
    likh("boom")
    wapas 1
}
x = side() agar koorh warna 42
"""
        vm, out = run(code)
        assert out.strip() == ""
        assert get_variable_value(vm, "x") == 42


class TestTernaryPrecedence:
    def test_binds_tighter_than_assignment(self):
        vm, _ = run("x = 1 + 2 agar sach warna 9")
        assert get_variable_value(vm, "x") == 3

    def test_arms_at_or_level(self):
        vm, _ = run("x = 1 agar koorh warna 2 + 3")
        assert get_variable_value(vm, "x") == 5

    def test_condition_includes_or(self):
        # condition parses at `ya` level: `sach ya koorh` is truthy -> 1
        vm, _ = run("x = 1 agar sach ya koorh warna 2")
        assert get_variable_value(vm, "x") == 1

    def test_sits_below_or_expression(self):
        # `(1 > 0) ya (2 > 5)` is truthy -> true arm
        vm, _ = run("x = 100 agar 1 > 0 ya 2 > 5 warna 200")
        assert get_variable_value(vm, "x") == 100

    def test_binds_tighter_than_call_argument_comma(self):
        _, out = run("likh(1 agar sach warna 2)")
        assert out.strip() == "1"


class TestTernaryAssociativity:
    def test_left_associative_chain(self):
        # (1 agar koorh warna 2) agar sach warna 3 -> inner yields 2 -> 2
        vm, _ = run("x = 1 agar koorh warna 2 agar sach warna 3")
        assert get_variable_value(vm, "x") == 2

    def test_left_associative_chain_second_cond_false(self):
        # (1 agar sach warna 2) agar koorh warna 3 -> inner yields 1 -> 3
        vm, _ = run("x = 1 agar sach warna 2 agar koorh warna 3")
        assert get_variable_value(vm, "x") == 3

    def test_parenthesised_nesting_in_else_arm(self):
        vm, _ = run("x = 1 agar koorh warna (5 agar sach warna 6)")
        assert get_variable_value(vm, "x") == 5

    def test_parenthesised_nesting_in_condition(self):
        # inner ternary yields koorh -> outer condition false -> 2
        vm, _ = run("x = 1 agar (koorh agar sach warna sach) warna 2")
        assert get_variable_value(vm, "x") == 2


class TestTernaryIntegration:
    def test_in_if_body(self):
        code = """
x = 10
y = 0
agar x > 5 {
    y = x agar x > 8 warna 8
} warna {
    y = 0
}
"""
        vm, _ = run(code)
        assert get_variable_value(vm, "y") == 10

    def test_in_function_body(self):
        code = """
kaam clamp(n) {
    wapas n agar n < 100 warna 100
}
x = clamp(150)
"""
        vm, _ = run(code)
        assert get_variable_value(vm, "x") == 100

    def test_as_function_argument(self):
        _, out = run("likh(1 agar koorh warna 2)")
        assert out.strip() == "2"

    def test_in_while_condition(self):
        # `warna koorh` (not a raw number) so the loop can actually exit:
        # raw numbers are always truthy in Sindlish (SdNumber has no __bool__).
        code = """
n = 0
jistain n agar n < 3 warna koorh {
    n = n + 1
}
"""
        vm, _ = run(code)
        assert get_variable_value(vm, "n") == 3

    def test_in_list_literal(self):
        vm, _ = run("xs = [1 agar sach warna 9, 2]")
        assert get_variable_value(vm, "xs") == [1, 2]

    def test_in_har_loop(self):
        code = """
total = 0
har x mein [1, 2, 3] {
    total = total + (x agar x > 1 warna 10)
}
"""
        vm, _ = run(code)
        assert get_variable_value(vm, "total") == 10 + 2 + 3

    def test_multiline_with_parens(self):
        code = """
x = (1 agar
     sach
     warna
     2)
"""
        vm, _ = run(code)
        assert get_variable_value(vm, "x") == 1

    def test_typed_declaration(self):
        # SEP #46 flagship: `adad max = a agar a > b warna b`
        vm, _ = run("adad max = 7 agar 7 > 3 warna 3")
        assert get_variable_value(vm, "max") == 7

    def test_pakko_declaration(self):
        vm, _ = run("pakko m = 7 agar 7 < 3 warna 9")
        assert get_variable_value(vm, "m") == 9

    def test_call_in_arms(self):
        # SEP shape: `status = "pass" agar f.score() >= 60 warna "fail"`
        code = """
kaam score() {
    wapas 61
}
s = "pass" agar score() >= 60 warna "fail"
"""
        vm, _ = run(code)
        assert get_variable_value(vm, "s") == "pass"

    def test_as_dict_value(self):
        vm, _ = run('d = {"a": 1 agar sach warna 2}')
        assert get_variable_value(vm, "d") == {"a": 1}

    def test_as_return_value(self):
        code = """
kaam pick() {
    wapas 1 agar sach warna 2
}
x = pick()
"""
        vm, _ = run(code)
        assert get_variable_value(vm, "x") == 1

    def test_as_index_expression(self):
        vm, _ = run("xs = [10, 20]\ny = xs[0 agar sach warna 1]")
        assert get_variable_value(vm, "y") == 10

    def test_as_operand_needs_parens(self):
        vm, _ = run("x = (1 agar sach warna 2) + 3")
        assert get_variable_value(vm, "x") == 4


class TestTernaryGhalt:
    def test_missing_warna_raises(self):
        with pytest.raises(LikhaiJeGhalti, match="warna"):
            run("x = 5 agar 3 > 2")

    def test_missing_warna_in_call_raises(self):
        with pytest.raises(LikhaiJeGhalti, match="warna"):
            run("likh(5 agar 3 > 2)")

    def test_missing_warna_multiline_raises(self):
        with pytest.raises(LikhaiJeGhalti, match="warna"):
            run("x = 5 agar\n3 > 2")

    def test_error_carries_position(self):
        with pytest.raises(LikhaiJeGhalti) as exc_info:
            run("x = 1\ny = 5 agar 3 > 2")
        err = exc_info.value
        assert getattr(err, "line", None) == 2

    def test_c_style_ternary_rejected(self):
        # `?` stays reserved for Result unwrap; there is no `cond ? a : b`.
        with pytest.raises(LikhaiJeGhalti):
            run("x = 1 ? 2 : 3")

    def test_stray_warna_without_expression_rejected(self):
        with pytest.raises(LikhaiJeGhalti):
            run("x = warna 5")

    def test_trailing_warna_without_agar_rejected(self):
        with pytest.raises(LikhaiJeGhalti):
            run("x = 5 warna 3")

    def test_missing_condition_rejected(self):
        with pytest.raises(LikhaiJeGhalti):
            run("x = 5 agar warna 3")

    def test_unparenthesised_nested_ternary_in_condition_rejected(self):
        # nested ternaries require parens (left-assoc otherwise: x agar y warna z agar w warna v)
        with pytest.raises(LikhaiJeGhalti, match="warna"):
            run("x = 5 agar 1 agar sach warna koorh warna 9")
