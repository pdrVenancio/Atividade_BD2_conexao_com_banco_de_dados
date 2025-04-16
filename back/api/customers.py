from flask import Blueprint, request, jsonify
from dao.orm.customer_dao import CustomerDAO as CustomerDAO_ORM
from dao.drive.customer_dao import CustomerDAO as CustomerDAO_DRIVE
from config.db_config import get_db_connection
from app import engine
from sqlalchemy.orm import sessionmaker

# Criando a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session_ORM = Session()

#Criando sessão com Drive
session_DRIVE = get_db_connection()

customers_bp = Blueprint('customers', __name__, url_prefix='/api')

@customers_bp.route('/orm-customers-get-all', methods=['GET'])
def list_customers_orm():
    try:
        customer_dao = CustomerDAO_ORM(session_ORM)
        response = customer_dao.get_all()
        customers = []
        
        for custumer in response:
            cis_dic = {
                "customerid": custumer.customerid,
                "companyname": custumer.companyname
            }
            customers.append(cis_dic)

        return jsonify(customers), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@customers_bp.route('/drive-customers-get-all', methods=['GET'])
def list_customers_drive():
    try:
        customer_dao = CustomerDAO_DRIVE(session_DRIVE)
        response = customer_dao.get_all()
        print(response)
       
        if not response:
            return jsonify({"error": "Cliente não encontrado"}), 404
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
