from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from controllers import OrderController

# 1. Configuração da conexão (substitua user/pass)
engine = create_engine('postgresql://postegres:root@localhost/northwind')
Session = sessionmaker(bind=engine)
session = Session()

# 2. Instancia o controller
controller = OrderController(use_orm=True, db_connection=session)

# 3. Teste de criação de pedido
print("=== TESTE DE CRIAÇÃO DE PEDIDO ===")
try:
    order_data = {
        'customer_id': 'ALFKI',  # ID válido do Northwind
        'employee_id': 1,        # ID válido de employee
        'order_date': '2023-11-20'
    }
    order_id = controller.create_order(order_data)
    print(f" Pedido criado com sucesso! ID: {order_id}")
except Exception as e:
    print(f"Falha ao criar pedido: {e}")

# 4. Teste de relatório
print("\n=== TESTE DE RELATÓRIO ===")
try:
    ranking = controller.get_employee_ranking('1996-01-01', '1996-12-31')  # Período com dados no Northwind
    print("Ranking de Funcionários:")
    for emp in ranking:
        print(f"  {emp['employee_name']}: {emp['total_sales']:.2f} (pedidos: {emp['total_orders']})")
except Exception as e:
    print(f"Falha ao gerar relatório: {e}")

# 5. Fecha a sessão
session.close()