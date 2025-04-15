from flask import Blueprint, request, jsonify
from dao.orm.customer_dao import CustomerDAO
from config.db_config import get_db_connection
from app import engine
from sqlalchemy.orm import sessionmaker
# Criando a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

customers_bp = Blueprint('customers', __name__, url_prefix='/api')

@customers_bp.route('/customers-get-all', methods=['GET'])
def list_customers():
    try:
        customer_dao = CustomerDAO(session)
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

# @customers_bp.route('/customers/<int:customer_id>', methods=['GET'])
# def get_customer(customer_id):
#     try:
#         customer_dao = CustomerDAO(session)
#         customer = customer_dao.get_by_id(customer_id)
#         if not customer:
#             return jsonify({"error": "Cliente não encontrado"}), 404
#         return jsonify(customer.to_dict()), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
