"""Shared utilities for Pydantic models."""

from typing import Any

from pydantic import BaseModel


def strip_unknown_fields(
    model_cls: type[BaseModel], data: dict[str, Any]
) -> dict[str, Any]:
    """Return a new dictionary containing only fields known to the model.

    This ensures that when `extra="forbid"` is set on a model, passing this
    dictionary will not trigger ValidationError for unknown fields.
    """
    known = set(model_cls.model_fields.keys())
    for _, info in model_cls.model_fields.items():
        if info.alias:
            known.add(info.alias)

    return {k: v for k, v in data.items() if k in known}
