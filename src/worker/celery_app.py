from celery import Celery
from src.api.degree_planner.dp.recommend import *

celery_broker = 'redis://redis:6379/0'
celery_backend = 'redis://redis:6379/1'
celery_app = Celery("celery_app", broker=celery_broker, backend=celery_backend)


@celery_app.task
async def dp_recommend(planner, userid:str):
    io = planner.default_io

    user = planner.get_user(userid)
    user
    taken_courses = user.get_active_schedule().courses()
    best_fulfillments = planner.fulfillment(user, user.active_schedule)

    recommendation = recommend(taken_courses, best_fulfillments, planner.catalog)
    formatted_recommendations = io.format_recommendations(recommendation[0])

    results = dict()

    for recommendation in formatted_recommendations:
        curr_list = results.get(recommendation['name'], [])
        curr_list.append(recommendation)
        curr_list = sorting.list_of_dictionary_sort(curr_list, 'courses_fulfilled')
        results.update({recommendation['name']:curr_list})
    
    return results

