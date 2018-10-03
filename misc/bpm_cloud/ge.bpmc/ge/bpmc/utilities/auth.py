# -*- coding: utf-8 -*-


from ge.bpmc.app.injection import Core


def validate_role_token(token):
    return token == Core.config.tokens.role()


def validate_component_token(token):
    return token == Core.config.tokens.component()
