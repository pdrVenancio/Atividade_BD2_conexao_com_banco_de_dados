from models.order_detail import OrderDetail

class OrderDetailDAO:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, detail: OrderDetail):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO northwind.order_details (
                    orderid, productid, unitprice, quantity, discount
                ) VALUES (%s, %s, %s, %s, %s)
            """, (
                detail.orderid, detail.productid, detail.unitprice,
                detail.quantity, detail.discount
            ))
        self.conn.commit()

    def get_by_order_id(self, orderid):
        details = []
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT orderid, productid, unitprice, quantity, discount
                FROM northwind.order_details
                WHERE orderid = %s
            """, (orderid,))
            rows = cur.fetchall()
            for row in rows:
                details.append(OrderDetail(*row))
        return details

    def delete_by_order_id(self, orderid):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM northwind.order_details WHERE orderid = %s", (orderid,))
        self.conn.commit()
