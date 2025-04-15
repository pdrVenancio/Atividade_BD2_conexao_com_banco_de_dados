class OrderModel:
    """Modelo simplificado para uso com psycopg2 (sem ORM)"""
    
    def __init__(self, order_id=None, customer_id=None, employee_id=None, order_date=None):
        self.order_id = order_id
        self.customer_id = customer_id
        self.employee_id = employee_id
        self.order_date = order_date
    
    def to_dict(self):
        return {
            'order_id': self.order_id,
            'customer_id': self.customer_id,
            'employee_id': self.employee_id,
            'order_date': str(self.order_date) if self.order_date else None
        }

class CustomerModel:
    """Modelo simplificado para clientes"""
    
    def __init__(self, customer_id=None, company_name=None):
        self.customer_id = customer_id
        self.company_name = company_name
    
    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'company_name': self.company_name
        }

# ... (outros modelos conforme necessidade)