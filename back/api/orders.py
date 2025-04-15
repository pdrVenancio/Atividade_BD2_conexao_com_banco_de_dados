from flask import Blueprint, request, jsonify
from controllers.order_controller import create_order_driver
from config.db_config import get_db_connection    # Conexão com o banco de dados

orders_bp = Blueprint('orders', __name__, url_prefix='/api')

@orders_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()  # Recebe os dados em formato JSON
    return create_order_driver(data, get_db_connection)

@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    # Adicione a lógica para buscar um pedido pelo ID
    # Exemplo: chamando um método no OrderDAO ou Controller para obter o pedido
    try:
        order_dao = OrderDAO(get_db_connection)
        order = order_dao.get_by_id(order_id)
        if not order:
            return jsonify({"error": "Pedido não encontrado"}), 404
        return jsonify(order.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
