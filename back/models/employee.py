from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from models import *

class Employee:
    """
    Modelo Employee - versão para uso com driver psycopg2
    Representa um funcionário no banco Northwind
    """
    def __init__(self, employeeid=None, lastname=None, firstname=None, 
                 title=None, titleofcourtesy=None, birthdate=None, 
                 hiredate=None, address=None, city=None, region=None, 
                 postalcode=None, country=None, homephone=None, 
                 extension=None, photo=None, notes=None, reportsto=None):
        self.employeeid = employeeid
        self.lastname = lastname
        self.firstname = firstname
        self.title = title
        self.titleofcourtesy = titleofcourtesy
        self.birthdate = birthdate
        self.hiredate = hiredate
        self.address = address
        self.city = city
        self.region = region
        self.postalcode = postalcode
        self.country = country
        self.homephone = homephone
        self.extension = extension
        self.photo = photo
        self.notes = notes
        self.reportsto = reportsto
    
    def get_full_name(self):
        return f"{self.firstname} {self.lastname}"

    def __str__(self):
        return f"{self.employeeid} - {self.get_full_name()}"


# Versão para SQLAlchemy
class EmployeeORM(Base):
    """
    Modelo Employee - versão para uso com SQLAlchemy ORM
    """
    __tablename__ = 'employees'
    __table_args__ = {'schema': 'northwind'}

    employeeid = Column(Integer, primary_key=True)
    lastname = Column(String(20), nullable=False)
    firstname = Column(String(10), nullable=False)
    title = Column(String(30))
    titleofcourtesy = Column(String(25))
    birthdate = Column(Date)
    hiredate = Column(Date)
    address = Column(String(60))
    city = Column(String(15))
    region = Column(String(15))
    postalcode = Column(String(10))
    country = Column(String(15))
    homephone = Column(String(24))
    extension = Column(String(4))
    notes = Column(Text)
    reportsto = Column(Integer, ForeignKey('northwind.employees.employeeid'))

    # Relacionamentos
    orders = relationship("OrderORM", back_populates="employee")
    manager = relationship("EmployeeORM", remote_side=[employeeid], backref="subordinates")

    def get_full_name(self):
        return f"{self.firstname} {self.lastname}"

    def __repr__(self):
        return f"<Employee(employeeid={self.employeeid}, name='{self.get_full_name()}')>"