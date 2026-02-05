import logging
import sys
from note_creator.utils.paths import ProjectPaths

class LoggerManager:
    """Configures and provides a logger with file and console handlers."""

    @staticmethod
    def create_logger(name: str = "automation_suite") -> logging.Logger:
        """Creates a logger with file (debug) and console (info) handlers.

        Args:
            name: Logger name. Defaults to "automation_suite".

        Returns:
            Configured logger instance. Idempotent: repeated calls return the same
            logger; handlers are added only once.
        """
        ProjectPaths.ensure_dirs()
        
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Formato para el archivo (Detallado)
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | [%(name)s] | %(message)s'
        )
        
        # Formato para consola (Limpio para Daniel)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')

        # Handler de Archivo
        file_handler = logging.FileHandler(ProjectPaths.LOG_FILE, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)

        # Handler de Consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)

        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger

# --- Ejecución y Exportación ---
# Esta es la variable que importarás en otros módulos
logger = LoggerManager.create_logger()