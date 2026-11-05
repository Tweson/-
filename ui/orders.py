from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QListWidget, QListWidgetItem, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush
from ui.stats_page import StatsPage
from ui import styles
import database as db

class StatusDialog(QDialog):
    def __init__(self, parent=None, current_status=""):
        super().__init__(parent)
        self.setWindowTitle("Смена статуса")
        self.setFixedSize(280, 250)
        self.setStyleSheet(styles.get_main_style())
        self.new_status = None
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        lbl = QLabel("Выберите новый статус:")
        lbl.setStyleSheet(styles.get_text_main() + " font-weight: bold; font-size: 14px;")
        layout.addWidget(lbl)
        
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(f"""
            QListWidget {{ background: {styles.CURRENT_THEME['card']}; border: 1px solid {styles.CURRENT_THEME['border']}; border-radius: 8px; outline: none; padding: 5px; font-weight: bold; }}
            QListWidget::item {{ padding: 10px; border-radius: 6px; }}
            QListWidget::item:hover {{ background: #F1F5F9; }}
            QListWidget::item:selected {{ background: #EFF6FF; color: #2563EB; }}
        """)
        
        statuses = [("Новый", "#0F172A"), ("В работе", "#2563EB"), ("Готов", "#10B981"), ("Выдан", "#64748B")]
        for text, color in statuses:
            item = QListWidgetItem(text)
            item.setForeground(QBrush(QColor(color)))
            self.list_widget.addItem(item)
            if text == current_status:
                self.list_widget.setCurrentItem(item)
        layout.addWidget(self.list_widget)
        
        btn_save = QPushButton("Применить")
        btn_save.setStyleSheet(styles.STYLE_BTN_BLUE)
        btn_save.clicked.connect(self.save)
        layout.addWidget(btn_save)

    def save(self):
        if self.list_widget.currentItem():
            self.new_status = self.list_widget.currentItem().text()
        self.accept()

class OrdersPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        self.stats_widget = StatsPage()
        layout.addWidget(self.stats_widget)

        filters_layout = QHBoxLayout()
        filters_layout.setSpacing(10)
        
        self.btn_filter_all = QPushButton("Все")
        self.btn_filter_new = QPushButton("Новые")
        self.btn_filter_work = QPushButton("В работе")
        self.btn_filter_ready = QPushButton("Готовые")
        self.btn_filter_issued = QPushButton("Выданные")
        
        for btn in [self.btn_filter_all, self.btn_filter_new, self.btn_filter_work, self.btn_filter_ready, self.btn_filter_issued]:
            btn.setStyleSheet(styles.STYLE_FILTER_BTN)
            filters_layout.addWidget(btn)
        
        filters_layout.addStretch()
        layout.addLayout(filters_layout)

        self.table_orders = QTableWidget()
        self.table_orders.setColumnCount(7) 
        self.table_orders.setHorizontalHeaderLabels(["Клиент", "Тираж", "Сумма", "Срок сдачи", "Материал", "Статус", "Удалить"])
        self.table_orders.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_orders.verticalHeader().setVisible(False)
        self.table_orders.setShowGrid(False)
        self.table_orders.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_orders.verticalHeader().setDefaultSectionSize(50)
        self.table_orders.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        
        header = self.table_orders.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.table_orders.setStyleSheet(styles.get_table_style())
        layout.addWidget(self.table_orders)

        self.btn_filter_all.clicked.connect(lambda: self.filter_orders("Все"))
        self.btn_filter_new.clicked.connect(lambda: self.filter_orders("Новый"))
        self.btn_filter_work.clicked.connect(lambda: self.filter_orders("В работе"))
        self.btn_filter_ready.clicked.connect(lambda: self.filter_orders("Готов"))
        self.btn_filter_issued.clicked.connect(lambda: self.filter_orders("Выдан"))

        self.filter_orders("Все")

    def filter_orders(self, status_filter):
        for btn in [self.btn_filter_all, self.btn_filter_new, self.btn_filter_work, self.btn_filter_ready, self.btn_filter_issued]:
            btn.setStyleSheet(styles.STYLE_FILTER_BTN)
        
        if status_filter == "Все":
            self.btn_filter_all.setStyleSheet(styles.STYLE_FILTER_BTN_ACTIVE)
        elif status_filter == "Новый":
            self.btn_filter_new.setStyleSheet(styles.STYLE_FILTER_BTN_ACTIVE)
        elif status_filter == "В работе":
            self.btn_filter_work.setStyleSheet(styles.STYLE_FILTER_BTN_ACTIVE)
        elif status_filter == "Готов":
            self.btn_filter_ready.setStyleSheet(styles.STYLE_FILTER_BTN_ACTIVE)
        elif status_filter == "Выдан":
            self.btn_filter_issued.setStyleSheet(styles.STYLE_FILTER_BTN_ACTIVE)

        orders = db.get_orders_by_status(status_filter)
        self.table_orders.setRowCount(len(orders))
        
        for row, o in enumerate(orders):
            item_client = QTableWidgetItem(str(o[1]))
            item_client.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            item_qty = QTableWidgetItem(str(o[2]))
            item_qty.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            item_total = QTableWidgetItem(f"{o[3]} ₽")
            item_total.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            item_date = QTableWidgetItem(str(o[5]))
            item_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            item_material = QTableWidgetItem(str(o[6]) if o[6] else "Удален")
            item_material.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table_orders.setItem(row, 0, item_client)
            self.table_orders.setItem(row, 1, item_qty)
            self.table_orders.setItem(row, 2, item_total)
            self.table_orders.setItem(row, 3, item_date)
            self.table_orders.setItem(row, 4, item_material)
            
            status = str(o[4])
            btn_status = QPushButton(f"{status} ›") 
            btn_status.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_status.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            
            if status == "Готов": color = "#10B981"
            elif status == "В работе": color = "#2563EB"
            elif status == "Выдан": color = "#64748B"
            else: color = "#0F172A"

            btn_status.setStyleSheet(f"""
                QPushButton {{
                    background: transparent; color: {color}; border: none; 
                    font-weight: bold; font-size: 14px; outline: none;
                }}
                QPushButton:hover {{ text-decoration: underline; }}
            """)
            
            btn_status.setProperty("order_id", o[0])
            btn_status.setProperty("current_status", status)
            btn_status.clicked.connect(self.open_status_dialog)
            
            self.table_orders.setCellWidget(row, 5, btn_status)

            btn_delete = QPushButton("X")
            btn_delete.setStyleSheet("""
                QPushButton {
                    background: #FEF2F2; color: #EF4444; 
                    border: 1px solid #EF4444; border-radius: 4px; 
                    padding: 2px 8px; font-weight: bold; font-size: 12px;
                }
                QPushButton:hover { background: #FEE2E2; }
            """)
            btn_delete.setFixedSize(30, 24) 
            btn_delete.setProperty("order_id", o[0])
            btn_delete.clicked.connect(self.delete_order_action)
            
            cell_widget = QWidget()
            cell_layout = QHBoxLayout(cell_widget)
            cell_layout.setContentsMargins(0, 0, 0, 0)
            cell_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cell_layout.addWidget(btn_delete)
            cell_widget.setStyleSheet("background: transparent;")
            
            self.table_orders.setCellWidget(row, 6, cell_widget)

    def delete_order_action(self):
        btn = self.sender()
        if btn:
            order_id = btn.property("order_id")
            reply = QMessageBox.question(self, 'Удаление', 'Вы уверены, что хотите удалить этот заказ?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                db.delete_order(order_id)
                self.stats_widget.load_stats()
                self.filter_orders("Все")

    def open_status_dialog(self):
        btn = self.sender()
        if btn:
            order_id = btn.property("order_id")
            current_status = btn.property("current_status")
            
            dialog = StatusDialog(self, current_status)
            if dialog.exec() and dialog.new_status:
                db.update_order_status(order_id, dialog.new_status)
                self.stats_widget.load_stats()
                self.filter_orders("Все")