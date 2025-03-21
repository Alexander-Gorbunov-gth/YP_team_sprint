import logging
from abc import ABC, abstractmethod
from typing import Any

from elasticsearch import AsyncElasticsearch
from elasticsearch import ConnectionError as ESConnectionError
from elasticsearch import NotFoundError
from elasticsearch_dsl import AsyncSearch, Q

logger = logging.getLogger(__name__)


class DBManager(ABC):
    """Абстрактный класс для управления базой данных."""

    def __init__(self, db_client: Any, db_name: str):
        self.db_client = db_client
        self.db_name = db_name

    @abstractmethod
    async def get_object_by_id(self, object_id: str) -> dict[str, Any] | None:
        """Получение объекта по ID."""

    @abstractmethod
    async def get_objects_by_query(
        self,
        query: str | None = None,
        fields: list[str] | None = None,
        person_uuid: str | None = None,
        nested_filters: list[str] | None = None,
        sort: str = "-imdb_rating",
        page_size: int = 10,
        page: int = 1,
    ) -> list[dict[str, Any]]:
        """Получение объектов по запросу."""


class ElasticManager(DBManager):
    """Класс для управления Elasticsearch."""

    def __init__(self, es_client: AsyncElasticsearch, index_name: str):
        super().__init__(es_client, index_name)
        self.es_client = es_client
        self.index_name = index_name

    async def get_object_by_id(self, object_id: str) -> dict[str, Any] | None:
        """Получение объекта из Elasticsearch по ID."""
        try:
            doc = await self.es_client.get(index=self.index_name, id=object_id)
            logger.info("Документ с ID {} успешно найден.".format(object_id))
            return doc["_source"]
        except NotFoundError:
            logger.warning("Документ с ID {} не найден.".format(object_id))
            return None
        except ESConnectionError as e:
            logger.error(
                "Ошибка подключения к Elasticsearch при поиске ID {}: {}".format(
                    object_id, e
                )
            )
            return None
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при поиске ID {}: {}".format(object_id, e)
            )
            return None

    async def get_objects_by_query(
        self,
        query: str | None = None,
        fields: list[str] | None = None,
        person_uuid: str | None = None,
        nested_filters: list[dict] | None = None,
        sort: str = "-imdb_rating",
        page_size: int = 10,
        page: int = 1,
    ) -> list[dict[str, Any]]:
        """
        Получение списка объектов из Elasticsearch по запросу.

        :param query: Поисковая строка.
        :param fields: Поля, в которых производится поиск.
        :param sort: Поле для сортировки (например, '-imdb_rating').
        :param page_size: Количество записей на странице.
        :param page: Номер страницы.
        :return: Список объектов в виде словарей.
        """

        try:
            search = await self._generate_query(
                query=query,
                fields=fields,
                person_uuid=person_uuid,
                nested_filters=nested_filters,
                sort=sort,
                page_size=page_size,
                page=page,
            )
            response = await search.execute()
            documents = [hit.to_dict() for hit in response]
            logger.info(
                "Запрос выполнен успешно. Найдено %s объектов.", len(documents)
            )
            return documents
        except ESConnectionError as e:
            logger.error(
                "Ошибка подключения к Elasticsearch при выполнении запроса: %s",
                e,
            )
            return None
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при выполнении запроса: %s", e
            )
            return None

    async def _generate_query(
        self,
        query: str | None = None,
        fields: list[str] | None = None,
        person_uuid: str | None = None,
        nested_filters: list[str] | None = None,
        sort: str = "-imdb_rating",
        page_size: int = 10,
        page: int = 1,
    ) -> AsyncSearch:
        """
        Генерация запроса для Elasticsearch с учетом поисковой фразы, полей, вложенных фильтров, сортировки и пагинации.

        :param query: Поисковая строка.
        :param fields: Поля для поиска.
        :param person_uuid: UUID человека для вложенных фильтров.
        :param nested_filters: Фильтры для вложенных объектов.
        :param sort: Поле для сортировки с направлением (например, '-imdb_rating').
        :param page_size: Количество записей на странице.
        :param page: Номер страницы.
        :return: Сгенерированный объект запроса AsyncSearch.
        """
        search = AsyncSearch(using=self.es_client, index=self.index_name)

        # Основной запрос
        if query and fields:
            must_queries = [
                Q("match", **{field: query}) for field in fields if field
            ]
            search = search.query("bool", must=must_queries)
            logger.debug("Сформирован запрос с поисковой строкой: %s", query)
        else:
            search = search.query(Q("match_all"))
            logger.debug("Сформирован запрос для получения всех документов.")

        if person_uuid and nested_filters:
            nested_queries = []
            for nested_field in nested_filters:
                nested_queries.append(
                    Q(
                        "nested",
                        path=nested_field,
                        query=Q("term", **{f"{nested_field}.id": person_uuid}),
                    )
                )
            search = search.query(
                "bool", should=nested_queries, minimum_should_match=1
            )
            logger.debug(
                "Добавлены вложенные фильтры для UUID %s: %s",
                person_uuid,
                nested_filters,
            )

        if sort is not None:
            for sort_field in sort.split(","):
                field = sort_field.lstrip("-")
                order = "desc" if sort_field.startswith("-") else "asc"
                search = search.sort({field: {"order": order}})
                logger.debug("Добавлена сортировка: %s (%s).", field, order)

        search = search[(page - 1) * page_size : page * page_size]
        return search
