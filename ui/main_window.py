from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame, QMessageBox)
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPixmap, QPainter, QBrush, QRegion
from ui.calc import CalcPage
from ui.orders import OrdersPage
from ui.stock import StockPage
from ui.add_material import AddPaperDialog
from ui.settings import SettingsDialog
from ui import styles
import database as db
import os

class MainWindow(QMainWindow):
    def __init__(self, user_name="Сотрудник"):
        super().__init__()
        db.backup_database()
        self.user_name = user_name
        self.setWindowTitle("Типография: Управление заказами")
        self.resize(1200, 700)
        self.setStyleSheet(styles.STYLE_MAIN_WINDOW)
        
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
        sidebar.setStyleSheet(styles.STYLE_SIDEBAR)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(15, 40, 15, 40)

        logo = QLabel("Типография")
        logo.setStyleSheet(styles.STYLE_LOGO)
        layout.addWidget(logo)
        layout.addSpacing(40)

        self.btn_tab_calc = QPushButton("Расчёт печати")
        self.btn_tab_orders = QPushButton("Заказы")
        self.btn_tab_stock = QPushButton("Склад бумаги")
        
        for btn in [self.btn_tab_calc, self.btn_tab_orders, self.btn_tab_stock]:
            btn.setStyleSheet(styles.STYLE_BTN_MENU)
            layout.addWidget(btn)
            layout.addSpacing(8)

        self.btn_tab_calc.setStyleSheet(styles.STYLE_BTN_MENU_ACTIVE)
        layout.addStretch()

        self.btn_settings = QPushButton("Настройки")
        self.btn_settings.setStyleSheet(styles.STYLE_BTN_MENU)
        self.btn_settings.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_settings.clicked.connect(self.open_settings)
        layout.addWidget(self.btn_settings)
        layout.addSpacing(15)

        profile_layout = QHBoxLayout()
        profile_layout.setContentsMargins(0, 0, 0, 0)
        profile_layout.setSpacing(10)

        self.avatar = QLabel()
        self.avatar.setFixedSize(40, 40)
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_avatar()
        
        name_layout = QVBoxLayout()
        name_layout.setSpacing(2)
        name_layout.setContentsMargins(0, 0, 0, 0)
        
        name_lbl = QLabel(self.user_name)
        name_lbl.setStyleSheet("font-weight: 900; color: #0F172A; font-size: 14px; border: none;")
        role_lbl = QLabel("Сотрудник")
        role_lbl.setStyleSheet("color: #64748B; font-size: 12px; border: none;")
        
        name_layout.addWidget(name_lbl)
        name_layout.addWidget(role_lbl)

        profile_layout.addWidget(self.avatar)
        profile_layout.addLayout(name_layout)
        profile_layout.addStretch()

        layout.addLayout(profile_layout)
        self.main_layout.addWidget(sidebar)

    def update_avatar(self):
        if os.path.exists('avatar.png'):
            pixmap = QPixmap('avatar.png')
            size = min(pixmap.width(), pixmap.height())
            rect = QRect((pixmap.width() - size) // 2, (pixmap.height() - size) // 2, size, size)
            cropped = pixmap.copy(rect).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            
            mask = QPixmap(40, 40)
            mask.fill(Qt.GlobalColor.transparent)
            painter = QPainter(mask)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(QBrush(Qt.GlobalColor.black))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(0, 0, 40, 40)
            painter.end()
            
            result = QPixmap(40, 40)
            result.fill(Qt.GlobalColor.transparent)
            painter = QPainter(result)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setClipRegion(QRegion(mask.mask()))
            painter.drawPixmap(0, 0, cropped)
            painter.end()
            
            self.avatar.setPixmap(result)
            self.avatar.setStyleSheet("background: transparent;")
        else:
            self.avatar.setText(self.user_name[0].upper())
            self.avatar.setStyleSheet(styles.STYLE_AVATAR)

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()
        self.update_avatar()

    def init_content(self):
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.addWidget(self.content_area)

        top_layout = QHBoxLayout()
        self.page_title = QLabel("Расчёт печати")
        self.page_title.setStyleSheet(styles.STYLE_TITLE)
        top_layout.addWidget(self.page_title)
        top_layout.addStretch()
        
        self.btn_add_paper = QPushButton("+ Добавить бумагу")
        self.btn_add_paper.setStyleSheet(styles.STYLE_BTN_BLUE)
        self.btn_add_paper.clicked.connect(self.open_add_paper_dialog)
        self.btn_add_paper.hide()
        top_layout.addWidget(self.btn_add_paper)
        
        self.content_layout.addLayout(top_layout)
        self.content_layout.addSpacing(20)

        self.calc_page = CalcPage()
        self.orders_page = OrdersPage()
        self.stock_page = StockPage()

        self.content_layout.addWidget(self.calc_page)
        self.content_layout.addWidget(self.orders_page)
        self.content_layout.addWidget(self.stock_page)

        self.orders_page.hide()
        self.stock_page.hide()

        self.btn_tab_calc.clicked.connect(lambda: self.switch_page(0))
        self.btn_tab_orders.clicked.connect(lambda: self.switch_page(1))
        self.btn_tab_stock.clicked.connect(lambda: self.switch_page(2))

    def open_add_paper_dialog(self):
        dialog = AddPaperDialog(self)
        if dialog.exec():
            self.calc_page.load_papers()
            self.stock_page.load_stock()
            QMessageBox.information(self, "Успех", "Материал добавлен!")

    def switch_page(self, index):
        self.calc_page.hide()
        self.orders_page.hide()
        self.stock_page.hide()
        self.btn_add_paper.hide()

        for btn in [self.btn_tab_calc, self.btn_tab_orders, self.btn_tab_stock]:
            btn.setStyleSheet(styles.STYLE_BTN_MENU)

        if index == 0:
            self.page_title.setText("Расчёт печати")
            self.calc_page.show()
            self.btn_tab_calc.setStyleSheet(styles.STYLE_BTN_MENU_ACTIVE)
        elif index == 1:
            self.page_title.setText("Заказы")
            self.orders_page.show()
            self.btn_tab_orders.setStyleSheet(styles.STYLE_BTN_MENU_ACTIVE)
            self.orders_page.stats_widget.load_stats()
            self.orders_page.filter_orders("Все")
        elif index == 2:
            self.page_title.setText("Склад бумаги")
            self.stock_page.show()
            self.btn_tab_stock.setStyleSheet(styles.STYLE_BTN_MENU_ACTIVE)
            self.btn_add_paper.show()
            self.stock_page.load_stock()