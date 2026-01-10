from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    category_id: int
    price: float
    brand: str


class ProductCreate(ProductBase):
    id: Optional[int] = None


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class SaleBase(BaseModel):
    product_id: int
    date: datetime
    quantity: int
    total_price: float


class SaleCreate(SaleBase):
    pass


class Sale(SaleBase):
    id: int

    class Config:
        from_attributes = True
