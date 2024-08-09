from backend.income import Income_Manager

class Expenses_Manager:
    def __init__(self, conn):
        self.conn = conn
        self.income_manager = Income_Manager(conn)

    def expenses(self, amount, category):
        sql = '''INSERT INTO expenses(amount, category, date) VALUES(?, ?, CURRENT_DATE)'''
        cur = self.conn.cursor()
        cur.execute(sql, (amount, category))
        self.conn.commit()
    def total_expenses(self):
        cur = self.conn.cursor()
        cur.execute("SELECT SUM(amount) FROM expenses")
        total_exp = cur.fetchone()[0]
        if total_exp:
            return total_exp
        else:
            return 0

    def expenses_date(self, date):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM expenses WHERE date=?", (date,))
        return cur.fetchall()

    def exp_group(self):
        cur = self.conn.cursor()
        cur.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        return cur.fetchall()

    def exp_sort(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM expenses ORDER BY amount")
        return cur.fetchall()
