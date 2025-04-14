from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'

    customerid = Column(String(5), primary_key=True)
    companyname = Column(String(40))
    contactname = Column(String(30))
    address = Column(String(50))
    city = Column(String(20))
    region = Column(String(15))
    postalcode = Column(String(9))
    country = Column(String(15))
    phone = Column(String(17))
    fax = Column(String(17))
    
    orders = relationship("Order", back_populates="customer")

class Order(Base):
    __tablename__ = 'orders'

    orderid = Column(Integer, primary_key=True)
    customerid = Column(String(5), ForeignKey('customers.customerid'))
    employeeid = Column(Integer, ForeignKey('employees.employeeid'))
    orderdate = Column(Date)
    requireddate = Column(Date)
    shippeddate = Column(Date)
    freight = Column(Numeric(15,4))
    shipname = Column(String(35))
    shipaddress = Column(String(50))
    shipcity = Column(String(15))
    shipregion = Column(String(15))
    shippostalcode = Column(String(9))
    shipcountry = Column(String(15))
    shipperid = Column(Integer)
    
    # Classes relacionadas
    customer = relationship("Customer", back_populates="orders")
    employee = relationship("Employee")
    details = relationship("OrderDetail")

class OrderDetail(Base):
    __tablename__ = 'order_details'
    
    orderid = Column(Integer, ForeignKey('orders.orderid'), primary_key=True)
    productid = Column(Integer, ForeignKey('products.productid'), primary_key=True)
    unitprice = Column(Numeric(13, 4))
    quantity = Column(Integer)
    discount = Column(Numeric(10, 4))
    
    order = relationship("Order", back_populates="details")
    product = relationship("Product")