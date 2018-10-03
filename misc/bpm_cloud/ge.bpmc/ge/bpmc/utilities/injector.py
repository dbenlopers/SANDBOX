# -*- coding: utf-8 -*-

from ge.bpmc.app.injection import Core


def set_configuration(data):
    Core.config.override(data)
    instanciate_configuration(Core.config, data)


def instanciate_configuration(ref, tree):
    # Calls the binding to ensure data is properly set
    for key in tree:
        val = tree[key]
        if isinstance(val, dict):
            instanciate_configuration(getattr(ref, key), val)
        else:
            getattr(ref, key)()
