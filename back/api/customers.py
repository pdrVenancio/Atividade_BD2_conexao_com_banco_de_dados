from flask import Blueprint, request, jsonify
from dao.drive.customer_dao import CustomerDAO
from config.db_config import get_db_connection

customers_bp = Blueprint('customers', __name__, url_prefix='/api')

@customers_bp.route('/customers', methods=['GET'])
def list_customers():
    try:
        customer_dao = CustomerDAO(get_db_connection)
        customers = customer_dao.get_all()
        return jsonify([customer.to_dict() for customer in customers]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@customers_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    try:
        customer_dao = CustomerDAO(get_db_connection)
        customer = customer_dao.get_by_id(customer_id)
        if not customer:
            return jsonify({"error": "Cliente não encontrado"}), 404
        return jsonify(customer.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
