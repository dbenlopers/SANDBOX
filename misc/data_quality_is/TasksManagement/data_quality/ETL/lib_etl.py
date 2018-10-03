# coding=utf-8
"""
Lib for ETL, function for processing and inserting data
"""
from data_quality.persistence.orm import ApplicationEntity, FTPconnection, IntegrationMode, Study, Customer, \
    CustomeDictionary, WorkAround, ConnectivityList, MessagePattern, DWFunctionality, CTLogPattern, DicomInput, \
    DicomInputPattern, InnovaLogPull, TranslatorConfig, SupportedDevice, DeviceVersionRequirement, DicomPattern, \
    Dosimetric
from data_quality.ETL.utilities import insert_object, update_object, flattenDict, flattenDict_alt, \
    fill_object, parse_deviceversionrequirement, _check_customer, _check_customdictionary, \
    _check_im, _check_ftpco, _check_pattern, _check_innovalog
from dateutil.parser import parse


def insert_ae(db_session, input_data, mapping):
    """
    insert application entity (only with sdm_key and serial_number filled
    :param db_session:
    :param input_data:
    :param mapping:
    :return:
    """
    if 'sdmKey' not in input_data.keys():
        return None
    data = flattenDict(input_data)

    # construct current ae object with input data
    new_ae = fill_object(ApplicationEntity(), data, mapping['AE'])
    new_ae.is_last = True

    # search for the same ae with sn, sdmkey and last_updated
    last_ae = db_session.query(ApplicationEntity).filter(ApplicationEntity.local_ae_id == new_ae.local_ae_id,
                                                         ApplicationEntity.serial_number == new_ae.serial_number,
                                                         ApplicationEntity.is_last == True)

    # if ftpconnection is effective
    ftpco = []
    if new_ae.ftp_connection_type is not None:
        if "ftpCtConnection" in input_data.keys() or "ftpInnovaConnection" in input_data.keys():
            ftpconnection = fill_object(FTPconnection(), data, mapping['FTPCon'])
            ftpconnection.hash = ftpconnection._hash()
            _ftpcon_in_base = _check_ftpco(db_session, ftpconnection)
            ftpco.append(ftpconnection if _ftpcon_in_base.count() == 0 else _ftpcon_in_base.first())

    intemode = []
    # if integration mode is defined (only VALIDATED* or DEVICE ALREADY KNOW are insert)
    if 'modalityIntegrationMode' in input_data.keys():
        for item in input_data['modalityIntegrationMode']:
            if "integrationRequestIssue" in item.keys():
                if item['integrationRequestIssue'][-1]['validationResult'].startswith('VALIDATED') or \
                        item['integrationRequestIssue'][-1]['validationResult'] == 'DEVICE ALREADY KNOWN':
                    integrationmode = fill_object(IntegrationMode(), flattenDict(item), mapping['IntegrationMode'])
                    _req_im = _check_im(db_session, integrationmode)

                    intemode.append(integrationmode if _req_im.count() == 0 else _req_im.first())
            else:
                integrationmode = fill_object(IntegrationMode(), flattenDict(item), mapping['IntegrationMode'])
                _req_im = _check_im(db_session, integrationmode)

                intemode.append(integrationmode if _req_im.count() == 0 else _req_im.first())

    # in case of not first revision
    if last_ae.count() == 0:
        new_ae.ftp_connection.extend(ftpco)
        new_ae.integration_mode.extend(intemode)
        insert_object(db_session, new_ae)
    else:
        # check if strictly equality, else insert it
        _changed = False

        # test if hash of ae are different, if yes change tag to True
        if new_ae._hash() != last_ae.first()._hash():
            _changed = True

        # test when ftp con are not null, if they are same
        if len(ftpco) != 0 and len(last_ae.first().ftp_connection) != 0:
            if ftpco[0].hash != last_ae.first().ftp_connection[0].hash:
                _changed = True

        # if one ae have ftp con and not other, tag
        if len(ftpco) != len(last_ae.first().ftp_connection):
            _changed = True

        # test if integration mode is same
        if str(sorted([elem.integration_mode for elem in intemode])) != str(
                sorted([elem.integration_mode for elem in last_ae.first().integration_mode])):
            _changed = True

        # if we have detected change on ae (by testing tag), we add relationship now and insert it
        if _changed:
            last_ae.first().is_last = False
            new_ae.ftp_connection.extend(ftpco)
            new_ae.integration_mode.extend(intemode)
            insert_object(db_session, new_ae)


def insert_customer(db_session, input_data, mapping):
    """
    Insert customer revision, with custom dict & ....
    :param db_session:
    :param input_data:
    :param mapping:
    :return:
    """
    new_customer = fill_object(Customer(), flattenDict(input_data), mapping['Customer'])
    new_customer.is_last = False
    # seach for a custome with same rev number
    cust_q = _check_customer(db_session, new_customer)

    # Only insert this customer revision if he doesn't exist
    if cust_q.count() == 0:

        # Add custom dictionary if one is present into data
        if 'customDictionaries' in input_data.keys():
            for item in input_data['customDictionaries']:
                cust_dict = fill_object(CustomeDictionary(), flattenDict(item), mapping['CustomeDictionary'])
                custdict_q = _check_customdictionary(db_session, cust_dict)

                new_customer.custome_dictionarys.append(cust_dict if custdict_q.count() == 0 else custdict_q.first())

        # Add workaround if one is present into data
        if 'workArounds' in input_data.keys():
            for name in input_data['workArounds']:
                wa = WorkAround()
                setattr(wa, "name", name)
                wa_q = db_session.query(WorkAround).filter(WorkAround.name == name)

                new_customer.workarounds.append(wa if wa_q.count() == 0 else wa_q.first())

        last_customer = db_session.query(Customer).filter(Customer.serial_number == new_customer.serial_number,
                                                          Customer.is_last == True)
        if last_customer.count() == 0:
            new_customer.is_last = True
        else:
            # if revision number from last customer is below new one, set is_last to true to new one and
            # false to previous
            if float(last_customer.first().revision_number) < float(new_customer.revision_number):
                last_customer.first().is_last = False
                new_customer.is_last = True
                new_customer.is_monitored = last_customer.first().is_monitored
            else:
                # if the new customer rev num is not the last, search the revnum-1 the new one and take
                # the is_monitored status flag
                previous_customer = db_session.query(Customer).filter(Customer.serial_number ==
                                                                      new_customer.serial_number,
                                                                      Customer.revision_number == (
                                                                              new_customer.revision_number - 1))
                if previous_customer.count() != 0: new_customer.is_monitored = previous_customer.first().is_monitored

        insert_object(db_session, new_customer)


def insert_connectivitylist(db_session, input_data, mapping, device_data):
    """
    Insert data into connectivity list
    :param db_session:
    :param input_data:
    :param mapping:
    :param device_data:
    :return:
    """
    connectivitylist = fill_object(ConnectivityList(), flattenDict(input_data), mapping['connectivityList'])

    if not isinstance(device_data['sdmKey'], int):
        return

    if device_data['sdmKey'] == 0:
        return
    setattr(connectivitylist, 'supported_device_id', device_data['sdmKey'])

    # Check integration mode if exists, if not insert it
    im = input_data['integrationMode']
    mod = input_data['modality']
    im_q = db_session.query(IntegrationMode).filter(IntegrationMode.integration_mode == im,
                                                    IntegrationMode.modality == mod)

    if im_q.count() == 0:
        new_integrationmode = fill_object(IntegrationMode(), input_data, mapping['IntegrationMode'])
        insert_object(db_session, new_integrationmode)
        integrationmode_id = new_integrationmode.id
    else:
        integrationmode_id = im_q.first().id

    setattr(connectivitylist, 'integration_mode_id', integrationmode_id)

    if 'expectedFiles' in input_data.keys():
        for pattern in input_data['expectedFiles']:
            messagepattern = MessagePattern()
            messagepattern.message_type = pattern
            q = db_session.query(MessagePattern).filter(MessagePattern.message_type == messagepattern.message_type)

            connectivitylist.messages_pattern.append(messagepattern if q.count() == 0 else q.first())

    if 'functionalities' in input_data.keys():
        for func in input_data['functionalities']:
            functionality = DWFunctionality()
            functionality.functionality = func
            q = db_session.query(DWFunctionality).filter(DWFunctionality.functionality == functionality.functionality)

            connectivitylist.functionalities.append(functionality if q.count() == 0 else q.first())

    insert_object(db_session, connectivitylist)


def upsert_device(db_session, input_data, mapping):
    """
    update or insert device
    :param db_session:
    :param input_data:
    :param mapping:
    :return:
    """
    device = fill_object(SupportedDevice(), flattenDict(input_data), mapping['device'])

    try:
        if not isinstance(int(device.id), int):
            return
    except:
        return

    # sdm key can be equal to 0 for temporary device that are not yet integrate
    if device.id == 0:
        return

    if device.id is not None:
        q = db_session.query(SupportedDevice).filter(SupportedDevice.id == int(device.id))

        if q.count() != 0:
            for att in ['is_deleted', 'characteristics', 'alternate_name', 'last_update']:
                if getattr(q.first(), att) is None and getattr(device, att) is not None:
                    setattr(q.first(), att, getattr(device, att))
        else:
            db_session.add(device)
        db_session.flush()


def insert_consolidation(db_session, input_data, mapping):
    """
    Insert consolidation data
    :param db_session:
    :param input_data:
    :param mapping:
    :return:
    """
    consolidation = fill_object(Study(), flattenDict(input_data), mapping['Consolidation'])
    db_session.add(consolidation)


def construct_consolidation(input_data, mapping):
    """
    construct an consolidation object
    :param input_data: json data
    :param mapping: mapping dict
    :return: an consolidation orm object
    """
    return fill_object(Study(), flattenDict(input_data), mapping['Consolidation'])


def upsert_consolidation(db_session, input_data, mapping):
    """
    Insert or update new consolidation data, delete dosimetric test associated to old study
    :param db_session:
    :param input_data:
    :param mapping:
    :return:
    """
    # Create new object that represent a consolidation/study/dosi_data
    _flattened_data = flattenDict(input_data)

    new_data = fill_object(Study(), _flattened_data, mapping['Consolidation'])

    # Check if probe are in incremental ways, if not
    if 'data.resultRows.dt_last_update' not in _flattened_data:
        db_session.bulk_save_objects([new_data])
        return

    # check if dt_created has more than 1 day of diff with dt_last_update, if so, we enter into update mode, else
    # data are inserted without other processing
    if (parse(_flattened_data['data.resultRows.dt_last_update']).date() - new_data.start_date.date()).days > 0:

        _old_data = db_session.query(Study).filter(Study.serial_number == new_data.serial_number,
                                                   Study.encrypted_siuid == new_data.encrypted_siuid)

        # If found previous data, we update them & remove old processing data
        if _old_data.count() != 0:
            # delete old data from resulting test
            db_session.query(Dosimetric).filter(Dosimetric.study_id == _old_data.first().id). \
                delete(synchronize_session=False)
            # update study entry
            values_for_update = new_data.tojson()
            if 'id' in values_for_update: del values_for_update['id']  # remove id who is null
            values_for_update['status'] = 'N'  # set study to N because is Null in newly create object
            _old_data.update(values=values_for_update, synchronize_session=False)
        else:
            # insert the new one
            db_session.bulk_save_objects([new_data])
    else:
        # insert new consolidation
        db_session.bulk_save_objects([new_data])


def insert_ctlog(db_session, input_data, mapping):
    """
    Insert ct log data
    :param db_session: sqlalchemy session
    :param input_data: data in dict format
    :param mapping: mapping in dict for flatten data
    :return:
    """
    ctlogpattern = fill_object(CTLogPattern(), flattenDict(input_data), mapping['CTlog'])
    db_session.add(ctlogpattern)


def construct_ctlog(input_data, mapping):
    """
    construct an ctlog object
    :param input_data: json data
    :param mapping: mapping dict
    :return: an ctlog orm object
    """
    return fill_object(CTLogPattern(), flattenDict(input_data), mapping['CTlog'])


def insert_dicominput(db_session, input_data, mapping):
    """
    Insert dicom input pattern
    :param db_session:
    :param input_data:
    :param mapping:
    :return:
    """
    data = flattenDict(input_data)
    DICOMINPUT = fill_object(DicomInput(), data, mapping['Dicominput'])

    _pattern_key = 'data.resultRows.pattern'
    for pattern in data[_pattern_key].split(','):
        _pattern = {_pattern_key + "." + str(i): elem for (i, elem) in enumerate(pattern.split('_'))}

        if len(_pattern) != 7:
            return

        dicompattern_tmp = fill_object(DicomPattern(), data, mapping["Dicompattern"])
        DICOMPATTERN = fill_object(dicompattern_tmp, _pattern, mapping["Dicompattern"])
        # DICOMPATTERN = fill_object(DicomPattern(), _pattern, mapping["Dicompattern"])
        DICOMPATTERN.hash = DICOMPATTERN._hash()

        dp_q = _check_pattern(db_session, DICOMPATTERN)

        DICOMINPUTPATTERN = fill_object(DicomInputPattern(), _pattern, mapping['Dicominputpattern'])
        if dp_q.count() == 0:
            insert_object(db_session, DICOMPATTERN)
            DICOMINPUTPATTERN.dicompattern = DICOMPATTERN
        else:
            DICOMINPUTPATTERN.dicompattern = dp_q.first()
        DICOMINPUT.dicom_patterns.append(DICOMINPUTPATTERN)

    db_session.add(DICOMINPUT)


def upsert_innovalog(db_session, input_data, mapping):
    """
    Insert innovalog data
    :param db_session: sqlalchemy session
    :param input_data: data in dict format (comming from pymongo
    :param mapping: dict that contain mapping for flatten dict
    :return:
    """
    innovalog = fill_object(InnovaLogPull(), flattenDict(input_data), mapping['Innovalog'])
    _already_in_base = _check_innovalog(db_session, innovalog)

    if not _already_in_base.count() > 0:  # if not inserted previously
        db_session.add(innovalog)
    elif _already_in_base.first().measure_date < innovalog.measure_date:  # update entry
        _already_in_base.first().datetime_first_fail = None
        _already_in_base.first().datetime_last_fail = None
        _already_in_base.first().status = 'N'
        update_object(db_session, _already_in_base.first(), innovalog.__dict__.copy(),
                      exclude=['id', '_sa_instance_state'])


def insert_translatorconfig(db_session, input_data, mapping, device_data):
    """
    Insert or update translator config
    :param db_session:
    :param input_data:
    :param mapping:
    :param device_data:
    :return:
    """
    data = flattenDict_alt(input_data)
    translator = fill_object(TranslatorConfig(), data, mapping['TranslatorConfig'])

    if device_data['sdmKey'] == 0:
        return

    if db_session.query(SupportedDevice).filter(SupportedDevice.id == device_data['sdmKey']).count() == 0:
        return

    setattr(translator, 'sdm_key', device_data['sdmKey'])

    try:
        to_set = parse_deviceversionrequirement(input_data['deviceVersionRequirements'])
        for dvr in to_set:
            device_version = DeviceVersionRequirement()
            for key, value in dvr.items():
                setattr(device_version, key, value)

            q = db_session.query(DeviceVersionRequirement).filter(DeviceVersionRequirement.rule == device_version.rule,
                                                                  DeviceVersionRequirement.value == device_version.value,
                                                                  DeviceVersionRequirement.relation == device_version.relation)
            translator.device_version_requirement.append(device_version if q.count() == 0 else q.first())

    except Exception as e:
        print(e)

    db_session.add(translator)
    db_session.flush()
