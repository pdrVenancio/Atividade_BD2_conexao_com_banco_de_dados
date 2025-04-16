from models.models import Employees
from models.models import Customers
from models.models import Orders
from models.models import OrderDetails
from models.models import Products


class OrderDAO:
    def __init__(self, session):
        self.session = session

    def insert(self, order: Orders):
        # pedgo o ultimo id criado
        last_order = self.session.query(Orders).order_by(Orders.orderid.desc()).first()
        next_id = last_order.orderid + 1 

        order.orderid = next_id  
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
