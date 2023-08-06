from abc import ABC, ABCMeta, abstractmethod
from typing import (
    Any,
    ChainMap,
    ClassVar,
    Dict,
    Iterator,
    List,
    Optional,
    Type,
    Union,
    overload,
)

from .enums import GraphQLOperationType
from .fields import GraphQLField, GraphQLFieldBase, GraphQLNestableField
from .typings import FieldBuilderT, NestableFieldBuilderT
from .utils import minify_graphql_call

__all__ = (
    "GraphQLFieldBuilder",
    "GraphQLNestableFieldBuilder",
    "GraphQLOperationBuilder",
)


class _GraphQLFieldBuilderBase(ABC):
    TEMPLATE: ClassVar[str]

    def __init__(self) -> None:
        if not hasattr(self.__class__, "TEMPLATE"):
            raise RuntimeError("The class does not have an TEMPLATE attribute set.")

    def __init_subclass__(cls) -> None:
        if hasattr(cls, "TEMPLATE"):
            cls.TEMPLATE = minify_graphql_call(cls.TEMPLATE)

    @abstractmethod
    def iter_calls(self, parent_substitutions: ChainMap[str, Any]) -> Iterator[str]:
        ...


class _GraphQLNestableBuilder:
    def __init__(self) -> None:
        super().__init__()
        self._fields: Dict[str, GraphQLFieldBase[Any]] = {}


class _GraphQLNestableFieldBuilderMeta(ABCMeta):
    @overload
    def __get__(
        self: Type[NestableFieldBuilderT], instance: None, owner: Any
    ) -> Type[NestableFieldBuilderT]:
        ...

    @overload
    def __get__(
        self: Type[NestableFieldBuilderT],
        instance: _GraphQLNestableBuilder,
        owner: Any,
    ) -> GraphQLNestableField[NestableFieldBuilderT]:
        ...

    def __get__(
        self: Type[NestableFieldBuilderT],
        instance: Optional[_GraphQLNestableBuilder],
        owner: Any,
    ) -> Union[
        GraphQLNestableField[NestableFieldBuilderT], Type[NestableFieldBuilderT]
    ]:
        if instance is None:
            return self
        builder_name = self.__name__
        builder: Optional[GraphQLNestableField[NestableFieldBuilderT]]
        builder = instance._fields.get(builder_name)  # type: ignore[assignment]
        if builder is None:
            builder = instance._fields[builder_name] = GraphQLNestableField(self)
        return builder


class _GraphQLFieldBuilderMeta(ABCMeta):
    @overload
    def __get__(
        self: Type[FieldBuilderT], instance: None, owner: Any
    ) -> Type[FieldBuilderT]:
        ...

    @overload
    def __get__(
        self: Type[FieldBuilderT], instance: _GraphQLNestableBuilder, owner: Any
    ) -> GraphQLField[FieldBuilderT]:
        ...

    def __get__(
        self: Type[FieldBuilderT],
        instance: Optional[_GraphQLNestableBuilder],
        owner: Any,
    ) -> Union[GraphQLField[FieldBuilderT], Type[FieldBuilderT]]:
        if instance is None:
            return self
        builder_name = self.__name__
        builder: Optional[GraphQLField[FieldBuilderT]]
        builder = instance._fields.get(builder_name)  # type: ignore[assignment]
        if builder is None:
            builder = instance._fields[builder_name] = GraphQLField(self)
        return builder


class GraphQLOperationBuilder(_GraphQLNestableBuilder):
    OPERATION_TYPE: ClassVar[GraphQLOperationType]

    def __init__(self) -> None:
        if not hasattr(self.__class__, "OPERATION_TYPE"):
            raise RuntimeError(
                "The class does not have an OPERATION_TYPE attribute set."
            )
        super().__init__()

    def iter_calls(self) -> Iterator[str]:
        parts = [f"{self.OPERATION_TYPE.value} {{"]
        substitutions: ChainMap[str, Any] = ChainMap()
        substitutions.maps = []
        for field in self._fields.values():
            parts.extend(field.iter_calls(substitutions))
        parts.append("}")
        yield "\n".join(parts)


class GraphQLNestableFieldBuilder(
    _GraphQLNestableBuilder,
    _GraphQLFieldBuilderBase,
    metaclass=_GraphQLNestableFieldBuilderMeta,
):
    def __init__(self, substitutions: Dict[str, Any]) -> None:
        super().__init__()
        self.substitutions = substitutions

    def iter_calls(self, parent_substitutions: ChainMap[str, Any]) -> Iterator[str]:
        substitutions = parent_substitutions.new_child(self.substitutions)
        template_substitutions = substitutions.new_child()
        parts: List[str] = []
        for field in self._fields.values():
            parts.extend(field.iter_calls(substitutions))
        template_substitutions["nested_call"] = "\n".join(parts)
        yield self.TEMPLATE % template_substitutions


class GraphQLFieldBuilder(_GraphQLFieldBuilderBase, metaclass=_GraphQLFieldBuilderMeta):
    def __init__(self) -> None:
        super().__init__()
        self.field_substitutions: List[Dict[str, Any]] = []

    def _append(self, substitutions: Dict[str, Any]) -> None:
        self.field_substitutions.append(substitutions)

    def iter_calls(self, parent_substitutions: ChainMap[str, Any]) -> Iterator[str]:
        substitutions = parent_substitutions.new_child()
        for substitutions.maps[0] in self.field_substitutions:
            yield self.TEMPLATE % substitutions
