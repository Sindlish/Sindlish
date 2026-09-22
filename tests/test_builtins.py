"""Tests for builtin functions: lambi and likh (as function call)."""

import pytest

from interpreter.errors import MatalabJeGhalti
from tests.conftest import extract_value, run


class TestLambi:
    """len()"""

    def test_lambi_list(self):
        interp, _ = run("x = [1, 2, 3]\nval = lambi(x)")
        assert extract_value(interp.variables["val"]["value"]) == 3

    def test_lambi_string(self):
        interp, _ = run('val = lambi("hello")')
        assert extract_value(interp.variables["val"]["value"]) == 5

    def test_lambi_empty_list(self):
        interp, _ = run("val = lambi([])")
        assert extract_value(interp.variables["val"]["value"]) == 0

    def test_lambi_empty_string(self):
        interp, _ = run('val = lambi("")')
        assert extract_value(interp.variables["val"]["value"]) == 0


class TestLikhFunction:
    """likh() as a function call (via CallNode)"""

    def test_likh_single_arg(self):
        _, out = run('likh("test")')
        assert out.strip() == "test"

    def test_likh_number(self):
        _, out = run("likh(42)")
        assert out.strip() == "42"

    def test_likh_multiple_args(self):
        _, out = run('likh("a", "b")')
        assert out.strip() == "a b"


class TestLikhKwargs:
    """likh(vich=, akhir=) keyword arguments (SEP 78, SEP 80)."""

    def test_default_behavior_unchanged(self):
        _, out = run('likh("a", "b")')
        assert out == "a b\n"

    def test_custom_vich(self):
        _, out = run('likh("a", "b", vich=", ")')
        assert out == "a, b\n"

    def test_custom_akhir(self):
        _, out = run('likh("a", "b", akhir="!")')
        assert out == "a b!"

    def test_no_newline_continuation(self):
        _, out = run('likh("a", akhir="")\nlikh("b")')
        assert out == "ab\n"

    def test_single_value_ignores_vich(self):
        # vich only sits between values; with a single value it is discarded
        _, out = run('likh("solo", vich=", ")')
        assert out == "solo\n"

    def test_single_value_with_akhir(self):
        _, out = run('likh("solo", akhir="!\n")')
        assert out == "solo!\n"

    def test_kwargs_dict_splat(self):
        _, out = run('k = {"vich": "-"}\nlikh("a", "b", **k)')
        assert out == "a-b\n"

    def test_positional_third_arg_is_a_printed_value(self):
        # vich/akhir are keyword-only; a third positional is just another value
        _, out = run('likh("a", "b", "-")')
        assert out == "a b -\n"

    def test_old_sep_kwarg_raises(self):
        with pytest.raises(MatalabJeGhalti, match="Achanak keyword"):
            run('likh("x", sep=", ")')

    def test_unknown_kwarg_raises(self):
        with pytest.raises(MatalabJeGhalti, match="Achanak keyword"):
            run('likh("x", bogus=1)')

    def test_kwargs_dict_unknown_key_raises(self):
        with pytest.raises(MatalabJeGhalti, match="Achanak keyword"):
            run('k = {"bogus": 1}\nlikh("x", **k)')


class TestBuiltinKwargRejection:
    """Builtins without a kwarg spec reject any keyword argument."""

    def test_lambi_rejects_kwargs(self):
        with pytest.raises(MatalabJeGhalti, match="Achanak keyword"):
            run('lambi("abc", bogus=1)')

    def test_silsilo_rejects_known_kwarg_name(self):
        with pytest.raises(MatalabJeGhalti, match="Achanak keyword"):
            run("silsilo(1, 5, step=1)")
