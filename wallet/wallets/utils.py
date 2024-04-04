from functools import lru_cache

import requests
from redis import Redis


def request_third_party_deposit():
    response = requests.post("http://localhost:8010/")

    result = response.json().get("data")
    if result == "success":
        return True
    return False


@lru_cache
def get_redis() -> Redis:
    redis = Redis()
    return redis
