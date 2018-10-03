# -*- coding: utf-8 -*-

import warnings

from sqlalchemy import exc as sa_exc

from .tables import (AeFtp, AeIntegration, ApplicationEntity,
                     ConnectivityFunctionality, ConnectivityList,
                     ConnectivityPattern, CtLogPattern, CtLogPatternStatus,
                     CustomDictionary, Customer, CustomerDictionary,
                     CustomerWorkaround, DeviceVersionRequirement, DicomInput,
                     DicomInputPattern, DicomInputStatus, DicomPattern,
                     Dosimetric, DwFunctionality, FtpConnection, IBISMain,
                     InnovaLogPull, InnovaLogPullStatus, IntegrationMode,
                     IntegrationModeMessageType, MessagePattern, Rationale,
                     SpecificTranslator, SpecificTranslatorElement, Status,
                     Study, SupportedDevice, TranslatorConfig,
                     TranslatorConfigDeviceVersionRequirement,
                     TranslatorConfigStatus, Workaround)
from .views import load_templates

status_table = Status._sa_class_manager.mapper.mapped_table
rationale_table = Rationale._sa_class_manager.mapper.mapped_table


def init_database(session):
    status_update_str = 'ON DUPLICATE KEY UPDATE `status`=VALUES(`status`)'
    rat_update_str = 'ON DUPLICATE KEY UPDATE `rationale`=VALUES(`rationale`)'
    #  Schema deployment
    IBISMain.metadata.create_all(session.bind)
    # Default values setup
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)
        session.execute(
            status_table.insert(append_string=status_update_str),
            [
                {'id': 1, 'status': 'OK'},
                {'id': 2, 'status': 'NOK'},
                {'id': 3, 'status': 'NA'}
            ])
        session.execute(
            rationale_table.insert(append_string=rat_update_str),
            [
                {'id': 1,   'rationale': 'NFF'},
                {'id': 2,   'rationale': 'ENHANCEMENT'},
                {'id': 3,   'rationale': 'LIMITED'},
                {'id': 4,   'rationale': 'WARNING'},
                {'id': 5,   'rationale': 'ERROR'},
                {'id': 6,   'rationale': 'CRITICAL'},
                {'id': 7,   'rationale': 'MISSING'},
                {'id': 8,   'rationale': 'EXTRA'},
                {'id': 9,   'rationale': 'NOIM'},
                {'id': 10,  'rationale': 'CL_UNKNOWN'},
                {'id': 11,  'rationale': 'NONSENSE'},
                {'id': 12,  'rationale': 'AE_UNKNOWN'}
            ])
    session.commit()
