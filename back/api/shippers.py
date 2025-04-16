
from flask import Blueprint, jsonify
from config.db_config import get_db_connection    # Conexão com o banco de dados sem orm
from dao.orm.shippers_dao import ShippDAO as ShippDAO_ORM
from dao.drive.shippers_dao import ShippDAO as ShippDAO_DRIVE
from app import engine
from sqlalchemy.orm import sessionmaker

# Criando a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session_ORM = Session()

#Criando sessão com Drive
session_DRIVE = get_db_connection()

shipp_bp = Blueprint('shipp', __name__, url_prefix='/api')


@shipp_bp.route('/orm-shipp-get-all', methods=['GET'])
def get_all_shipp():
    try:
        shipp_dao = ShippDAO_ORM(session_ORM)
        response = shipp_dao.get_all()

        navios = []
        for shipp in response:
            shipp_dict = {
                "shipperid": shipp.shipperid,
                "companyname": shipp.companyname,
            }
            navios.append(shipp_dict)

        return jsonify(navios), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@shipp_bp.route('/drive-shipp-get-all', methods=['GET'])
def get_all_shipp_drive():
    try:
        shipp_dao = ShippDAO_DRIVE(session_DRIVE)
        response = shipp_dao.get_all()

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500