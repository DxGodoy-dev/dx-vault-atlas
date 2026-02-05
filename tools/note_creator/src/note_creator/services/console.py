import sys
import os

from typing import TypeVar
from enum import Enum

_E = TypeVar("_E", bound=Enum)

class ConsoleInterface:
    """Service to handle clean I/O operations for CLI tools."""

    @staticmethod
    def query(prompt: str) -> str:
        """
        Queries the user for input with a clean, flushed prompt.
        Ensures cross-platform compatibility and buffer safety.
        """
        # 1. Usamos una f-string limpia con un separador visual Senior
        formatted_prompt = f" \033[1;34m»\033[0m {prompt}: "
        
        try:
            # 2. Escribimos directamente al descriptor de archivo de la salida estándar
            sys.stdout.write(formatted_prompt)
            sys.stdout.flush()

            # 3. Lectura de bajo nivel para blindaje total
            line = sys.stdin.buffer.readline()
            if not line:
                return ""
                
            return line.decode('utf-8', errors='replace').strip()
            
        except EOFError:
            return ""

    @staticmethod
    def choose_enum(label: str, enum_cls: type[_E], default_index: int = 0) -> _E:
        """Shows a numbered menu for the enum and returns the selected member."""
        members = list(enum_cls)
        for i, m in enumerate(members):
            display = m.value if isinstance(m.value, str) else f"{m.name} ({m.value})"
            print(f"  {i + 1}. {display}")
        
        prompt = f"\n{label} [1-{len(members)}] (default {default_index + 1}): "
        raw = ConsoleInterface.query(prompt).strip() or str(default_index + 1)
        
        try:
            idx = int(raw)
            if 1 <= idx <= len(members):
                return members[idx - 1]
        except ValueError:
            pass
        return members[default_index]