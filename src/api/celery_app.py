from celery import Celery
from os import environ
from degree_planner.dp.recommend import recommend
from degree_planner.dp.fulfill import get_optimized_fulfillment, get_group_fulfillment

celery_broker = 'redis://redis:6379/0'
celery_backend = 'redis://redis:6379/1'
celery_app = Celery("celery_app", broker=celery_broker, backend=celery_backend)

celery_app.conf.update(
    task_serializer=environ.get('CELERY_TASK_SERIALIZER', 'pickle'),
    result_serializer=environ.get('CELERY_RESULT_SERIALIZER', 'pickle'),
    accept_content=environ.get('CELERY_ACCEPT_CONTENT', 'pickle').split(','),
    result_expires=60,
)

@celery_app.task()
def dp_recommend(taken_courses, catalog, requirements, custom_tags=None) -> dict:
    recommendation = recommend(taken_courses, catalog, requirements, custom_tags)
    return recommendation

@celery_app.task()
def dp_fulfill(taken_courses, requirements, forced_wildcard_resolutions=None) -> dict:
    fulfillment = get_optimized_fulfillment(taken_courses, requirements, forced_wildcard_resolutions)
    return fulfillment

@celery_app.task()
def dp_fulfill_groups(fulfillments, groups, forced_groupings=None) -> list:
    fulfillment_groups = get_group_fulfillment(fulfillments, groups, forced_groupings)
    return fulfillment_groups
