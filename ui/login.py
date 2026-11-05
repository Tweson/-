from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QStackedLayout, QFrame)
from PyQt6.QtCore import Qt
from ui.main_window import MainWindow
from ui import styles
import database as db
import os

class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        if os.path.exists("settings.ini"):
            with open("settings.ini", "r") as f:
                if "theme=dark" in f.read():
                    styles.set_theme("dark")

        self.setWindowTitle("Типография: Вход")
        self.resize(400, 500)
        self.setStyleSheet(styles.get_auth_style())
        
        self.stack = QStackedLayout()
        self.setLayout(self.stack)
        
        self.init_login_page()
        self.init_register_page()

    def init_login_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)
        
        card = QFrame()
        card.setStyleSheet(styles.get_card_style())
        c_layout = QVBoxLayout(card)
        c_layout.setContentsMargins(30, 30, 30, 30)
        c_layout.setSpacing(15)

        title = QLabel("Вход в систему")
        title.setStyleSheet(f"font-size: 24px; {styles.get_text_main()}")
        c_layout.addWidget(title)

        self.login_user = QLineEdit()
        self.login_user.setPlaceholderText("Логин")
        self.login_user.setStyleSheet(styles.get_input_style())
        c_layout.addWidget(self.login_user)

        self.login_pass = QLineEdit()
        self.login_pass.setPlaceholderText("Пароль")
        self.login_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_pass.setStyleSheet(styles.get_input_style())
        c_layout.addWidget(self.login_pass)

        btn_login = QPushButton("Войти")
        btn_login.setStyleSheet(styles.STYLE_BTN_BLUE)
        btn_login.clicked.connect(self.do_login)
        c_layout.addWidget(btn_login)

        lbl_reg = QLabel('<a href="reg" style="color: #64748B; text-decoration: none;">Нет аккаунта?<br>Зарегистрироваться</a>')
        lbl_reg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_reg.setStyleSheet(f"font-size: 13px; {styles.get_text_sub()}")
        lbl_reg.setTextFormat(Qt.TextFormat.RichText)
        lbl_reg.setOpenExternalLinks(False)
        lbl_reg.linkActivated.connect(lambda: self.stack.setCurrentIndex(1))
        c_layout.addWidget(lbl_reg)

        layout.addWidget(card)
        self.stack.addWidget(page)

    def init_register_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)
        
        card = QFrame()
        card.setStyleSheet(styles.get_card_style())
        c_layout = QVBoxLayout(card)
        c_layout.setContentsMargins(30, 30, 30, 30)
        c_layout.setSpacing(15)

        title = QLabel("Регистрация")
        title.setStyleSheet(f"font-size: 24px; {styles.get_text_main()}")
        c_layout.addWidget(title)

        self.reg_name = QLineEdit()
        self.reg_name.setPlaceholderText("Имя сотрудника")
        self.reg_name.setStyleSheet(styles.get_input_style())
        c_layout.addWidget(self.reg_name)

        self.reg_user = QLineEdit()
        self.reg_user.setPlaceholderText("Логин")
        self.reg_user.setStyleSheet(styles.get_input_style())
        c_layout.addWidget(self.reg_user)

        self.reg_pass = QLineEdit()
        self.reg_pass.setPlaceholderText("Пароль")
        self.reg_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_pass.setStyleSheet(styles.get_input_style())
        c_layout.addWidget(self.reg_pass)

        btn_register = QPushButton("Зарегистрироваться")
        btn_register.setStyleSheet(styles.STYLE_BTN_GREEN)
        btn_register.clicked.connect(self.do_register)
        c_layout.addWidget(btn_register)

        lbl_login = QLabel('<a href="login" style="color: #64748B; text-decoration: none;">Уже есть аккаунт?<br>Войти</a>')
        lbl_login.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_login.setStyleSheet(f"font-size: 13px; {styles.get_text_sub()}")
        lbl_login.setTextFormat(Qt.TextFormat.RichText)
        lbl_login.setOpenExternalLinks(False)
        lbl_login.linkActivated.connect(lambda: self.stack.setCurrentIndex(0))
        c_layout.addWidget(lbl_login)

        layout.addWidget(card)
        self.stack.addWidget(page)

    def do_login(self):
        login = self.login_user.text()
        password = self.login_pass.text()
        
        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль!")
            return

        user = db.check_user(login, password)
        if user:
            self.open_main(user[0])
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль!")

    def do_register(self):
        name = self.reg_name.text()
        login = self.reg_user.text()
        password = self.reg_pass.text()
        
        if not name or not login or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        if db.register_user(name, login, password):
            QMessageBox.information(self, "Успех", "Аккаунт создан! Теперь войдите.")
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Ошибка", "Этот логин уже занят!")

    def open_main(self, user_name):
        self.window = MainWindow(user_name)
        self.window.show()
        self.close()