"""Reusable synchronous SQLAlchemy repository primitives.

Repositories only manage persistence.  Transaction boundaries remain in the
calling service, allowing several repository operations to be committed as a
single unit of work.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy import Select, select
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session

ModelT = TypeVar("ModelT")


class CRUDRepository(Generic[ModelT]):
    """Small, type-aware CRUD base for SQLAlchemy declarative models."""

    def __init__(self, model: type[ModelT]) -> None:
        self.model = model
        self.primary_key = inspect(model).primary_key[0].key

    def get(self, db: Session, identifier: Any) -> ModelT | None:
        return db.get(self.model, identifier)

    def list(
        self,
        db: Session,
        *,
        offset: int = 0,
        limit: int = 100,
        filters: Mapping[str, Any] | None = None,
        statement: Select[tuple[ModelT]] | None = None,
    ) -> Sequence[ModelT]:
        query = statement or select(self.model)
        if filters:
            query = query.filter_by(**dict(filters))
        return db.scalars(query.offset(offset).limit(limit)).all()

    def create(self, db: Session, **values: Any) -> ModelT:
        instance = self.model(**values)
        db.add(instance)
        db.flush()
        return instance

    def update(self, db: Session, instance: ModelT, **values: Any) -> ModelT:
        mapper = inspect(self.model)
        valid_columns = {column.key for column in mapper.columns}
        unknown = set(values) - valid_columns
        if unknown:
            raise ValueError(f"Unknown {self.model.__name__} fields: {sorted(unknown)}")
        for name, value in values.items():
            setattr(instance, name, value)
        db.flush()
        return instance

    def delete(self, db: Session, instance: ModelT) -> None:
        db.delete(instance)
        db.flush()
