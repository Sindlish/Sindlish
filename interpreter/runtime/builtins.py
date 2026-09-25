"""
Built-in functions for the Sindlish language.

Standalone functions available in the global scope: lambi, likh, majmuo, puch, qisam, silsilo.
"""

from typing import ClassVar

from ..errors import HalndeVaktGhalti, MatalabJeGhalti, QisamJeGhalti
from ..objects import SdNull, SdNumber, SdRange, SdSet, SdString


def register(registry_dict):
    """Decorator to auto-register functions into a dictionary."""

    def decorator(func):
        registry_dict[func.__name__] = func
        return func

    return decorator


KWARG_UNSET = object()

SILSILO_SLOTS = ("shuru", "akhir", "qadam")


class SimpleBuiltins:
    """Built-in standalone functions available in the global scope."""

    functions: ClassVar[dict] = {}

    # Registered-name -> {keyword argument: default value}. The VM validates
    # every keyword against this spec, fills defaults, then hands the bound
    # kwargs dict to the builtin. Builtins absent from this mapping reject
    # all keyword arguments. A spec whose defaults are KWARG_UNSET declares
    # names the builtin must distinguish "caller passed it" from "filled in
    # for the caller" — it recovers the passed ones by identity.
    kwarg_specs: ClassVar[dict] = {
        "likh": {"vich": SdString(" "), "akhir": SdString("\n")},
        "silsilo": dict.fromkeys(SILSILO_SLOTS, KWARG_UNSET),
    }

    @staticmethod
    def resolve_kwargs(name, kwargs: dict) -> dict:
        """Reject unknown names and fill declared defaults for a builtin call."""
        spec = SimpleBuiltins.kwarg_specs.get(name, {})
        for key in kwargs:
            if key not in spec:
                raise MatalabJeGhalti(f"Achanak keyword argument '{key}' milo.")
        for key, default in spec.items():
            kwargs.setdefault(key, default)
        return kwargs

    @register(functions)
    def majmuo(self, args, kwargs=None):
        """Create a new set from arguments."""
        if len(args) == 0:
            return SdSet(set())
        if len(args) == 1:
            return SdSet(set(args[0]))
        raise MatalabJeGhalti("majmuo() khe 0 ya 1 argument khapay.")

    @register(functions)
    def lambi(self, args, kwargs=None):
        """Return the length of a collection or string."""
        if len(args) != 1:
            raise MatalabJeGhalti("lambi() khe sirf 1 argument khapay.")
        obj = args[0]
        if isinstance(obj, SdRange):
            return SdNumber(len(obj))
        if hasattr(obj, "elements"):
            return SdNumber(len(obj.elements))
        if hasattr(obj, "pairs"):
            return SdNumber(len(obj.pairs))
        if hasattr(obj, "value") and isinstance(obj.value, (str, dict)):
            return SdNumber(len(obj.value))
        raise QisamJeGhalti(f"'{obj.type.name}' ji lambai nathi mapay saghjay.")

    @register(functions)
    def likh(self, args, kwargs=None):
        """Print values to stdout, joined with ``vich`` and finished with ``akhir``."""
        kwargs = {} if kwargs is None else kwargs
        sep = str(kwargs.get("vich", SdString(" ")))
        end = str(kwargs.get("akhir", SdString("\n")))
        print(*(str(arg) for arg in args), sep=sep, end=end)
        return SdNull()

    @register(functions)
    def puch(self, args, kwargs=None):
        """Takes input from user."""
        prompt = " ".join(str(arg) for arg in args)
        return SdString(input(prompt))

    @staticmethod
    def silsilo_adad(label, value):
        """Require an int SdNumber, reporting it as ``label`` in the message."""
        if not isinstance(value, SdNumber):
            raise QisamJeGhalti(
                f"silsilo() khe '{label}' argument 'adad' khapyo paye, par "
                f"'{value.type.name}' milyo."
            )
        if not isinstance(value.value, int):
            raise QisamJeGhalti(
                f"silsilo() khe '{label}' argument 'adad' khapyo paye, par 'dahai' milyo."
            )
        return int(value.value)

    @register(functions)
    def silsilo(self, args, kwargs=None):
        """Return a lazy range from shuru (inclusive) to akhir (exclusive) stepping by qadam."""
        supplied = (
            {}
            if kwargs is None
            else {name: value for name, value in kwargs.items() if value is not KWARG_UNSET}
        )

        if not supplied:
            values = [self.silsilo_adad(f"{i + 1}jo", arg) for i, arg in enumerate(args)]
            if len(values) == 1:
                start, end, step = 0, values[0], 1
            elif len(values) == 2:
                start, end, step = values[0], values[1], 1
            elif len(values) == 3:
                start, end, step = values
            else:
                raise MatalabJeGhalti("silsilo() khe 1, 2, ya 3 arguments khapan.")
        else:
            if len(args) > len(SILSILO_SLOTS):
                raise MatalabJeGhalti("silsilo() khe 1, 2, ya 3 arguments khapan.")
            bound = {}
            for i, arg in enumerate(args):
                slot = SILSILO_SLOTS[i]
                if slot in supplied:
                    raise MatalabJeGhalti(f"silsilo() khe '{slot}' argument dobara milo.")
                bound[slot] = self.silsilo_adad(f"{i + 1}jo", arg)
            for slot, value in supplied.items():
                bound[slot] = self.silsilo_adad(slot, value)
            if "akhir" not in bound:
                raise MatalabJeGhalti("silsilo() khe 'akhir' argument laai value lazmi aahe.")
            start = bound.get("shuru", 0)
            end = bound["akhir"]
            step = bound.get("qadam", 1)

        if step == 0:
            raise HalndeVaktGhalti("silsilo() jo step zero (0) natho thi saghjay.")

        return SdRange(start, end, step)

    @register(functions)
    def qisam(self, args, kwargs=None):
        """Returns the type of the object."""
        if len(args) != 1:
            raise MatalabJeGhalti("qisam() khe sirf 1 argument khapay.")
        try:
            return SdString(args[0].type.name)
        except AttributeError:
            raise HalndeVaktGhalti("qisam() builtins jo qisam natho bodaey sghe.") from None

    def get_all(self):
        """Return all registered built-in functions."""
        return self.functions
