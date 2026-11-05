from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QMessageBox, QFileDialog, QFrame)
from PyQt6.QtGui import QPixmap, QPainter, QBrush, QRegion
from PyQt6.QtCore import Qt, QRect
import database as db
import os
import sys

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.setFixedSize(400, 380)
        self.setStyleSheet("background-color: #F8FAFC; font-family: Arial;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QLabel("Настройки системы")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #0F172A;")
        layout.addWidget(title)

        avatar_frame = QFrame()
        avatar_frame.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #E2E8F0;")
        a_layout = QHBoxLayout(avatar_frame)
        a_layout.setContentsMargins(15, 15, 15, 15)
        
        self.avatar_lbl = QLabel()
        self.avatar_lbl.setFixedSize(60, 60)
        self.avatar_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar_lbl.setStyleSheet("background-color: #E2E8F0; border-radius: 30px; color: #64748B; font-size: 24px; font-weight: bold;")
        self.load_avatar_preview()
        a_layout.addWidget(self.avatar_lbl)
        
        btn_change_avatar = QPushButton("Сменить аватарку")
        btn_change_avatar.setStyleSheet("background: #2563EB; color: white; padding: 8px 15px; border-radius: 8px; font-weight: bold; border: none;")
        btn_change_avatar.clicked.connect(self.change_avatar)
        a_layout.addWidget(btn_change_avatar)
        
        layout.addWidget(avatar_frame)

        restore_frame = QFrame()
        restore_frame.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #E2E8F0;")
        r_layout = QVBoxLayout(restore_frame)
        r_layout.setContentsMargins(15, 15, 15, 15)
        
        lbl_restore = QLabel("Резервное копирование")
        lbl_restore.setStyleSheet("font-weight: bold; color: #0F172A; font-size: 14px; border: none;")
        r_layout.addWidget(lbl_restore)
        
        lbl_desc = QLabel("Восстановить базу данных из файла")
        lbl_desc.setStyleSheet("color: #64748B; font-size: 12px; border: none;")
        r_layout.addWidget(lbl_desc)
        
        btn_restore = QPushButton("Восстановить БД")
        btn_restore.setStyleSheet("""
            QPushButton {
                background: #FEF2F2; color: #EF4444; border: 1px solid #EF4444; 
                padding: 10px; border-radius: 8px; font-weight: bold; margin-top: 10px;
            }
            QPushButton:hover { background: #FEE2E2; }
        """)
        btn_restore.clicked.connect(self.restore_db)
        r_layout.addWidget(btn_restore)
        
        layout.addWidget(restore_frame)
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

    def restore_db(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл резервной копии", "backups", "Database Files (*.db)")
        
        if file_path:
            reply = QMessageBox.question(
                self, 
                'Восстановление БД', 
                'Вы уверены? Текущая база данных будет заменена выбранной копией. Все несохраненные изменения будут потеряны.',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                if db.restore_database(file_path):
                    QMessageBox.information(self, "Успех", "База данных успешно восстановлена! Программа будет перезагружена.")
                    os.execl(sys.executable, sys.executable, *sys.argv)
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось восстановить базу данных.")