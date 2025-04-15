from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from app import engine
from dao.orm.employee_dao import EmployeeDAO
from dao.orm.order_dao import OrderDAO
from datetime import datetime

# Criando a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

reports_bp = Blueprint('reports', __name__, url_prefix='/api')

@reports_bp.route('/order/<int:order_id>', methods=['GET'])
def get_order_report(order_id):
    try:
        # Utilizando o DAO com SQLAlchemy
        order_dao = OrderDAO(session)
        order = order_dao.get_by_id(order_id)
        
        if not order:
            return jsonify({"error": "Pedido não encontrado"}), 404

        return jsonify(order.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reports_bp.route('/employee-ranking', methods=['GET'])
def get_employee_ranking():
    try:
        # Recebendo as datas de início e fim como parâmetros de URL
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # Verificando se as datas foram fornecidas
        if not start_date or not end_date:
            return jsonify({"error": "Parâmetros de data ausentes"}), 400
        
        # Ajustando as datas para o formato 'YYYY-MM-DD HH:MM:SS'
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d 00:00:00')
            end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d 23:59:59')
        except ValueError:
            return jsonify({"error": "Formato de data inválido. Use o formato 'YYYY-MM-DD'."}), 400

        # Utilizando o DAO com SQLAlchemy
        employee_dao = EmployeeDAO(session)
        response = employee_dao.get_employee_ranking(start_date, end_date)

        rankings = [
            {
                "position": i + 1,
                "firstname": row.firstname,
                "lastname": row.lastname,
                "soma_qtd": row.soma_qtd,
                "valor_total": float(row.valor_total)  # Garantir que é serializável
            }
            for i, row in enumerate(response)
        ]
        
        
        if not rankings:
            return jsonify({"message": "Nenhum funcionário encontrado para o intervalo de tempo fornecido."}), 404
        
        return jsonify({"ranking": rankings}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
