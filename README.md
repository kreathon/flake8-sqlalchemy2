# flake8-sqlalchemy2

`flake8` plugin to enforce modern, typed SQLAlchemy 2.0.


## Installation

Use `uvx` for a one-time check of your code base:
```bash
uvx --with flake8-sqlalchemy2 flake8 --select SA2
```

Install via `pip` for using as "permanent" `flake8` plugin:
```bash
pip install flake8-sqlalchemy2
```

## Rules

### missing-mapped-type-annotation (SA201)

#### What it does
Checks for existence of `Mapped` or other ORM container class type annotations in SQLAlchemy
models.

#### Why is this bad?
If an annotation is missing, type checkers will treat the corresponding field as type `Any`.

#### Example
```python
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass


class MyModel(Base):
    __tablename__ = "my_model"
    id: Mapped[int] = mapped_column(primary_key=True)

    count = mapped_column(Integer)


m = MyModel()
reveal_type(m.count)  #  note: Revealed type is "Any"
```

Use instead:
```python
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass


class MyModel(Base):
    __tablename__ = "my_model"
    id: Mapped[int] = mapped_column(primary_key=True)

    count: Mapped[int]


m = MyModel()
reveal_type(m.count)  # note: Revealed type is "builtins.int"
```

### legacy-collection (SA202)

#### What it does
Checks for existence of `DynamicMapped`.

#### Why is this bad?
`DynamicMapped` is considered legacy and exposes the legacy query API.

#### Example
```python
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import DynamicMapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass


class MyModel(Base):
    __tablename__ = "my_model"
    id: Mapped[int] = mapped_column(primary_key=True)

    children: DynamicMapped["Child"] = relationship()
```

Use instead:
```python
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import WriteOnlyMapped

class Base(DeclarativeBase):
  pass


class MyModel(Base):
    __tablename__ = "my_model"
    id: Mapped[int] = mapped_column(primary_key=True)

    children: WriteOnlyMapped["Child"] = relationship()
```

### legacy-relationship (SA203)

#### What it does
Checks for existence of `relationship` definition with `backref` keyword argument.

#### Why is this bad?
`backref` is considered legacy. It adds dynamic attributes that type checkers and code completion cannot understand.

#### Example
```python
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
c.parent  # error: "Child" has no attribute "parent"; maybe "parent_id"?  [attr-defined]
```

Use instead:
```python
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

    children: Mapped[List["Child"]] = relationship(back_populates="parent")


class Child(Base):
    __tablename__ = "child"
    id: Mapped[int] = mapped_column(primary_key=True)

    parent_id: Mapped[int] = mapped_column(ForeignKey("parent.id"))
    parent: Mapped["Parent"] = relationship(back_populates="children")
```

## Note on `ruff`

Q: Why still use `flake8` when there is `ruff`!?

A: For rules not supported by `ruff`. There is a proposed [merge request](https://github.com/astral-sh/ruff/pull/18065) to bring the first SQLAlchemy linting rule (`SA201`) to `ruff` ("needs-decision" tagged).

## Note on `flake8-sqlalchemy`

Q: Why not integrate these rules into `flake8-sqlalchemy`?

A: The focus of this package are rules for modern, typed SQLAlchemy. Furthermore, I wanted to learn something new.
