from models.models import OrderDetails

class OrderDetailDAO:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, detail: OrderDetails):
        with self.conn.cursor() as cur:
            cur.execute("SELECT MAX(orderid) FROM northwind.orders")
            last_id_order = cur.fetchone()[0]
            new_order_id = int(last_id_order)

            cur.execute("""
            INSERT INTO northwind.order_details (
                orderid, productid, unitprice, quantity, discount
            ) VALUES (%s, %s, %s, %s, %s)
            """, (
                new_order_id,
                detail.productid,
                detail.unitprice,
                detail.quantity,
                detail.discount
            ))
            return new_order_id

            # cur.execute(f"""
            #         INSERT INTO northwind.order_details (
            #             orderid, productid, unitprice, quantity, discount
            #         ) VALUES ('{new_order_id}, '{detail.productid}, '{detail.unitprice}, '{detail.quantity}, '{detail.discount})
            #     """)
            # return new_order_id

        
    def get_by_order_id(self, orderid):
        details = []
        with self.conn.cursor() as cur:
            cur.execute(f"""
                    SELECT *
                    FROM northwind.order_details
                    WHERE orderid = {orderid}
                """)
            metadata_colunas_orders = [desc[0] for desc in cur.description]
            for item in cur:
                dicionario = dict(zip(metadata_colunas_orders, item))
                details.append(dicionario)
            return details

