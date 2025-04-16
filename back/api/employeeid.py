from flask import Blueprint, request, jsonify
# from controllers.order_controller import create_order_driver
from config.db_config import get_db_connection    # Conexão com o banco de dados sem orm
from dao.orm.employee_dao import EmployeeDAO as EmployeeDAO_ORM
from dao.drive.employee_dao import EmployeeDAO as EmployeeDAO_DRIVE
from app import engine
from sqlalchemy.orm import sessionmaker

# Criando a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session_ORM = Session()

#Criando sessão com Drive
session_DRIVE = get_db_connection()

employee_bp = Blueprint('employee', __name__, url_prefix='/api')

@employee_bp.route('/orm-employee-get-all', methods=['GET'])
def get_employee():
    try:
        employee_dao = EmployeeDAO_ORM(session_ORM)

        response =  employee_dao.get_all()

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
    
@employee_bp.route('/drive-employee-get-all', methods=['GET'])
def get_employee_drive():
    try:
        employee_dao = EmployeeDAO_DRIVE(session_DRIVE)

        response =  employee_dao.get_all()

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

