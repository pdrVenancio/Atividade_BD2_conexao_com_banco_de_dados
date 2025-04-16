from models.models import Customers

class CustomerDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Customers).all()


    
    
