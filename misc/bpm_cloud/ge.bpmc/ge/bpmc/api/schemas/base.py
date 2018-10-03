# -*- coding: utf-8 -*-

from flask_restful_swagger_2 import Schema


class SQLAlchemySchemaBase(Schema):

    _primary = None

    @classmethod
    def requirements_without_primary(self):
        return (
            dict([(k, v) for k, v in self.properties.items()
                  if k != self._primary]),
            [x for x in self.required if x != self._primary])
