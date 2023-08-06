
# dcolor

![issues](https://img.shields.io/github/issues/tatsuya4649/dcolor)
![forks](https://img.shields.io/github/forks/tatsuya4649/dcolor)
![starts](https://img.shields.io/github/forks/tatsuya4649/dcolor)
![python](https://img.shields.io/pypi/pyversions/dcolor)
![pypi](https://badge.fury.io/py/dcolor.svg)

dcolor is open-source package for Python.

dcolor for easily modifying charactor.

## Install

```
$ pip install dcolor
```

## Usage

```python:normal.py
print("Hello World")
```

output:

![normal](https://raw.githubusercontent.com/tatsuya4649/dcolor/master/docs/assets/usage/normal.png)

```python:colors.py
for dcolor import colors

color_string = colors("Hello World", "red")

print(color_string)
```

output:

![colors](https://raw.githubusercontent.com/tatsuya4649/dcolor/master/docs/assets/usage/colors.png)

```python:backgrounds.py
for dcolor import backgrounds

back_string = backgrounds("Hello World", "red")

print(back_string)
```
output:

![backgrounds](https://raw.githubusercontent.com/tatsuya4649/dcolor/master/docs/assets/usage/backgrounds.png)

```python:attributes.py
for dcolor import attributes

attr_string = attributes("Hello World", "bold")

print(attr_string)
```

output:

![attributes](https://raw.githubusercontent.com/tatsuya4649/dcolor/master/docs/assets/usage/attributes.png)

## LICENSE

dcolor project is licensed under the terms of MIT license.
