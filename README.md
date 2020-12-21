#Junior Python Developer position 
#Test task

##Installation

```shell
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

Install dependencies:
```shell
poetry install
```

Use created venv:

```shell
poetry shell
```

##Using

Run from the main directory of the project to get help about the options:

```shell
python -m decision.words_counter_cli -h
```

Run from the main directory of the project to run words counting in the directory:

```shell
python -m decision.words_counter_cli -d directory_path
```

To make test start for the CLI interface please run it from the main directory of the project:

```shell
python -m decision.words_counter_cli -d ./test_data
```
