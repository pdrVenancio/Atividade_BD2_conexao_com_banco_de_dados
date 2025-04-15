from datetime import date
from sqlalchemy import func
from dao.base_dao import BaseDAO

class ReportDAOPsycopg:
    def __init__(self, connection):
        self.conn = connection
    
    def get_employee_ranking(self, start_date: date, end_date: date):
        with self.conn.cursor() as cursor:
            query = """
            SELECT e.first_name || ' ' || e.last_name as employee_name,
                   COUNT(o.order_id) as total_orders,
                   SUM(od.quantity * od.unit_price) as total_sales
            FROM employees e
            JOIN orders o ON e.employee_id = o.employee_id
            JOIN order_details od ON o.order_id = od.order_id
            WHERE o.order_date BETWEEN %s AND %s
            GROUP BY e.employee_id
            ORDER BY total_sales DESC
            """
            cursor.execute(query, (start_date, end_date))
            return cursor.fetchall()

class ReportDAOSQLAlchemy:
    def __init__(self, session):
        self.session = session
    
    def get_employee_ranking(self, start_date: date, end_date: date):
        result = self.session.query(
            Employee.first_name,
            Employee.last_name,
            func.count(Order.order_id).label('total_orders'),
            func.sum(OrderDetail.quantity * OrderDetail.unit_price).label('total_sales')
        ).join(Order).join(OrderDetail).filter(
            Order.order_date.between(start_date, end_date)
        ).group_by(Employee.employee_id).order_by(func.sum(OrderDetail.quantity * OrderDetail.unit_price).desc())
        
        return [
            {
                "employee_name": f"{first_name} {last_name}",
                "total_orders": total_orders,
                "total_sales": float(total_sales) if total_sales else 0.0
            } for first_name, last_name, total_orders, total_sales in result
        ]