from models.models import Shippers

class ShippDAO:
    def __init__(self, session):
        self.session = session

    def get_by_id(self, shipp_id):
        return self.session.query(Shippers).get(shipp_id)
    
    def get_all(self):
        return self.session.query(Shippers).all()

    def insert(self, shipp : Shippers):
        self.session.add(shipp)
        self.session.commit()
        return shipp.shipperid