# is_string

![tests](https://github.com/przemo199/is_string/actions/workflows/tests.yml/badge.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/is_string)

A small Python library to determine if something is a string

## Installation


```bash
pip install is-string
```

## Usage

```python
from is_string import is_string

print(is_string('1')) #True
print(is_string(1))   #False
```

or

```python
import is_string

print(is_string.is_string('1')) #True
print(is_string.is_string(1))   #False
```

## Credits

This project was inspired by the work done by [Jacob Tomlinson](https://github.com/jacobtomlinson), especially the brilliant Python library [is-number](https://github.com/jacobtomlinson/is-number)
