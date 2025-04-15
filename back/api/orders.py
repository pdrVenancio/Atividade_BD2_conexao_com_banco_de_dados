from flask import Blueprint, request, jsonify
from controllers.order_controller import create_order_driver
from config.db_config import get_db_connection    # Conexão com o banco de dados sem orm
from dao.orm.order_dao import OrderDAO
from app import engine
from sqlalchemy.orm import sessionmaker

# Criando a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

orders_bp = Blueprint('orders', __name__, url_prefix='/api')

@orders_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()  # Recebe os dados em formato JSON
    return create_order_driver(data, session)

@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id): 
    try:
        order_dao = OrderDAO(session)
        
        response = order_dao.get_by_id(order_id)

        order, customer, employee = response
        order_dict = {
            "order": {
                "orderid": order.orderid,
                "customerid": order.customerid,
                "date": str(order.orderdate)  # converter datetime para string
            },
            "customer": {
                "customerid": customer.customerid,
                "companyname": customer.companyname
            },
            "employee": {
                "employeeid": employee.employeeid,
                "firstname": employee.firstname,
                "lastname": employee.lastname
            }
        }

        if not order_dict:
            return jsonify({"error": "Pedido não encontrado"}), 404
        return jsonify(order_dict), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
