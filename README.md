# Turbo

Refactoring REN-ISAC `turbo-telegram` repository.

# How to run

Install the project using `poetry`

```
poetry install
```

Run the command line (renamed to `turbo`) using

```
turbo --token 12345
```

For more details view the original repo [here](https://github.com/renisac/turbo-telegram/tree/main).

## Changes implemented

* Migrated project to use `poetry`
* Tested ane evaluated for `python3.12` and upgraded package stack
* Restructured client.py -> main client used to communicate with the service
* Restructure print formatting for `raw` and `table`
* Implemented missing functionality of `timeout` and `proxy`
* Removed un-necessary imports of `arrow`
* Added basic unit tests and used `tox`
* Cleaned up files used and removed deprecated functions (colors, move away from versioneer for github actions in the future)

# TODO:

* Support more versions of Python
* Deploy changes to `pypi` or similar
* Implement CI/CD using Github Actions
* Add more unit tests
* Refactor all client-like repos under REN-ISAC into one package or one library
* ...
