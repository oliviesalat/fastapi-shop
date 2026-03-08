from pydantic import BaseModel, Field
from typing import Optional
from .category import CategoryResponse
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=100,
                      description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., gt=0, description="Product price")
    category_id: int = Field(..., gt=0, description="Product category id")
    image_url: Optional[str] = Field(None, description="Product image url")

class ProductCreate(ProductBase):
    pass

class ProductResponse(BaseModel):
    id: int = Field(..., gt=0, description="Unique product id")
    name: str
    description: Optional[str]
    price: float
    category_id: int
    image_url: Optional[str]
    created_at: datetime
    category: CategoryResponse = Field(..., description="Product category")

    class Config:
        from_attributes = True

class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    total: int = Field(..., gt=0, description="Total product count")
