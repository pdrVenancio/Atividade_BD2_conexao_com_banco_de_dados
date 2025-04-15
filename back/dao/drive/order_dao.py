from models.models import Orders
from models.models import OrderDetails

class OrderDAO:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, order: Orders):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO orders (
                    customerid, employeeid, orderdate, requireddate, shippeddate,
                    freight, shipname, shipaddress, shipcity, shipregion,
                    shippostalcode, shipcountry
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING orderid
            """, (
                order.customerid, order.employeeid, order.orderdate, order.requireddate,
                order.shippeddate, order.freight, order.shipname,
                order.shipaddress, order.shipcity, order.shipregion,
                order.shippostalcode, order.shipcountry
            ))

            orderid = cur.fetchone()[0]

            # Inserir os detalhes do pedido (se houver)
            for detail in order.order_details:
                cur.execute("""
                    INSERT INTO order_details (
                        orderid, productid, unitprice, quantity, discount
                    ) VALUES (%s, %s, %s, %s, %s)
                """, (
                    orderid, detail.productid, detail.unitprice,
                    detail.quantity, detail.discount
                ))

            self.conn.commit()
            return orderid

    def get_by_id(self, orderid):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT orderid, customerid, employeeid, orderdate, requireddate,
                       shippeddate, shipvia, freight, shipname, shipaddress, 
                       shipcity, shipregion, shippostalcode, shipcountry
                FROM northwind.orders
                WHERE orderid = %s
            """, (orderid,))
            row = cur.fetchone()
            if not row:
                return None

            order = Order(*row)

            # Carregar detalhes do pedido
            cur.execute("""
                SELECT productid, unitprice, quantity, discount
                FROM northwind.order_details
                WHERE orderid = %s
            """, (orderid,))
            details = cur.fetchall()
            for d in details:
                detail = OrderDetails(orderid=orderid, *d)
                order.add_order_detail(detail)

            return order

    def get_all(self):
        orders = []
        with self.conn.cursor() as cur:
            cur.execute("SELECT orderid FROM orders")
            ids = cur.fetchall()
            for (orderid,) in ids:
                order = self.get_by_id(orderid)
                if order:
                    orders.append(order)
        return orders
