from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from backend.app.schemas.product import ProductResponse, ProductListResponse
from ..database import get_db
from ..services.product_service import ProductService

router = APIRouter(
    prefix='/api/products',
    tags=['products']
)


@router.get('', response_model=ProductListResponse, status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db)) -> ProductListResponse:
    return ProductService(db).get_all_products()


@router.get('/{product_id}', response_model=ProductResponse, status_code=status.HTTP_200_OK)
def get_product(product_id: int, db: Session = Depends(get_db)) -> ProductResponse:
    return ProductService(db).get_product_by_id(product_id)


@router.get("/category/{category_id}", response_model=ProductListResponse, status_code=status.HTTP_200_OK)
def get_products_by_category(category_id: int, db: Session = Depends(get_db)) -> ProductListResponse:
    return ProductService(db).get_products_by_category(category_id)
