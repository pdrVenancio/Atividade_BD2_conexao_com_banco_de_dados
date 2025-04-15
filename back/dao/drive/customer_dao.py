from models.customer import Customer

class CustomerDAO:
    def __init__(self, conn):
        self.conn = conn

    def get_by_id(self, customerid):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT customerid, companyname, contactname, contacttitle,
                       address, city, region, postalcode, country, phone, fax
                FROM customers
                WHERE customerid = %s
            """, (customerid,))
            row = cur.fetchone()
            if row:
                return Customer(*row)
        return None

    def get_all(self):
        customers = []
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM customers")
            rows = cur.fetchall()
            for row in rows:
                customers.append(Customer(*row))
        return customers

    def insert(self, customer: Customer):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO customers (
                    customerid, companyname, contactname, contacttitle,
                    address, city, region, postalcode, country, phone, fax
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                customer.customerid, customer.companyname, customer.contactname,
                customer.contacttitle, customer.address, customer.city,
                customer.region, customer.postalcode, customer.country,
                customer.phone, customer.fax
            ))
            self.conn.commit()
