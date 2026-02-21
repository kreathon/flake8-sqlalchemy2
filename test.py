from typing import List

from sqlalchemy import ForeignKey

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship


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


c = Child()
p = Parent(children=[c])
c.parent
