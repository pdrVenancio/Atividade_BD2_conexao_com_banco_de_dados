from sqlalchemy import Column, String
from .base import Base
from models import *

class Customer:
    """
    Modelo Customer - versão para uso com driver psycopg2
    Representa um cliente no banco Northwind
    """
    def __init__(self, customerid=None, companyname=None, contactname=None, 
                 contacttitle=None, address=None, city=None, region=None, 
                 postalcode=None, country=None, phone=None, fax=None):
        
        self.customerid = customerid
        self.companyname = companyname
        self.contactname = contactname
        self.contacttitle = contacttitle
        self.address = address
        self.city = city
        self.region = region
        self.postalcode = postalcode
        self.country = country
        self.phone = phone
        self.fax = fax

    def __str__(self):
        return f"{self.customerid} - {self.companyname} ({self.contactname})"


# Versão para SQLAlchemy
class CustomerORM(Base):
    """
    Modelo Customer - versão para uso com SQLAlchemy ORM
    """
    __tablename__ = 'customers'
    __table_args__ = {'schema': 'northwind'}

    customerid = Column(String(5), primary_key=True)
    companyname = Column(String(40), nullable=False)
    contactname = Column(String(30))
    contacttitle = Column(String(30))
    address = Column(String(60))
    city = Column(String(15))
    region = Column(String(15))
    postalcode = Column(String(10))
    country = Column(String(15))
    phone = Column(String(24))
    fax = Column(String(24))

    def __repr__(self):
        return f"<Customer(customerid='{self.customerid}', companyname='{self.companyname}')>"