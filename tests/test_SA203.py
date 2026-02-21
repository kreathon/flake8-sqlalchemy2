from __future__ import annotations

import ast

from src.flake8_sqlalchemy2 import Checker


def test_import_simple():
    code = """\
from typing import List

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
    children: Mapped[List["Child"]] = relationship(backref="parent")


class Child(Base):
    __tablename__ = "child"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent.id"))
"""

    tree = ast.parse(code)
    plugin = Checker(tree)
    assert [f"{line}:{col + 1} {msg}" for line, col, msg, _ in plugin.run()] == [
        "21:52 SA203 Use of legacy relationship `backref` consider using `back_populates` instead"
    ]


def test_import_orm():
    code = """\
from typing import List

import sqlalchemy as sa
from sqlalchemy import orm

class Base(orm.DeclarativeBase):
    pass


class Parent(Base):
    __tablename__ = "parent"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    children: orm.Mapped[List["Child"]] = orm.relationship(backref="parent")


class Child(Base):
    __tablename__ = "child"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    parent_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("parent.id"))
"""

    tree = ast.parse(code)
    plugin = Checker(tree)
    assert [f"{line}:{col + 1} {msg}" for line, col, msg, _ in plugin.run()] == [
        "14:60 SA203 Use of legacy relationship `backref` consider using `back_populates` instead"
    ]
