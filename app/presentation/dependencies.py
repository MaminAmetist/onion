from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.category_service import CategoryService
from app.application.services.post_service import PostService
from app.domain.repositories.categories import ICategoryRepository
from app.domain.repositories.posts import IPostRepository
from app.infrastructure.database.dependencies import get_db
from app.infrastructure.persistence.sqlalchemy.category_repository import \
    CategorySQLAlchemyRepository
from app.infrastructure.persistence.sqlalchemy.post_repository import PostSQLAlchemyRepository


def get_category_repo(db: AsyncSession = Depends(get_db)) -> ICategoryRepository:
    return CategorySQLAlchemyRepository(db)


def get_category_service(repo: ICategoryRepository = Depends(get_category_repo)) -> CategoryService:
    return CategoryService(repo)


def get_post_repo(db: AsyncSession = Depends(get_db)) -> IPostRepository:
    return PostSQLAlchemyRepository(db)


# CategoryRepository также нужен для PostService (для проверки существования категории)
def get_category_repo_for_post_service(db: AsyncSession = Depends(get_db)) -> ICategoryRepository:
    return CategorySQLAlchemyRepository(db)


def get_post_service(
        post_repo: IPostRepository = Depends(get_post_repo),
        category_repo: ICategoryRepository = Depends(get_category_repo_for_post_service)
) -> PostService:
    return PostService(post_repo=post_repo, category_repo=category_repo)
