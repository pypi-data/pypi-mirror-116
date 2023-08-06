# Feature Catalog

Install library from local folder using pip:

```bash
pip install --upgrade .
```

Install library from package file

```bash
# first create the package
python setup.py clean --all
python setup.py sdist bdist_wheel

# install using pip
pip install dist/*.whl
```

## Testing

```bash
pip install -r dev_requirements.txt
python -m pytest
```

## Building and releasing 

```bash
python -m pip install --user --upgrade setuptools wheel twine

rm -rf dist/ 

python setup.py sdist bdist_wheel

twine upload -u td-aoa -p <user@pass> dist/*

```