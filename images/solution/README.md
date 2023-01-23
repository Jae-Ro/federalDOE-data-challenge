# CodeTest Package

This is a simple example package for the Tamr Federal DOE Codetest take-home assignment.

[Github Link](https://github.com/Jae-Ro/federalDOE-data-challenge/images/solution)

### This package was developed using the following versions of python and pip:
* python v3.10.8
* pip v22.3.1

## Prerequisites
If running locally (not in docker container), make sure you create a `.env` file in the `images/solution` directory with the following content
```
DB_HOST=127.0.0.1
DB_UN=codetest
DB_PW=swordfish
```

## How to Install Package in Dev Editable Mode:
```bash
$ cd images/solution
$ pip install -e .
```

## How to Run Test Suite:
```bash
$ cd images/solution
$ pytest -v -s tests/
```
** Note: integration and e2e (end-to-end) tests require database connection, so make sure you run `$ docker compose up database` from the root directory where `docker-compose.yml` lives before running these tests
