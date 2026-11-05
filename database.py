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
        updated_at TEXT,
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

try:
    cursor.execute("ALTER TABLE orders ADD COLUMN updated_at TEXT")
except sqlite3.OperationalError:
    pass

cursor.execute("SELECT COUNT(*) FROM papers")
if cursor.fetchone()[0] == 0:
    papers = [
        ("Мелованная матовая 150гр", 12.50, 2400),
        ("Мелованная глянцевая 130гр", 11.00, 1800),
        ("Офсетная 80гр", 4.00, 5000),
        ("Офсетная 100гр", 5.50, 3000),
        ("Картон 300гр", 25.00, 1200),
        ("Картон 250гр", 20.00, 800),
        ("Дизайнерская бумага", 35.00, 300),
        ("Самоклеящаяся бумага", 18.00, 1500)
    ]
    cursor.executemany("INSERT INTO papers (name, price, stock) VALUES (?, ?, ?)", papers)
    conn.commit()

cursor.execute("SELECT COUNT(*) FROM users WHERE login = '123'")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO users (name, login, password) VALUES (?, ?, ?)", ("Никита", "123", "123"))
    conn.commit()

def init_test_orders():
    cursor.execute("SELECT COUNT(*) FROM orders")
    if cursor.fetchone()[0] == 0:
        now = datetime.datetime.now()
        d5 = now.replace(day=5, hour=10, minute=0, second=0, microsecond=0)
        d6 = now.replace(day=6, hour=12, minute=0, second=0, microsecond=0)
        d7 = now.replace(day=7, hour=14, minute=0, second=0, microsecond=0)
        d8 = now.replace(day=8, hour=16, minute=0, second=0, microsecond=0)
        today = now.replace(hour=10, minute=0, second=0, microsecond=0)

        test_orders = [
            ("ООО Ромашка", 500, 4500.00, 1, "Выдан", d5.strftime('%d.%m.%Y'), d5.strftime('%Y-%m-%d %H:%M:%S')),
            ("ИП Иванов", 1000, 12500.00, 3, "Выдан", d6.strftime('%d.%m.%Y'), d6.strftime('%Y-%m-%d %H:%M:%S')),
            ("Кафе Зерно", 200, 3200.00, 2, "Выдан", d7.strftime('%d.%m.%Y'), d7.strftime('%Y-%m-%d %H:%M:%S')),
            ("Студия Дизайна", 300, 8500.00, 1, "Готов", d8.strftime('%d.%m.%Y'), d8.strftime('%Y-%m-%d %H:%M:%S')),
            ("ООО Вектор", 150, 2000.00, 5, "Готов", d5.strftime('%d.%m.%Y'), d5.strftime('%Y-%m-%d %H:%M:%S')),
            ("Магазин Рост", 800, 9800.00, 4, "В работе", d6.strftime('%d.%m.%Y'), d6.strftime('%Y-%m-%d %H:%M:%S')),
            ("Галерея Среда", 250, 4100.00, 1, "В работе", d7.strftime('%d.%m.%Y'), d7.strftime('%Y-%m-%d %H:%M:%S')),
            ("Быстро Парк", 2000, 24000.00, 1, "Новый", d8.strftime('%d.%m.%Y'), d8.strftime('%Y-%m-%d %H:%M:%S')),
            ("Кофейня Кофе", 100, 1500.00, 2, "Новый", d5.strftime('%d.%m.%Y'), d5.strftime('%Y-%m-%d %H:%M:%S')),
            ("Школа №5", 500, 6200.00, 3, "Выдан", d6.strftime('%d.%m.%Y'), d6.strftime('%Y-%m-%d %H:%M:%S')),
            ("Срочный заказ 1", 100, 2500.00, 1, "В работе", today.strftime('%d.%m.%Y'), today.strftime('%Y-%m-%d %H:%M:%S')),
            ("Срочный заказ 2", 50, 1200.00, 2, "Новый", today.strftime('%d.%m.%Y'), today.strftime('%Y-%m-%d %H:%M:%S'))
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

def get_orders_by_status(status):
    query = """
        SELECT o.id, o.client, o.qty, o.total_price, o.status, o.deadline, p.name 
        FROM orders o
        LEFT JOIN papers p ON o.paper_id = p.id
    """
    if status != "Все":
        query += f" WHERE o.status = '{status}'"
    
    query += """
        ORDER BY 
            CASE o.status 
                WHEN 'Новый' THEN 1 
                WHEN 'В работе' THEN 2 
                WHEN 'Готов' THEN 3 
                WHEN 'Выдан' THEN 4 
                ELSE 5 
            END ASC,
            substr(o.deadline, 7, 4) ASC, 
            substr(o.deadline, 4, 2) ASC, 
            substr(o.deadline, 1, 2) ASC
    """
    
    cursor.execute(query)
    return cursor.fetchall()

def delete_order(order_id):
    cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()

def update_stock(paper_id, qty):
    cursor.execute("UPDATE papers SET stock = stock - ? WHERE id = ?", (qty, paper_id))
    conn.commit()

def update_order_status(order_id, new_status):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("UPDATE orders SET status = ?, updated_at = ? WHERE id = ?", (new_status, now, order_id))
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

def get_stats_filtered(period, date_start_str=None, date_end_str=None):
    now = datetime.datetime.now()
    
    if period == "Свой период" and date_start_str and date_end_str:
        date_condition = f"AND created_at BETWEEN '{date_start_str} 00:00:00' AND '{date_end_str} 23:59:59'"
    elif period == "Сегодня":
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
    
    today_str = now.strftime('%d.%m.%Y')
    cursor.execute(f"SELECT COUNT(*) FROM orders WHERE deadline = '{today_str}' AND status != 'Выдан'")
    due_today = cursor.fetchone()[0]
    
    return {
        "revenue": revenue,
        "total_orders": total_orders,
        "in_work": in_work,
        "ready": ready,
        "issued": issued,
        "due_today": due_today
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
        return True
    except Exception as e:
        print(f"Ошибка бэкапа: {e}")
        return False

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