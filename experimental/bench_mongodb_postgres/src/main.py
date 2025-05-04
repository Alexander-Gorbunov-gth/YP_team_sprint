from src.services import MongoDB, Postgres
from src.utils.enums import DatabaseType, RequestType
from src.bench_results.create_result import CreateReuslts


def main():
    services = {
        DatabaseType.MONGODB: MongoDB(),
        DatabaseType.POSTGRES: Postgres(),
    }

    create_reuslts = CreateReuslts(
        services=[service for service in services.keys()],
        requests=[
            RequestType.INSERT_ONE, RequestType.INSERT_MANY,
            RequestType.SELECT_ONE, RequestType.SELECT_MANY,
            RequestType.UPDATE_ONE, RequestType.UPDATE_MANY,
            RequestType.DELETE_ONE, RequestType.DELETE_MANY,
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
