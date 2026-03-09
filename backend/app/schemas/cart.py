from pydantic import BaseModel, Field
from typing import Optional


class CartItemBase(BaseModel):
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity")


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(CartItemBase):
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(..., gt=0, description="New quantity")


class CartItem(BaseModel):
    product_id: int
    name: str = Field(..., description="Product name")
    price: float = Field(..., gt=0, description="Price")
    quantity: int = Field(..., gt=0, description="Quantity")
    subtotal: float = Field(..., gt=0, description="Subtotal (price * quantity)")
    image_url: Optional[str] = Field(None, description="Product image url")


class CartResponse(BaseModel):
    items: list[CartItem] = Field(..., description="Cart items")
    total: float = Field(..., gt=0, description="Total price")
    items_count: int = Field(..., gt=0, description="Total number of items")

class CartRequest(BaseModel):
    cart: dict[int, int] = Field(default_factory=dict)

class AddToCartRequest(BaseModel):
    product_id: int
    quantity: int
    cart: dict[int, int] = Field(default_factory=dict)


class UpdateCartRequest(BaseModel):
    product_id: int
    quantity: int
    cart: dict[int, int] = Field(default_factory=dict)


class RemoveFromCartRequest(BaseModel):
    cart: dict[int, int] = Field(default_factory=dict)
