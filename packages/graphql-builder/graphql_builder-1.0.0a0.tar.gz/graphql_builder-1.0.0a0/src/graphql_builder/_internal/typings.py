from typing import Any, ChainMap, Dict, Iterator, Protocol, TypeVar

__all__ = ("FieldBuilderT", "NestableFieldBuilderT")


class GraphQLFieldBuilderProtocol(Protocol):
    def __init__(self) -> None:
        ...

    def _append(self, substitutions: Dict[str, Any]) -> None:
        ...

    def iter_calls(self, parent_substitutions: ChainMap[str, Any]) -> Iterator[str]:
        ...


class GraphQLNestableFieldBuilderProtocol(Protocol):
    def __init__(self, substitutions: Dict[str, Any]) -> None:
        ...

    def iter_calls(self, parent_substitutions: ChainMap[str, Any]) -> Iterator[str]:
        ...


FieldBuilderT = TypeVar("FieldBuilderT", bound=GraphQLFieldBuilderProtocol)
NestableFieldBuilderT = TypeVar(
    "NestableFieldBuilderT", bound=GraphQLNestableFieldBuilderProtocol
)
