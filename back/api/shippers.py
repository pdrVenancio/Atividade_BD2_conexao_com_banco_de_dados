
from flask import Blueprint, request, jsonify
# from controllers.order_controller import create_order_driver
from config.db_config import get_db_connection    # Conexão com o banco de dados sem orm
from dao.orm.shippers_dao import ShippDAO
from app import engine
from sqlalchemy.orm import sessionmaker

# Criando a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

shipp_bp = Blueprint('shipp', __name__, url_prefix='/api')


@shipp_bp.route('/shipp-get-all', methods=['GET'])
def get_all_shipp():
    try:
        shipp_dao = ShippDAO(session)
        response = shipp_dao.get_all()

        navios = []
        for shipp in response:
            shipp_dict = {
                "shipperid": shipp.shipperid,
                "companyname": shipp.companyname,
            }
            navios.append(shipp_dict)

        return jsonify({"shipps": navios}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500