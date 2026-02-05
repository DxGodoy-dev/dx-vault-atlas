import sys
import os

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