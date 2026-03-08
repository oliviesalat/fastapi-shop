from sqlalchemy.orm import Session, joinedload
from typing import Optional, List, Type

from backend.app.models import Product
from ..models import Category
from ..models.product import Product
from ..schemas.product import ProductCreate, ProductBase


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .all()
        )

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.id == product_id)
            .first()
        )

    def get_by_category(self, category_id: int) -> list[Product]:
        return (
            (self.db.query(Product)
             .options(joinedload(Product.category))
             .filter(Product.category_id == category_id))
            .all()
        )

    def create(self, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_multiple_by_ids(self, product_ids: list[int]) -> list[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.id.in_(product_ids))
            .all()
        )
