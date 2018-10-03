# coding=utf-8
"""
Lib for ETL, function for processing and inserting data
"""
import json
import logging
import os
from enum import Enum
from time import time

from dateutil.parser import parse

from ge.ibis.entities.manager import IBISEntityManager
from ge.ibis.entities.workflow import ProcessingStatus

from .utilities import (aggregate_dict, aggregate_version, booleanify, dateify,
                        explode_as_dict, first_not_null, flatten_unformatted,
                        listify, substring, to_dvrs, value_or_null)

RULES_MAP = {
    'booleanify': booleanify,
    'dateify': dateify,
    'substring': substring,
    'replace_by': value_or_null,
    'listify': listify
}

AGGREGATION_RULES_MAP = {
    'agg_in_dict': aggregate_dict,
    'agg_version': aggregate_version,
    'first_not_null': first_not_null
}

ENTITY_SYNC_MAP = {
    'ApplicationEntity': 'sync_aes'
}

SUPPORTED_DEVICE_UPDATABLE_FIELDS = [
    'is_deleted', 'characteristics', 'alternate_name', 'last_update']


class ValidationResults(Enum):
    Validated = 'VALIDATED'
    DeviceAlreadyKnown = 'DEVICE ALREADY KNOWN'


class GIBSDataSynchronizer:

    def __init__(self, logger, data_retriever, entity_manager_factory,
                 session_factory, mapping_path=os.path.join(
            os.path.dirname(__file__), "mapping.json"),
            batch_size_commit_threshold=3000):
        """
        :data_retriever: a GIBSDataRetriever instance
        :entity_manager: a ge.ibis.entities.manager.IBISEntityManager instance
        :return:
        """
        self._logger = logger
        self._data_retriever = data_retriever
        self._em_factory = entity_manager_factory
        self._session_factory = session_factory
        self.mapping_path = mapping_path
        self.batch_size_commit_threshold = batch_size_commit_threshold
        self.load_mapping()

    def load_mapping(self):
        with open(self.mapping_path, 'r') as mapping_file:
            self.mapping = json.load(mapping_file)
            mapping_file.close()

    def apply_rules(self, rules, data):
        """
        Applies rules defined in the "rules" section of an entity in the
        mapping file. Will fail if the rules does not exist in the RULES_MAP.

        :rules: The dictionary containing the rules to apply
        :data: The DWIB item dict
        """
        for field, config in rules.items():
            kwargs = config.get('args') or {}
            data[field] = RULES_MAP.get(config['name'])(data.get(field, None),
                                                        **kwargs)

    def to_orm_representation(self, item_data, fields_mapping,
                              aggregation_rules):
        """
        Transform received MongoDB data to its expected ORM representation.

        :item_data: The actual item dict received from MongoDB
        :fields_mapping: The "fields" dictionary of an entity in the mapping
        file. Used to map the DWIB field to its expected ORM field.
        :aggregation_rules: The "aggregation_rules" dictionary of an entity
        in the mapping file. Used when some aggregation rules are
        necessary.
        """
        destination_fields = list(fields_mapping.values())
        uniq_destination_fields = set(destination_fields)
        formatted_dict = {}
        aggregations = [k for k, t in
                        [(x, destination_fields.count(x))
                         for x in uniq_destination_fields] if t > 1]
        for origin, destination in fields_mapping.items():
            if destination in aggregation_rules:
                rule_name = aggregation_rules.get(destination)
                rule = AGGREGATION_RULES_MAP.get(
                    rule_name, lambda x, y, z: z)
                formatted_dict[destination] = rule(
                    formatted_dict.get(destination, None),
                    origin, item_data.get(origin))
            else:
                formatted_dict[destination] = item_data.get(origin)
        return formatted_dict

    def get_mapped_data(self, entity_key, item_data):
        """
        Apply transformation rules to MongoDB item and returns its
        expected ORM representation.

        :entity_key: The mapping.json entity key used to load configuration
        :item_data: The actual item dict received from MongoDB
        """
        flat = flatten_unformatted(item_data)
        entity_mapping = self.mapping.get('entities').get(entity_key)
        fields_mapping = entity_mapping['fields']
        rules_mapping = entity_mapping.get('rules', {})
        aggregation_rules_mapping = entity_mapping.get('aggregation_rules', {})
        self.apply_rules(rules_mapping, flat)
        return self.to_orm_representation(
            flat, fields_mapping, aggregation_rules_mapping)

    def sync(self, import_method_name, syncing_method_name, *args,
             pre_sync_method=None, post_sync_method=None, **kwargs):
        """
        Syncs business items between MongoDB and IBIS.

        :import_method_name: A GIBSDataRetriever method providing data from
        MongoDB
        :syncing_method_name: A method of this class to call per import method
        yielded item
        :import_args: A list of arguments to pass to the import_method
        :pre_sync_method: Method to call before iterating on the import_method
        results
        :post_sync_method: Method to call after iterating on the import_method
        results
        :kwargs: Named params passed to syncing_method
        """
        import_method = getattr(self._data_retriever, import_method_name)
        syncing_method = getattr(self, syncing_method_name)

        data = import_method(*args)
        start = time()
        counter = 0

        with self._session_factory() as session:
            em = self._em_factory.update_session(session)
            if pre_sync_method and data:
                pre_sync_method(em, session)

            for input_data in data:
                counter += 1
                if counter == self.batch_size_commit_threshold:
                    session.commit()
                    counter = 0
                    self._logger.info('Commiting...')
                try:
                    syncing_method(input_data, em, session, **kwargs)
                except Exception as e:
                    self._logger.warn(
                        'An error occured during execution of %s: %s' % (
                            syncing_method.__name__, str(e)))

            if post_sync_method and data:
                post_sync_method(em, session)

        end = time()
        self._logger.warn('Done sync in %.02f seconds' % (end-start))

    ###########################################
    # Business items sync implementation
    ###########################################

    def sync_aes(self, last_pull_date):
        """
        Syncs Application Entities between MongoDB and target db
        :last_pull_date: A string containing the last pull date acting as a
        starting point for synchronization
        """
        self.sync('import_aes', 'sync_ae', last_pull_date)

    def sync_customers(self, last_pull_date):
        """
        Syncs Customers between MongoDB and target db
        :last_pull_date: A string containing the last pull date acting as a
        starting point for synchronization
        """
        self.sync('import_customers', 'sync_customer', last_pull_date)

    def sync_connectivity_lists(self):
        """
        Syncs Connectivity lists between MongoDB and target db
        """
        devices = {str(d['_id']): d for d
                   in self._data_retriever.import_devices()}
        kwargs = {'devices': devices}
        self.sync(
            'import_integration_revisions', 'sync_connectivity_list',
            pre_sync_method=self.pre_sync_connectivity_list,
            post_sync_method=self.post_sync_connectivity_list,
            **kwargs)

    def pre_sync_connectivity_list(self, em, session):
        em.truncate_connectivity_pattern()
        em.truncate_connectivity_functionality()
        em.truncate_connectivity_list()

    def post_sync_connectivity_list(self, em, session):
        session.execute("CALL update_im_mt()")
        self._logger.warn('Calling stored proc "update_im_mt"')

    def sync_supported_devices(self):
        """
        Syncs Supported Devices between MongoDB and target db
        """
        self.sync('import_devices', 'sync_supported_device')

    def sync_studies(self, serial_number, last_pull_date):
        """
        Syncs Studies between MongoDB and target db
        :serial_number: The serial number of the customer
        :last_pull_date: A string containing the last pull date acting as a
        starting point for synchronization
        """
        kwargs = {'serial_number': serial_number}
        self.sync('import_studies', 'sync_study',
                  serial_number, last_pull_date, **kwargs)

    def sync_ct_logs(self, serial_number, last_pull_date):
        """
        Syncs CTLogs between MongoDB and target db
        :serial_number: The serial number of the customer
        :last_pull_date: A string containing the last pull date acting as a
        starting point for synchronization
        """
        kwargs = {'serial_number': serial_number}
        self.sync('import_ct_logs', 'sync_ct_log',
                  serial_number, last_pull_date, **kwargs)

    def sync_innova_logs(self, serial_number, last_pull_date):
        """
        Syncs InnovaLogs between MongoDB and target db
        :serial_number: The serial number of the customer
        :last_pull_date: A string containing the last pull date acting as a
        starting point for synchronization
        """
        kwargs = {'serial_number': serial_number}
        self.sync('import_innova_logs', 'sync_innova_log',
                  serial_number, last_pull_date, **kwargs)

    def sync_dicom_patterns(self, serial_number, last_pull_date):
        """
        Syncs Dicom patterns between MongoDB and target db
        :serial_number: The serial number of the customer
        :last_pull_date: A string containing the last pull date acting as a
        starting point for synchronization
        """
        pattern_key = 'data.resultRows.pattern'
        kwargs = {'serial_number': serial_number,
                  'p_keys': ['%s.%s' % (pattern_key, x) for x in range(0, 7)]}
        self.sync('import_dicom_patterns', 'sync_dicom_pattern',
                  serial_number, last_pull_date, **kwargs)

    def sync_translator_configurations(self):
        """
        Syncs TranslatorConfiguration lists between MongoDB and target db
        """
        devices = {str(d['_id']): d for d
                   in self._data_retriever.import_devices()}
        kwargs = {'devices': devices}
        self.sync(
            'import_translator_configuration', 'sync_translator_configuration',
            pre_sync_method=self.pre_sync_translator_configurations,
            **kwargs)

    def pre_sync_translator_configurations(self, em, session):
        em.truncate_translator_config_device_version_requirement()
        em.truncate_translator_config()

    ###################################
    # Single item sync methods
    ###################################

    def sync_ae(self, input_data, em, session):
        """
        Syncing method of an Application Entity item.

        :input_data: DWIB dictionary of a single item
        :em: a ge.ibis.entities.manager.EntityManager.IBISEntityManager
        instance with an active session
        :session: a scoped_session instance
        """
        # Stop policies

        if 'sdmKey' not in input_data:
            return None

        # Get mapped data for AE

        ae = self.get_mapped_data('AE', input_data)
        ae['is_last'] = True
        local_ae_id = ae['local_ae_id']
        serial_number = ae['serial_number']
        relationship_updates = False

        # Checks if FTP connection is active

        ftp_connection = None
        if ae['ftp_connection_type'] is not None:
            if (('ftpCtConnection' in input_data) or
                    ('ftpInnovaConnection' in input_data)):
                ftpcon = self.get_mapped_data('FTPCon', input_data)
                hashed = em.hash_ftp_connection(ftpcon)
                existing_ftp_con = em.get_ftp_connection(
                    ('hash', hashed), keep_context=True)
                ftp_connection = existing_ftp_con
                if not existing_ftp_con:
                    relationship_updates = True
                    ftpcon['hash'] = hashed
                    ftp_connection = (
                        em.add_ftp_connection(
                            ftpcon, keep_context=True))
                ae['ftp_connection'] = [ftp_connection]

        # Check if integration modes are set

        integration_modes = []
        if 'modalityIntegrationMode' in input_data:
            for item in input_data['modalityIntegrationMode']:
                im = self.get_mapped_data('IntegrationMode', item)
                ignore_item = not (
                    ('integrationRequestIssue' not in item) or
                    (
                        item['integrationRequestIssue'][-1].get(
                            'validationResult')
                        in [ValidationResults.Validated.value,
                            ValidationResults.DeviceAlreadyKnown.value]
                    ))
                if not ignore_item:
                    existing_im = em.get_im_by_attrs(
                        im['integration_mode'], im['modality'])
                    if not existing_im:
                        relationship_updates = True
                        integration_mode = em.add_integration_mode(
                            im, keep_context=True)
                    else:
                        integration_mode = existing_im
                    integration_modes.append(integration_mode)
        if integration_modes:
            ae['integration_mode'] = integration_modes

        # Searches the latest revision of the AE

        last_ae = em.get_last_application_entity_by_attrs(local_ae_id,
                                                          serial_number)

        # If no previous AE revision exists

        if not last_ae:
            em.add_application_entity(ae)
        else:
            new_hash = em.hash_application_entity(ae)
            if relationship_updates or (last_ae._hash() != new_hash):
                em.upd_application_entity(
                    ('id', last_ae.id), values={'is_last': None})
                em.add_application_entity(ae)

    def sync_customer(self, input_data, em, session):
        """
        Syncing method of a Customer item.

        :input_data: DWIB dictionary of a single item
        :em: a ge.ibis.entities.manager.EntityManager.IBISEntityManager
        instance with an active session
        :session: a scoped_session instance
        """
        cust = self.get_mapped_data('Customer', input_data)
        cust['is_last'] = True
        serial_number = cust['serial_number']
        revision_number = cust['revision_number']

        revision_exists = em.get_customer_by_attrs(serial_number,
                                                   revision_number)

        # Stop policies

        if revision_exists:
            return

        # Checks if custom dictionnaries are set

        custom_dictionaries = []
        if 'customDictionaries' in input_data:
            for item in input_data['customDictionaries']:
                cd = self.get_mapped_data('CustomDictionary', item)
                existing_cd = em.get_custom_dictionary_by_attrs(
                    cd['local_id'], cd['code'], cd['description'])
                custom_dict = (existing_cd if existing_cd else
                               em.add_custom_dictionary(cd, keep_context=True))
                custom_dictionaries.append(custom_dict)
        if custom_dictionaries:
            cust['custom_dictionaries'] = custom_dictionaries

        # Checks if workarounds are set

        workarounds = []
        if 'workArounds' in input_data:
            for name in input_data['workArounds']:
                wa = {'name': name}
                existing_wa = em.get_workaround(
                    ('name', name), keep_context=True)
                workaround = (existing_wa if existing_wa else
                              em.add_workaround(wa, keep_context=True))
                workarounds.append(workaround)
        if workarounds:
            cust['workarounds'] = workarounds

        last_customer = em.get_last_customer_by_serial(serial_number)

        if last_customer:
            # If new customer revision, gets the last customer is_monitored
            # flag and unmark last customer entry as the latest in the database
            if float(last_customer.revision_number) < float(revision_number):
                cust['is_monitored'] = last_customer.is_monitored
                em.upd_customer(
                    ('id', last_customer.id), values={'is_last': None})
            # Gets the previous customer revision if available to check
            # if the customer should be monitored
            else:
                prev = em.get_previous_customer_revision_by_serial(
                    serial_number, revision_number)
                if prev:
                    cust['is_monitored'] = prev.is_monitored

        em.add_customer(cust)

    def sync_connectivity_list(self, input_data, em, session, devices={}):
        """
        Syncing method of a Connectivity list item.

        :input_data: DWIB dictionary of a single item
        :em: a ge.ibis.entities.manager.EntityManager.IBISEntityManager
        instance with an active session
        :session: a scoped_session instance
        :devices: dict of devices with id as key
        """
        device = devices.get(str(input_data['device'].id), {})
        sdm_key = device['sdmKey']
        integration_mode = input_data['integrationMode']
        modality = input_data['modality']
        cl = self.get_mapped_data('ConnectivityList', input_data)

        # Stop policies

        if not device or (not isinstance(sdm_key, int)) or sdm_key == 0:
            return

        # Prevents fails if supported device is not synced
        if not em.get_supported_device(('id', sdm_key)):
            return

        # Setting supported device

        cl['supported_device_id'] = sdm_key

        # Checks if integration mode is set

        im = em.get_im_by_attrs(integration_mode, modality)
        if not im:
            data = self.get_mapped_data('IntegrationMode', input_data)
            im = em.add_integration_mode(
                data, keep_context=True)

        cl['integration_mode_id'] = im.id

        # Checks if expected files are set and extract message patterns

        message_patterns = []
        if 'expectedFiles' in input_data:
            for pattern in input_data['expectedFiles']:
                existing_mp = em.get_message_pattern(
                    ('message_type', pattern), keep_context=True)
                message_pattern = (existing_mp if existing_mp else
                                   em.add_message_pattern(
                                       {'message_type': pattern},
                                       keep_context=True))
                message_patterns.append(message_pattern)
            if message_patterns:
                cl['messages_pattern'] = message_patterns

        # Checks if functionalities are set

        functionalities = []
        if 'functionalities' in input_data:
            for feat in input_data['functionalities']:
                existing_dwf = em.get_dw_functionality(
                    ('functionality', feat), keep_context=True)
                dw_functionality = (existing_dwf if existing_dwf else
                                    em.add_dw_functionality(
                                        {'functionality': feat},
                                        keep_context=True))
                functionalities.append(dw_functionality)
        if functionalities:
            cl['functionalities'] = list(set(functionalities))

        em.add_connectivity_list(cl)

    def sync_supported_device(self, input_data, em, session):
        """
        Syncing method of a Supported Device item.

        :input_data: DWIB dictionary of a single item
        :em: a ge.ibis.entities.manager.EntityManager.IBISEntityManager
        instance with an active session
        :session: a scoped_session instance
        """
        device = self.get_mapped_data('Device', input_data)
        sdm_key = device['id']
        existing_device = em.get_supported_device(
            ('id', sdm_key))

        # Update existing entry if exists or create new entry

        if existing_device:
            updates = {k: getattr(existing_device, k)
                       for k in SUPPORTED_DEVICE_UPDATABLE_FIELDS}
            em.upd_supported_device(('id', sdm_key), values=updates)
        else:
            em.add_supported_device(device)

    def sync_study(self, input_data, em, session, serial_number='0'):
        """
        Syncing method of a Study item.

        :input_data: DWIB dictionary of a single item
        :em: a ge.ibis.entities.manager.EntityManager.IBISEntityManager
        instance with an active session
        :session: a scoped_session instance
        """
        study = self.get_mapped_data('Study', input_data)
        encrypted_siuid = study['encrypted_siuid']
        existing_study = em.get_study_by_attrs(
            serial_number, encrypted_siuid)

        # Update existing entry if exists or create new entry

        if existing_study:
            study['status'] = ProcessingStatus.NEW.value
            em.del_study_related_dosimetric(
                existing_study.id)
            em.upd_study(('id', existing_study.id), values=study)
        else:
            em.add_study(study)
        em.upd_customer_monitor_flag(serial_number, True)

    def sync_ct_log(self, input_data, em, session, serial_number='0'):
        """
        Syncing method of a CTLog item.

        :input_data: DWIB dictionary of a single item
        :em: a ge.ibis.entities.manager.EntityManager.IBISEntityManager
        instance with an active session
        :session: a scoped_session instance
        """
        ctlog = self.get_mapped_data('CTLog', input_data)
        em.add_ct_log_pattern(ctlog)
        em.upd_customer_monitor_flag(serial_number, True)

    def sync_innova_log(self, input_data, em, session, serial_number='0'):
        """
        Syncing method of a InnovaLog item.

        :input_data: DWIB dictionary of a single item
        :em: a ge.ibis.entities.manager.EntityManager.IBISEntityManager
        instance with an active session
        :session: a scoped_session instance
        """
        innovalog = self.get_mapped_data('InnovaLog', input_data)
        aet = innovalog['aet']
        existing_ilog = em.get_innovalogpull_by_attrs(serial_number, aet)

        # Update existing entry if exists or create new entry

        if existing_ilog and (
                existing_ilog.measure_date < innovalog['measure_date']):
            innovalog['datetime_first_fails'] = None
            innovalog['datetime_last_fails'] = None
            innovalog['status'] = ProcessingStatus.NEW.value
            em.upd_innova_log_pull(('id', existing_ilog.id), values=innovalog)
        else:
            em.add_innova_log_pull(innovalog)
        em.upd_customer_monitor_flag(serial_number, True)

    def sync_dicom_pattern(self, input_data, em, session, serial_number='0',
                           p_keys=[]):
        """
        Syncing method of a Dicom pattern.

        :input_data: DWIB dictionary of a single item
        :em: a ge.ibis.entities.manager.EntityManager.IBISEntityManager
        instance with an active session
        :session: a scoped_session instance
        """
        dicom_input = self.get_mapped_data('DicomInput', input_data)
        patterns = dicom_input.pop('raw_patterns', [])

        dicom_input_obj = em.add_dicom_input(
            dicom_input, keep_context=True)
        dicom_input['dicom_patterns'] = []
        base_pattern = {k: v for k, v in
                        self.get_mapped_data(
                            'DicomPattern', input_data).items()
                        if v is not None}

        for pattern_data in patterns:

            # Generate actual pattern object
            raw_pattern = explode_as_dict(pattern_data, '_', p_keys)
            pattern = self.get_mapped_data('DicomPattern', raw_pattern)
            pattern.update(base_pattern)
            hashed = em.hash_dicom_pattern(pattern)
            pattern['hash'] = hashed

            # Check if pattern exists, if not creates it

            pattern_obj = (
                em.get_dicom_pattern(('hash', hashed), keep_context=True) or
                em.add_dicom_pattern(pattern, keep_context=True))

            # Create linked DicomInputPattern

            input_pattern = self.get_mapped_data(
                'DicomInputPattern', raw_pattern)
            input_pattern['dicom_pattern'] = [pattern_obj]
            input_pattern['dicom_input'] = [dicom_input_obj]
            dicom_input['dicom_patterns'].append(
                em.add_dicom_input_pattern(input_pattern, keep_context=True))

        # Update the parent Dicom input with its associated patterns

        em.upd_dicom_input(('id', dicom_input_obj.id), values=dicom_input)

        last_customer = em.get_last_customer_by_serial(serial_number)
        if last_customer:
            em.upd_customer(
                ('id', last_customer.id), values={'is_monitored': True})

    def sync_translator_configuration(self, input_data, em, session,
                                      devices={}):
        """
        Syncing method of a Translator config.

        :input_data: DWIB dictionary of a single item
        :em: a ge.ibis.entities.manager.EntityManager.IBISEntityManager
        instance with an active session
        :session: a scoped_session instance
        :devices: a list of device ids (str)
        """

        # Select device

        device_id = str(input_data['device'].id)
        device = devices[device_id] if device_id in devices else {}

        # Stop policies

        if (('sdmKey' not in device) or (device['sdmKey'] == 0) or not
                em.get_supported_device(
                    ('id', device['sdmKey']))):
            return

        # Extract Translator config & Device Version Requirements

        t_conf = self.get_mapped_data('TranslatorConfig', input_data)
        t_conf['sdm_key'] = device['sdmKey']

        device_v_reqs = []
        for dvr in to_dvrs(input_data['deviceVersionRequirements']):
            device_v_reqs.append(
                em.get_dvr_by_values(
                    dvr['rule'], dvr['value'], dvr['relation']) or
                em.add_device_version_requirement(dvr, keep_context=True))

        t_conf['device_version_requirement'] = device_v_reqs

        em.add_translator_config(t_conf)
