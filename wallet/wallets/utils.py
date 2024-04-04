from datetime import datetime

import requests


def request_third_party_deposit():
    response = requests.post("http://localhost:8010/")

    result = response.json().get("data")
    if result == "success":
        return True
    return False


def add_task_to_redis(trasnaction_id: str, draw_time: datetime): ...
