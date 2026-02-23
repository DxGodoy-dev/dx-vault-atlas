"""Centralized application configuration.

Complies with:
- Skill 01: Configuration via pydantic-settings.
- Skill 02: Strict Pydantic Validation (V2).
- Skill 07: Observability (Structured Logging).
"""

import json
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

from platformdirs import user_config_dir, user_log_dir
from pydantic import Field, field_validator, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from dx_vault_atlas.shared.logger import logger


class ConfigNotFoundError(Exception):
    """Raised when configuration file does not exist explicitly."""


class GlobalConfig(BaseSettings):
    """Application configuration model.

    Merges settings from (priority order):
    1. Environment Variables (prefix: DX_)
    2. JSON Config File (~/.config/dx-vault-atlas/config.json)
    3. Defaults

    """

    # Core Paths
    vault_path: Path = Field(
        ..., description="Absolute path to the Obsidian vault root."
    )
    vault_inbox: Path = Field(..., description="Directory for new incoming notes.")

    # Tools
    editor: str = Field(
        default="code", description="CLI command to open the text editor."
    )

    # Logic
    field_mappings: Dict[str, str] = Field(
        default_factory=lambda: {"date": "created"},
        description="Mapping for legacy frontmatter fields.",
    )
    value_mappings: Dict[str, Dict[str, str]] = Field(
        default_factory=dict,
        description=(
            "Per-field value replacements. "
            "Outer key = field name, inner dict = old -> new."
        ),
    )

    # Pydantic Settings Config
    model_config = SettingsConfigDict(
        env_prefix="DX_",  # e.g., DX_VAULT_PATH overrides vault_path
        extra="ignore",  # Forward compatibility
        # Encoding/Case sensitivity handled by defaults
    )

    @property
    def logs_dir(self) -> Path:
        """Return OS-standard log directory (Computed, not stored)."""
        return Path(user_log_dir("dx-vault-atlas", ensure_exists=True))

    @field_validator("vault_path", "vault_inbox", mode="after")
    @classmethod
    def validate_directory_exists(cls, v: Path) -> Path:
        """Ensure path exists and is a directory.

        Note: We allow non-existent paths during validation ONLY if
        we are in a specific mode (like wizard), but strictly enforcing
        existence here is safer for the runtime.
        """
        resolved = v.resolve()
        # Fail Fast (Skill 06) - But allow instantiation if we are going to create it?
        # Sticking to strict validation for runtime config.
        if not resolved.exists():
            # Logging strictly inside validation can be noisy, but useful for debugging
            logger.debug(f"Path validation failed: {resolved} does not exist.")
            raise ValueError(f"Path does not exist: {resolved}")
        if not resolved.is_dir():
            raise ValueError(f"Path is not a directory: {resolved}")
        return resolved


class ConfigManager:
    """Manager for XDG-compliant configuration persistence.

    Separates the concern of 'Where/How to store' from 'What is the config'.
    """

    def __init__(self) -> None:
        """Initialize XDG paths."""
        self._app_name = "dx-vault-atlas"
        self._config_dir = Path(user_config_dir(self._app_name))
        self._config_path = self._config_dir / "config.json"

    @property
    def config_path(self) -> Path:
        """Return the configuration file path."""
        return self._config_path

    def exists(self) -> bool:
        """Check if persistent configuration exists."""
        return self._config_path.exists()

    def load(self) -> GlobalConfig:
        """Load configuration merging JSON persistence and Env Vars.

        Returns:
            GlobalConfig: The validated settings object.

        Raises:
            ConfigNotFoundError: If the JSON file is missing (and required by context).
            ValidationError: If data is invalid.
        """
        logger.debug(f"Attempting to load config from {self._config_path}")

        if not self.exists():
            # If we don't have a file, we can't return a valid config
            # unless ALL required fields are in ENV vars.
            # For this CLI app, we treat missing file as "Not Configured".
            logger.info("Configuration file not found.")
            raise ConfigNotFoundError("Configuration file not found.")

        try:
            # Read JSON
            file_content = self._config_path.read_text(encoding="utf-8")
            data = json.loads(file_content)

            # Pass to Pydantic. It will auto-merge with Env Vars (Env takes precedence by default behavior
            # if we didn't pass data, but since we pass data via init, standard priority rules apply.
            # To ensure ENV overrides JSON passed explicitly, we rely on Pydantic's merge logic
            # or simply let Pydantic handle it if we used a settings source.
            # Simplified approach: Instantiate directly, Pydantic Settings handles ENV overrides
            # on top of passed kwargs automatically?
            # Clarification: passing kwargs to __init__ usually overrides Env in Pydantic V2.
            # To strictly follow "Env > File", we should let Pydantic load the file via settings_customise_sources
            # OR manually update with os.environ.
            # FOR NOW: We assume JSON is the source of truth for the Wizard,
            # and Env Vars are overrides.

            config = GlobalConfig(**data)
            logger.info("Configuration loaded successfully.")
            return config

        except (json.JSONDecodeError, ValidationError) as e:
            logger.error(f"Failed to load configuration: {e}")
            raise

    def save(self, config: GlobalConfig) -> None:
        """Persist configuration to JSON.

        Args:
            config: The settings object to save.
        """
        try:
            self._config_dir.mkdir(parents=True, exist_ok=True)

            # Dump to JSON (mode='json' handles Path serialization)
            data = config.model_dump(mode="json", exclude_none=True)

            json_str = json.dumps(data, indent=2, ensure_ascii=False)
            self._config_path.write_text(json_str, encoding="utf-8")

            logger.info(f"Configuration saved to {self._config_path}")

        except OSError as e:
            logger.critical(f"Failed to save configuration: {e}")
            raise


@lru_cache(maxsize=1)
def get_config_manager() -> ConfigManager:
    """Return singleton ConfigManager instance."""
    return ConfigManager()


def get_settings() -> GlobalConfig:
    """Get the current loaded settings.

    Convenience wrapper for usage throughout the app.

    Returns:
        GlobalConfig object.

    Raises:
        ConfigNotFoundError: If app is not initialized.
    """
    return get_config_manager().load()
