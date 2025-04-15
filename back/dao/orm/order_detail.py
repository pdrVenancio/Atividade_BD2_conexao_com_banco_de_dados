from models.order_detail import OrderDetailORM

class OrderDetailDAO:
    def __init__(self, session):
        self.session = session

    def insert(self, detail: OrderDetailORM):
        self.session.add(detail)
        self.session.commit()

    def get_by_order_id(self, orderid):
        return self.session.query(OrderDetailORM).filter_by(orderid=orderid).all()

    def delete_by_order_id(self, orderid):
        self.session.query(OrderDetailORM).filter_by(orderid=orderid).delete()
        self.session.commit()
