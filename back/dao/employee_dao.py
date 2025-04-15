from dao.base_dao import BaseDAO

class EmployeeDAOPsycopg(BaseDAO):
    def __init__(self, connection):
        self.conn = connection
    
    # Implementações específicas para funcionários

class EmployeeDAOSQLAlchemy(BaseDAO):
    def __init__(self, session):
        self.session = session
    
    # Implementações específicas para funcionários