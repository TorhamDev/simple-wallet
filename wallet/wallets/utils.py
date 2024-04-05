import json
from functools import lru_cache

import pydantic
import requests
from redis import Redis
from redis.exceptions import ConnectionError as RedisConnectionError
from redis.exceptions import RedisError

from wallets.exceptions import ThirdPartyError


def request_third_party_deposit():
    response = requests.post("http://localhost:8010/")

    result = response.json().get("data")
    if result == "success":
        # return value or anything u get from 3rd party
        return True
    return False


@lru_cache
def get_redis() -> Redis:
    redis = Redis()
    return redis


class WithdrawFlowManager:
    tr_to_withdraw = []

    def __init__(self, tr_to_withdraw: list) -> None:
        self.tr_to_withdraw = tr_to_withdraw

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type:
            print(f"Restore again to redis bc of: {exc_type.__name__} - {str(exc_val)}")
            r = get_redis()
            r.lpush("transactions", *self.tr_to_withdraw)

        if exc_type is json.decoder.JSONDecodeError:
            print(f"An JSON error occurred: {exc_type.__name__} - {str(exc_val)}")

        elif exc_type is pydantic.ValidationError:
            print(f"An PYDANTIC error occurred: {exc_type.__name__} - {str(exc_val)}")

        elif exc_type is RedisError:
            print(f"An REDISERROR error occurred: {exc_type.__name__} - {str(exc_val)}")

        elif exc_type is RedisConnectionError:
            print(
                f"An RedisConnectionError error occurred: {exc_type.__name__} - {str(exc_val)}"
            )
        elif exc_type is ThirdPartyError:
            print(
                f"An ThirdPartyError error occurred: {exc_type.__name__} - {str(exc_val)}"
            )

        return True
