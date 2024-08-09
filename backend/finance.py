from backend.income import Income_Manager
from backend.expenses import Expenses_Manager

class Finance_Manager:
    def __init__(self, conn):
        self.conn = conn
        self.income_manager = Income_Manager(conn)
        self.expenses_manager = Expenses_Manager(conn)

    def balance(self):
        balance = self.income_manager.total_income() - self.expenses_manager.total_expenses()
        return balance
