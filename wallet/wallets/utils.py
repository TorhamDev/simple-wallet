import json
from functools import lru_cache
from logging import getLogger

import pydantic
import requests
from redis import Redis
from redis.exceptions import ConnectionError as RedisConnectionError
from redis.exceptions import RedisError

from wallets.constants import TRANSACTIONS_REDIS_KEY
from wallets.exceptions import ThirdPartyError

logger = getLogger(__name__)


def request_third_party_deposit():
    response = requests.post("http://localhost:8010/")

    result = response.json().get("data")
    if result == "success":
        # return value or anything u get from 3rd party
        return True

    # better to raise? idk
    return False


@lru_cache
def get_redis() -> Redis:
    redis = Redis()
    return redis


def lpush_to_redis(items: list) -> int:
    r = get_redis()
    result = r.lpush(TRANSACTIONS_REDIS_KEY, *items)

    # u can check result with length of ur items to make sure all pushed into redis
    return result


def handle_third_party() -> None:
    result = request_third_party_deposit()

    if not result:
        raise ThirdPartyError

    # some other things to do here...


class WithdrawHandler:
    def __init__(self, tr_in_progress) -> None:
        self.tr_in_progress = tr_in_progress

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type:
            logger.warning(
                f"Restore again to redis bc of: {exc_type.__name__} - {str(exc_val)}"
            )
            logger.warning(f"Restore {self.tr_in_progress}")
            if self.tr_in_progress:
                lpush_to_redis([self.tr_in_progress])

        if exc_type is json.decoder.JSONDecodeError:
            # do what you have to do about this error
            logger.warning(
                f"An JSON error occurred: {exc_type.__name__} - {str(exc_val)}"
            )

        elif exc_type is pydantic.ValidationError:
            # do what you have to do about this error
            logger.warning(
                f"An PYDANTIC error occurred: {exc_type.__name__} - {str(exc_val)}"
            )

        elif exc_type is RedisError:
            # do what you have to do about this error
            logger.warning(
                f"An REDISERROR error occurred: {exc_type.__name__} - {str(exc_val)}"
            )

        elif exc_type is RedisConnectionError:
            # do what you have to do about this error
            logger.warning(
                f"An RedisConnectionError error occurred: {exc_type.__name__} - {str(exc_val)}"
            )

        elif exc_type is ConnectionError:
            # do what you have to do about this error
            logger.warning(
                f"An ConnectionError error occurred: {exc_type.__name__} - {str(exc_val)}"
            )

        elif exc_type is ThirdPartyError:
            # do what you have to do about this error
            logger.warning(
                f"An ThirdPartyError error occurred: {exc_type.__name__} - {str(exc_val)}"
            )

        elif exc_type is Exception:
            # there is somthing happend that i have no idea about, like WTF
            # so i will log it as a critical
            logger.critical(
                f"An Unkown error occurred: {exc_type.__name__} - {str(exc_val)}"
            )
        return True
