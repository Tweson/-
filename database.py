import sqlite3
import datetime
import os
import shutil
import glob

conn = sqlite3.connect('typography.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS papers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL,
        stock INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client TEXT NOT NULL,
        qty INTEGER NOT NULL,
        total_price REAL,
        paper_id INTEGER,
        status TEXT,
        deadline TEXT,
        created_at TEXT,
        FOREIGN KEY (paper_id) REFERENCES papers (id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        login TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

cursor.execute("SELECT COUNT(*) FROM papers")
if cursor.fetchone()[0] == 0:
    papers = [
        ("Мелованная матовая", 12.50, 2400),
        ("Офсетная", 4.00, 150),
        ("Картон", 25.00, 1200)
    ]
    cursor.executemany("INSERT INTO papers (name, price, stock) VALUES (?, ?, ?)", papers)
    conn.commit()

def init_test_orders():
    cursor.execute("SELECT COUNT(*) FROM orders")
    if cursor.fetchone()[0] == 0:
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)
        two_days_ago = now - datetime.timedelta(days=2)

        test_orders = [
            ("ООО Ромашка", 500, 4500.00, 1, "Выдан", now.strftime('%d.%m.%Y'), now.strftime('%Y-%m-%d 10:30:00')),
            ("ИП Иванов", 1000, 12500.00, 1, "Выдан", yesterday.strftime('%d.%m.%Y'), yesterday.strftime('%Y-%m-%d 14:15:00')),
            ("Кафе Зерно", 200, 3200.00, 2, "Выдан", two_days_ago.strftime('%d.%m.%Y'), two_days_ago.strftime('%Y-%m-%d 09:20:00')),
            ("Студия Дизайна", 300, 8500.00, 1, "Готов", now.strftime('%d.%m.%Y'), now.strftime('%Y-%m-%d 11:45:00')),
            ("ООО Вектор", 150, 2000.00, 3, "Готов", yesterday.strftime('%d.%m.%Y'), yesterday.strftime('%Y-%m-%d 16:20:00')),
            ("Магазин Рост", 800, 9800.00, 2, "В работе", now.strftime('%d.%m.%Y'), now.strftime('%Y-%m-%d 09:00:00')),
            ("Галерея Среда", 250, 4100.00, 1, "В работе", yesterday.strftime('%d.%m.%Y'), yesterday.strftime('%Y-%m-%d 12:10:00')),
            ("Быстро Парк", 2000, 24000.00, 1, "Новый", now.strftime('%d.%m.%Y'), now.strftime('%Y-%m-%d 15:00:00')),
            ("Кофейня Кофе", 100, 1500.00, 2, "Новый", yesterday.strftime('%d.%m.%Y'), yesterday.strftime('%Y-%m-%d 17:30:00')),
            ("Школа №5", 500, 6200.00, 3, "Выдан", two_days_ago.strftime('%d.%m.%Y'), two_days_ago.strftime('%Y-%m-%d 13:40:00'))
        ]
        
        cursor.executemany('''
            INSERT INTO orders (client, qty, total_price, paper_id, status, deadline, created_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', test_orders)
        conn.commit()

init_test_orders()

def get_papers():
    cursor.execute("SELECT id, name, price, stock FROM papers")
    return cursor.fetchall()

def get_paper_by_name(name):
    cursor.execute("SELECT id, name, price, stock FROM papers WHERE name = ?", (name,))
    return cursor.fetchone()

def save_order(client, qty, total_price, paper_id, deadline):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        "INSERT INTO orders (client, qty, total_price, paper_id, status, deadline, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (client, qty, total_price, paper_id, "Новый", deadline, now)
    )
    conn.commit()

def get_orders():
    cursor.execute("""
        SELECT o.id, o.client, o.qty, o.total_price, o.status, o.deadline, p.name 
        FROM orders o
        LEFT JOIN papers p ON o.paper_id = p.id
        ORDER BY o.created_at DESC, o.id DESC
    """)
    return cursor.fetchall()

def get_orders_by_status(status):
    if status == "Все":
        cursor.execute("""
            SELECT o.id, o.client, o.qty, o.total_price, o.status, o.deadline, p.name 
            FROM orders o
            LEFT JOIN papers p ON o.paper_id = p.id
            ORDER BY o.created_at DESC, o.id DESC
        """)
    else:
        cursor.execute("""
            SELECT o.id, o.client, o.qty, o.total_price, o.status, o.deadline, p.name 
            FROM orders o
            LEFT JOIN papers p ON o.paper_id = p.id
            WHERE o.status = ? 
            ORDER BY o.created_at DESC, o.id DESC
        """, (status,))
    return cursor.fetchall()

def update_stock(paper_id, qty):
    cursor.execute("UPDATE papers SET stock = stock - ? WHERE id = ?", (qty, paper_id))
    conn.commit()

def update_order_status(order_id, new_status):
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
    conn.commit()

def add_paper(name, price, stock):
    cursor.execute(
        "INSERT INTO papers (name, price, stock) VALUES (?, ?, ?)",
        (name, price, stock)
    )
    conn.commit()

def update_paper(paper_id, name, price, stock):
    cursor.execute(
        "UPDATE papers SET name = ?, price = ?, stock = ? WHERE id = ?",
        (name, price, stock, paper_id)
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

def get_stats_filtered(period):
    now = datetime.datetime.now()
    
    if period == "Сегодня":
        date_start = now.strftime('%Y-%m-%d 00:00:00')
        date_end = now.strftime('%Y-%m-%d 23:59:59')
        date_condition = f"AND created_at BETWEEN '{date_start}' AND '{date_end}'"
    elif period == "Вчера":
        yesterday = now - datetime.timedelta(days=1)
        date_start = yesterday.strftime('%Y-%m-%d 00:00:00')
        date_end = yesterday.strftime('%Y-%m-%d 23:59:59')
        date_condition = f"AND created_at BETWEEN '{date_start}' AND '{date_end}'"
    else:
        date_condition = ""

    cursor.execute(f"SELECT SUM(total_price) FROM orders WHERE status = 'Выдан' {date_condition}")
    revenue = cursor.fetchone()[0] or 0.0
    
    cursor.execute(f"SELECT COUNT(*) FROM orders WHERE 1=1 {date_condition}")
    total_orders = cursor.fetchone()[0]
    
    cursor.execute(f"SELECT COUNT(*) FROM orders WHERE status = 'В работе' {date_condition}")
    in_work = cursor.fetchone()[0]
    
    cursor.execute(f"SELECT COUNT(*) FROM orders WHERE status = 'Готов' {date_condition}")
    ready = cursor.fetchone()[0]
    
    cursor.execute(f"SELECT COUNT(*) FROM orders WHERE status = 'Выдан' {date_condition}")
    issued = cursor.fetchone()[0]
    
    return {
        "revenue": revenue,
        "total_orders": total_orders,
        "in_work": in_work,
        "ready": ready,
        "issued": issued
    }

def backup_database():
    if not os.path.exists('backups'):
        os.makedirs('backups')

    now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_file = f'backups/typography_{now}.db'

    try:
        shutil.copy2('typography.db', backup_file)
        
        backups = sorted(glob.glob('backups/typography_*.db'))
        if len(backups) > 7:
            for old_backup in backups[:-7]:
                os.remove(old_backup)
                
        print(f"Бэкап создан: {backup_file}")
    except Exception as e:
        print(f"Ошибка бэкапа: {e}")

def restore_database(backup_file_path):
    try:
        global conn
        conn.close()
        shutil.copy2(backup_file_path, 'typography.db')
        conn = sqlite3.connect('typography.db')
        return True
    except Exception as e:
        print(f"Ошибка восстановления: {e}")
        return False