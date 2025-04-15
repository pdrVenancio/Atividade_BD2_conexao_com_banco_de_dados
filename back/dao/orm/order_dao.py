from models.order import OrderORM
from models.order_detail import OrderDetailORM

class OrderDAO:
    def __init__(self, session):
        self.session = session

    def insert(self, order: OrderORM):
        self.session.add(order)
        self.session.commit()
        return order.orderid

    def get_by_id(self, orderid):
        return self.session.query(OrderORM).filter_by(orderid=orderid).first()

    def get_all(self):
        return self.session.query(OrderORM).all()
