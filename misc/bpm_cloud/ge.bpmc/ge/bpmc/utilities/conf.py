# -*- coding: utf-8 -*-


def check_configuration_keys(expected_keys, configuration):
    """
    Checks that expected configuration keys are present.

    Keyword arguments:
    expected_keys -- A dictionary. Keys are section and
    values are lists of options.
    configuration -- A configparser.ConfigParser instance
    """
    for section, options in expected_keys.items():
        if section not in configuration.sections():
            raise LookupError(
                'Missing section "%s" in configuration' % section)
        for opt in options:
            if not configuration.has_option(section, opt):
                msg = 'Missing option "%s", section "%s" in configuration file'
                raise LookupError(msg % (opt, section))
