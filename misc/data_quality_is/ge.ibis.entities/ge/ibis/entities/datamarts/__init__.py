# -*- coding: utf-8 -*-

from .tables import (CtLogLast15Days, DevicesOverview, DosimetricLast15Days,
                     IBISData, PatternLast15Days, StudyDataSource)


def init_database(session):
    IBISData.metadata.create_all(session.bind)
    session.commit()
