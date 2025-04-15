from models.models import Customers

class CustomerDAO:
    def __init__(self, session):
        self.session = session

    def get_by_id(self, customerid):
        return self.session.query(Customers).get(customerid)

    def get_all(self):
        return self.session.query(Customers).all()

    def insert(self, customer: Customers):
        self.session.add(customer)
        self.session.commit()
    
    
