from models.employee import EmployeeORM

class EmployeeDAO:
    def __init__(self, session):
        self.session = session

    def get_by_id(self, employeeid):
        return self.session.query(EmployeeORM).get(employeeid)

    def get_all(self):
        return self.session.query(EmployeeORM).all()
