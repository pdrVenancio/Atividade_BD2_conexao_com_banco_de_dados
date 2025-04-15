import psycopg2
from models.product import Product

class ProductDAO:
    def __init__(self, conn):
        self.conn = conn

    def get_by_id(self, product_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM northwind.products WHERE productid = %s", (product_id,))
            row = cur.fetchone()
            if row:
                return Product(*row)
        return None
