import sqlite3
import tkinter as tk
from frontend.tk_gui import GUI
import os

if __name__ == "__main__":
    db_path = os.path.join('finance_db', 'finance.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)

    root = tk.Tk()
    root.geometry("700x300")
    root.resizable(False, False)
    app = GUI(root, conn)
    root.mainloop()
