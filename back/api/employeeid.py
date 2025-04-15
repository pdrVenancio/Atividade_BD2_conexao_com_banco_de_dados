from flask import Blueprint, request, jsonify
# from controllers.order_controller import create_order_driver
from config.db_config import get_db_connection    # Conexão com o banco de dados sem orm
from dao.orm.employee_dao import EmployeeDAO
from app import engine
from sqlalchemy.orm import sessionmaker

# Criando a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

employee_bp = Blueprint('employee', __name__, url_prefix='/api')

@employee_bp.route('/employee-get-all', methods=['GET'])
def get_employee():
    try:
        employee_dao = EmployeeDAO(session)

        response =  employee_dao.get_all(session)

        employees = []
        for emp in response:
            emp_dic = {
                "employeeid" :emp.employeeid,
                "lastname" :emp.lastname,
                "firstname" :emp.firstname
            } 
            employees.append(emp_dic)


        return jsonify(employees), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
