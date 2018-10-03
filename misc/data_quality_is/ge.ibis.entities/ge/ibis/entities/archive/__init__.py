# -*- coding: utf-8 -*-

from .tables import IBISArchive


def init_database(session):
    IBISArchive.metadata.create_all(session.bind)
    session.commit()
