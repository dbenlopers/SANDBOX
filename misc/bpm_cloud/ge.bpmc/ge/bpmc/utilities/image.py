# -*- coding: utf-8 -*-

import pickle
from io import BytesIO


def file_content_to_bpm_representation(buffer):
    """
    Generate a list of bytes lists (one list per line) from a BytesIO buffer

    :buffer: a BytesIO instance
    """
    return pickle.loads(buffer.getvalue())


def bpm_representation_to_buffer(img_bytes_array):
    """
    Generate a BytesIO instance from a list of bytes lists

    :img_bytes_array: a list of bytes lists, eg: [[241, 214, ...]]
    """
    return BytesIO(pickle.dumps(img_bytes_array))
