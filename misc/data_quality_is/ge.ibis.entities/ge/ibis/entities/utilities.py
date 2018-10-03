# -*- coding: utf-8 -*-

import functools
import inspect

from sqlalchemy.orm import relationships
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.exc import NoResultFound

RelationshipComparator = relationships.RelationshipProperty.Comparator


def rgetattr(obj, attr, *args):
    """
    Recursive getattr utility allowing to pass a dotted_name
    attribute sequence.

    Keyword arguments:
    :obj: Python object
    :attr: dotted sequence (do not start with a '.')
    :args: arguments to pass to the getattr method
    """
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))


def orm_attributes(class_, exclude_primary=True, exclude_relations=False):
    """
    Utility to list ORM attributes of an object mapped by SQLAlchemy.

    Keyword arguments:
    :parma class_: SQLAlchemy mapped python class
    :param exclude_primary: if attributes flagged as primary keys should
                      be excluded or not (must be primary key and be
                      autoincremented)
    :param exclude_relations: same, with relations
    """
    table = rgetattr(class_, '_sa_class_manager.mapper.mapped_table.c')
    return [x[0] for x in
            filter(lambda x: (
                isinstance(x[1], InstrumentedAttribute) and
                (not isinstance(x[1].comparator,
                                RelationshipComparator) if exclude_relations
                   else True) and
                (not (hasattr(x[1], 'primary_key') and
                      x[1].primary_key and
                      x[1].autoincrement)
                 if exclude_primary else True)),
        inspect.getmembers(class_))]


def filter_attributes(class_, attrs, exclude_primary=True):
    """
    Utility to filter attributes (set 's') and SQLAlchemy's mapped
    class (set 't') for a union operation.
    Returns only attributes keys and associated values
    if keys exist in 't'.

    Keyword arguments:
    :param class_: SQLAlchemy mapped python class
    :param attrs: List of (key, value) tuples
    :param exclude_primary: if attributes flagged as primary keys should
                      be excluded or not (must be primary key and be
                      autoincremented)
    :return: dict
    """
    def f(x): return x[0] in orm_attributes(class_, exclude_primary)
    return {k: v for k, v in filter(f, attrs)}


def sortedvalue(val):
    """
    Sorts a dict value based on its type.

    :param val: A python object
    """
    if isinstance(val, dict):
        return sorteditems(val)
    elif isinstance(val, (list, tuple)):
        return sorted(val)
    return val


def sorteditems(_dict):
    """
    Sorts a dictionnary by its keys. Acts recursively for nested dicts.

    :param _dict: A python dict
    """
    return {k: sortedvalue(v) for k, v in sorted(_dict.items())}
