from models.models import Products

class ProductDAO:
    def __init__(self, session):
        self.session = session

    def get_by_id(self, product_id):
        return self.session.query(Products).get(product_id)
    
    def get_all(self):
        return self.session.query(Products).all()

    # def insert(self, prod : Products):
    #     self.session.add(prod)
    #     self.session.commit()
    #     return prod.productid