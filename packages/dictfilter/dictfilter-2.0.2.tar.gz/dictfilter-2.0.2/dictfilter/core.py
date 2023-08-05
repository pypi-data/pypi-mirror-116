import collections.abc


def _nested_update(base, other):
    for k, v in other.items():
        if isinstance(v, collections.abc.Mapping):
            base[k] = _nested_update(base.get(k, {}), v)
        elif isinstance(v, list):
            for a, b in zip(base[k], v):
                _nested_update(a, b)
        else:
            base[k] = v
    return base


def _filter(data, fields):
    out = {}

    for field in fields:
        key, *rest = field.split('.', maxsplit=1)

        if key not in data:
            # TODO: maybe add a 'strict' option to raise an exception here.
            continue

        if rest:
            many = isinstance(data[key], list)
            sub_element = query(data[key], rest)

            existing_element = out.get(key, [] if many else {})
            if many and existing_element:
                for current, new in zip(out[key], sub_element):
                    _nested_update(current, new)
            elif not many and existing_element:
                _nested_update(out[key], sub_element)
            else:
                out[key] = sub_element
        else:
            out[key] = data[key]

    return out


def query(data, fields):
    many = isinstance(data, list)
    if many:
        return [_filter(d, fields) for d in data]
    else:
        return _filter(data, fields)
