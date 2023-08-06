"""Easy solution for dynamic generation of GraphQL operations."""

from ._internal.builders import (
    GraphQLFieldBuilder,
    GraphQLFieldBuilder as FieldBuilder,
    GraphQLNestableFieldBuilder,
    GraphQLNestableFieldBuilder as NestableFieldBuilder,
    GraphQLOperationBuilder,
    GraphQLOperationBuilder as OperationBuilder,
)
from ._internal.enums import GraphQLOperationType, GraphQLOperationType as OperationType
from ._internal.fields import (
    GraphQLField,
    GraphQLField as Field,
    GraphQLFieldBase,
    GraphQLFieldBase as FieldBase,
    GraphQLNestableField,
    GraphQLNestableField as NestableField,
)

__version__ = "1.0.0a0"

__all__ = (
    # builders
    "GraphQLFieldBuilder",
    "FieldBuilder",
    "GraphQLNestableFieldBuilder",
    "NestableFieldBuilder",
    "GraphQLOperationBuilder",
    "OperationBuilder",
    # enums
    "GraphQLOperationType",
    "OperationType",
    # fields
    "GraphQLField",
    "Field",
    "GraphQLFieldBase",
    "FieldBase",
    "GraphQLNestableField",
    "NestableField",
)
