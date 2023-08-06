import dataclasses
import inspect
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Protocol,
    Tuple,
    Type,
    TypeVar,
    Union,
    runtime_checkable,
)

_T = TypeVar("_T")
_Type = TypeVar("_Type", bound=type)


class _MissingType(Protocol):

    @classmethod
    def __subclasshook__(cls, subclass, /):
        return subclass is type(dataclasses.MISSING)


@runtime_checkable
class _DClsOrObj(Protocol):
    __dataclass_fields__: Dict[str, dataclasses.Field]


@runtime_checkable
class GenericAliasProto(Protocol):
    __origin__: type
    __args__: Tuple[Any, ...]
    __parameters__: Tuple[Any, ...]

    def __init__(self, __origin: type, __args: Any, /) -> None:
        ...

    def __getattr__(self, __name: str, /) -> Any:
        ...


@runtime_checkable
class AnnotatedAlias(Protocol):
    __args__: Tuple[Any]
    __metadata__: Tuple


class Empty:
    ...


TEmpty = Union[Type[inspect.Parameter.empty], Empty, _MissingType]

empty: Empty = ...


@runtime_checkable
class NamedTupleProto(Protocol):
    __annotations__: Dict[str, Any]
    _fields: ClassVar[Tuple[str, ...]]
    _field_defaults: ClassVar[Dict[str, Any]]
    _field_types: ClassVar[Dict[str, Any]]

    def __new__(cls: Type[_T], /, **kwargs) -> _T:
        ...


@runtime_checkable
class DataClassProto(Protocol):
    __annotations__: Dict[str, Any]
    __dataclass_fields__: ClassVar[Dict[str, dataclasses.Field]]

    def __new__(cls: Type[_T], /, **kwargs) -> _T:
        ...


@runtime_checkable
class ValidDataClassProto(DataClassProto, Protocol):

    @classmethod
    def __subclasshook__(cls, subclass, /):
        if not isinstance(subclass, _DClsOrObj):
            return False
        for f in subclass.__dataclass_fields__.values():
            if f.type is dataclasses.InitVar and f.default is dataclasses.MISSING:
                return False
        return True


@runtime_checkable
class TypedDictProto(Protocol):
    __annotations__: Dict[str, Any]
    __total__: ClassVar[bool]

    def __new__(cls: Type[_T], /, **kwargs) -> _T:
        ...


@runtime_checkable
class NamedClassProto(Protocol):
    __annotations__: Dict[str, Any]

    def __new__(cls: Type[_T], /, **kwargs) -> _T:
        ...


register_named_class: Callable[[_Type], _Type]


class ForwardRefProto(Protocol):
    __forward_arg__: str


def as_forward_ref(instance, /) -> ForwardRefProto:
    ...
