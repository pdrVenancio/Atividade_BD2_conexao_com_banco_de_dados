from models.models import OrderDetails
from models.models import Products
from models.models import Orders

class OrderDetailDAO:
    def __init__(self, session):
        self.session = session

    def insert(self, detail: OrderDetails):
        try:
            last_order = self.session.query(Orders).order_by(Orders.orderid.desc()).first()
            detail.orderid = last_order.orderid
            self.session.add(detail)
            self.session.commit()
            return detail.orderid
        except Exception as e:
            self.session.rollback()
            return 'Erro ao inserir'

    def get_by_order_id(self, orderid):
        response = self.session.query(OrderDetails, Products)\
                        .join(Products, Products.productid == OrderDetails.productid)\
                        .filter(OrderDetails.orderid == orderid)\
                        .all()
        print(response)
        return response 
    
    def delete_by_order_id(self, orderid):
        self.session.query(OrderDetails).filter_by(orderid=orderid).delete()
        self.session.commit()
