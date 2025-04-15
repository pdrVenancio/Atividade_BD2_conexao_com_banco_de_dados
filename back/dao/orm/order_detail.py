from models.order_detail import OrderDetailORM
from models.product import ProductORM

class OrderDetailDAO:
    def __init__(self, session):
        self.session = session

    def insert(self, detail: OrderDetailORM):
        self.session.add(detail)
        self.session.commit()

    def get_by_order_id(self, orderid):
        response = self.session.query(OrderDetailORM, ProductORM)\
            .join(ProductORM, ProductORM.productid == OrderDetailORM.productid)\
            .filter(OrderDetailORM.orderid == orderid)\
            .all()
        print(response)
        return response 
    def delete_by_order_id(self, orderid):
        self.session.query(OrderDetailORM).filter_by(orderid=orderid).delete()
        self.session.commit()
