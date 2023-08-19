import redis
import json

redis_client = redis.StrictRedis(host='redis-userdata', port=6379, db=0)

'''
USER'S SCHEDULE_IDS
'''
def has_user(userid:str) -> bool:
    return redis_client.exists(f'user:{userid}')

async def get_user_schedules(userid:str) -> set:
    retrieved_user = redis_client.get(f'user:{userid}')

    if retrieved_user:
        schedule_ids = json.loads(retrieved_user)
        return set(schedule_ids)
    else:
        return set()
    
async def set_user_schedules(userid:str, schedule_ids:set):
    schedule_ids = list(schedule_ids)
    schedule_ids_json = json.dumps(schedule_ids)
    redis_client.set(f'user:{userid}', schedule_ids_json)


async def add_user_schedule(userid:str, schedule_id:str):
    schedule_ids = await get_user_schedules(userid)
    schedule_ids.add(schedule_id)
    await set_user_schedules(userid, schedule_ids)

async def remove_user_schedule(userid:str, schedule_id:str):
    schedule_ids = await get_user_schedules(userid)
    schedule_ids.remove(schedule_id)
    await set_user_schedules(userid, schedule_ids)

async def delete_user(userid:str):
    schedule_ids = await get_user_schedules(userid)
    for schedule_id in schedule_ids:
        await delete_schedule(schedule_id)
    redis_client.delete(f'user:{userid}')

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


'''
WRAPPER FUNCTIONS
'''

async def wrapper_get_schedule(userid:str, schedule_name:str):
    schedule_id = get_schedule_id(userid, schedule_name)
    schedule = await get_schedule(schedule_id)
    return schedule

async def wrapper_save_schedule(userid:str, schedule_name:str, schedule_data):
    schedule_id = get_schedule_id(userid, schedule_name)

    await add_user_schedule(userid, schedule_id)
    await save_schedule(schedule_id, schedule_data)

async def wrapper_delete_schedule(userid:str, schedule_name:str):
    schedule_id = get_schedule_id(userid, schedule_name)
    await remove_user_schedule(userid, schedule_id)
    await delete_schedule(schedule_id)


def get_schedule_id(userid:str, schedule_name:str):
    return f'{userid}:{schedule_name}'

def get_schedule_name(schedule_id:str):
    if ':' in schedule_id:
        return schedule_id[schedule_id.find(':') + 1:]
    return schedule_id

def get_redis_status():
    all_keys = redis_client.keys('*')
    all_kv_pairs = dict()
    for key in all_keys:
        value = redis_client.get(key)
        all_kv_pairs.update({key.decode('utf-8'):value.decode('utf-8')})
    return all_kv_pairs