class CeleryConfig(object):
    BROKER_URL = 'redis://$APP_BROKER_HOST:$APP_BROKER_PORT/0'
    CELERY_IMPORTS = ('superset.sql_lab', )
    CELERY_RESULT_BACKEND = 'redis://$APP_BROKER_HOST:$APP_BROKER_PORT/0'
    CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}

CELERY_CONFIG = CeleryConfig

from werkzeug.contrib.cache import RedisCache
RESULTS_BACKEND = RedisCache(
    host='$APP_BROKER_HOST', port=$APP_BROKER_PORT, key_prefix='superset_results')

