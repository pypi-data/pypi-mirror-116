# COVID Data Loader

[![forthebadge made-with-python](https://raw.githubusercontent.com/alesanmed-educational-projects/covid-data/main/assets/img/made-with-python.svg)](https://www.python.org/)

![Tests](https://github.com/alesanmed-educational-projects/covid-data/actions/workflows/python-app.yml/badge.svg)
![Build](https://github.com/alesanmed-educational-projects/covid-data/actions/workflows/pypi-publish.yml/badge.svg)
[![PyPI version](https://d25lcipzij17d.cloudfront.net/badge.svg?id=py&type=6e&v=0.1.18)](https://badge.fury.io/py/covid-data)


This project is part of the [Core Data COVID](https://github.com/alesanmed-educational-projects/core-data-covid-project) project. Here are the tools needed for:
- Create the database
- Populate the database
- Query the data

# Table of contents

- [Installation 📥](#installation)
  - [Library 📖](#library)
  - [CLI 🤖](#tio)
- [Configuration ⚙](#configuration)
- [Usage as CLI 🎛️](#use-as-cli)
  - [loadcsv](#loadcsv)
  - [scrap](#scrap)
  - [Populate DB from backup](#populate-from-backup)
- [Contributing ♥](#contribuir)
  - [Add new scrappers](#add-scrappers)
  - [Add new commands](#add-commands)
- [As library](#as-library)
- [License](#license)

## Installation 📥 <a name="installation"></a>

### Library 📖  <a name="library"></a>

To use this project as a library, you have to install it with `pip`:

```
pip install covid-data
```

### CLI 🤖 <a name="cli"></a>

To use it as CLI, you still have to install it with `pip`. After that, you can run the commands from a terminal:

```
covid-data --help
```

## Configuration ⚙ <a name="configuration"></a>

The project looks for the following environment variables to configure several parts:

- POSTGRES_USER: Postgres username
- POSTGRES_PASS: Postgres password
- POSTGRES_HOST: Postgres host
- POSTGRES_PORT: Postgres port
- POSTGRES_DB: Postgres database
- CAGEDATA_API_KEY: OpenCageData API Key

You can create the OpenCage data ley from their [website](https://opencagedata.com/). The package uses it to enrich and normalize places.

## Usage as CLI 🎛️ <a name="use-as-cli"></a>

To populate the database, you may use the commands the library provides.

The first step is to create the database with the schema available [here](covid_data/db/schema/db_schema.sql). The database structure is the following one:

![Database ERD](https://github.com/alesanmed-educational-projects/covid-data/raw/main/assets/img/erd-covid.png)

Once the package finishes creating the database, you can populate it from a CSV with the command:

```bash
❯ covid-data loadcsv /path/to/confirmed.csv,/path/to/dead.csv,/path/to/recovered.csv -tf -o
```

For getting help on how to use the command, run:

```bash
❯ covid-data --help
Usage: covid-data [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  loads    Loads FILES as CSV data.
  scrap    Scrap cases of chosen COUNTRY.
```

### loadcsv <a name="loadcsv"></a>

```bash
❯ covid-data loadcsv --help
Usage: covid-data loadcsv [OPTIONS] FILES

  Loads FILES as CSV data. If you want to load several files, each file should be separated by a comma

Options:
  -t, --type TEXT      Type of cases contained in each file, separated by
                       comma. Leave blank if using --type-in-file
  -tf, --type-in-file  Set this to true if the file names are <case_type>.csv
                       Being <case_type> one of confirmed, recovered or dead
  -o, --optimize       Set to true to skip lines for places that has more
                       cases than columns on the CSV
  --help               Show this message and exit.
```

This command allows you to populate the database with one or more CSV files. Each file may only contain one case type.

You have to provide the paths separated by commas.

As well as with the file names, each file case type has to be separated by commas. Pass the type list under the argument `--type` and **in the same order** as the files.

Another option is not using the `--type` argument. In that case, you have to name the files according to the case type each of them contains (e.g., `recovered.csv`). If you choose this alternative, you have to set the flag `--type-in-file`.

The last flag is `--optimize`. If set, for each row, the CLI is going to get the country from that row. Then check the number of cases already saved for that country (with the same type as the file). If the country has the same or more number of cases as columns are in the CSV, it will skip that row.

An example of how to run the command for loading all CSVs:

```bash
❯ covid-data loadcsv /path/to/confirmed.csv,/path/to/dead.csv,/path/to/recovered.csv -tf -o
```

In that example, I'm using the file name to specify the case type contained. I'm also setting the optimization flag.

### scrap <a name="scrap"></a>

With this command, you can scrap the cases of a specific country, allowing you to extend the data from that country.

The command usage is as follows:

```bash
❯ covid-data scrap --help
Usage: covid-data scrap [OPTIONS] COUNTRY

  Scrap cases of chosen COUNTRY. To check available countries to scrap use
  --check

Options:
  --check to Use this to check available countries
  --start-date TEXT  Date to start scraping cases from, in format DD/MM/YYYY
  --help             Show this message and exit.
``` 

There is one required argument, the country to scrap. If you want to know which countries are available, you can pass whatever value to `COUNTRY` and set the flag `--check`:

```bash
❯ covid-data scrap XXX --check
Available countries are:
        France
        Spain
```

Once you know which country to scrap, you can launch the command:

```bash
❯ covid-data scrap Spain
Fetching cases for province 1/20
Fetching cases for province 2/20
Fetching cases for province 3/20
...
```

You can set the start date with the argument `--start-date`. The date format required is `DD/MM/YYYY`

```bash
❯ covid-data scrap France --start-date 01/08/2021
```

### Populate DB from backup <a name="populate-from-backup"></a>

You may find attached to each [release](https://github.com/alesanmed-educational-projects/covid-data/releases), a `covid-data.sql` file. That script allows you to load into an SQL database the most recent data.

If you run that script on the `covid-data` database, it will populate it with the necessary data for running the app.


## Contributing ♥ <a name="contributing"></a>

You can become part of this project by proposing (and even implementing) enhancements, new commands, or new scrappers.

### Add new scrappers <a name="add-scrappers"></a>

Adding a new scrapper is as simple as creating a new file named `<country_name>.py` in the folder `covid_data/scrappers` and make that file expose a function with the following signature:

```python
def scrap(db_engine: psycopg2._psycopg.connection, start_date: datetime.datetime)
```

That function has to be in charge of scrapping, processing, formatting as well as saving new cases for the requested country.
### Add new commands <a name="add-commands"></a>

Adding a new command is also a simple process. Place a file named `<command_name>.py` in the folder `covid_data/commands` and expose a function `main` with the needed [click](https://click.palletsprojects.com/en/8.0.x/) decorators.

A mandatory decorator is `@click.command("command-name")`, to avoid overwriting commands as all functions are named `main`.
## As library <a name="as-library"></a>

The potential of this library is offered by the `db` submodule, which you can find on [CODE](CODE.md).

## License <a name="license"></a>

[The Unlicense](LICENSE)
