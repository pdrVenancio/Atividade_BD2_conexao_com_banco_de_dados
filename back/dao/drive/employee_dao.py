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
                FROM employees
                WHERE employeeid = %s
            """, (employeeid,))
            row = cur.fetchone()
            if row:
                return Employee(*row)
        return None

    def get_all(self):
        employees = []
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM employees")
            rows = cur.fetchall()
            for row in rows:
                employees.append(Employee(*row))
        return employees
