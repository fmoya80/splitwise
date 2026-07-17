# Conexión local con Splitwise

Este proyecto crea una base mínima para conectar una cuenta personal de
Splitwise desde Python. Valida el usuario autenticado, lista sus grupos y
descarga una página pequeña de gastos como prueba. Los datos se guardan en
formato JSON para poder construir después DataFrames centrados en grupos.

## Instalación

En Windows, cree y active un entorno virtual:

```bat
python -m venv venv
venv\Scripts\activate
```

Instale las dependencias:

```bat
pip install -r requirements.txt
```

## Configuración de la API Key

Cree su archivo local de configuración a partir del ejemplo:

```bat
copy .env.example .env
```

Abra `.env` y reemplace el valor de ejemplo por su API Key personal:

```env
SPLITWISE_API_KEY=mi_api_key
```

La aplicación envía esta clave exclusivamente mediante el header
`Authorization: Bearer <SPLITWISE_API_KEY>`. El archivo `.env` está ignorado
por Git: **nunca suba su API Key a GitHub**.

Para esta primera conexión local no se necesitan Consumer Key, Consumer Secret
ni OAuth.

## Ejecución

Ejecute una consulta de prueba de hasta diez gastos:

```bat
python main.py --limit 10
```

También puede filtrar los gastos:

```bat
python main.py --dated-after "2025-01-01T00:00:00Z" --limit 10
```

Para elegir un grupo desde un menú (por ejemplo, `Casita`), ejecute:

```bat
python main.py --select-group --limit 50
```

El programa listará los grupos y solicitará el número correspondiente. También
puede indicar el ID directamente, sin menú:

```bat
python main.py --group-id 123456789 --limit 50
```

Los filtros opcionales disponibles son `--dated-after`, `--dated-before`,
`--group-id`, `--select-group` y `--limit`. Esta versión obtiene una única página de resultados;
la paginación completa se añadirá más adelante.

## Archivos generados

Después de una ejecución correcta se crean estos archivos locales en `data/raw`:

- `current_user.json`: perfil del usuario autenticado.
- `groups.json`: grupos asociados a la cuenta.
- `sample_expenses.json`: muestra de gastos solicitada.

Estos datos crudos también están ignorados por Git para proteger la información
personal de la cuenta.

## Análisis en un notebook

Abra `notebooks/explore_group_expenses.ipynb` con Jupyter o VS Code después de
ejecutar la extracción del grupo. El notebook carga `sample_expenses.json` y
crea un DataFrame de Pandas llamado `expenses_df` para empezar el análisis.
Los archivos raw contienen información personal y permanecen fuera de Git.
