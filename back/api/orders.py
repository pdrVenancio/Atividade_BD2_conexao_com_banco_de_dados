from flask import Blueprint, request, jsonify
from config.db_config import get_db_connection   
from dao.orm.order_dao import OrderDAO as OrderDAO_ORM
from dao.drive.order_dao import OrderDAO as OrderDAO_DRIVE
from models.models import Orders 
from app import engine
from sqlalchemy.orm import sessionmaker

# Criando a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session_ORM = Session()

#Criando sessão com Drive
session_DRIVE = get_db_connection()

orders_bp = Blueprint('orders', __name__, url_prefix='/api')

# Exemplo de jsaon para inserção
# O id sera gerado altomaticamente

# {   
#   "customerid": "ALFKI",
#   "employeeid": 5,
#   "orderdate": "2025-04-15",
#   "requireddate": "2025-04-20",
#   "shippeddate": "2025-04-20",
#   "freight": 25.5,
#   "shipname": "Alfreds Futterkiste",
#   "shipaddress": "Obere Str. 57",
#   "shipcity": "Berlin",
#   "shipregion" : "Lara",
#   "shippostalcode" : "3508",
#   "shipcountry": "Germany",
#   "shipperid" : null
# }

@orders_bp.route('/orm-orders/insert', methods=['POST'])
def create_order_orm():
    try:
        data = request.get_json()  # Recebe os dados em formato JSON
        order_dao = OrderDAO_ORM(session_ORM)

        order = Orders(**data) 

        response =  order_dao.insert(order)
        return jsonify({"product": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@orders_bp.route('/orm-orders-get/<int:order_id>', methods=['GET'])
def get_order_orm(order_id): 
    try:
        order_dao = OrderDAO_ORM(session_ORM)
        
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

@orders_bp.route('/drive-orders/insert', methods=['POST'])
def create_order_drive():
    try:
        data = request.get_json() 
        order_dao = OrderDAO_DRIVE(session_DRIVE)

        order = Orders(**data) 

        response =  order_dao.insert(order)
        return jsonify({"product": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@orders_bp.route('/drive-orders-get/<int:order_id>', methods=['GET'])
def get_order_drive(order_id): 
    try:
        order_dao = OrderDAO_DRIVE(session_DRIVE)
        
        response = order_dao.get_by_id(order_id)

        if not response:
            return jsonify({"error": "Pedido não encontrado"}), 404
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
