# CodeTest Package

This is a simple example package for the Tamr Federal DOE Codetest take-home assignment.

[Github Repo](https://github.com/Jae-Ro/federalDOE-data-challenge/images/solution)

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
