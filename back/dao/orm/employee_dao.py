from sqlalchemy.orm import sessionmaker
from sqlalchemy import DateTime,func
from models.employee import EmployeeORM
from models.order_detail import OrderDetailORM
from models.order import OrderORM

class EmployeeDAO:
    def __init__(self, session):
        self.session = session

    def get_by_id(self, employeeid):
        """Busca um funcionário pelo ID."""
        employee = self.session.query(EmployeeORM).filter(EmployeeORM.employeeid == employeeid).first()
        return employee

    def get_all(self):
        """Retorna todos os funcionários."""
        employees = self.session.query(EmployeeORM).all()
        return employees
    
    def get_employee_ranking(self, start_date, end_date):
        """
        Retorna o ranking dos funcionários com base no intervalo de tempo fornecido.
        """
        rankings = self.session.query(

            EmployeeORM.firstname,
            EmployeeORM.lastname,
            func.sum(OrderDetailORM.quantity).label('soma_qtd'),
            func.sum(OrderDetailORM.unitprice * OrderDetailORM.quantity).label('valor_total')
        )\
        .select_from(OrderORM)\
        .outerjoin(OrderDetailORM, OrderORM.orderid == OrderDetailORM.orderid)\
        .outerjoin(EmployeeORM, OrderORM.employeeid == EmployeeORM.employeeid)\
        .filter(func.cast(OrderORM.orderdate, DateTime) >= func.cast(start_date, DateTime), 
                func.cast(OrderORM.orderdate, DateTime) <= func.cast(end_date, DateTime))\
        .group_by(EmployeeORM.firstname, EmployeeORM.lastname)\
        .order_by(func.sum(OrderDetailORM.unitprice * OrderDetailORM.quantity).desc())\
        .all()

        return rankings
