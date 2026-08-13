"""Shared building blocks for the application.

Import utilities from their defining modules (for example,
``from common.pagination import PaginationParams``).  Keeping this initializer
lightweight prevents a repository import from eagerly loading optional FastAPI
or Pydantic dependencies.
"""
