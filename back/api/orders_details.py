from flask import Blueprint, request, jsonify
from controllers.order_controller import create_order_driver
from config.db_config import get_db_connection    # Conexão com o banco de dados sem orm
from dao.orm.order_detail import OrderDetailDAO
from models.models import OrderDetails
from app import engine
from sqlalchemy.orm import sessionmaker

# Criando a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

orders_details_bp = Blueprint('orders_details', __name__, url_prefix='/api')



# Exemplo de jsaon para inserção


@orders_details_bp.route('/order_details/insert', methods=['POST'])
def insert_order_details():
    try:
        data = request.get_json()
        order_detail_dao = OrderDetailDAO(session)

        orders_details = OrderDetails(**data)

        response =  order_detail_dao.insert(orders_details)
        return jsonify({"order_details": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@orders_details_bp.route('/orders_details/<int:order_id>', methods=['GET'])
def get_order(order_id): 
    try:
        order_details_dao = OrderDetailDAO(session)
        
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
