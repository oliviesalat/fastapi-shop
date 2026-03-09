from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from backend.app.schemas.cart import (CartResponse, CartItemUpdate, CartItemCreate,
                                      AddToCartRequest, UpdateCartRequest, RemoveFromCartRequest, CartRequest)
from ..database import get_db
from ..services.cart_service import CartService

router = APIRouter(
    prefix='/api/cart',
    tags=['cart']
)


@router.post('', response_model=CartResponse, status_code=status.HTTP_200_OK)
def get_cart(request: CartRequest, db: Session = Depends(get_db)) -> CartResponse:
    return CartService(db).get_cart_details(request.cart)


@router.post('/add', status_code=status.HTTP_200_OK)
def add_to_cart(request: AddToCartRequest, db: Session = Depends(get_db)):
    item = CartItemCreate(product_id=request.product_id, quantity=request.quantity)
    updated_cart = CartService(db).add_to_cart(request.cart, item)
    return {'cart': updated_cart}


@router.put('/update', status_code=status.HTTP_200_OK)
def update_cart_item(request: UpdateCartRequest, db: Session = Depends(get_db)):
    item = CartItemUpdate(product_id=request.product_id, quantity=request.quantity)
    updated_cart = CartService(db).update_cart_item(request.cart, item)
    return {'cart': updated_cart}


@router.delete('/remove/{product_id}', status_code=status.HTTP_200_OK)
def remove_from_cart(product_id: int, request: RemoveFromCartRequest, db: Session = Depends(get_db)):
    service = CartService(db)
    updated_cart = service.remove_from_cart(request.cart, product_id)
    return {'cart': updated_cart}
