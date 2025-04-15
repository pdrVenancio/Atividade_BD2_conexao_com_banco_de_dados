from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import Base
from models import *

class Order:
    """
    Modelo Order - versão para uso com driver psycopg2
    Representa um pedido no banco Northwind
    """
    def __init__(self, orderid=None, customerid=None, employeeid=None, 
                 orderdate=None, requireddate=None, shippeddate=None, 
                 shipvia=None, freight=None, shipname=None, shipaddress=None, 
                 shipcity=None, shipregion=None, shippostalcode=None, 
                 shipcountry=None):
        self.orderid = orderid
        self.customerid = customerid
        self.employeeid = employeeid
        self.orderdate = orderdate or datetime.now()
        self.requireddate = requireddate
        self.shippeddate = shippeddate
        self.shipvia = shipvia
        self.freight = freight
        self.shipname = shipname
        self.shipaddress = shipaddress
        self.shipcity = shipcity
        self.shipregion = shipregion
        self.shippostalcode = shippostalcode
        self.shipcountry = shipcountry
        self.order_details = []  # Lista de OrderDetail
    
    def add_order_detail(self, order_detail):
        self.order_details.append(order_detail)
    
    def get_total(self):
        total = 0
        for detail in self.order_details:
            total += detail.quantity * detail.unitprice * (1 - detail.discount)
        return total

    def __str__(self):
        return f"Order #{self.orderid} - Customer: {self.customerid}, Date: {self.orderdate}"


# Versão para SQLAlchemy
class OrderORM(Base):
    """
    Modelo Order - versão para uso com SQLAlchemy ORM
    """
    __tablename__ = 'orders'
    __table_args__ = {'schema': 'northwind'}

    orderid = Column(Integer, primary_key=True)
    customerid = Column(String(5), ForeignKey('northwind.customers.customerid'))
    employeeid = Column(Integer, ForeignKey('northwind.employees.employeeid'))
    orderdate = Column(DateTime)
    requireddate = Column(DateTime)
    shippeddate = Column(DateTime)
    freight = Column(Float)
    shipname = Column(String(40))
    shipaddress = Column(String(60))
    shipcity = Column(String(15))
    shipregion = Column(String(15))
    shippostalcode = Column(String(10))
    shipcountry = Column(String(15))

    # Relacionamentos
    customer = relationship("CustomerORM")
    employee = relationship("EmployeeORM", back_populates="orders")
    order_details = relationship("OrderDetailORM", back_populates="order")

    def get_total(self):
        total = 0
        for detail in self.order_details:
            total += detail.quantity * detail.unitprice * (1 - detail.discount)
        return total

    def __repr__(self):
        return f"<Order(orderid={self.orderid}, customerid='{self.customerid}', date='{self.orderdate}')>"
    