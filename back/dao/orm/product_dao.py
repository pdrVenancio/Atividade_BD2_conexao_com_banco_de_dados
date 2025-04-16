from models.models import Products

class ProductDAO:
    def __init__(self, session):
        self.session = session
    
    def get_all(self):
        return self.session.query(Products).all()
