PROCESSING_ROUTES = {
    'ge.bpmc.tasks.processing.*': {'queue': 'processing'}
}

MATCHING_ROUTES = {
    'ge.bpmc.tasks.matching.*': {'queue': 'matching'}
}

SCHEDULED_ROUTES = {
    'ge.bpmc.tasks.periodic.*': {'queue': 'periodic'}
}

ROUTES = {}
ROUTES.update(PROCESSING_ROUTES)
ROUTES.update(MATCHING_ROUTES)
ROUTES.update(SCHEDULED_ROUTES)
