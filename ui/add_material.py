from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QSpinBox, QDoubleSpinBox, QComboBox)
import database as db

class AddPaperDialog(QDialog):
    def __init__(self, parent=None, paper_data=None):
        super().__init__(parent)
        self.paper_data = paper_data
        self.setWindowTitle("Редактирование материала" if paper_data else "Добавление / Пополнение материала")
        self.setFixedSize(420, 350)
        self.setStyleSheet("background-color: #FFFFFF; font-family: Arial;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        if not paper_data:
            layout.addWidget(QLabel("Выберите существующую бумагу (или создайте новую):"))
            self.combo_existing = QComboBox()
            self.combo_existing.setStyleSheet("padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px; color: #0F172A; min-height: 20px;")
            self.combo_existing.addItem("--- Создать новую бумагу ---", 0)
            for p in db.get_papers():
                self.combo_existing.addItem(f"{p[1]} - Остаток: {p[3]}", p[0])
            self.combo_existing.currentIndexChanged.connect(self.on_existing_selected)
            layout.addWidget(self.combo_existing)
            
            line = QLabel("<hr>")
            layout.addWidget(line)

        layout.addWidget(QLabel("Название бумаги:"))
        self.input_name = QLineEdit()
        self.input_name.setStyleSheet("padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px; color: #0F172A; min-height: 20px;")
        self.input_name.setPlaceholderText("Например: Мелованная матовая")
        layout.addWidget(self.input_name)

        layout.addWidget(QLabel("Цена за лист (₽):"))
        self.input_price = QDoubleSpinBox()
        self.input_price.setRange(0.1, 1000.0)
        self.input_price.setValue(10.0)
        self.input_price.setStyleSheet("padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px; color: #0F172A; min-height: 20px;")
        layout.addWidget(self.input_price)

        layout.addWidget(QLabel("Количество (Прибавить к остатку, л):"))
        self.input_stock = QSpinBox()
        self.input_stock.setRange(0, 100000)
        self.input_stock.setValue(0)
        self.input_stock.setStyleSheet("padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px; color: #0F172A; min-height: 20px;")
        layout.addWidget(self.input_stock)

        if self.paper_data:
            self.input_name.setText(str(self.paper_data[1]))
            self.input_price.setValue(float(self.paper_data[2]))
            self.input_stock.setValue(0)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        
        if self.paper_data:
            btn_delete = QPushButton("Удалить")
            btn_delete.setStyleSheet("background: #EF4444; color: white; padding: 10px; border-radius: 6px; font-weight: bold; border: none; min-height: 20px;")
            btn_delete.clicked.connect(self.delete_data)
            btn_layout.addWidget(btn_delete)

        btn_cancel = QPushButton("Отмена")
        btn_cancel.setStyleSheet("background: #F1F5F9; color: #334155; padding: 10px; border-radius: 6px; border: 1px solid #D1D5DB; font-weight: bold; min-height: 20px;")
        btn_cancel.clicked.connect(self.reject)
        
        btn_save = QPushButton("Сохранить")
        btn_save.setStyleSheet("background: #2563EB; color: white; padding: 10px; border-radius: 6px; font-weight: bold; border: none; min-height: 20px;")
        btn_save.clicked.connect(self.save_data)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)

    def on_existing_selected(self, index):
        paper_id = self.combo_existing.currentData()
        if paper_id == 0:
            self.input_name.clear()
            self.input_price.setValue(10.0)
            self.input_stock.setValue(0)
        else:
            papers = db.get_papers()
            p = next((x for x in papers if x[0] == paper_id), None)
            if p:
                self.input_name.setText(str(p[1]))
                self.input_price.setValue(float(p[2]))
                self.input_stock.setValue(0)

    def save_data(self):
        name = self.input_name.text()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название бумаги!")
            return
        
        existing_paper = db.get_paper_by_name(name)
        qty_to_add = self.input_stock.value()

        # ЕСЛИ РЕДАКТИРУЕМ СУЩЕСТВУЮЩУЮ БУМАГУ (двойной клик)
        if self.paper_data:
            new_stock = self.paper_data[3] + qty_to_add # Прибавляем к старому остатку
            db.update_paper(self.paper_data[0], name, self.input_price.value(), new_stock)
            
        # ЕСЛИ ДОБАВЛЯЕМ СУЩЕСТВУЮЩУЮ ЧЕРЕЗ ВЫПАДАЮЩИЙ СПИСОК
        elif existing_paper:
            new_stock = existing_paper[3] + qty_to_add
            db.update_paper(existing_paper[0], existing_paper[1], self.input_price.value(), new_stock)
            
        # ЕСЛИ СОЗДАЕМ НОВУЮ
        else:
            db.add_paper(name, self.input_price.value(), qty_to_add)
            
        self.accept()

    def delete_data(self):
        reply = QMessageBox.question(self, 'Удаление', 'Вы уверены, что хотите удалить этот материал?', 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            db.delete_paper(self.paper_data[0])
            self.accept()