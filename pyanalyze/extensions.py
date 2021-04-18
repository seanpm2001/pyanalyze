"""

Extensions to the type system supported by pyanalyze.

"""
from dataclasses import dataclass
from typing import Tuple


class _ParameterTypeGuardMeta(type):
    def __getitem__(self, params: Tuple[str, object]) -> "ParameterTypeGuard":
        if not isinstance(params, tuple) or len(params) != 2:
            raise TypeError(
                "ParameterTypeGuard[...] should be instantiated "
                "with two arguments (a variable name and a type)."
            )
        if not isinstance(params[0], str):
            raise TypeError("The first argument to ParameterTypeGuard must be a string")
        return ParameterTypeGuard(params[0], params[1])


@dataclass(frozen=True)
class ParameterTypeGuard(metaclass=_ParameterTypeGuardMeta):
    """A guard on an arbitrary parameter.

    Example usage:

        def is_int(arg: object) -> Annotated[bool, ParameterTypeGuard["arg", int]]:
            return isinstance(arg, int)

    """

    varname: str
    guarded_type: object


class _HasAttrGuardMeta(type):
    def __getitem__(self, params: Tuple[str, str, object]) -> "HasAttrGuard":
        if not isinstance(params, tuple) or len(params) != 3:
            raise TypeError(
                "HasAttrGuard[...] should be instantiated "
                "with three arguments (a variable name, an attribute name, and a type)."
            )
        if not isinstance(params[0], str):
            raise TypeError("The first argument to HasAttrGuard must be a string")
        return HasAttrGuard(params[0], params[1], params[2])


@dataclass(frozen=True)
class HasAttrGuard(metaclass=_HasAttrGuardMeta):
    """A guard on an arbitrary parameter that checks for the presence of an attribute.

    A return type of HasAttrGuard[param, attr, type] means that param has an attribute
    named attr of type type.

    Example usage:

        def has_time(arg: object) -> Annotated[bool, HasAttrGuard["arg", Literal["time"], int]]:
            attr = getattr(arg, "time", None)
            return isinstance(attr, int)

        T = TypeVar("T", bound=str)

        def hasattr(obj: object, name: T) -> Annotated[bool, HasAttrGuard["obj", T, Any]]:
            try:
                getattr(obj, name)
                return True
            except AttributeError:
                return False

    """

    varname: str
    attribute_name: object
    attribute_type: object
