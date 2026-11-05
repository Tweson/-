import pytest
import sqlite3
import database as db


@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    db.conn = sqlite3.connect(":memory:")
    db.cursor = db.conn.cursor()
    db.cursor.execute(
        """CREATE TABLE papers (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER)"""
    )
    db.cursor.execute(
        """CREATE TABLE orders (id INTEGER PRIMARY KEY, client TEXT, qty INTEGER, total_price REAL, paper_id INTEGER, status TEXT, deadline TEXT, created_at TEXT)"""
    )
    db.cursor.execute(
        """CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, login TEXT UNIQUE, password TEXT)"""
    )

    db.cursor.execute(
        "INSERT INTO papers (name, price, stock) VALUES ('Тестовая бумага', 10.0, 1000)"
    )
    db.conn.commit()

    yield

    db.conn.close()


def test_add_and_get_paper():
    db.add_paper("Новая бумага", 15.0, 500)
    papers = db.get_papers()
    assert any(p[1] == "Новая бумага" for p in papers)


def test_save_order():
    db.save_order("Тестовый клиент", 100, 5000.0, 1, "01.01.2026")
    orders = db.get_orders()
    assert any(o[1] == "Тестовый клиент" for o in orders)


def test_update_stock():
    db.update_stock(1, 100)
    papers = db.get_papers()
    stock = next(p[3] for p in papers if p[0] == 1)
    assert stock == 900


def test_update_order_status():
    db.save_order("Клиент 2", 50, 2500.0, 1, "01.01.2026")
    orders = db.get_orders()
    order_id = orders[0][0]

    db.update_order_status(order_id, "Готов")
    updated_orders = db.get_orders()
    updated_status = next(o[4] for o in updated_orders if o[0] == order_id)
    assert updated_status == "Готов"


def test_register_and_check_user():
    db.register_user("Иван", "ivan_test", "12345")
    user = db.check_user("ivan_test", "12345")
    assert user is not None
    assert user[0] == "Иван"


def test_check_wrong_user():
    user = db.check_user("ivan_test", "wrong_pass")
    assert user is None


def test_delete_paper():
    db.add_paper("Удаляемая бумага", 5.0, 10)
    papers_before = db.get_papers()
    target_id = next(p[0] for p in papers_before if p[1] == "Удаляемая бумага")

    db.delete_paper(target_id)
    papers_after = db.get_papers()
    assert not any(p[0] == target_id for p in papers_after)


def test_get_stats():
    db.save_order("Клиент 3", 10, 1000.0, 1, "01.01.2026")
    orders = db.get_orders()
    order_id = orders[0][0]
    db.update_order_status(order_id, "Выдан")

    stats = db.get_stats_filtered("За всё время")
    assert stats["revenue"] >= 1000.0
    assert stats["total_orders"] > 0
