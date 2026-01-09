from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    category_id: int
    price: float


class ProductCreate(ProductBase):
    pass


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
    date: str
    quantity: int
    total_price: float


class SaleCreate(SaleBase):
    pass


class Sale(SaleBase):
    id: int

    class Config:
        from_attributes = True
