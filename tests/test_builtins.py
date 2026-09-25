"""Tests for builtin functions: lambi, likh and silsilo (as function call)."""

import pytest

from interpreter.errors import HalndeVaktGhalti, MatalabJeGhalti, QisamJeGhalti
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


def silsilo_value(expr):
    """Run a silsilo expression and hand back the SdRange it produced."""
    vm, _ = run(f"r = {expr}")
    return vm.globals.records["r"].value


def snapshot(sd_range):
    """Reduce a SdRange to the shape the SEP compares: bounds, len, iteration."""
    return (
        sd_range.start,
        sd_range.stop,
        sd_range.step,
        len(sd_range),
        [n.value for n in sd_range],
    )


class TestSilsiloKwargs:
    """silsilo(shuru=, akhir=, qadam=) keyword arguments (SEP 81)."""

    @pytest.mark.parametrize(
        "kwarg_call,positional_twin",
        [
            ("silsilo(akhir=5)", "silsilo(5)"),
            ("silsilo(shuru=1, akhir=5)", "silsilo(1, 5)"),
            ("silsilo(shuru=1, akhir=10, qadam=2)", "silsilo(1, 10, 2)"),
            ("silsilo(qadam=2, akhir=10)", "silsilo(0, 10, 2)"),
            ("silsilo(shuru=10, akhir=0, qadam=-2)", "silsilo(10, 0, -2)"),
            ("silsilo(shuru=5, akhir=1)", "silsilo(5, 1)"),
        ],
    )
    def test_keyword_form_equals_positional_twin(self, kwarg_call, positional_twin):
        assert snapshot(silsilo_value(kwarg_call)) == snapshot(
            silsilo_value(positional_twin)
        )

    @pytest.mark.parametrize(
        "mixed_call,positional_twin",
        [
            ("silsilo(1, 2, qadam=3)", "silsilo(1, 2, 3)"),
            ("silsilo(1, akhir=5, qadam=2)", "silsilo(1, 5, 2)"),
        ],
    )
    def test_mixed_positional_and_keyword(self, mixed_call, positional_twin):
        assert snapshot(silsilo_value(mixed_call)) == snapshot(
            silsilo_value(positional_twin)
        )

    def test_kwargs_dict_splat(self):
        code = 'k = {"shuru": 1, "akhir": 10, "qadam": 2}\nr = silsilo(**k)'
        vm, _ = run(code)
        assert snapshot(vm.globals.records["r"].value) == snapshot(
            silsilo_value("silsilo(1, 10, 2)")
        )

    def test_keyword_names_are_independent_of_order(self):
        assert snapshot(silsilo_value("silsilo(shuru=1, qadam=2, akhir=10)")) == snapshot(
            silsilo_value("silsilo(1, 10, 2)")
        )

    def test_explicit_zero_is_not_mistaken_for_an_unset_keyword(self):
        # shuru=0 equals the default, so a value comparison would lose it
        assert snapshot(silsilo_value("silsilo(shuru=0, akhir=5)")) == snapshot(
            silsilo_value("silsilo(0, 5)")
        )

    def test_explicit_default_step_is_not_mistaken_for_an_unset_keyword(self):
        assert snapshot(silsilo_value("silsilo(1, 5, qadam=1)")) == snapshot(
            silsilo_value("silsilo(1, 5)")
        )
        with pytest.raises(MatalabJeGhalti, match=r"(?i)dobara"):
            run("silsilo(1, 2, 3, qadam=1)")

    def test_star_args_splat_reaches_the_positional_path(self):
        assert snapshot(silsilo_value("silsilo(*[1, 2])")) == snapshot(
            silsilo_value("silsilo(1, 2)")
        )

    def test_empty_kwargs_dict_splat_is_no_keywords(self):
        assert snapshot(silsilo_value("silsilo(1, 2, **{})")) == snapshot(
            silsilo_value("silsilo(1, 2)")
        )
        with pytest.raises(MatalabJeGhalti, match=r"1, 2, ya 3"):
            run("silsilo(**{})")

    def test_range_stays_lazy(self):
        _, out = run("likh(qisam(silsilo(1, 5, qadam=2)))")
        assert out.strip() == "SILSILO"

    def test_str_representation_unchanged(self):
        _, out = run("likh(silsilo(shuru=1, akhir=5, qadam=2))")
        assert "silsilo(1, 5, 2)" in out

    @pytest.mark.parametrize("name", ["bogus", "start", "stop", "step"])
    def test_unknown_kwarg_raises(self, name):
        with pytest.raises(MatalabJeGhalti, match="Achanak keyword"):
            run(f"silsilo(1, 5, {name}=1)")

    def test_kwargs_dict_unknown_key_raises(self):
        with pytest.raises(MatalabJeGhalti, match="Achanak keyword"):
            run('k = {"bogus": 1}\nsilsilo(1, 5, **k)')

    def test_zero_step_raises(self):
        with pytest.raises(HalndeVaktGhalti, match="(?i)step"):
            run("silsilo(akhir=10, qadam=0)")

    @pytest.mark.parametrize(
        "code",
        [
            "silsilo(shuru=1.5, akhir=5)",
            "silsilo(shuru=1, akhir=2.5)",
            "silsilo(shuru=1, akhir=5, qadam=0.5)",
            'silsilo(shuru="a", akhir=5)',
        ],
    )
    def test_non_integer_keyword_argument_raises(self, code):
        with pytest.raises(QisamJeGhalti, match=r"(?i)adad"):
            run(code)

    def test_non_integer_keyword_message_names_the_keyword(self):
        with pytest.raises(QisamJeGhalti, match="qadam"):
            run("silsilo(shuru=1, akhir=5, qadam=1.5)")

    @pytest.mark.parametrize(
        "code",
        [
            "silsilo(1, 2, akhir=3)",
            "silsilo(1, 2, 3, shuru=0)",
            "silsilo(shuru=1, 2)",
        ],
    )
    def test_repeated_argument_raises(self, code):
        with pytest.raises(MatalabJeGhalti, match=r"(?i)dobara"):
            run(code)

    def test_missing_akhir_raises(self):
        with pytest.raises(MatalabJeGhalti, match="akhir"):
            run("silsilo(1, qadam=3)")

    def test_too_many_positional_and_keyword_raises(self):
        with pytest.raises(MatalabJeGhalti, match=r"1, 2, ya 3"):
            run("silsilo(1, 2, 3, 4, qadam=1)")


class TestBuiltinKwargRejection:
    """Builtins without a kwarg spec reject any keyword argument."""

    def test_lambi_rejects_kwargs(self):
        with pytest.raises(MatalabJeGhalti, match="Achanak keyword"):
            run('lambi("abc", bogus=1)')

    def test_puch_rejects_kwargs(self):
        with pytest.raises(MatalabJeGhalti, match="Achanak keyword"):
            run("puch('hi', bogus=1)")

    def test_qisam_rejects_kwargs(self):
        with pytest.raises(MatalabJeGhalti, match="Achanak keyword"):
            run("qisam(1, bogus=1)")

    def test_english_step_kwarg_raises(self):
        with pytest.raises(MatalabJeGhalti, match="Achanak keyword"):
            run("silsilo(1, 5, step=1)")
