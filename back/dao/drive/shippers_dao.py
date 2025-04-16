class ShippDAO:
    def __init__(self, conn):
        self.conn = conn

    def get_all(self):
        shippers = []
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM northwind.shippers")
            metadata_colunas_orders = [desc[0] for desc in cur.description]
            for item in cur:
                dicionario = dict(zip(metadata_colunas_orders, item))
                shippers.append(dicionario)
        return shippers
