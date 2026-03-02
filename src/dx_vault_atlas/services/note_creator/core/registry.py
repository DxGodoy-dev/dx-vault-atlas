"""Dynamic registry for note templates and models."""

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

if TYPE_CHECKING:
    from dx_vault_atlas.services.note_creator.models.enums import NoteTemplate


# Map template enums to their corresponding Pydantic note models
_MODEL_REGISTRY: dict["NoteTemplate", type[BaseModel]] = {}


def register_model(template: "NoteTemplate") -> callable:
    """Decorator to register a Pydantic model to a specific NoteTemplate.

    Args:
        template: The NoteTemplate enum to register this model under.

    Returns:
        The decorator function.
    """

    def decorator(cls: type[BaseModel]) -> type[BaseModel]:
        _MODEL_REGISTRY[template] = cls
        return cls

    return decorator


def get_model(
    template: "NoteTemplate", default: type[BaseModel] | None = None
) -> type[BaseModel]:
    """Retrieve the registered Pydantic model for a given template.

    Args:
        template: The NoteTemplate enum to lookup.
        default: Fallback model if not found.

    Returns:
        The matched Pydantic model type, or the default.
    """
    if default is not None:
        return _MODEL_REGISTRY.get(template, default)
    return _MODEL_REGISTRY[template]


def has_field(template: Any, field_name: str) -> bool:  # noqa: ANN401
    """Check if the model registered for a template requires a specific field.

    Args:
        template: The NoteTemplate enum. If not valid, returns False.
        field_name: The name of the field to check for in the Pydantic model.

    Returns:
        True if the field is defined on the model, False otherwise.
    """
    # Import locally to avoid circular dependencies if enums imports registry
    from dx_vault_atlas.services.note_creator.models.enums import NoteTemplate

    if not _MODEL_REGISTRY:
        from dx_vault_atlas.services.note_creator.models import note  # noqa: F401

    if isinstance(template, str) and not isinstance(template, NoteTemplate):
        try:
            template = NoteTemplate(template)
        except ValueError:
            return False

    if not isinstance(template, NoteTemplate) or template not in _MODEL_REGISTRY:
        return False

    model_cls = _MODEL_REGISTRY[template]

    # Check if the field is either directly in model_fields,
    # or if the model_cls inherently defines it through its schema.
    # We can also check if it's in the model's annotations.
    return field_name in model_cls.model_fields
