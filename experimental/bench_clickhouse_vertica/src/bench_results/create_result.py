import datetime

from src.core.config import settings
from src.utils.sql_tools import (
    DatabaseType, SQLRequests,
    SQLTools
)


class CreateReuslts:
    def __init__(
        self,
        services: list[DatabaseType],
        requests: list[SQLRequests]
    ):
        self.services = services
        self.requests = requests
        self.date_now = datetime.datetime.now(tz=datetime.timezone.utc)
        self.data = ""
        self._create_header()

    def _create_header(self):
        services_row = ', '.join(
            [service.value.title() for service in self.services]
        )
        requests_row = ', '.join([request.value for request in self.requests])
        self.data += (
            f"Bench date: {self.date_now}\n"
            f"Services: {services_row}\n"
            f"Requests type: {requests_row}\n"
            f"Quantity requests: {settings.col_requests}\n"
            "\n"
        )

    def add_result(self, service: DatabaseType, results: dict):
        sql_tools = SQLTools(database_type=service)
        results_row = '\n'.join([
            f"{request.value} = {result:.4f}s"
            for request, result in results.items()
        ])
        sql_row = '\n'.join([
            f"{request.value} = '''{sql_tools.get_sql_request(request)}'''"
            for request in results.keys()
        ])
        self.data += (
            f"{service.value.title()}:\n"
            f"{results_row}\n"
            "SQL requests:\n"
            f"{sql_row}\n"
            "\n"
        )

    def write_data(self):
        date = self.date_now.strftime("%Y_%m_%d_%H_%M")
        with open(f"./src/bench_results/data/{date}.txt", "a+") as file:
            file.write(self.data)
