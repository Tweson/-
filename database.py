import sqlite3

conn = sqlite3.connect('typography.db')
cursor = conn.cursor()

# Таблица бумаги
cursor.execute('''
    CREATE TABLE IF NOT EXISTS papers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        density INTEGER,
        price REAL,
        stock INTEGER
    )
''')

# Таблица заказов
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client TEXT NOT NULL,
        qty INTEGER NOT NULL,
        total_price REAL,
        paper_id INTEGER,
        status TEXT,
        deadline TEXT, 
        FOREIGN KEY (paper_id) REFERENCES papers (id)
    )
''')

# НОВАЯ ТАБЛИЦА: Пользователи
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        login TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# Заполняем склад при первом запуске
cursor.execute("SELECT COUNT(*) FROM papers")
if cursor.fetchone()[0] == 0:
    papers = [
        ("Мелованная матовая", 150, 12.50, 2400),
        ("Офсетная", 80, 4.00, 150),
        ("Картон", 300, 25.00, 1200)
    ]
    cursor.executemany("INSERT INTO papers (name, density, price, stock) VALUES (?, ?, ?, ?)", papers)
    conn.commit()

def get_papers():
    cursor.execute("SELECT id, name, density, price, stock FROM papers")
    return cursor.fetchall()

def save_order(client, qty, total_price, paper_id, deadline):
    # Сохраняем заказ (БЕЗ списания бумаги, списание происходит в main_window)
    cursor.execute(
        "INSERT INTO orders (client, qty, total_price, paper_id, status, deadline) VALUES (?, ?, ?, ?, ?, ?)",
        (client, qty, total_price, paper_id, "Новый", deadline)
    )
    conn.commit()

def get_orders():
    # Сортируем по статусу (В работе -> Новый -> Готов -> Выдан)
    cursor.execute("""
        SELECT id, client, qty, total_price, status, deadline 
        FROM orders 
        ORDER BY 
            CASE status 
                WHEN 'В работе' THEN 1 
                WHEN 'Новый' THEN 2 
                WHEN 'Готов' THEN 3 
                WHEN 'Выдан' THEN 4 
                ELSE 5 
            END
    """)
    return cursor.fetchall()

def update_stock(paper_id, qty):
    # Списываем РОВНО столько, сколько передали (без умножений)
    cursor.execute("UPDATE papers SET stock = stock - ? WHERE id = ?", (qty, paper_id))
    conn.commit()

def update_order_status(order_id, new_status):
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
    conn.commit()

def add_paper(name, density, price, stock):
    cursor.execute(
        "INSERT INTO papers (name, density, price, stock) VALUES (?, ?, ?, ?)",
        (name, density, price, stock)
    )
    conn.commit()

def update_paper(paper_id, name, density, price, stock):
    cursor.execute(
        "UPDATE papers SET name = ?, density = ?, price = ?, stock = ? WHERE id = ?",
        (name, density, price, stock, paper_id)
    )
    conn.commit()

def delete_paper(paper_id):
    cursor.execute("DELETE FROM papers WHERE id = ?", (paper_id,))
    conn.commit()

def register_user(name, login, password):
    try:
        cursor.execute("INSERT INTO users (name, login, password) VALUES (?, ?, ?)", (name, login, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def check_user(login, password):
    cursor.execute("SELECT name FROM users WHERE login = ? AND password = ?", (login, password))
    return cursor.fetchone()