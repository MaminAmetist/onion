from collections.abc import Sequence

from app.application.schemas.post import PostBase, PostRead
from app.domain.repositories.categories import ICategoryRepository
from app.domain.repositories.posts import IPostRepository


class PostService:
    def __init__(self, post_repo: IPostRepository, category_repo: ICategoryRepository):
        self.post_repo = post_repo
        self.category_repo = category_repo

    async def get_post_by_id(self, post_id: int) -> PostRead | None:
        post = await self.post_repo.get_by_id(post_id)
        if post is None:
            return None
        return PostRead.model_validate(post)

    async def get_all_posts(self, skip: int = 0, limit: int = 100) -> Sequence[PostRead]:
        posts = await self.post_repo.get_all(skip, limit)
        return [
            PostRead.model_validate(post)
            for post in posts
            if post is not None
        ]

    async def get_posts_by_category_id(
            self,
            category_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> Sequence[PostRead]:
        posts = await self.post_repo.get_by_category_id(category_id, skip, limit)
        return [
            PostRead.model_validate(post)
            for post in posts
            if post is not None
        ]

    async def create_post(self, post_data: PostBase) -> PostRead:
        category = await self.category_repo.get_by_id(post_data.category_id)
        if not category:
            raise ValueError(f"Category with id '{post_data.category_id}' does not exist.")

        post = await self.post_repo.create(
            title=post_data.title,
            content=post_data.content,
            category_id=post_data.category_id
        )
        return PostRead.model_validate(post)
