# sfilter
Tool for filtering out stinky/smelling code

## Example usage
```shell
python -c'import sfilter.main as sf;sf.run_all("<path_to_project>")'
```

## Build, install and check distribution readiness the project
```shell
PIPENV_IGNORE_VIRTUALENVS=1 pipenv run python setup.py bdist_wheel
PIPENV_IGNORE_VIRTUALENVS=1 pipenv run pip install -e .
pipenv shell
python
```
```python
import src.sfilter.main as tic

tic.run_all("src/sfilter")
exit()
```
```shell
exit
PIPENV_IGNORE_VIRTUALENVS=1 pipenv run python setup.py sdist
tar tzf dist/try_improve_code-<version>.tar.gz 
```

## Publish
```shell

```


## Run all checks
```shell
PIPENV_IGNORE_VIRTUALENVS=1 pipenv run python -c'import sfilter.main as sf;sf.run_all("./sfilter")'
```

## Step by step

1. Clean before analysis:
    ```shell
    PIPENV_IGNORE_VIRTUALENVS=1 pipenv run python -c'import sfilter.main as sf;sf.clean_before_test()'
    ```
1. Run black:
    ```shell
    PIPENV_IGNORE_VIRTUALENVS=1 pipenv run python -c'import sfilter.main as sf;sf.run_black("./sfilter")'
    ```
1. Run isort:
    ```shell
    PIPENV_IGNORE_VIRTUALENVS=1 pipenv run python -c'import sfilter.main as sf;sf.run_isort("./sfilter")'
    ```
1. Run flake8:
    ```shell
    PIPENV_IGNORE_VIRTUALENVS=1 pipenv run python -c'import sfilter.main as sf;sf.run_flake8("./sfilter")'
    ```
1. Run radon:
    ```shell
    PIPENV_IGNORE_VIRTUALENVS=1 pipenv run python -c'import sfilter.main as sf;sf.run_radon("./sfilter")'
    ```
1. Run final checks:
    ```shell
    PIPENV_IGNORE_VIRTUALENVS=1 pipenv run python -c'import sfilter.main as sf;sf.check_quality()'
    ```
