---
version: '1.0'
type: ref
title: "_Configuracion_de_Herramientas_CLI_con_Python_y_pyproject"
created: 2026-02-09 02:08:33.853228
updated: 2026-02-09 02:08:33.853228
aliases:
- _Configuracion_de_Herramientas_CLI_con_Python_y_pyproject
tags: []
---
Para transformar un proyecto de Python en una herramienta del sistema ejecutable desde cualquier lugar sin activar manualmente entornos virtuales, se utiliza el estándar de empaquetado moderno (PEP 517/660).

1. Estructura del pyproject.toml
El archivo pyproject.toml reemplaza al antiguo setup.py. Define cómo se construye el paquete y qué comandos registra en el sistema.

```TOML 
[build-system] requires = ["setuptools>=61.0"] build-backend = "setuptools.build_meta"

[project] name = "nombre-herramienta" version = "0.1.0" dependencies = [ "pydantic", # Ejemplo de dependencias ]

[project.scripts]

Comando que escribirás en la terminal = "paquete.modulo:función"
mi-comando = "core.main:run"

[tool.setuptools] package-dir = {"" = "src"} # Define src como la raíz del código 
```

2. Funcionamiento Interno: El "Editable Install"
Al ejecutar pip install -e . ocurren tres procesos clave:

Resolución de Metadatos: Pip lee el pyproject.toml para entender las dependencias y el nombre del ejecutable.

Generación de Shims (Wrappers): Se crea un archivo ejecutable en la carpeta bin del entorno virtual. Este archivo contiene un Shebang que apunta directamente al intérprete de Python de ese venv.

Mapeo de Rutas: En lugar de copiar los archivos a site-packages, se crea un enlace (archivo .pth) que apunta a tu carpeta de desarrollo. Esto permite que los cambios en el código sean instantáneos.

3. Ejecución Global (Sin activar el venv)
Para que el comando funcione fuera de la carpeta del proyecto y sin source .venv/activate, el sistema operativo debe saber dónde encontrar el ejecutable del venv.

El flujo del PATH
Cuando escribes mi-comando, el sistema busca en las carpetas listadas en la variable de entorno $PATH. Como el binario vive en .venv/bin/, tenemos dos formas de integrarlo al sistema:

A. El Enlace Simbólico (Recomendado)
Se crea un acceso directo en una carpeta que ya esté en el PATH del sistema (como ~/.local/bin).
```BASH
# Crear el enlace (fuerza la actualización si ya existe)
ln -sf /ruta/absoluta/al/proyecto/.venv/bin/mi-comando ~/.local/bin/mi-comando 
```

B. El Alias de Shell
Define un atajo en la configuración de tu terminal (.bashrc o .zshrc). 
```BASH 
alias mi-comando='/ruta/absoluta/al/proyecto/.venv/bin/mi-comando' 
```

4. Consideraciones Senior de Arquitectura
Independencia del CWD (Current Working Directory): La herramienta debe usar pathlib y __file__ para localizar sus plantillas o logs. Nunca debe asumir que el usuario está ejecutando el comando desde la carpeta del proyecto.

Imports Absolutos: Al usar package-dir = {"" = "src"}, los archivos dentro de src/ no deben usar el prefijo src. en sus imports. Esto asegura que el paquete sea instalable y portable.

Shebang y Aislamiento: Internamente, el ejecutable generado empieza con algo como #!/ruta/al/venv/bin/python. Esto garantiza que, aunque lo llames desde el Home, se use el intérprete con las librerías correctas (Pydantic, Jinja2, etc.), manteniendo el sistema global limpio.

Entry Points: La función apuntada en [project.scripts] (ej. main:main) debe actuar como un orquestador que maneje excepciones de alto nivel y señales del sistema (como KeyboardInterrupt), asegurando una salida limpia de la terminal.