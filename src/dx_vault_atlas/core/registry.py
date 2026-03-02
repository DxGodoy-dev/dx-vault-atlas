"""Note model registry to implement Open/Closed Principle."""

from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class NoteModelRegistry:
    """Registry to map note type strings to their Pydantic models."""

    _registry: dict[str, type[BaseModel]] = {}

    @classmethod
    def register(cls, name: str) -> callable:
        """Register a note model inheriting from BaseNote."""

        def decorator(model_cls: type[T]) -> type[T]:
            cls._registry[name] = model_cls
            return model_cls

        return decorator

    @classmethod
    def get_model(cls, name: str) -> type[BaseModel] | None:
        """Get the Pydantic model class for a given note type name."""
        return cls._registry.get(name)

    @classmethod
    def get_all(cls) -> dict[str, type[BaseModel]]:
        """Return a copy of the registry dictionary."""
        return cls._registry.copy()


register_note_type = NoteModelRegistry.register
