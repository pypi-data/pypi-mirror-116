![PyPI - Python Version](https://img.shields.io/pypi/pyversions/beunique)  ![PyPI - Status](https://img.shields.io/pypi/status/beunique)  ![PyPI](https://img.shields.io/pypi/v/beunique) ![PyPI - License](https://img.shields.io/pypi/l/beunique)
# [beunique]

## This is a basic project for learning how to make the PIP([PyPI]) package

### To install the package!
#### On Windows:
```bash 
$ pip install beunique
```
#### On macOS and Linux:
```bash
$ sudo pip3 install beunique
```

# Changelog

Check the [changelog here].
### Available modules in beunique package is
```bash
|_beunique
  |_data_collection
  |_repeat
```
### How to use:
### Example 1:
```python
from beunique import data_collection
# instanciate a variable for data_collection class.
collector = data_collection() #A url or path is expected, default url is 'https://raw.githubusercontent.com/cs109/2014_data/master/countries.csv'
collector.print_head() #Default value of rows is 5.
```
#### output 
```text
   Country  Region
0   Algeria  AFRICA
1    Angola  AFRICA
2     Benin  AFRICA
3  Botswana  AFRICA
4   Burkina  AFRICA
```
### Example 2:
```python
collector.print_head(3) # Here we are specifying for 3 rows.
```
#### output
```text
   Country  Region
0  Algeria  AFRICA
1   Angola  AFRICA
2    Benin  AFRICA
```
### Example 3:
```python
from beunique import repeat
# instanciate a variable for repeat class.
repetitor = repeat() 
repetitor.print_repeat() #The default word is hello and count is 100.
```
#### output
```text
                hello hello hello hello hello 
                hello hello hello hello hello 
                hello hello hello hello hello 
                hello hello hello hello hello 
                hello hello hello hello hello 
                hello hello hello hello hello 
                hello hello hello hello hello 
                hello hello hello hello hello 
                hello hello hello hello hello 
                hello hello hello hello hello 
                hello hello hello hello hello 
                hello hello hello hello hello 
                hello hello hello hello hello 
                hello hello hello hello hello 
                hello hello hello hello hello 
                hello hello hello hello hello 
                hello hello hello hello hello 
                hello hello hello hello hello 
                hello hello hello hello hello 
                hello hello hello hello hello 
```
### Example 4:
```python
repetitor.print_repeat("congrats",10) # Here we are specifying word as congrats for 10 times.
```
#### output
```text
            congrats congrats congrats congrats congrats 
            congrats congrats congrats congrats congrats
```

# License
[MIT License]

Copyright (c) 2020 [Dara Ekanth]

[PyPI]: https://pypi.org/
[changelog here]: https://github.com/Dara-Ekanth/todo_custom_package/releases
[beunique]: https://pypi.org/project/beunique/
[MIT License]: https://github.com/Dara-Ekanth/todo_custom_package/blob/master/LICENSE
[Dara Ekanth]: https://github.com/Dara-Ekanth/ 