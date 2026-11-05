from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QMessageBox, QFileDialog, QFrame, QComboBox)
from PyQt6.QtGui import QPixmap, QPainter, QBrush, QRegion
from PyQt6.QtCore import Qt, QRect, pyqtSignal
import database as db
from ui import styles
import os
import sys

class SettingsDialog(QDialog):
    theme_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.setFixedSize(400, 480)
        self.setStyleSheet(styles.get_main_style())
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        self.title = QLabel("Настройки системы")
        self.title.setStyleSheet(f"font-size: 20px; {styles.get_text_main()}")
        layout.addWidget(self.title)

        self.avatar_frame = QFrame()
        self.avatar_frame.setStyleSheet(styles.get_card_style())
        a_layout = QHBoxLayout(self.avatar_frame)
        a_layout.setContentsMargins(15, 15, 15, 15)
        
        self.avatar_lbl = QLabel()
        self.avatar_lbl.setFixedSize(60, 60)
        self.avatar_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.load_avatar_preview()
        a_layout.addWidget(self.avatar_lbl)
        
        btn_change_avatar = QPushButton("Сменить аватарку")
        btn_change_avatar.setStyleSheet(styles.STYLE_BTN_BLUE)
        btn_change_avatar.clicked.connect(self.change_avatar)
        a_layout.addWidget(btn_change_avatar)
        
        layout.addWidget(self.avatar_frame)

        self.theme_frame = QFrame()
        self.theme_frame.setStyleSheet(styles.get_card_style())
        t_layout = QHBoxLayout(self.theme_frame)
        t_layout.setContentsMargins(15, 15, 15, 15)
        
        self.lbl_theme = QLabel("Тема оформления:")
        self.lbl_theme.setStyleSheet(styles.get_text_main())
        t_layout.addWidget(self.lbl_theme)
        
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["Светлая", "Темная"])
  
        if styles.CURRENT_THEME == styles.THEME_DARK:
            self.combo_theme.setCurrentText("Темная")
        else:
            self.combo_theme.setCurrentText("Светлая")
            
        self.combo_theme.setStyleSheet(styles.get_input_style())
        self.combo_theme.currentTextChanged.connect(self.change_theme)
        t_layout.addWidget(self.combo_theme)
        layout.addWidget(self.theme_frame)

        self.restore_frame = QFrame()
        self.restore_frame.setStyleSheet(styles.get_card_style())
        r_layout = QVBoxLayout(self.restore_frame)
        r_layout.setContentsMargins(15, 15, 15, 15)
        
        self.lbl_restore = QLabel("Резервное копирование")
        self.lbl_restore.setStyleSheet(f"font-weight: bold; font-size: 14px; {styles.get_text_main()}")
        r_layout.addWidget(self.lbl_restore)
        
        btn_backup = QPushButton("Сделать бэкап сейчас")
        btn_backup.setStyleSheet(styles.STYLE_BTN_GREEN)
        btn_backup.clicked.connect(self.make_backup)
        r_layout.addWidget(btn_backup)

        btn_restore = QPushButton("Восстановить БД из файла")
        btn_restore.setStyleSheet("background: #FEF2F2; color: #EF4444; border: 1px solid #EF4444; padding: 10px; border-radius: 8px; font-weight: bold;")
        btn_restore.clicked.connect(self.restore_db)
        r_layout.addWidget(btn_restore)
        
        layout.addWidget(self.restore_frame)
        layout.addStretch()

        btn_close = QPushButton("Закрыть")
        btn_close.setStyleSheet("background: #F1F5F9; color: #334155; padding: 12px; border-radius: 8px; border: 1px solid #D1D5DB; font-weight: bold;")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)

    def load_avatar_preview(self):
        if os.path.exists('avatar.png'):
            pixmap = QPixmap('avatar.png')
            self.set_round_avatar(pixmap)
        else:
            self.avatar_lbl.setText("Н")
            self.avatar_lbl.setStyleSheet(styles.STYLE_AVATAR)

    def set_round_avatar(self, pixmap):
        size = min(pixmap.width(), pixmap.height())
        rect = QRect((pixmap.width() - size) // 2, (pixmap.height() - size) // 2, size, size)
        cropped = pixmap.copy(rect).scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        mask = QPixmap(60, 60)
        mask.fill(Qt.GlobalColor.transparent)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(Qt.GlobalColor.black))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, 60, 60)
        painter.end()
        
        result = QPixmap(60, 60)
        result.fill(Qt.GlobalColor.transparent)
        painter = QPainter(result)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setClipRegion(QRegion(mask.mask()))
        painter.drawPixmap(0, 0, cropped)
        painter.end()
        
        self.avatar_lbl.setPixmap(result)
        self.avatar_lbl.setStyleSheet("background: transparent;")

    def change_avatar(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите картинку", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            try:
                pixmap = QPixmap(file_path)
                pixmap.save('avatar.png')
                self.load_avatar_preview()
                QMessageBox.information(self, "Успех", "Аватарка обновлена!")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить картинку: {e}")

    def change_theme(self, theme):
        if theme == "Темная":
            styles.set_theme("dark")
            with open("settings.ini", "w") as f:
                f.write("theme=dark")
        else:
            styles.set_theme("light")
            with open("settings.ini", "w") as f:
                f.write("theme=light")

        self.setStyleSheet(styles.get_main_style())
        self.title.setStyleSheet(f"font-size: 20px; {styles.get_text_main()}")
        self.avatar_frame.setStyleSheet(styles.get_card_style())
        self.theme_frame.setStyleSheet(styles.get_card_style())
        self.restore_frame.setStyleSheet(styles.get_card_style())
        self.lbl_theme.setStyleSheet(styles.get_text_main())
        self.lbl_restore.setStyleSheet(f"font-weight: bold; font-size: 14px; {styles.get_text_main()}")
        self.combo_theme.setStyleSheet(styles.get_input_style())
        
        self.theme_changed.emit()

    def make_backup(self):
        if db.backup_database():
            QMessageBox.information(self, "Успех", "Бэкап базы данных успешно создан в папке backups!")
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось создать бэкап.")

    def restore_db(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл резервной копии", "backups", "Database Files (*.db)")
        if file_path:
            reply = QMessageBox.question(self, 'Восстановление БД', 'Вы уверены? Текущая база данных будет заменена выбранной копией.', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                if db.restore_database(file_path):
                    QMessageBox.information(self, "Успех", "База данных восстановлена! Перезапустите программу.")
                    os.execl(sys.executable, sys.executable, *sys.argv)
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось восстановить базу данных.")