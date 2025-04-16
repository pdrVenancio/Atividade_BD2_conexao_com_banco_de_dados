from models.models import Orders

class OrderDAO:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, order: Orders):
        with self.conn.cursor() as cur:
            cur.execute("SELECT MAX(orderid) FROM northwind.orders")
            last_id_order = cur.fetchone()[0]
            new_order_id = int(last_id_order) + 1
            cur.execute("""
            INSERT INTO northwind.orders (
                orderid,
                customerid,
                employeeid,
                orderdate,
                requireddate,
                shippeddate,
                freight,
                shipname,
                shipaddress,
                shipcity,
                shipregion,
                shippostalcode,
                shipcountry
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, (
            new_order_id,
            order.customerid,
            order.employeeid,
            order.orderdate,
            order.requireddate,
            order.shippeddate,
            order.freight,
            order.shipname,
            order.shipaddress,
            order.shipcity,
            order.shipregion,
            order.shippostalcode,
            order.shipcountry
        ))

            return  new_order_id

    def get_by_id(self, orderid):
        order = []
        with self.conn.cursor() as cur:
            cur.execute(f"""SELECT 
                ord.orderdate,
                ord.orderid,
                cus.companyname,
                emp.firstname,
                emp.lastname	
            FROM northwind.orders ord
            LEFT JOIN northwind.customers cus ON ord.customerid = cus.customerid
            LEFT JOIN northwind.employees emp ON ord.employeeid = emp.employeeid 
            WHERE ord.orderid = {orderid}""")
            metadata = [desc[0] for desc in cur.description]
            for row in cur.fetchall():
                order.append(dict(zip(metadata, row)))
        return order