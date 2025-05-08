import time

cache = {}

last_time_cleaned = time.time() * 1000

def in_cache(key, storeId):
    key = str(key) + "-" + str(storeId)
    now = time.time() * 1000

    clean_sku_cache(now)

    if (key not in cache) or (now > cache[key]):
        cache[key] = now + 60000
        return False

    return True

def clean_sku_cache(now):
    global last_time_cleaned

    if (now - last_time_cleaned < 10000):
        return

    for key in list(cache):
        if (cache[key] < time.time() * 1000):
            del cache[key]

    last_time_cleaned = now
