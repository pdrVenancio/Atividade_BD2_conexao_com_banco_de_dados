
class EmployeeDAO:
    def __init__(self, conn):
        self.conn = conn

    def get_all(self):
        employees = []
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM northwind.employees")
            metadata_colunas_orders = [desc[0] for desc in cur.description]
            for item in cur:
                dicionario = dict(zip(metadata_colunas_orders, item))
                employees.append(dicionario)

            return employees
        
    
    def get_employee_ranking(self, start_date, end_date):
        """
        Retorna o ranking de funcionários com base no intervalo de tempo dado.
        """
        rankings = []
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    emp.employeeid,
                    emp.firstname,
                    emp.lastname,
                    COUNT(ord.orderid) AS qtd_pedidos,
                    SUM(ode.quantity) AS soma_qtd_produtos,
                    SUM(ode.unitprice * ode.quantity) AS valor_total
                FROM northwind.orders ord
                LEFT JOIN northwind.order_details ode ON ord.orderid = ode.orderid
                LEFT JOIN northwind.employees emp ON ord.employeeid = emp.employeeid
                WHERE ord.orderdate BETWEEN %s AND %s
                GROUP BY emp.employeeid, emp.firstname, emp.lastname
                ORDER BY valor_total DESC;
            """, (start_date, end_date))

            rows = cur.fetchall()
            for row in rows:
                rankings.append({
                    "employeeid": row[0],
                    "firstname": row[1],
                    "lastname": row[2],
                    "qtd_pedidos": row[3],
                    "soma_qtd_produtos": row[4],
                    "valor_total": row[5]
                })
        return rankings
