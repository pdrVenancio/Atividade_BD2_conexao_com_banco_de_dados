from flask import Blueprint, request, jsonify
from config.db_config import get_db_connection    # Conexão com o banco de dados sem orm
from dao.orm.order_detail import OrderDetailDAO as OrderDetailDAO_ORM
from dao.drive.order_detail_dao import OrderDetailDAO as OrderDetailDAO_DRIVE
from models.models import OrderDetails
from app import engine
from sqlalchemy.orm import sessionmaker

# Criando a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session_ORM = Session()

#Criando sessão com Drive
session_DRIVE = get_db_connection()

orders_details_bp = Blueprint('orders_details', __name__, url_prefix='/api')

# Exemplo de json para inserção
# {
#     "productid": 1,
#     "unitprice": 18.0,
#     "quantity": 5,
#     "discount": 0.1
# }

@orders_details_bp.route('/orm-order_details/insert', methods=['POST'])
def insert_order_details_orm():
    try:
        data = request.get_json()
        order_detail_dao = OrderDetailDAO_ORM(session_ORM)

        orders_details = OrderDetails(**data)

        response =  order_detail_dao.insert(orders_details)
        return jsonify({"order_details": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@orders_details_bp.route('/orm-orders_details/<int:order_id>', methods=['GET'])
def get_order_detail_orm(order_id): 
    try:
        order_details_dao = OrderDetailDAO_ORM(session_ORM)
        
        response = order_details_dao.get_by_order_id(order_id)

        produtos = []
        for order_detail, product in response:
            order_detail_dict = {
                "orderid": order_detail.orderid,
                "productid": order_detail.productid,
                "quantity": order_detail.quantity,
                "product_name": product.productname,
                "product_price": product.unitprice
            }
            produtos.append(order_detail_dict)
        

        if not produtos:
            return jsonify({"error": "Pedido não encontrado"}), 404
        return jsonify(produtos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@orders_details_bp.route('/drive-order_details/insert', methods=['POST'])
def insert_order_details_drive():
    try:
        data = request.get_json()
        order_detail_dao = OrderDetailDAO_DRIVE(session_DRIVE)

        orders_details = OrderDetails(**data)

        response =  order_detail_dao.insert(orders_details )
        return jsonify({"order_details": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@orders_details_bp.route('/drive-orders_details/<int:order_id>', methods=['GET'])
def get_order_detail_drive(order_id): 
    try:
        order_details_dao = OrderDetailDAO_DRIVE(session_DRIVE)
        
        response = order_details_dao.get_by_order_id(order_id)

        if not response:
            return jsonify({"error": "Pedido não encontrado"}), 404
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500