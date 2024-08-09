class Income_Manager:
    def __init__(self, conn):
        self.conn = conn

    def income(self, amount, source):
        sql = '''INSERT INTO income(amount, source, date) VALUES(?, ?, CURRENT_DATE)'''
        cur = self.conn.cursor()
        cur.execute(sql, (amount, source))
        self.conn.commit()

    def total_income(self):
        cur = self.conn.cursor()
        cur.execute("SELECT SUM(amount) FROM income")
        total_inc = cur.fetchone()[0]#берем перший елемент
        if total_inc:
            return total_inc
        else:
            return 0 #треба бо виличе помилку

    def incomes_date(self, date):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM income WHERE date=?", (date,))
        return cur.fetchall()#повертає все у вигляді списку

    def inc_group(self):
        cur = self.conn.cursor()
        cur.execute("SELECT source, SUM(amount) FROM income GROUP BY source")
        return cur.fetchall()

    def inc_sort(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM income ORDER BY amount")
        return cur.fetchall()
