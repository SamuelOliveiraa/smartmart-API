from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Permite acessar todos os produtos de uma categoria: minha_categoria.products
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))
    brand = Column(String)

    # Permite acessar a categoria do produto: meu_produto.category.name
    category = relationship("Category", back_populates="products")
    sales = relationship("Sale", back_populates="product")


class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    date = Column(DateTime, default=datetime.utcnow)
    quantity = Column(Integer)
    total_price = Column(Float)

    product = relationship("Product", back_populates="sales")
