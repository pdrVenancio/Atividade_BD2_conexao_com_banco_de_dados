from abc import ABC, abstractmethod

class BaseDAO(ABC):
    @abstractmethod
    def create_order(self, order_data):
        pass
    
    @abstractmethod
    def get_order_details(self, order_id):
        pass
    
    @abstractmethod
    def get_employee_ranking(self, start_date, end_date):
        pass