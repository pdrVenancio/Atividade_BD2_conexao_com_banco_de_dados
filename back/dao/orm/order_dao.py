from models.models import Employees
from models.models import Customers
from models.models import Orders
from models.models import OrderDetails
from models.models import Products


class OrderDAO:
    def __init__(self, session):
        self.session = session

    def insert(self, order: Orders):
        self.session.add(order)
        self.session.commit()
        return order.orderid

    def get_by_id(self, orderid):
        response  = self.session.query(Orders, Customers, Employees)\
        .join(Customers, Orders.customerid == Customers.customerid, isouter=True)\
        .join(Employees, Orders.employeeid == Employees.employeeid, isouter=True)\
        .filter(Orders.orderid == orderid)\
        .first()
        return response    

    def get_all(self):
        return self.session.query(Orders).all()
