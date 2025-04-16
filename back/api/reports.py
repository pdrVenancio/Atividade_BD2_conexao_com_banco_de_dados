from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from config.db_config import get_db_connection
from app import engine
from dao.orm.employee_dao import EmployeeDAO as EmployeeDAO_ORM
from dao.drive.employee_dao import EmployeeDAO as EmployeeDAO_DRIVE
from datetime import datetime

# Criando a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session_ORM = Session()

#Criando sessão com Drive
session_DRIVE = get_db_connection()

reports_bp = Blueprint('reports', __name__, url_prefix='/api')

# O ranking é baseado no valor total vendido
# ?start_date=1996-01-01&end_date=1996-12-31
@reports_bp.route('/orm-employee-ranking', methods=['GET'])
def get_employee_ranking_orm():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not start_date or not end_date:
            return jsonify({"error": "Parâmetros de data ausentes"}), 400
        
        # Ajustando as datas para o formato 'YYYY-MM-DD HH:MM:SS'
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d 00:00:00')
            end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d 23:59:59')
        except ValueError:
            return jsonify({"error": "Formato de data inválido. Use o formato 'YYYY-MM-DD'."}), 400

        employee_dao = EmployeeDAO_ORM(session_ORM)
        response = employee_dao.get_employee_ranking(start_date, end_date)

        rankings = [
            {
                "position": i + 1,
                "firstname": row.firstname,
                "lastname": row.lastname,
                "soma_qtd_produtos": row.soma_qtd_produtos,
                "pedidos_qtd": row.pedidos_qtd,
                "valor_total": float(row.valor_total) 
            }
            for i, row in enumerate(response)
        ]
        
        
        if not rankings:
            return jsonify({"message": "Nenhum funcionário encontrado para o intervalo de tempo fornecido."}), 404
        
        return jsonify(rankings), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# O ranking é baseado no valor total vendido
# ?start_date=1996-01-01&end_date=1996-12-31
@reports_bp.route('/drive-employee-ranking', methods=['GET'])
def get_employee_ranking_drive():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not start_date or not end_date:
            return jsonify({"error": "Parâmetros de data ausentes"}), 400
            
        # Ajustando as datas para o formato 'YYYY-MM-DD HH:MM:SS'
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d 00:00:00')
            end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d 23:59:59')
        except ValueError:
            return jsonify({"error": "Formato de data inválido. Use o formato 'YYYY-MM-DD'."}), 400

        employee_dao = EmployeeDAO_DRIVE(session_DRIVE)
        response = employee_dao.get_employee_ranking(start_date, end_date)

        if not response:
            return jsonify({"message": "Nenhum funcionário encontrado para o intervalo de tempo fornecido."}), 404
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

