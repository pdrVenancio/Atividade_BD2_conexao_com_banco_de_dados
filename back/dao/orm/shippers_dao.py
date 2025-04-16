from models.models import Shippers

class ShippDAO:
    def __init__(self, session):
        self.session = session
    
    def get_all(self):
        return self.session.query(Shippers).all()

