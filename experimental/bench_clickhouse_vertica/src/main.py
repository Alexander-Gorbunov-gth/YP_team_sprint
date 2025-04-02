from bench_results.create_result import CreateReuslts
from services import ClickHouse, Vertica
from src.utils.sql_tools import DatabaseType, SQLRequests


def main():
    services = {
        DatabaseType.CLICKHOUSE: ClickHouse(),
        DatabaseType.VERTICA: Vertica()
    }

    create_reuslts = CreateReuslts(
        services=[service for service in services.keys()],
        requests=[
            SQLRequests.INSERT, SQLRequests.SELECT,
            SQLRequests.UPDATE, SQLRequests.DELETE
        ]
    )

    for service, service_cls in services.items():
        create_reuslts.add_result(
            service=service,
            results=service_cls.bench()
        )

    create_reuslts.write_data()


if __name__ == "__main__":
    main()
