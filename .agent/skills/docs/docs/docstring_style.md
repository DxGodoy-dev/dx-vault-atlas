# STANDARD: Documentation (Google Style)

## 1. Regla de Oro
**MANDATORIO:** Toda función pública, clase y módulo debe tener docstring.
**FORMATO:** Google Style Guide. Es el más legible y standard en Data/ML/Backend moderno.

## 2. Estructura Requerida
```python
def connect_database(url: str, timeout: int = 30) -> DatabaseConnection:
    """Establishes a connection to the primary database.

    Retries the connection up to 3 times if a transient error occurs.

    Args:
        url (str): The JDBC or ODBC connection string.
        timeout (int): Max time in seconds to wait for handshake. Defaults to 30.

    Returns:
        DatabaseConnection: An active pool object ready for queries.

    Raises:
        ConnectionTimeoutError: If the server is unreachable after retries.
        AuthenticationError: If credentials in url are invalid.
    """
```

## 3. Tip
No documentes lo obvio (ej: `def get_name(): """Gets the name."""`). Documenta el **contexto**, los **side-effects** y sobre todo las **excepciones**.
