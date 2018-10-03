# -*- coding: utf-8 -*-

import hashlib
import json

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base as sq_declarative_base
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.sql.expression import Insert

from .utilities import orm_attributes, sorteditems


# Let's make this a class decorator
def declarative_base(cls): return sq_declarative_base(cls=cls)


@compiles(Insert)
def append_string(insert, compiler, **kw):
    s = compiler.visit_insert(insert, **kw)
    if 'append_string' in insert.kwargs:
        return s + " " + insert.kwargs['append_string']
    return s


class db_base(object):
    """
    Add some default properties and methods to the SQLAlchemy declarative base.
    """

    ignored_attributes = []

    @property
    def columns(self):
        return [c.name for c in self.__table__.columns]

    @property
    def columnitems(self):
        return dict([(c, getattr(self, c)) for c in self.columns])

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.columnitems)

    def tojson(self):
        return self.columnitems

    @property
    def filtereditems(self):
        ignore = self.ignored_attributes + ['_sa_instance_state']
        return {k: v for k, v in self.columnitems.items()
                if k not in ignore}

    def _hash(self):
        text = json.dumps(sorteditems(self.filtereditems)).encode('utf-8')
        return hashlib.md5(text).hexdigest()

    @classmethod
    def hash_from_dict(cls, attributes):
        ignore = cls.ignored_attributes + ['_sa_instance_state']
        filtered = {k: v for k, v in attributes.items()
                    if k in orm_attributes(
                        cls, exclude_primary=False, exclude_relations=True) and
                    k not in ignore}
        text = json.dumps(sorteditems(filtered)).encode('utf-8')
        return hashlib.md5(text).hexdigest()

    @classmethod
    def from_dict(cls, attributes):
        obj = cls()
        filtered = {k: v for k, v in attributes.items()
                    if k in orm_attributes(cls, exclude_primary=False)}
        r_keys = [k for k, v in filtered.items() if isinstance(v, list)]
        relationships = {k: filtered.pop(k) for k in r_keys}
        obj.__dict__.update(filtered)
        for k, v in relationships.items():
            if getattr(obj, k) is not None:
                getattr(obj, k).extend(v)
            else:
                setattr(obj, k, v[0])
        return obj
