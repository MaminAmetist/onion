from collections.abc import Sequence

from app.application.schemas.category import CategoryBase, CategoryRead
from app.domain.repositories.categories import ICategoryRepository


class CategoryService:
    def __init__(self, category_repo: ICategoryRepository):
        self.category_repo = category_repo

    async def get_category_by_id(self, category_id: int) -> CategoryRead | None:
        category = await self.category_repo.get_by_id(category_id)
        if category is None:
            return None
        return CategoryRead.model_validate(category)

    async def get_category_by_name(self, name: str) -> CategoryRead | None:
        category = await self.category_repo.get_by_name(name)
        if category is None:
            return None
        return CategoryRead.model_validate(category)

    async def get_all_categories(self, skip: int = 0, limit: int = 100) -> Sequence[CategoryRead]:
        categories = await self.category_repo.get_all(skip, limit)
        return [
            CategoryRead.model_validate(category)
            for category in categories
            if category is not None
        ]

    async def create_category(self, category_data: CategoryBase) -> CategoryRead:
        existing_category = await self.category_repo.get_by_name(category_data.name)
        if existing_category:
            raise ValueError(f"Category with name '{category_data.name}' already exists.")
        category = await self.category_repo.create(name=category_data.name)
        return CategoryRead.model_validate(category)
