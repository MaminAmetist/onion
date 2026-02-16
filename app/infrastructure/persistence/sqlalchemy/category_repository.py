from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.category import Category
from app.domain.repositories.categories import ICategoryRepository


class CategorySQLAlchemyRepository(ICategoryRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, category_id: int) -> Category | None:
        result = await self.db.scalar(select(Category).where(Category.id == category_id))
        return result

    async def get_by_name(self, name: str) -> Category | None:
        result = await self.db.scalar(select(Category).where(Category.name == name))
        return result

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Category]:
        result = await self.db.scalars(select(Category).offset(skip).limit(limit))
        return result.all()

    async def create(self, name: str) -> Category:
        db_category = Category(name=name)
        self.db.add(db_category)
        await self.db.commit()
        await self.db.refresh(db_category)
        return db_category
