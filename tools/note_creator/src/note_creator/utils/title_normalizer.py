import sys
from datetime import datetime
import re
import unicodedata

class TitleNormalizer:
    """
    Handles the transformation of raw strings into standardized 
    Obsidian filenames with high-precision timestamps.
    """

    @classmethod
    def normalize(cls, raw_title: str) -> str:
        """
        Entry point: Orchestrates the timestamp generation and title sanitation.
        
        Args:
            raw_title: The user-provided title string.
            
        Returns:
            A string in the format: YYYYMMDDHHMMSS_sanitized_title
        """
        if not raw_title or not raw_title.strip():
            raise ValueError("El título no puede estar vacío.")

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        clean_name = cls._sanitize(raw_title)
        
        return f"{timestamp}_{clean_name}"

    @staticmethod
    def _sanitize(text: str) -> str:
        """
        Internal logic to clean the string. 
        Private to maintain the 'normalize' method as the sole interface.
        """
        # 1. Descomposición Unicode y eliminación de acentos
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
        
        # 2. Normalización a minúsculas y eliminación de caracteres no alfanuméricos
        text = text.lower()
        text = re.sub(r'[^a-z0-9]+', '_', text)
        
        # 3. Limpieza de bordes
        return text.strip('_')