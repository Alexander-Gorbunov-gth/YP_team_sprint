from locust import HttpUser, task, between
import uuid
import random


class LoadTestUser(HttpUser):
    wait_time = between(1, 2)  # интервал между запросами

    @task
    def send_event_click(self):
        self.client.post(
            "/api/v1/event/click/",
            json={
                "token": str(uuid.uuid4()),  # имитация уникального токена
                "payload": {"video_id": "test_id", "watched_seconds": 10},
            },
            headers={"User-Agent": "LocustLoadTest"},
            timeout=2,
        )
