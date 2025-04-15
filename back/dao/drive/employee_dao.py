from models.employee import Employee

class EmployeeDAO:
    def __init__(self, conn):
        self.conn = conn

    def get_by_id(self, employeeid):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT employeeid, lastname, firstname, title, titleofcourtesy,
                       birthdate, hiredate, address, city, region, postalcode,
                       country, homephone, extension, photo, notes, reportsto
                FROM northwind.employees
                WHERE employeeid = %s
            """, (employeeid,))
            row = cur.fetchone()
            if row:
                return Employee(*row)
        return None

    def get_all(self):
        employees = []
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM northwind.employees")
            rows = cur.fetchall()
            for row in rows:
                employees.append(Employee(*row))
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
                    SUM(ode.quantity) AS soma_qtd,
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
                    "soma_qtd": row[3],
                    "valor_total": row[4]
                })
        return rankings
