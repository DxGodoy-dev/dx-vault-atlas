---
tags: []
source: ia
created: 24-01-2026
updated: 2026-02-09 02:05:06.660234
version: '1.0'
type: note
---
# *Configuración Inicial y Seguridad SSH*

### Identidad Global
Antes de cualquier desarrollo, se debe establecer la firma digital del desarrollador. Esto garantiza la trazabilidad en equipos profesionales.

* **Comandos de Identidad**:

	```bash
    git config --global user.name "Daniel Godoy"
    git config --global user.email "tu_email@ejemplo.com"
    ```

* **Validación de Configuración**: Para verificar los valores activos en el entorno actual.

	```bash
    git config --list
	```

### Autenticación Segura mediante SSH
En entornos de ingeniería, el uso de **SSH (Secure Shell)** es obligatorio frente a HTTPS para evitar el ingreso manual de credenciales y asegurar el túnel de comunicación.

#### Generación de Llaves (Algoritmo Ed25519)
Se recomienda **Ed25519** por ser más rápido y seguro que RSA.

```bash
ssh-keygen -t ed25519 -C "tu_email@ejemplo.com"
# Presionar Enter para la ruta por defecto y añadir una passphrase si se desea.
```



#### Vinculación con el Proveedor (GitHub/GitLab)
1. Iniciar el agente: `eval "$(ssh-agent -s)"`
2. Añadir la llave: `ssh-add ~/.ssh/id_ed25519`
3. Copiar la llave pública para pegarla en el perfil del proveedor:

```bash
    cat ~/.ssh/id_ed25519.pub
```

### Guard Clauses de Conexión
Antes de realizar el primer `push`, validar que la conexión SSH es exitosa:

```bash
ssh -T git@github.com
```