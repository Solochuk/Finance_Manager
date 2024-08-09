import sqlite3
import os
def create_database(db_folder='finance_db', db_name='finance.db'):
    db_path = os.path.join(db_folder, db_name)
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        source TEXT NOT NULL,
        date DATE DEFAULT (date('now'))
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date DATE DEFAULT (date('now'))
    )
    ''')

    conn.commit()
    conn.close()
    print(f"База даних '{db_name}' створена успішно!")

if __name__ == '__main__':
    create_database()
