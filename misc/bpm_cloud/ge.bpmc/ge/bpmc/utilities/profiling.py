# -*- coding: utf-8 -*-

import json
from datetime import datetime
from time import time

from ge.bpmc.app.injection import Core
from ge.bpmc.utilities.logging import ge_format_time


def profile(fname):
    def func_decorator(func):
        def func_wrapper(*args, **kwargs):
            logger = Core.profiler()
            start = time()
            result = func(*args, **kwargs)
            end = time()
            data = {}
            data['timestamp'] = ge_format_time(datetime.now())
            data['func'] = fname
            data['duration_seconds'] = float('%0.4f' % (end - start))
            logger.info(json.dumps(data))
            return result
        return func_wrapper
    return func_decorator


def reflect(item):
    parts = item.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


class Profiler:

    @classmethod
    def wrap_tasks(cls, module, tasks):
        mod = reflect(module)
        for name in tasks:
            task = getattr(mod, name)
            fname = module + '.' + name
            wrapped = profile(fname)(getattr(task, 'run'))
            setattr(task, 'run', wrapped)

    @classmethod
    def wrap_class(cls, dotted_name, methods):
        class_ = reflect(dotted_name)
        for m in methods:
            fname = dotted_name + '.' + m
            wrapped = profile(fname)(getattr(class_, m))
            setattr(class_, m, wrapped)


def setup_task_profiling():
    Profiler.wrap_tasks('ge.bpmc.tasks.processing', ['process_image'])
    Profiler.wrap_tasks('ge.bpmc.tasks.periodic',
                        ['manage_processed_procedures'])
    Profiler.wrap_tasks('ge.bpmc.tasks.matching', ['match_procedure_images'])


def setup_resource_profiling():
    Profiler.wrap_class('ge.bpmc.services.storage.StorageService', [
        'query_image', 'query_metrics_image', 'store_image',
        'store_metrics_image'])
    Profiler.wrap_class('ge.bpmc.services.workflow.WorkflowService', [
        'get_image_result', 'get_procedure_result', 'get_exam_result'])
