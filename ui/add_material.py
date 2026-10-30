from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QSpinBox, QDoubleSpinBox)
import database as db

class AddPaperDialog(QDialog):
    def __init__(self, parent=None, paper_data=None):
        super().__init__(parent)
        self.paper_data = paper_data
        self.setWindowTitle("Редактирование материала" if paper_data else "Добавление материала")
        self.setFixedSize(400, 350)
        self.setStyleSheet("background-color: #FFFFFF; font-family: Arial;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Название бумаги:"))
        self.input_name = QLineEdit()
        self.input_name.setStyleSheet("padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px; color: #0F172A;")
        self.input_name.setPlaceholderText("Например: Мелованная матовая")
        layout.addWidget(self.input_name)

        layout.addWidget(QLabel("Плотность (гр):"))
        self.input_density = QSpinBox()
        self.input_density.setRange(50, 500)
        self.input_density.setValue(150)
        self.input_density.setStyleSheet("padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px; color: #0F172A;")
        layout.addWidget(self.input_density)

        layout.addWidget(QLabel("Цена за лист (₽):"))
        self.input_price = QDoubleSpinBox()
        self.input_price.setRange(0.1, 1000.0)
        self.input_price.setValue(10.0)
        self.input_price.setStyleSheet("padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px; color: #0F172A;")
        layout.addWidget(self.input_price)

        layout.addWidget(QLabel("Количество на складе (л):"))
        self.input_stock = QSpinBox()
        self.input_stock.setRange(0, 100000)
        self.input_stock.setValue(1000)
        self.input_stock.setStyleSheet("padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px; color: #0F172A;")
        layout.addWidget(self.input_stock)

        if self.paper_data:
            self.input_name.setText(str(self.paper_data[1]))
            self.input_density.setValue(int(self.paper_data[2]))
            self.input_price.setValue(float(self.paper_data[3]))
            self.input_stock.setValue(int(self.paper_data[4]))

        layout.addStretch()

        btn_layout = QHBoxLayout()
        
        if self.paper_data:
            btn_delete = QPushButton("Удалить")
            btn_delete.setStyleSheet("background: #EF4444; color: white; padding: 10px; border-radius: 6px; font-weight: bold; border: none;")
            btn_delete.clicked.connect(self.delete_data)
            btn_layout.addWidget(btn_delete)

        btn_cancel = QPushButton("Отмена")
        btn_cancel.setStyleSheet("background: #F1F5F9; color: #334155; padding: 10px; border-radius: 6px; border: 1px solid #D1D5DB; font-weight: bold;")
        btn_cancel.clicked.connect(self.reject)
        
        btn_save = QPushButton("Сохранить")
        btn_save.setStyleSheet("background: #2563EB; color: white; padding: 10px; border-radius: 6px; font-weight: bold; border: none;")
        btn_save.clicked.connect(self.save_data)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)

    def save_data(self):
        name = self.input_name.text()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название бумаги!")
            return
        
        if self.paper_data:
            db.update_paper(self.paper_data[0], name, self.input_density.value(), self.input_price.value(), self.input_stock.value())
        else:
            db.add_paper(name, self.input_density.value(), self.input_price.value(), self.input_stock.value())
            
        self.accept()

    def delete_data(self):
        reply = QMessageBox.question(self, 'Удаление', 'Вы уверены, что хотите удалить этот материал?', 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            db.delete_paper(self.paper_data[0])
            self.accept()