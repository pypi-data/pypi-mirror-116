from dictfilter import query


def test_single_flat_query():
    unfiltered = {
        'a': 1,
        'b': True,
        'c': 'testing',
    }

    expected = {'a': 1, 'c': 'testing'}

    assert query(unfiltered, ['a', 'c']) == expected


def test_many_flat_query():
    unfiltered = [{
        'a': 1,
        'b': True,
        'c': 'testing',
    }, {
        'a': 5,
        'b': False,
        'c': 'another',
    }]

    expected = [{'a': 1, 'c': 'testing'}, {'a': 5, 'c': 'another'}]

    assert query(unfiltered, ['a', 'c']) == expected


def test_single_full_nested_query():
    unfiltered = {
        'a': 1,
        'b': {
            'nest': True,
            'second': 13,
        },
        'c': 'testing',
    }

    expected = {
        'b': {
            'nest': True,
            'second': 13,
        },
        'c': 'testing',
    }

    assert query(unfiltered, ['b', 'c']) == expected


def test_single_select_nested_query():
    unfiltered = {
        'a': 1,
        'b': {
            'nest': True,
            'unwanted': 7,
        },
        'c': 'testing',
    }

    expected = {
        'b': {
            'nest': True,
        },
        'c': 'testing',
    }

    assert query(unfiltered, ['b.nest', 'c']) == expected


def test_many_full_nested_query():
    unfiltered = [{
        'a': 1,
        'b': {
            'nest': True,
            'second': 13,
        },
        'c': 'testing',
    }, {
        'a': 5,
        'b': {
            'nest': False,
            'second': 4,
        },
        'c': 'another',
    }]

    expected = [{
        'b': {
            'nest': True,
            'second': 13,
        },
        'c': 'testing',
    }, {
        'b': {
            'nest': False,
            'second': 4,
        },
        'c': 'another',
    }]

    assert query(unfiltered, ['b', 'c']) == expected


def test_many_select_nested_query():
    unfiltered = [{
        'a': 1,
        'b': {
            'nest': True,
            'unwanted': 7,
        },
        'c': 'testing',
    }, {
        'a': 5,
        'b': {
            'nest': False,
            'unwanted': 91,
        },
        'c': 'another',
    }]

    expected = [{
        'b': {
            'nest': True,
        },
        'c': 'testing',
    }, {
        'b': {
            'nest': False,
        },
        'c': 'another',
    }]

    assert query(unfiltered, ['b.nest', 'c']) == expected


def test_single_multi_nested_query():
    unfiltered = {
        'unwanted': 6,
        'b': {
            'nest': True,
            'other': 'another',
        },
        'c': 'testing',
    }

    expected = {
        'b': {
            'nest': True,
            'other': 'another',
        },
        'c': 'testing',
    }

    assert query(unfiltered, ['b.nest', 'b.other', 'c']) == expected


def test_many_multi_nested_query():
    unfiltered = [{
        'unwanted': 6,
        'b': {
            'nest': True,
            'other': 'another',
        },
        'c': 'testing',
    }, {
        'unwanted': 23,
        'b': {
            'nest': False,
            'other': 'the other',
        },
        'c': 'another',
    }]

    expected = [{
        'b': {
            'nest': True,
            'other': 'another',
        },
        'c': 'testing',
    }, {
        'b': {
            'nest': False,
            'other': 'the other',
        },
        'c': 'another',
    }]

    assert query(unfiltered, ['b.nest', 'b.other', 'c']) == expected


def test_single_multi_nested_list_query():
    unfiltered = {
        'unwanted': 6,
        'b': [{
            'nest': True,
            'other': 'another',
        }, {
            'nest': False,
            'other': 'the other',
        }],
        'c': 'testing',
    }

    expected = {
        'b': [{
            'nest': True,
            'other': 'another',
        }, {
            'nest': False,
            'other': 'the other',
        }],
        'c': 'testing',
    }

    assert query(unfiltered, ['b.nest', 'b.other', 'c']) == expected


def test_many_multi_nested_list_query():
    unfiltered = [{
        'unwanted': 6,
        'b': [{
            'nest': True,
            'other': 'another',
        }, {
            'nest': False,
            'other': 'the other',
        }],
        'c': 'testing',
    }, {
        'unwanted': 2,
        'b': [{
            'nest': False,
            'other': 'the third',
        }, {
            'nest': True,
            'other': 'final',
        }],
        'c': 'another',
    }]

    expected = [{
        'b': [{
            'nest': True,
            'other': 'another',
        }, {
            'nest': False,
            'other': 'the other',
        }],
        'c': 'testing',
    }, {
        'b': [{
            'nest': False,
            'other': 'the third',
        }, {
            'nest': True,
            'other': 'final',
        }],
        'c': 'another',
    }]

    assert query(unfiltered, ['b.nest', 'b.other', 'c']) == expected


def test_non_existent_fields_query():
    unfiltered = {
        'a': 1,
        'b': True,
        'c': 'testing',
    }

    expected = {'a': 1, 'c': 'testing'}

    assert query(unfiltered, ['a', 'c', 'd']) == expected


def test_deep_nested_query():
    unfiltered = {
        'a': {
            'b': {
                'c': {
                    'value': 5,
                    'another': 6
                },
                'irrelevant_c': 10,
            },
            'irrelevant_b': 10,
        },
        'irrelevant_a': 10,
    }

    expected = {'a': {'b': {'c': {'value': 5}}}}
    assert query(unfiltered, ['a.b.c.value']) == expected


def test_deep_nested_query_with_multiple_fields():
    unfiltered = {
        'a': {
            'b': {
                'c': 'foo',
                'd': 'bar',
                'e': 'ignore',
            }
        }
    }

    expected = {
        'a': {
            'b': {
                'c': 'foo',
                'd': 'bar',
            }
        }
    }

    assert query(unfiltered, ['a.b.c', 'a.b.d']) == expected


def test_deep_nested_list_query_with_multiple_fields():
    unfiltered = {
        'a': {
            'b': [{
                'c': 'foo',
                'd': 'bar',
                'e': 'ignore',
            }, {
                'c': 'baz',
                'd': 'qux',
                'e': 'ignore',
            }]
        }
    }

    expected = {
        'a': {
            'b': [{
                'c': 'foo',
                'd': 'bar',
            }, {
                'c': 'baz',
                'd': 'qux',
            }]
        }
    }

    assert query(unfiltered, ['a.b.c', 'a.b.d']) == expected


def test_deep_nested_list_query_with_mismatched_lists():
    unfiltered = {
        'a': {
            'b': [{
                'c': 'foo',
                'e': 'ignore',
            }, {
                'd': 'qux',
                'e': 'ignore',
            }]
        }
    }

    expected = {
        'a': {
            'b': [{
                'c': 'foo',
            }, {
                'd': 'qux',
            }]
        }
    }

    assert query(unfiltered, ['a.b.c', 'a.b.d']) == expected
