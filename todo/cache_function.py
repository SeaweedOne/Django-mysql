from django.core.cache import cache

# This function increase value by one
def incrKey(key, value, timeout=None):
    return cache.incr(key, delta=value)


# This function set value
def setKey(key, value, timeout=None):
    return cache.set(key, value, timeout=timeout)


# This function set value if key exist then give error
def addKey(key, value, timeout=None):
    return cache.add(key, value, timeout=timeout)


# this function get value by key
def getKey(key):
    return cache.get(key)


# this function delete value by key
def deleteKey(key):
    return cache.delete(key)


# this function delete value by pattern
def getAllKey(pattern):
    return cache.keys(pattern)


CACHE_TTL = 60 * 5  # 5분 동안 캐시 유지

def get_todo_list_from_cache():
    # Redis에서 "todos" 키로 저장된 데이터를 가져옴
    todos = cache.get('todos')
    return todos

def set_todo_list_to_cache(data):
    # Redis에 "todos" 키로 데이터 저장
    cache.set('todos', data, timeout=CACHE_TTL)

def invalidate_todo_cache():
    # 캐시 무효화 (삭제)
    cache.delete('todos')