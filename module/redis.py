from typing import Optional
from redis import Redis
from module import core, auxiliary
import config
import json

REDIS = Redis()
TASK_KEY = f'{config.REDIS_KEY_PREFIX}_task'
QUEUE_KEY = f'{config.REDIS_KEY_PREFIX}_queue'

def init() -> None:
    global REDIS
    REDIS = Redis(host=config.REDIS['host'], port=config.REDIS['port'], password=config.REDIS['password'], db=config.REDIS['db'])

def add(token: str, targetFormat: str, sourceFormat: Optional[str], modes: list, parameter: dict) -> None:
    REDIS.hset(TASK_KEY, token, json.dumps({
        'targetFormat': targetFormat,
        'sourceFormat': sourceFormat,
        'modes': modes,
        'parameter': parameter,
        'state': core.State.WAIT,
        'timestamp': auxiliary.getTimestamp()
    }))
    REDIS.save()

    REDIS.lpush(QUEUE_KEY, token)
    REDIS.save()

def getTasks() -> dict:
    tasks = REDIS.hgetall(TASK_KEY)
    if tasks:
        return {token.decode(): json.loads(task.decode()) for token, task in tasks.items()}
    return {}

def getTask(token: str) -> Optional[dict]:
    task = REDIS.hget(TASK_KEY, token)
    if task:
        return json.loads(task)
    return None

def queueDequeue() -> Optional[str]:
    token = REDIS.lpop(QUEUE_KEY)
    if token:
        return token.decode()
    return None

def setTaskState(token: str, state: core.State) -> bool:
    task = getTask(token)
    if task:
        task['state'] = state
        REDIS.hset(TASK_KEY, token, json.dumps(task))
        REDIS.save()
        return True
    return False

def deleteTask(token: str) -> bool:
    REDIS.hdel(TASK_KEY, token)
    return REDIS.save()

def deleteQueue(token: str) -> bool:
    REDIS.lrem(QUEUE_KEY, 0, token)
    return REDIS.save()