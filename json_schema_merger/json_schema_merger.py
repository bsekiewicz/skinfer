# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
import itertools


def merge_property_list(first_properties, second_properties):
    result = {}

    for key, value in first_properties.items():
        if key in second_properties:
            result[key] = _merge_schema(value, second_properties[key])
        else:
            result[key] = value

    for key, value in second_properties.items():
        if key not in result:
            result[key] = value

    return result


def get_reserved_keys(schema_type):
    if schema_type:
        return set(['type', 'properties', 'required'])
    else:
        raise NotImplementedError(
            "Missing implementation for schema type: %s" % schema_type)


def copy_nonreserved_keys(first, second):
    reserved_keys = get_reserved_keys(first.get('type'))

    return ((key, value)
            for key, value in itertools.chain(first.items(), second.items())
            if key not in reserved_keys)


def merge_objects(first, second):
    required = list(set(first.get('required', [])) &
                    set(second.get('required', [])))

    result = {
        'type': 'object',
        'properties': merge_property_list(first.get('properties', {}),
                                          second.get('properties', {})),
    }

    if required:
        result['required'] = required

    result.update(copy_nonreserved_keys(first, second))

    return result


def merge_strings(first, second):
    return second


def _merge_schema(first, second):
    assert first.get('type') == second.get('type'), (
        "Merging schemas for different types is not yet supported (%s, %s)" % (first.get('type'), second.get('type')))

    schema_type = first.get('type')

    if schema_type == 'object':
        return merge_objects(first, second)
    elif schema_type == 'string':
        return merge_strings(first, second)
    else:
        raise NotImplementedError("Type %s is not yet supported" % schema_type)


def merge_schema(first, second):
    if not (type(first) == type(second) == dict):
        raise ValueError("Argument is not a schema")

    if not (first.get('type') == second.get('type') == 'object'):
        raise NotImplementedError("Unsupported root type")

    return merge_objects(first, second)
