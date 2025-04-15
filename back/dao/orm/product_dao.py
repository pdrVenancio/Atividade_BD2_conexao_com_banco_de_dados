from models.product import ProductORM

class ProductDAO:
    def __init__(self, session):
        self.session = session

    def get_by_id(self, product_id):
        return self.session.query(ProductORM).get(product_id)
