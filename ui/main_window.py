from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox,
                             QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QDateEdit,
                             QDialog, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QBrush
from logic import calculate_price
from ui.add_material import AddPaperDialog
import database as db

# Окно смены статуса
class StatusDialog(QDialog):
    def __init__(self, parent=None, current_status=""):
        super().__init__(parent)
        self.setWindowTitle("Смена статуса")
        self.setFixedSize(280, 250)
        self.setStyleSheet("background-color: #F8FAFC; font-family: Arial;")
        self.new_status = None
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        lbl = QLabel("Выберите новый статус:")
        lbl.setStyleSheet("color: #0F172A; font-weight: bold; font-size: 14px; border: none;")
        layout.addWidget(lbl)
        
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                outline: none;
                padding: 5px;
            }
            QListWidget::item { padding: 10px; border-radius: 6px; }
            QListWidget::item:hover { background: #F1F5F9; }
            QListWidget::item:selected { background: #EFF6FF; color: #2563EB; }
        """)
        
        statuses = [
            ("Новый", "#0F172A"),
            ("В работе", "#2563EB"),
            ("Готов", "#10B981"),
            ("Выдан", "#64748B")
        ]
        
        for text, color in statuses:
            item = QListWidgetItem(text)
            item.setForeground(QBrush(QColor(color)))
            self.list_widget.addItem(item)
            if text == current_status:
                self.list_widget.setCurrentItem(item)
                
        layout.addWidget(self.list_widget)
        
        btn_save = QPushButton("Применить")
        btn_save.setStyleSheet("background: #2563EB; color: white; padding: 12px; border-radius: 8px; font-weight: bold; border: none;")
        btn_save.clicked.connect(self.save)
        layout.addWidget(btn_save)

    def save(self):
        if self.list_widget.currentItem():
            self.new_status = self.list_widget.currentItem().text()
        self.accept()

class MainWindow(QMainWindow):
    def __init__(self, user_name="Сотрудник"):
        super().__init__()
        self.user_name = user_name
        self.setWindowTitle("Типография: Управление заказами")
        self.resize(1200, 700)
        self.setStyleSheet("background-color: #F8FAFC; font-family: Arial, sans-serif;")
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.init_sidebar()
        self.init_content()

    def init_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E2E8F0;")
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 40, 20, 40)

        logo = QLabel("Типография")
        logo.setStyleSheet("font-size: 24px; font-weight: bold; color: #0F172A; border: none;")
        layout.addWidget(logo)
        layout.addSpacing(40)

        self.btn_tab_calc = QPushButton("Расчёт печати")
        self.btn_tab_orders = QPushButton("Заказы")
        self.btn_tab_stock = QPushButton("Склад бумаги")
        
        for btn in [self.btn_tab_calc, self.btn_tab_orders, self.btn_tab_stock]:
            btn.setStyleSheet("""
                QPushButton { 
                    text-align: left; padding: 12px 15px; font-size: 14px; 
                    border: none; border-radius: 8px; color: #64748B; 
                    background: transparent; font-weight: 500;
                }
                QPushButton:hover { background-color: #F1F5F9; color: #0F172A; }
            """)
            layout.addWidget(btn)
            layout.addSpacing(5)

        layout.addStretch()

        profile_frame = QFrame()
        profile_frame.setStyleSheet("border: none;")
        p_layout = QVBoxLayout(profile_frame)
        p_layout.setContentsMargins(0, 0, 0, 0)
        
        name_lbl = QLabel(self.user_name)
        name_lbl.setStyleSheet("font-weight: bold; color: #0F172A; font-size: 14px; border: none;")
        role_lbl = QLabel("Сотрудник")
        role_lbl.setStyleSheet("color: #64748B; font-size: 12px; border: none;")
        
        p_layout.addWidget(name_lbl)
        p_layout.addWidget(role_lbl)
        layout.addWidget(profile_frame)

        self.main_layout.addWidget(sidebar)

    def init_content(self):
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.addWidget(self.content_area)

        top_layout = QHBoxLayout()
        self.page_title = QLabel("Расчёт печати")
        self.page_title.setStyleSheet("font-size: 32px; font-weight: bold; color: #0F172A; border: none;")
        top_layout.addWidget(self.page_title)
        top_layout.addStretch()
        
        self.btn_add_paper = QPushButton("+ Добавить бумагу")
        self.btn_add_paper.setStyleSheet("background: #2563EB; color: white; padding: 10px 20px; border-radius: 8px; font-weight: bold; border: none;")
        self.btn_add_paper.clicked.connect(self.open_add_paper_dialog)
        self.btn_add_paper.hide()
        top_layout.addWidget(self.btn_add_paper)
        
        self.content_layout.addLayout(top_layout)
        self.content_layout.addSpacing(20)

        self.calc_page = self.create_calc_page()
        self.orders_page = self.create_orders_page()
        self.stock_page = self.create_stock_page()

        self.content_layout.addWidget(self.calc_page)
        self.content_layout.addWidget(self.orders_page)
        self.content_layout.addWidget(self.stock_page)

        self.orders_page.hide()
        self.stock_page.hide()

        self.btn_tab_calc.clicked.connect(lambda: self.switch_page(0))
        self.btn_tab_orders.clicked.connect(lambda: self.switch_page(1))
        self.btn_tab_stock.clicked.connect(lambda: self.switch_page(2))

        self.load_papers()

    def create_calc_page(self):
        page = QWidget()
        layout = QHBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        left_col = QVBoxLayout()
        left_col.setSpacing(20)

        card1 = QFrame()
        card1.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #E2E8F0;")
        c1 = QVBoxLayout(card1)
        c1.setContentsMargins(25, 25, 25, 25)
        c1.setSpacing(10)
        c1.addWidget(QLabel("<b style='color:#0F172A; font-size:16px; border:none;'>01 Заказ и тираж</b>"))
        
        lbl1 = QLabel("Клиент")
        lbl1.setStyleSheet("color: #64748B; font-size: 12px; font-weight: bold; border: none;")
        c1.addWidget(lbl1)
        self.input_client = QLineEdit()
        self.input_client.setStyleSheet("padding: 10px; border: 1px solid #D1D5DB; border-radius: 8px; background: white; color: #0F172A; font-size: 14px;")
        c1.addWidget(self.input_client)

        lbl2 = QLabel("Тираж (шт)")
        lbl2.setStyleSheet("color: #64748B; font-size: 12px; font-weight: bold; border: none;")
        c1.addWidget(lbl2)
        self.input_qty = QLineEdit()
        self.input_qty.setStyleSheet("padding: 10px; border: 1px solid #D1D5DB; border-radius: 8px; background: white; color: #0F172A; font-size: 14px;")
        c1.addWidget(self.input_qty)
        
        lbl3 = QLabel("Дата сдачи")
        lbl3.setStyleSheet("color: #64748B; font-size: 12px; font-weight: bold; border: none;")
        c1.addWidget(lbl3)
        self.date_deadline = QDateEdit()
        self.date_deadline.setDate(QDate.currentDate().addDays(3))
        self.date_deadline.setCalendarPopup(True)
        self.date_deadline.setStyleSheet("padding: 10px; border: 1px solid #D1D5DB; border-radius: 8px; background: white; color: #0F172A; font-size: 14px;")
        c1.addWidget(self.date_deadline)
        
        left_col.addWidget(card1)

        card2 = QFrame()
        card2.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #E2E8F0;")
        c2 = QVBoxLayout(card2)
        c2.setContentsMargins(25, 25, 25, 25)
        c2.setSpacing(10)
        c2.addWidget(QLabel("<b style='color:#0F172A; font-size:16px; border:none;'>02 Бумага и печать</b>"))
        
        self.combo_paper = QComboBox()
        self.combo_paper.setStyleSheet("""
            QComboBox {
                padding: 10px 15px; border: 1px solid #D1D5DB; border-radius: 8px;
                background: white; color: #0F172A; font-size: 14px;
            }
            QComboBox:hover { border: 1px solid #2563EB; }
            QComboBox::drop-down { subcontrol-origin: padding; subcontrol-position: top right; width: 40px; border-left-width: 0px; }
            QComboBox::down-arrow {
                image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiM2NDc0OEMiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cG9seWxpbmUgcG9pbnRzPSI2IDkgMTIgMTUgMTggOSI+PC9wb2x5bGluZT48L3N2Zz4=);
                width: 16px; height: 16px; margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: white; border: 1px solid #E2E8F0; border-radius: 8px;
                selection-background-color: #F1F5F9; selection-color: #2563EB; color: #0F172A; outline: none; padding: 5px;
            }
        """)
        c2.addWidget(self.combo_paper)
        left_col.addWidget(card2)
        left_col.addStretch()
        
        layout.addLayout(left_col, 60)

        right_col = QVBoxLayout()
        right_col.setSpacing(20)

        price_card = QFrame()
        price_card.setStyleSheet("background: #2563EB; border-radius: 12px; border: none;")
        pc = QVBoxLayout(price_card)
        pc.setContentsMargins(25, 25, 25, 25)
        lbl_price_title = QLabel("Стоимость заказа")
        lbl_price_title.setStyleSheet("color:#DBEAFE; font-size:14px; border:none; font-weight: 500;")
        pc.addWidget(lbl_price_title)
        self.lbl_price = QLabel("0.00 ₽")
        self.lbl_price.setStyleSheet("color: white; font-size: 38px; font-weight: bold; border: none;")
        pc.addWidget(self.lbl_price)
        right_col.addWidget(price_card)

        btn_calc = QPushButton("Рассчитать")
        btn_calc.setStyleSheet("background: #10B981; color: white; padding: 15px; border-radius: 8px; font-weight: bold; font-size: 15px; border: none;")
        btn_calc.clicked.connect(self.do_calculate)
        right_col.addWidget(btn_calc)

        btn_save = QPushButton("Сохранить заказ")
        btn_save.setStyleSheet("background: #2563EB; color: white; padding: 15px; border-radius: 8px; font-weight: bold; font-size: 15px; border: none;")
        btn_save.clicked.connect(self.do_save)
        right_col.addWidget(btn_save)

        right_col.addStretch()
        layout.addLayout(right_col, 40)
        return page

    def create_orders_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.table_orders = QTableWidget()
        self.table_orders.setColumnCount(5)
        self.table_orders.setHorizontalHeaderLabels(["Клиент", "Тираж", "Сумма", "Срок сдачи", "Статус"])
        self.table_orders.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_orders.verticalHeader().setVisible(False)
        self.table_orders.setShowGrid(False)
        self.table_orders.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_orders.verticalHeader().setDefaultSectionSize(50)
        self.table_orders.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        
        header = self.table_orders.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.table_orders.setStyleSheet("""
            QTableWidget { background: white; border: 1px solid #E2E8F0; border-radius: 12px; color: #0F172A; outline: none; }
            QTableWidget::item { border-bottom: 1px solid #F1F5F9; padding: 10px; }
            QHeaderView::section { background: #F8FAFC; padding: 12px; border: none; border-bottom: 1px solid #E2E8F0; font-weight: bold; color: #64748B; font-size: 12px; }
        """)
        layout.addWidget(self.table_orders)
        return page

    def create_stock_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.table_stock = QTableWidget()
        self.table_stock.setColumnCount(4)
        self.table_stock.setHorizontalHeaderLabels(["Бумага", "Плотность", "Цена (₽)", "Остаток (л.)"])
        self.table_stock.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_stock.verticalHeader().setVisible(False)
        self.table_stock.setShowGrid(False)
        self.table_stock.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_stock.verticalHeader().setDefaultSectionSize(50)
        self.table_stock.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        
        header = self.table_stock.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        self.table_stock.setStyleSheet("""
            QTableWidget { background: white; border: 1px solid #E2E8F0; border-radius: 12px; color: #0F172A; outline: none; }
            QTableWidget::item { border-bottom: 1px solid #F1F5F9; padding: 10px; }
            QHeaderView::section { background: #F8FAFC; padding: 12px; border: none; border-bottom: 1px solid #E2E8F0; font-weight: bold; color: #64748B; font-size: 12px; }
        """)
        self.table_stock.cellDoubleClicked.connect(self.edit_paper)
        layout.addWidget(self.table_stock)
        return page

    def open_add_paper_dialog(self):
        dialog = AddPaperDialog(self)
        if dialog.exec():
            self.load_papers()
            self.load_stock()
            QMessageBox.information(self, "Успех", "Материал добавлен!")

    def edit_paper(self, row, column):
        paper_id = self.table_stock.item(row, 0).data(Qt.ItemDataRole.UserRole)
        papers = db.get_papers()
        paper_data = next((p for p in papers if p[0] == paper_id), None)
        
        if paper_data:
            dialog = AddPaperDialog(self, paper_data)
            if dialog.exec():
                self.load_papers()
                self.load_stock()

    def switch_page(self, index):
        self.calc_page.hide()
        self.orders_page.hide()
        self.stock_page.hide()
        self.btn_add_paper.hide()

        if index == 0:
            self.page_title.setText("Расчёт печати")
            self.calc_page.show()
        elif index == 1:
            self.page_title.setText("Заказы")
            self.orders_page.show()
            self.load_orders()
        elif index == 2:
            self.page_title.setText("Склад бумаги")
            self.stock_page.show()
            self.btn_add_paper.show()
            self.load_stock()

    def load_papers(self):
        self.combo_paper.clear()
        for p in db.get_papers():
            self.combo_paper.addItem(f"{p[1]} ({p[2]} гр.)", p[0])

    def load_orders(self):
        self.table_orders.blockSignals(True)
        orders = db.get_orders()
        self.table_orders.setRowCount(len(orders))
        
        for row, o in enumerate(orders):
            item_client = QTableWidgetItem(str(o[1]))
            item_client.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_client.setData(Qt.ItemDataRole.UserRole, o[0])
            
            item_qty = QTableWidgetItem(str(o[2]))
            item_qty.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            item_total = QTableWidgetItem(f"{o[3]} ₽")
            item_total.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            item_date = QTableWidgetItem(str(o[5]))
            item_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table_orders.setItem(row, 0, item_client)
            self.table_orders.setItem(row, 1, item_qty)
            self.table_orders.setItem(row, 2, item_total)
            self.table_orders.setItem(row, 3, item_date)
            
            status = str(o[4])
            btn_status = QPushButton(f"{status}  ›") 
            btn_status.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_status.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            
            if status == "Готов":
                color = "#10B981"
            elif status == "В работе":
                color = "#2563EB"
            elif status == "Выдан":
                color = "#64748B"
            else:
                color = "#0F172A"

            btn_status.setStyleSheet(f"""
                QPushButton {{
                    background: transparent; 
                    color: {color}; 
                    border: none; 
                    font-weight: bold;
                    font-size: 14px;
                    outline: none;
                }}
                QPushButton:hover {{
                    text-decoration: underline;
                }}
            """)
            
            btn_status.setProperty("order_id", o[0])
            btn_status.setProperty("current_status", status)
            btn_status.clicked.connect(self.open_status_dialog)
            
            self.table_orders.setCellWidget(row, 4, btn_status)
            
        self.table_orders.blockSignals(False)

    def open_status_dialog(self):
        btn = self.sender()
        if btn:
            order_id = btn.property("order_id")
            current_status = btn.property("current_status")
            
            dialog = StatusDialog(self, current_status)
            if dialog.exec() and dialog.new_status:
                db.update_order_status(order_id, dialog.new_status)
                self.load_orders()

    def load_stock(self):
        papers = db.get_papers()
        self.table_stock.setRowCount(len(papers))
        for row, p in enumerate(papers):
            item_name = QTableWidgetItem(str(p[1]))
            item_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_name.setData(Qt.ItemDataRole.UserRole, p[0])
            
            item_density = QTableWidgetItem(f"{p[2]} гр.")
            item_density.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            item_price = QTableWidgetItem(f"{p[3]} ₽")
            item_price.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            item_stock = QTableWidgetItem(f"{p[4]} л.")
            item_stock.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table_stock.setItem(row, 0, item_name)
            self.table_stock.setItem(row, 1, item_density)
            self.table_stock.setItem(row, 2, item_price)
            self.table_stock.setItem(row, 3, item_stock)

    def do_calculate(self):
        try:
            qty = int(self.input_qty.text())
            paper_id = self.combo_paper.currentData()
            price = next(p[3] for p in db.get_papers() if p[0] == paper_id)
            total = calculate_price(qty, 4, price)
            self.lbl_price.setText(f"{total:.2f} ₽")
        except:
            QMessageBox.warning(self, "Ошибка", "Введите корректный тираж!")

    def do_save(self):
        client = self.input_client.text()
        qty_text = self.input_qty.text()
        
        if not client or not qty_text:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return
            
        try:
            total_str = self.lbl_price.text().replace(" ₽", "").replace(" ", "").strip()
            total = float(total_str)
            if total == 0.0:
                QMessageBox.warning(self, "Ошибка", "Сначала нажмите 'Рассчитать'!")
                return

            qty = int(qty_text)
            paper_id = self.combo_paper.currentData()
            deadline = self.date_deadline.date().toString("dd.MM.yyyy")
            
            db.save_order(client, qty, total, paper_id, deadline)
            db.update_stock(paper_id, qty)
            
            QMessageBox.information(self, "Успех", "Заказ сохранен, бумага списана!")
            
            self.input_client.clear()
            self.input_qty.clear()
            self.lbl_price.setText("0.00 ₽")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))
            #