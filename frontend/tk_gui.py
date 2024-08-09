import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from backend.finance import Finance_Manager

class GUI:
    def __init__(self, master, conn):
        self.master = master
        self.conn = conn
        self.manager = Finance_Manager(conn)

        self.master.title("Finance Manager")

        #доходи
        self.income_amount_label = tk.Label(master, text="Сума доходу\n (грн)")
        self.income_amount_label.grid(row=0, column=0)
        self.income_amount_entry = tk.Entry(master)
        self.income_amount_entry.grid(row=0, column=1)

        self.income_source_label = tk.Label(master, text="Джерело доходу")
        self.income_source_label.grid(row=1, column=0)
        self.income_source_entry = tk.Entry(master)
        self.income_source_entry.grid(row=1, column=1)

        self.income_button = tk.Button(master, text="Додати дохід", command=self.add_income)
        self.income_button.grid(row=2, column=1, columnspan=1)

        #витрати
        self.expenses_amount_label = tk.Label(master, text="Сума витрат\n (грн)")
        self.expenses_amount_label.grid(row=3, column=0)
        self.expenses_amount_entry = tk.Entry(master)
        self.expenses_amount_entry.grid(row=3, column=1)

        self.expenses_category_label = tk.Label(master, text="Категорія витрат")
        self.expenses_category_label.grid(row=4, column=0)
        self.expenses_category_entry = tk.Entry(master)
        self.expenses_category_entry.grid(row=4, column=1)

        self.expenses_button = tk.Button(master, text="Додати витрату", command=self.add_expense)
        self.expenses_button.grid(row=5, column=1, columnspan=1)

        #баланс
        self.balance_label = tk.Label(master, text="Поточний баланс: ")
        self.balance_label.grid(row=8, column=0, rowspan=8)
        self.balance_value_label = tk.Label(master, text=f"")
        self.balance_value_label.grid(row=8, column=1, rowspan=8)
        self.update_balance()

        #табло доходів
        self.income_list_label = tk.Label(master, text="Табло доходів:")
        self.income_list_label.grid(row=0, column=2, padx=5, pady=5)
        self.income_listbox = tk.Listbox(master, width=30, height=15)
        self.income_listbox.grid(row=1, column=2, rowspan=20, padx=20, pady=5)

        #табло витрат
        self.expenses_list_label = tk.Label(master, text="Табло витрат:")
        self.expenses_list_label.grid(row=0, column=3, padx=5, pady=5)
        self.expenses_listbox = tk.Listbox(master,  width=30, height=15)
        self.expenses_listbox.grid(row=1, column=3, rowspan=20, padx=0, pady=0)

        self.calendar_button = tk.Button(master, text="Календар доходів і витрат", command=self.calendar)
        self.calendar_button.grid(row=10,rowspan=12 ,column=1)

        self.lists()

    def add_income(self):
        try:
            amount = float(self.income_amount_entry.get())
            source = self.income_source_entry.get()
            self.manager.income_manager.income(amount, source)
            self.update_balance()
            self.lists()
        except ValueError:
            messagebox.showerror("Помилка", "Введіть нормально суму доходу.")
        self.lists()

    def add_expense(self):
        try:
            amount = float(self.expenses_amount_entry.get())
            category = self.expenses_category_entry.get()
            balance = self.manager.balance()
            untouchable_money = 0.1 * balance
            if balance - amount < untouchable_money:
                if not messagebox.askyesno("Попередження", "Операція перевищує ліміт. Ви впевнені, що хочете продовжити?"):
                    messagebox.showwarning("Попередження", "Операцію скасовано.")
                    return False
            self.manager.expenses_manager.expenses(amount, category)
            self.update_balance()
            self.lists()
        except ValueError:
            messagebox.showerror("Помилка", "Введіть нормально суму витрат.")

    def update_balance(self):
        balance = self.manager.balance()
        self.balance_value_label.config(text=str(balance))

    def lists(self):
        self.income_listbox.delete(0, tk.END)
        incomes = self.manager.income_manager.inc_sort()
        for income in incomes:
            self.income_listbox.insert(tk.END, f" {income[2]}: {income[1]}.грн ({income[3]})")

        self.expenses_listbox.delete(0, tk.END)
        expenses = self.manager.expenses_manager.exp_sort()
        for expense in expenses:
            self.expenses_listbox.insert(tk.END, f" {expense[2]}: {expense[1]}.грн ({expense[3]})")

    def calendar(self):
        top = tk.Toplevel(self.master)#створює вікно поверх основного
        Calendar_window(top, self.manager)

class Calendar_window:
    def __init__(self, master, manager):
        master.resizable(False, False)

        self.master = master
        self.manager = manager
        self.master.title("Календар доходів та витрат")

        self.cal = Calendar(master, selectmode='day', date_pattern='y-mm-dd')
        self.cal.grid(padx=10, pady=10)

        self.show_button = tk.Button(master, text="Показати доходи/витрати", command=self.show)
        self.show_button.grid(padx=10, pady=10)

        self.entries_listbox = tk.Listbox(master, width=50, height=20)
        self.entries_listbox.grid(padx=10, pady=10)

    def show(self):
        date = self.cal.get_date()
        self.entries_listbox.delete(0, tk.END)

        incomes = self.manager.income_manager.incomes_date(date)
        expenses = self.manager.expenses_manager.expenses_date(date)

        self.entries_listbox.insert(tk.END, f"Доходи за {date}:")
        for income in incomes:
            self.entries_listbox.insert(tk.END, f" {income[2]}: {income[1]}.грн ({income[3]})")

        self.entries_listbox.insert(tk.END, f"Витрати за {date}:")
        for expense in expenses:
            self.entries_listbox.insert(tk.END, f" {expense[2]}: {expense[1]}.грн ({expense[3]})")
