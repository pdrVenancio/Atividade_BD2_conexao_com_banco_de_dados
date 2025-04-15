from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base
from models import *

class Product:
    """
    Modelo Product - versão para uso com driver psycopg2
    Representa um produto no banco Northwind
    """
    def __init__(self, productid=None, productname=None, supplierid=None, 
                 categoryid=None, quantityperunit=None, unitprice=None, 
                 unitsinstock=None, unitsonorder=None, reorderlevel=None, 
                 discontinued=False):
        self.productid = productid
        self.productname = productname
        self.supplierid = supplierid
        self.categoryid = categoryid
        self.quantityperunit = quantityperunit
        self.unitprice = unitprice
        self.unitsinstock = unitsinstock
        self.unitsonorder = unitsonorder
        self.reorderlevel = reorderlevel
        self.discontinued = discontinued

    def __str__(self):
        return f"{self.productid} - {self.productname} (${self.unitprice})"


# Versão para SQLAlchemy
class ProductORM(Base):
    """
    Modelo Product - versão para uso com SQLAlchemy ORM
    """
    __tablename__ = 'products'
    __table_args__ = {'schema': 'northwind'}

    productid = Column(Integer, primary_key=True)
    productname = Column(String(40), nullable=False)
    # supplierid = Column(Integer, ForeignKey('suppliers.supplierid'))
    # categoryid = Column(Integer, ForeignKey('categories.categoryid'))
    supplierid = Column(Integer)
    categoryid = Column(Integer)
    quantityperunit = Column(String(20))
    unitprice = Column(Float)
    unitsinstock = Column(Integer)
    unitsonorder = Column(Integer)
    reorderlevel = Column(Integer)
    discontinued = Column(Boolean, nullable=False)

    # Relacionamentos (opcional, dependendo da necessidade)
    # supplier = relationship("SupplierORM")
    # category = relationship("CategoryORM")

    def __repr__(self):
        return f"<Product(productid={self.productid}, name='{self.productname}', price=${self.unitprice})>"