# -*- coding: utf-8 -*-
import enum
from configparser import ConfigParser

import requests
from ge.bpmc.app.injection import Contexts, Core, Factories, Services
from ge.bpmc.persistence.orm import RepositoryORM
from ge.bpmc.tests.base import BaseDataModelTestCase, ResultWrapper
from ge.bpmc.utilities import conf as ConfUtils
from ge.bpmc.utilities.sqlalchemy import (sqlalchemy_get_unique_item_or_none,
                                          transaction)
from ge.bpmc.utilities.swagger import (get_swagger_enum_type,
                                       get_table_swagger_schema,
                                       get_validation_schema, validate_payload)
from mockito import mock, unstub, when
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound


class StringEnum(enum.Enum):
    Unpaired = 'U'


class FloatEnum(enum.Enum):
    Unpaired = 2.0


class IntEnum(enum.Enum):
    Unpaired = 1


class OtherEnum(enum.Enum):
    Unpaired = []


class UtilitiesTestCase(BaseDataModelTestCase):

    def setUp(self):
        super(UtilitiesTestCase, self).setUp()

    def tearDown(self):
        super(UtilitiesTestCase, self).tearDown()

    @transaction(Core.logger, Contexts.em)
    def test_sqlalchemy_get_unique_item_or_none(self):
        repository = self.em.get_repository('uid', 1)
        self.assertEqual(repository, None)
        with self.assertRaises(NoResultFound):
            self.em._session_.query(RepositoryORM).one()
        rep = self.create_repository()
        rep2 = self.create_repository(name='test_repo2', host='127.0.0.2')
        with self.assertRaises(MultipleResultsFound):
            self.em._session_.query(RepositoryORM).one()

    def test_transaction(self):
        @transaction(Core.logger, Contexts.em)
        def test_commit():
            self.em._session_.add(
                RepositoryORM(None, 'test', '127.0.0.1'))
        wrapper = ResultWrapper()
        wrapper2 = ResultWrapper()
        wrapper.EXPECTED_RESPONSE = 'Commit'
        wrapper2.EXPECTED_RESPONSE = 'Close session'
        when(self.em._session_).commit().thenAnswer(wrapper.exec)
        when(self.em._session_).close().thenAnswer(wrapper2.exec)
        test_commit()
        self.assertEqual(wrapper.RESPONSE, wrapper.EXPECTED_RESPONSE)
        self.assertEqual(wrapper2.RESPONSE, wrapper2.EXPECTED_RESPONSE)
        unstub(self.em._session_)

        @transaction(Core.logger, Contexts.em)
        def test_rollback():
            raise Exception('Rollback')
        wrapper = ResultWrapper()
        wrapper.EXPECTED_RESPONSE = 'Rollback'
        when(self.em._session_).rollback().thenAnswer(wrapper.exec)
        when(Core.logger()).warning(...).thenReturn(None)
        with self.assertRaises(Exception):
            test_rollback()
        self.assertEqual(wrapper.RESPONSE, wrapper.EXPECTED_RESPONSE)
        unstub(self.em._session_)
        unstub(Core.logger())

    def test_check_configuration_keys(self):
        # check_configuration_keys
        parser = ConfigParser()
        parser.read_dict({'section1': {'opt1': 'val1'}})
        expected_keys = {'section1': ['opt1']}
        wrapper = ResultWrapper()
        wrapper.EXPECTED_RESPONSE = 'Ok'
        (when(ConfUtils).check_configuration_keys(...)
         .thenAnswer(wrapper.exec))
        ConfUtils.check_configuration_keys(expected_keys, parser)
        self.assertEqual(wrapper.RESPONSE, wrapper.EXPECTED_RESPONSE)
        unstub(ConfUtils)

        expected_keys = {'section1': ['opt2']}
        with self.assertRaises(LookupError):
            ConfUtils.check_configuration_keys(expected_keys, parser)

    def test_get_swagger_enum_type(self):
        res = get_swagger_enum_type(
            [x.value for x in list(StringEnum.__members__.values())])
        self.assertEqual(res, 'string')
        res = get_swagger_enum_type(
            [x.value for x in list(FloatEnum.__members__.values())])
        self.assertEqual(res, 'numeric')
        res = get_swagger_enum_type(
            [x.value for x in list(IntEnum.__members__.values())])
        self.assertEqual(res, 'integer')
        res = get_swagger_enum_type(
            [x.value for x in list(OtherEnum.__members__.values())])
        self.assertEqual(res, 'string')
