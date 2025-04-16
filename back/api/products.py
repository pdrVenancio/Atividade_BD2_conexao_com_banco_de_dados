from flask import Blueprint, request, jsonify
# from controllers.order_controller import create_order_driver
from config.db_config import get_db_connection    # Conexão com o banco de dados sem orm
from dao.orm.product_dao import ProductDAO
from app import engine
from sqlalchemy.orm import sessionmaker

# Criando a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

product_bp = Blueprint('product', __name__, url_prefix='/api')

# @product_bp.route('/product-insert', methods=['POST'])
# def create_order():
#     try:
#         data = request.get_json()
#         order_dao = ProductDAO(session)

#         response =  order_dao.insert(data,session)
#         return jsonify({"product": response}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@product_bp.route('/product-get-all', methods=['GET'])
def get_all_product():
    try:
        product_dao = ProductDAO(session)
        response = product_dao.get_all()

        produtos = []
        for product in response:
            product_dict = {
                "productid": product.productid,
                "productname": product.productname,
                "unitprice" : product.unitprice
            }
            produtos.append(product_dict)

        return jsonify({"products": produtos}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500