import redis
import json

redis_client = redis.StrictRedis(host='redis-userdata', port=6379, db=0)

async def purify():
    all_keys = redis_client.keys('*')
    for key in all_keys:
        redis_client.delete(key)
        print(f'deleted entry with key {key}')


'''
SCHEDULE DATA
'''

async def get_schedule(schedule_id:str):
    retrieved_schedule = redis_client.get(f'schedule:{schedule_id}')
    if retrieved_schedule:
        schedule = json.loads(retrieved_schedule)
        return schedule

async def save_schedule(schedule_id:str, schedule_data):
    schedule_json = json.dumps(schedule_data)
    redis_client.set(f'schedule:{schedule_id}', schedule_json)

async def delete_schedule(schedule_id:str):
    redis_client.delete(f'schedule:{schedule_id}')


def get_redis_status():
    all_keys = redis_client.keys('*')
    all_kv_pairs = dict()
    for key in all_keys:
        value = redis_client.get(key)
        all_kv_pairs.update({key.decode('utf-8'):value.decode('utf-8')})
    return all_kv_pairs