
class CustomerDAO:
    def __init__(self, conn):
        self.conn = conn

    def get_all(self):  
        customers = []
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM northwind.customers")

            metadata_colunas_orders = [desc[0] for desc in cur.description]
            for item in cur:
                dicionario = dict(zip(metadata_colunas_orders, item))
                customers.append(dicionario)

            return customers