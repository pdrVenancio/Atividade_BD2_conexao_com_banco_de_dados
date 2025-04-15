from models.customer import CustomerORM

class CustomerDAO:
    def __init__(self, session):
        self.session = session

    def get_by_id(self, customerid):
        return self.session.query(CustomerORM).get(customerid)

    def get_all(self):
        return self.session.query(CustomerORM).all()

    def insert(self, customer: CustomerORM):
        self.session.add(customer)
        self.session.commit()
