from models.employee import EmployeeORM
from models.customer import CustomerORM
from models.order import OrderORM
from models.order_detail import OrderDetailORM
from models.product import ProductORM


class OrderDAO:
    def __init__(self, session):
        self.session = session

    def insert(self, order: OrderORM):
        self.session.add(order)
        self.session.commit()
        return order.orderid

    def get_by_id(self, orderid):
        response  = self.session.query(OrderORM, CustomerORM, EmployeeORM)\
        .join(CustomerORM, OrderORM.customerid == CustomerORM.customerid, isouter=True)\
        .join(EmployeeORM, OrderORM.employeeid == EmployeeORM.employeeid, isouter=True)\
        .filter(OrderORM.orderid == orderid)\
        .first()
        return response    

    def get_all(self):
        return self.session.query(OrderORM).all()
