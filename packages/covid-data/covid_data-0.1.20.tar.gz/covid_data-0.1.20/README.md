# Data Loader

[![forthebadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

![Tests](https://github.com/alesanmed-educational-projects/covid-data/actions/workflows/python-app.yml/badge.svg)
![Build](https://github.com/alesanmed-educational-projects/covid-data/actions/workflows/pypi-publish.yml/badge.svg)
[![PyPI version](https://d25lcipzij17d.cloudfront.net/badge.svg?id=py&type=6e&v=0.1.18)](https://badge.fury.io/py/covid-data)


Este proyecto contiene las herramientas necesarias para:
- Crear la base de datos
- Cargar datos en esa base de datos
- Consultar esos datos

# Table of contents

- [Instalación 📥](#instalacion)
  - [Biblioteca 📖](#biblioteca)
  - [CLI 🤖](#cli)
- [Configuración ⚙](#configuracion)
- [Uso como CLI 🎛️](#uso-como-cli)
  - [loadcsv](#loadcsv)
  - [scrap](#scrap)
  - [Cargar la base de datos desde un backup](#cargar-la-base-de-datos-desde-un-backup)
- [Contribuir ♥](#contribuir)
  - [Añadir nuevos scrappers](#añadir-nuevos-scrappers)
  - [Añadir nuevos comandos](#añadir-nuevos-comandos)
- [Como biblioteca](#como-biblioteca)
- [License](#license)

## Instalación 📥 <a name="instalacion"></a>

### Biblioteca 📖  <a name="biblioteca"></a>

Para usarlo como biblioteca basta con instalarlo con `pip`

```
pip install covid-data
```

### CLI 🤖 <a name="cli"></a>

Para usarlo como CLI, sigue siendo necesario instalarlo con `pip` y, una vez instalado, será suficiente con ejecutarlo desde una consola.

```
covid_data --help
```

## Configuración ⚙ <a name="configuracion"></a>

Este proyecto se vale de las siguientes variables de entorno para su configuración:

```
POSTGRES_USER: Usuario de Postgres
POSTGRES_PASS: Contraseña de Postgres
POSTGRES_HOST: Host donde se encuentra Postgres
POSTGRES_PORT: Puerto para acceder a Postgres
POSTGRES_DB:   Base de datos a la que conectarse
CAGEDATA_API_KEY: Clave api de OpenCageData
```

La clave API de OpenCageData se puede crear desde su [web](https://opencagedata.com/) y se usa para enriquecer y normalizar localizaciones.

## Uso como CLI 🎛️ <a name="uso-como-cli"></a>

Para cargar los datos se pueden usar los comandos expuestos por la librería.

Lo primero será crear la base de datos con el esquema disponible [aquí](covid_data/db/schema/db_schema.sql). La estructura de la base de datos es la siguiente:

![Database ERD](https://github.com/alesanmed-educational-projects/covid-data/raw/main/assets/img/erd-covid.png)

Una vez está creada la base de datos, se pueden cargar los datos de los archivos CSV con el siguiente comando:

```bash
covid_data loadcsv /path/to/confirmed.csv,/path/to/dead.csv,/path/to/recovered.csv -tf -o
```

Para obtener ayuda sobre cómo usar el comando, ejecuta:

```bash
❯ covid_data --help
Usage: app.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  loadcsv  Loads FILES as CSV data.
  scrap    Scrap cases of chosen COUNTRY.
```

### loadcsv <a name="loadcsv"></a>

```bash
❯ covid_data loadcsv --help
Usage: app.py loadcsv [OPTIONS] FILES

  Loads FILES as CSV data. If you want to load several files, each file should
  be separated by comma

Options:
  -t, --type TEXT      Type of cases contained in each file, separated by
                       comma. Leave blank if using --type-in-file
  -tf, --type-in-file  Set this to true if the file names are <case_type>.csv
                       Being <case_type> one of confirmed, recovered or dead
  -o, --optimize       Set to true to skip lines for places that has more
                       cases than columns on the CSV
  --help               Show this message and exit.
```

Este comando te permite procesar y cargar en la base de datos uno o más archivos CSV. Cada archivo debe contener información de un solo tipo de casos.

Las rutas a los archivos deben ir separados por comas.

De igual manera, el tipo de caso de cada archivo debe ir separados por comas en el argumento `--type` y **en el mismo orden** que los archivos.

Otra opción es no usar el argumento `--type` y nombrar los archivos con el tipo de caso que contienten, e.g. `recovered.csv`. Si se toma esta alternativa, se debe usar el parámetro `--type-in-file`.

Por último, el argumento `--optimize` se saltará todas las filas en las que el país al que hacen referencia ya tenga el mismo (o más) número de casos del tipo del archivo, que columnas tiene el CSV.

Un ejemplo de uso de este comando para cargar los CSVs con todos los datos es:

```bash
covid_data loadcsv /path/to/confirmed.csv,/path/to/dead.csv,/path/to/recovered.csv -tf -o
```

Usa el nombre del archivo para nombrar el tipo de caso y la optimización.

### scrap <a name="scrap"></a>

Este comando permite hacer scrapping de un país concreto. Se usa para ampliar datos por país.

El uso de este comando se detalla aquí:

```bash
Usage: app.py scrap [OPTIONS] COUNTRY

  Scrap cases of chosen COUNTRY. To check available countries to scrap use
  --check

Options:
  --check            Use this to check available countries
  --start-date TEXT  Date to start scraping cases from, in format DD/MM/YYYY
  --help             Show this message and exit.
``` 

Hay un argumento que es obligatorio y es el país a scrappear. Si se quiere saber qué países hay disponibles, basta con poner cualquier valor en `COUNTRY` y pasar el parámetro `--check`:

```bash
❯ covid_data scrap XXX --check
Available countries are:
        France
        Spain
```

Y, una vez se sabe qué país se va a usar, se lanza el scrapper:

```bash
❯ covid_data scrap spain
Fetching cases for province 1/20
Fetching cases for province 2/20
Fetching cases for province 3/20
...
```

Se puede especificar la fecha de inicio usando el argumento `--start-date`. La fecha debe estar en formato `DD/MM/YYYY`

```bash
covid_data scrap France --start-date 01/08/2021
```

### Cargar la base de datos desde un backup <a name="cargar-la-base-de-datos-desde-un-backup"></a>

En cada [release](https://github.com/alesanmed-educational-projects/covid-data/releases) se adjunta un archivo `covid-data.sql` con el que se pueden cargar los datos más recientes, hasta el momento de crear esa release.

Ejecutando ese archivo sobre la base de datos `covid-data` vacía, se rellenará con todos los datos necesarios para la ejecución.


## Contribuir ♥ <a name="contribuir"></a>

A este proyecto se puede contribuir con mejoras, añadiendo nuevos comandos o añadiendo nuevos scrappers.

### Añadir nuevos scrappers <a name="añadir-nuevos-scrappers"></a>

Añadir un nuevo scrapper para un país es tan sencillo como colocar un archivo `<country_name>.py` en la carpeta `covid_data/scrappers` y que ese archivo exponga una función:

```python
def scrap(db_engine: psycopg2._psycopg.connection, start_date: datetime.datetime)
```

### Añadir nuevos comandos <a name="añadir-nuevos-comandos"></a>

Añadir un nuevo comando implica colocar un archivo `<command_name>.py` en la carpeta `covid_data/commands` y que ese archivo exponga una función `main` con todos los decoradores de [click](https://click.palletsprojects.com/en/8.0.x/) necesarios.

Un decorador obligatorio es `@click.command("command_name")`, pues si no se pone, el comando será `main`.
## Como biblioteca <a name="como-biblioteca"></a>

La parte más interesante de este paquete como biblioteca es el sumbódulo `db`, que se detalla en el archivo [CODE](CODE.md).

## License <a name="license"></a>

[The Unlicense](LICENSE)
