# Exporta os modelos para uso externo
from .base_model import BaseModel
from .northwind import Order, Customer, Employee, OrderDetail  # ORM
from .northwind_models import OrderModel, CustomerModel       # Driver puro

__all__ = ['BaseModel', 'Order', 'Customer', 'Employee', 'OrderDetail', 'OrderModel', 'CustomerModel']