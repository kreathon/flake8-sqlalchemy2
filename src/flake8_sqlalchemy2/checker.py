from __future__ import annotations

import ast
from collections.abc import Generator
from importlib.metadata import version
from typing import Any
MAPPING_NAMES = {
            "association_proxy",
            "column_property",
            "composite",
            "mapped_column",
            "relationship",
            "synonym",
            "mapped_column",
        }

def is_mapped_attribute(func_node: ast.expr) -> bool:
    """
    Placeholder for the logic that identifies SQLAlchemy
    constructs like `mapped_column()` or `Column()`.
    """
    # Simplified check for demonstration
    if isinstance(func_node, ast.Name):
        return func_node.id in MAPPING_NAMES
    elif isinstance(func_node, ast.Attribute):
        return func_node.attr in MAPPING_NAMES
    return False


class Checker:
    """
    Flake8 plugin to help you write SQLAlchemy2.
    """

    name = "flake8-sqlalchemy2"
    version = version("flake8-sqlalchemy2")

    __slots__ = ("tree",)

    def __init__(self, tree: ast.AST) -> None:
        self.tree = tree

    messages = {
        "SQLAlchemyMissingMappedTypeAnnotation": "SA201 Missing `Mapped` or other ORM container class type annotation",
    }

    def run(self) -> Generator[tuple[int, int, str, type[Any]]]:
        for node in ast.walk(self.tree):
            # Check if the statement is an assignment: `targets = value`
            if isinstance(node, ast.Assign):
                value = node.value
                targets = node.targets

                # Check if the value is a function call
                if isinstance(value, ast.Call):
                    # helpers::is_mapped_attribute logic
                    if is_mapped_attribute(value.func):
                        # SQLAlchemy doesn't allow multiple targets (e.g., x = y = mapped_column())
                        if len(targets) != 1:
                            continue
                        target = targets[0]
                        yield (
                            target.lineno,
                            target.col_offset,
                            self.messages["SQLAlchemyMissingMappedTypeAnnotation"],
                            type(self),
                        )
