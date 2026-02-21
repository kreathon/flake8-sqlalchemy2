from __future__ import annotations

import ast

from src.flake8_sqlalchemy2 import Checker


def test_import_simple():
    code = """\
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    DeclarativeBase,
    relationship,
    column_property,
)


class Base(DeclarativeBase):
    pass


class Parent(Base):
    __tablename__ = "parent"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: DynamicMapped["Child"] = relationship(back_populates="parent")


class Child(Base):
    __tablename__ = "child"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent.id"))
    parent: Mapped["Parent"] = relationship(back_populates="children")
"""

    tree = ast.parse(code)
    plugin = Checker(tree)
    assert [f"{line}:{col + 1} {msg}" for line, col, msg, _ in plugin.run()] == [
        "19:15 SA202 Use of legacy collection `DynamicMapped` consider using `WriteOnlyMapped`"
    ]


def test_import_orm():
    code = """\
import sqlalchemy as sa
from sqlalchemy import orm


class Base(orm.DeclarativeBase):
    pass


class Parent(Base):
    __tablename__ = "parent"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    children: orm.DynamicMapped["Child"] = orm.relationship(back_populates="parent")


class Child(Base):
    __tablename__ = "child"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    parent_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("parent.id"))
    parent: orm.Mapped["Parent"] = orm.relationship(back_populates="children")
"""

    tree = ast.parse(code)
    plugin = Checker(tree)
    assert [f"{line}:{col + 1} {msg}" for line, col, msg, _ in plugin.run()] == [
        "13:15 SA202 Use of legacy collection `DynamicMapped` consider using `WriteOnlyMapped`"
    ]
