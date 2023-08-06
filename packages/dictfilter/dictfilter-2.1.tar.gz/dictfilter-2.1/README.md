# dictfilter

## installation

```shell
pip install dictfilter
```

## usage

```python
from dictfilter import query

bsg = {
    'class': 'Battlestar',
    'model': 'Jupiter',
    'name': 'Galactica',
    'crew': {
        'commander': 'William Adama',
        'xo': 'Saul Tigh',
        'cag': 'Kara Thrace',
    }
}

result = query(bsg, ['class', 'name', 'crew.commander'])

# {
#     'class': 'Battlestar',
#     'name': 'Galactica',
#     'crew': {
#         'commander': 'William Adama',
#     }
# }
```

The default delimiter used in field names is dot `.` however this can be changed 
with the `delimiter` keyword argument to `query`:

```python
result = query(bsg, ['class', 'name', 'crew > commander'], delimiter=' > ')

# {
#     'class': 'Battlestar',
#     'name': 'Galactica',
#     'crew': {
#         'commander': 'William Adama',
#     }
# }
```

## django integration

Register the dictfilter middleware in `settings.py`:

```python
MIDDLEWARE = [
    ...
    'dictfilter.django.middleware.DictFilterMiddleware',
]
```

By default, every 2xx series response will be filtered based on a 
comma-separated `fields` parameter in the query string.
