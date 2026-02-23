"""Main entry point for note migrator service."""

import sys

from dx_vault_atlas.services.note_migrator.app import create_app
from dx_vault_atlas.shared.config import get_settings
from dx_vault_atlas.shared.logger import logger


def main() -> None:
    """Entry point for dxva migrate command."""
    try:
        settings = get_settings()
        app = create_app(settings)
        app.run()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        logger.exception("Fatal error")
        sys.exit(1)


if __name__ == "__main__":
    main()
