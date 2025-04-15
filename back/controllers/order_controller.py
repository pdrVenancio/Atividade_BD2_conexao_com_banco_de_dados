from dao.drive.customer_dao import CustomerDAO
from dao.drive.employee_dao import EmployeeDAO
from dao.drive.order_dao import OrderDAO
from dao.drive.order_detail_dao import OrderDetailDAO
from models.models import Orders
from models.models import OrderDetails

def create_order_driver(data, conn):
    """
    Cria um novo pedido utilizando psycopg2 (driver).
    data: dicionário com os dados do pedido
    conn: conexão psycopg2
    """
    try:
        customer_dao = CustomerDAO(conn)
        employee_dao = EmployeeDAO(conn)
        order_dao = OrderDAO(conn)

        # 1. Validar cliente
        customer = customer_dao.get_by_id(data["customerid"])
        if not customer:
            return {"error": "Cliente não encontrado"}, 404

        # 2. Validar funcionário
        employee = employee_dao.get_by_id(data["employeeid"])
        if not employee:
            return {"error": "Funcionário não encontrado"}, 404

        # 3. Criar pedido
        order = Orders(
            customerid=data["customerid"],
            employeeid=data["employeeid"],
            orderdate=data.get("orderdate"),
            requireddate=data.get("requireddate"),
            shippeddate=data.get("shippeddate"),
            shipvia=data.get("shipvia"),
            freight=data.get("freight"),
            shipname=data.get("shipname"),
            shipaddress=data.get("shipaddress"),
            shipcity=data.get("shipcity"),
            shipregion=data.get("shipregion"),
            shippostalcode=data.get("shippostalcode"),
            shipcountry=data.get("shipcountry")
        )

        # 4. Adicionar itens
        for item in data["items"]:
            detail = OrderDetails(
                productid=item["productid"],
                unitprice=item["unitprice"],
                quantity=item["quantity"],
                discount=item.get("discount", 0)
            )
            order.add_order_detail(detail)

        # 5. Inserir pedido e detalhes
        order_id = order_dao.insert(order)

        return {"message": "Pedido criado com sucesso", "orderid": order_id}, 201

    except Exception as e:
        return {"error": str(e)}, 500
