from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.application.schemas.category import CategoryRead, CategoryBase
from app.application.services.category_service import CategoryService
from app.presentation.dependencies import get_category_service

router = APIRouter()


@router.post("/", response_model=CategoryRead, status_code=201)
async def create_category_endpoint(
        category_data: CategoryBase,
        service: CategoryService = Depends(get_category_service)
):
    try:
        return await service.create_category(category_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{category_id}", response_model=CategoryRead)
async def read_category_endpoint(
        category_id: int,
        service: CategoryService = Depends(get_category_service)
):
    db_category = await service.get_category_by_id(category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.get("/", response_model=List[CategoryRead])
async def read_categories_endpoint(
        skip: int = 0, limit: int = 100,
        service: CategoryService = Depends(get_category_service)
):
    categories = await service.get_all_categories(skip=skip, limit=limit)
    return categories
