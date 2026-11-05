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
        
        if os.path.exists("settings.ini"):
            with open("settings.ini", "r") as f:
                if "theme=dark" in f.read():
                    styles.set_theme("dark")

        self.user_name = user_name
        self.setWindowTitle("Типография: Управление заказами")
        self.resize(1200, 700)
        self.setStyleSheet(styles.get_main_style())
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.init_sidebar()
        self.init_content()

    def init_sidebar(self):
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(260)
        self.sidebar.setStyleSheet(styles.get_sidebar_style())
        layout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(15, 40, 15, 40)

        self.logo = QLabel("Типография")
        self.logo.setStyleSheet("font-size: 26px; font-weight: 900; color: #2563EB; border: none; padding-left: 5px;")
        layout.addWidget(self.logo)
        layout.addSpacing(40)

        self.btn_tab_calc = QPushButton("Расчёт печати")
        self.btn_tab_orders = QPushButton("Заказы")
        self.btn_tab_stock = QPushButton("Склад бумаги")
        
        for btn in [self.btn_tab_calc, self.btn_tab_orders, self.btn_tab_stock]:
            btn.setStyleSheet(styles.get_btn_menu_style())
            layout.addWidget(btn)
            layout.addSpacing(8)

        self.btn_tab_calc.setStyleSheet(styles.get_btn_menu_active_style())
        layout.addStretch()

        self.btn_settings = QPushButton("Настройки")
        self.btn_settings.setStyleSheet(styles.get_btn_menu_style())
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
        
        self.name_lbl = QLabel(self.user_name)
        self.name_lbl.setStyleSheet(f"font-weight: 900; font-size: 14px; {styles.get_text_main()}")
        self.role_lbl = QLabel("Сотрудник")
        self.role_lbl.setStyleSheet(f"font-size: 12px; {styles.get_text_sub()}")
        
        name_layout.addWidget(self.name_lbl)
        name_layout.addWidget(self.role_lbl)

        profile_layout.addWidget(self.avatar)
        profile_layout.addLayout(name_layout)
        profile_layout.addStretch()

        layout.addLayout(profile_layout)
        self.main_layout.addWidget(self.sidebar)

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
        dialog.theme_changed.connect(self.apply_new_theme)
        dialog.exec()
        self.update_avatar()

    def apply_new_theme(self):
        # 1. Применяем главный стиль
        self.setStyleSheet(styles.get_main_style())
        self.sidebar.setStyleSheet(styles.get_sidebar_style())
        self.name_lbl.setStyleSheet(f"font-weight: 900; font-size: 14px; {styles.get_text_main()}")
        self.role_lbl.setStyleSheet(f"font-size: 12px; {styles.get_text_sub()}")
        
        # 2. Обновляем кнопки меню
        for btn in [self.btn_tab_calc, self.btn_tab_orders, self.btn_tab_stock, self.btn_settings]:
            btn.setStyleSheet(styles.get_btn_menu_style())
            
        if self.calc_page.isVisible():
            self.btn_tab_calc.setStyleSheet(styles.get_btn_menu_active_style())
        elif self.orders_page.isVisible():
            self.btn_tab_orders.setStyleSheet(styles.get_btn_menu_active_style())
        elif self.stock_page.isVisible():
            self.btn_tab_stock.setStyleSheet(styles.get_btn_menu_active_style())

        # 3. Обновляем заголовок
        self.page_title.setStyleSheet(f"font-size: 32px; font-weight: 900; {styles.get_text_main()}")
        self.btn_add_paper.setStyleSheet(styles.STYLE_BTN_BLUE)

        # 4. ГЛАВНЫЙ ФИКС: Полностью пересобираем контентную часть
        # Удаляем старую контентную область
        self.main_layout.removeWidget(self.content_area)
        self.content_area.deleteLater()
        
        # Создаем новую контентную область
        self.init_content()
        
        # Переключаем на первую страницу по умолчанию
        self.switch_page(0)
        
    def init_content(self):
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.addWidget(self.content_area)

        top_layout = QHBoxLayout()
        self.page_title = QLabel("Расчёт печати")
        self.page_title.setStyleSheet(f"font-size: 32px; font-weight: 900; {styles.get_text_main()}")
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
            btn.setStyleSheet(styles.get_btn_menu_style())

        if index == 0:
            self.page_title.setText("Расчёт печати")
            self.calc_page.show()
            self.btn_tab_calc.setStyleSheet(styles.get_btn_menu_active_style())
        elif index == 1:
            self.page_title.setText("Заказы")
            self.orders_page.show()
            self.btn_tab_orders.setStyleSheet(styles.get_btn_menu_active_style())
            self.orders_page.stats_widget.load_stats()
            self.orders_page.filter_orders("Все")
        elif index == 2:
            self.page_title.setText("Склад бумаги")
            self.stock_page.show()
            self.btn_tab_stock.setStyleSheet(styles.get_btn_menu_active_style())
            self.btn_add_paper.show()
            self.stock_page.load_stock()