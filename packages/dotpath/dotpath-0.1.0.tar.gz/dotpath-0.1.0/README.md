# dotpath
A simple module to access Python props using dotpath.

## Example
```python
from dotpath import dotpath

# A object
pets_dic = {
    'pets': {
        'dog': {
            'name': 'Billy',
            'age': 5,
            'friends': ['Joe', 'Jack'],
        },
        'cat': {
            'name': 'Joe',
            'age': 6,
            'friends': ['Billy', 'Pop'],
        },
    },
}

dog_name = getpath(pets_dic, 'pets.dog.name') # Returns Billy
cat_name = getpath(pets_dic, 'pets.cat.name') # Returns Joe
```