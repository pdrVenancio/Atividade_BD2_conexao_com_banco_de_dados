import psycopg2
from sqlalchemy.orm import Session
from models.northwind import Order, OrderDetail
from dao.base_dao import BaseDAO

class OrderDAOPsycopg(BaseDAO):
    """Implementação usando psycopg2 (Driver puro)"""
    
    def __init__(self, connection):
        self.conn = connection
    
    def create_order(self, order_data, unsafe=False):
        with self.conn.cursor() as cursor:
            if unsafe:
                # Versão vulnerável a SQL Injection
                query = f"""
                INSERT INTO orders (customer_id, employee_id, order_date)
                VALUES ('{order_data["customer_id"]}', 
                        '{order_data["employee_id"]}', 
                        '{order_data["order_date"]}')
                RETURNING order_id
                """
            else:
                # Versão segura
                query = """
                INSERT INTO orders (customer_id, employee_id, order_date)
                VALUES (%s, %s, %s)
                RETURNING order_id
                """
                params = (
                    order_data["customer_id"],
                    order_data["employee_id"],
                    order_data["order_date"]
                )
            
            cursor.execute(query, params if not unsafe else None)
            order_id = cursor.fetchone()[0]
            self.conn.commit()
            return order_id
    
    def get_order_details(self, order_id):
        with self.conn.cursor() as cursor:
            query = """
            SELECT o.order_id, o.order_date, c.company_name, 
                   e.first_name || ' ' || e.last_name as employee_name,
                   p.product_name, od.quantity, od.unit_price
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN employees e ON o.employee_id = e.employee_id
            JOIN order_details od ON o.order_id = od.order_id
            JOIN products p ON od.product_id = p.product_id
            WHERE o.order_id = %s
            """
            cursor.execute(query, (order_id,))
            return cursor.fetchall()

class OrderDAOSQLAlchemy(BaseDAO):
    """Implementação usando SQLAlchemy (ORM)"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_order(self, order_data):
        new_order = Order(
            customer_id=order_data["customer_id"],
            employee_id=order_data["employee_id"],
            order_date=order_data["order_date"]
        )
        self.session.add(new_order)
        self.session.commit()
        return new_order.order_id
    
    def get_order_details(self, order_id):
        order = self.session.query(Order).get(order_id)
        if not order:
            return None
        
        return {
            "order_id": order.order_id,
            "order_date": order.order_date,
            "customer_name": order.customer.company_name,
            "employee_name": f"{order.employee.first_name} {order.employee.last_name}",
            "items": [
                {
                    "product_name": detail.product.product_name,
                    "quantity": detail.quantity,
                    "unit_price": detail.unit_price
                } for detail in order.details
            ]
        }