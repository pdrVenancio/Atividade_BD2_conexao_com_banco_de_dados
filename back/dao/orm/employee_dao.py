from sqlalchemy import DateTime,func
from models.models import Employees
from models.models import OrderDetails
from models.models import Orders

class EmployeeDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        employees = self.session.query(Employees).all()
        return employees
    
    def get_employee_ranking(self, start_date, end_date):
        rankings = self.session.query(

            Employees.firstname,
            Employees.lastname,
            func.count(Orders.orderid).label('pedidos_qtd'),
            func.sum(OrderDetails.quantity).label('soma_qtd_produtos'),
            func.sum(OrderDetails.unitprice * OrderDetails.quantity).label('valor_total')
        )\
        .select_from(Orders)\
        .outerjoin(OrderDetails, Orders.orderid == OrderDetails.orderid)\
        .outerjoin(Employees, Orders.employeeid == Employees.employeeid)\
        .filter(func.cast(Orders.orderdate, DateTime) >= func.cast(start_date, DateTime), 
                func.cast(Orders.orderdate, DateTime) <= func.cast(end_date, DateTime))\
        .group_by(Employees.firstname, Employees.lastname)\
        .order_by(func.sum(OrderDetails.unitprice * OrderDetails.quantity).desc())\
        .all()

        return rankings
