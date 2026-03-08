from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from backend.app.schemas.category import CategoryResponse
from ..database import get_db
from ..services.category_service import CategoryService

router = APIRouter(
    prefix='/api/categories',
    tags=['categories']
)


@router.get('', response_model=list[CategoryResponse], status_code=status.HTTP_200_OK)
def get_categories(db: Session = Depends(get_db)) -> list[CategoryResponse]:
    return CategoryService(db).get_all_categories()


@router.get('/{category_id}', response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def get_category(category_id: int, db: Session = Depends(get_db)) -> CategoryResponse:
    return CategoryService(db).get_category_by_id(category_id)
