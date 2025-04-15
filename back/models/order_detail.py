from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from models import *

class OrderDetail:
    """
    Modelo OrderDetail - versão para uso com driver psycopg2
    Representa um item de pedido no banco Northwind
    """
    def __init__(self, orderid=None, productid=None, unitprice=0, 
                 quantity=1, discount=0):
        self.orderid = orderid
        self.productid = productid
        self.unitprice = unitprice
        self.quantity = quantity
        self.discount = discount
        self.product = None  # Referência ao produto (populado posteriormente)
    
    def get_subtotal(self):
        return self.quantity * self.unitprice * (1 - self.discount)

    def __str__(self):
        product_name = self.product.productname if self.product else f"Product #{self.productid}"
        return f"{product_name} - Qty: {self.quantity}, Price: ${self.unitprice}"


# Versão para SQLAlchemy
class OrderDetailORM(Base):
    """
    Modelo OrderDetail - versão para uso com SQLAlchemy ORM
    """
    __tablename__ = 'order_details'
    __table_args__ = {'schema': 'northwind'}

    orderid = Column(Integer, ForeignKey('northwind.orders.orderid'), primary_key=True)
    productid = Column(Integer, ForeignKey('northwind.products.productid'), primary_key=True)
    unitprice = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    discount = Column(Float, nullable=False)

    # Relacionamentos
    order = relationship("OrderORM", back_populates="order_details")
    product = relationship("ProductORM")

    def get_subtotal(self):
        return self.quantity * self.unitprice * (1 - self.discount)

    def __repr__(self):
        return f"<OrderDetail(orderid={self.orderid}, productid={self.productid}, quantity={self.quantity})>"