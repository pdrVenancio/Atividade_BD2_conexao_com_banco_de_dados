from flask import Blueprint, jsonify
from config.db_config import get_db_connection  
from dao.orm.product_dao import ProductDAO as ProductDAO_ORM
from dao.drive.product_dao import ProductDAO as ProductDAO_DRIVE
from app import engine
from sqlalchemy.orm import sessionmaker

# Criando a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session_ORM = Session()

#Criando sessão com Drive
session_DRIVE = get_db_connection()

product_bp = Blueprint('product', __name__, url_prefix='/api')

@product_bp.route('/orm-product-get-all', methods=['GET'])
def get_all_product_orm():
    try:
        product_dao = ProductDAO_ORM(session_ORM)
        response = product_dao.get_all()

        produtos = []
        for product in response:
            product_dict = {
                "productid": product.productid,
                "productname": product.productname,
                "unitprice" : product.unitprice
            }
            produtos.append(product_dict)

        return jsonify(produtos), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@product_bp.route('/drive-product-get-all', methods=['GET'])
def get_all_product_drive():
    try:
        product_dao = ProductDAO_DRIVE(session_DRIVE)
        response = product_dao.get_all()

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500