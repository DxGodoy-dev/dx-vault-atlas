import sys
from pathlib import Path

class ProjectPaths:
    """Gestiona la localización de recursos internos y directorios de usuario."""

    # 1. LOCALIZACIÓN INTERNA (Código y Plantillas)
    # Se basa en la ubicación de este archivo, no en archivos externos como .gitignore
    # Estructura: .../note_creator/utils/paths.py -> parent es utils/ -> parent es note_creator/
    PACKAGE_ROOT: Path = Path(__file__).resolve().parent.parent
    
    # Las plantillas siempre viajan dentro del paquete
    TEMPLATES: Path = PACKAGE_ROOT / "templates"

    # 2. LOCALIZACIÓN EXTERNA (Datos del Usuario)
    # Definimos la raíz de trabajo donde el usuario lanza el comando
    # Si prefieres una carpeta fija como ~/.config/note_creator, se cambiaría aquí
    APP_DIR: Path = Path.home() / "dx-vault-atlas"
    LOGS: Path = APP_DIR / "logs"
    NOTES: Path = APP_DIR / "notes"
    LOG_FILE: Path = LOGS / "automation.log"

    @classmethod
    def ensure_dirs(cls) -> None:
        """Asegura la existencia de directorios de escritura para el usuario.
        
        Nota: No intentamos crear TEMPLATES aquí porque es de solo lectura 
        en la instalación del paquete.
        """
        for directory in [cls.LOGS, cls.NOTES]:
            directory.mkdir(parents=True, exist_ok=True)
            
        # Guard clause para asegurar que las plantillas existen donde el paquete dice
        if not cls.TEMPLATES.exists():
            # Aquí podrías usar tu logger centralizado si ya está inicializado
            raise FileNotFoundError(
                f"ERROR CRÍTICO: No se hallaron plantillas en {cls.TEMPLATES}. "
                "Verifique la instalación del paquete."
            )

    @classmethod
    def setup_pythonpath(cls) -> None:
        """Mantiene compatibilidad para ejecuciones locales de desarrollo."""
        # En producción (instalado), esto no suele ser necesario si el entrypoint
        # está bien definido en pyproject.toml, pero ayuda en testing.
        src_path = str(cls.PACKAGE_ROOT.parent)
        if src_path not in sys.path:
            sys.path.insert(0, src_path)