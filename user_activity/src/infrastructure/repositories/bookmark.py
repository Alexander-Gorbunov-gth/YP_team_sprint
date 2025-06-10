from src.domain.bookmark import Bookmark
from src.infrastructure.models import BookmarkModel
from src.infrastructure.repositories.base import AbstractRepository, BeanieBaseRepository


class AbstractBookmarkRepository(AbstractRepository[Bookmark]):
    pass


class BeanieBookmarkRepository(AbstractBookmarkRepository, BeanieBaseRepository[Bookmark]):
    pass


def get_bookmark_repository() -> AbstractBookmarkRepository:
    return BeanieBookmarkRepository(model=BookmarkModel, domain_model=Bookmark)
