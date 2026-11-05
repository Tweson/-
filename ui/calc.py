from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QComboBox, QMessageBox, QFrame, QDateEdit)
from PyQt6.QtCore import QDate
from logic import calculate_price
import database as db
from ui import styles

class CalcPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        left_col = QVBoxLayout()
        left_col.setSpacing(20)

        card1 = QFrame()
        card1.setStyleSheet(styles.get_card_style())
        c1 = QVBoxLayout(card1)
        c1.setContentsMargins(25, 25, 25, 25)
        c1.setSpacing(10)
        
        lbl_title1 = QLabel("01 Заказ и тираж")
        lbl_title1.setStyleSheet(f"font-size: 16px; {styles.get_text_main()}")
        c1.addWidget(lbl_title1)
        
        lbl1 = QLabel("Клиент")
        lbl1.setStyleSheet(f"font-size: 12px; {styles.get_text_sub()}")
        c1.addWidget(lbl1)
        self.input_client = QLineEdit()
        self.input_client.setStyleSheet(styles.get_input_style())
        c1.addWidget(self.input_client)

        lbl2 = QLabel("Тираж (шт)")
        lbl2.setStyleSheet(f"font-size: 12px; {styles.get_text_sub()}")
        c1.addWidget(lbl2)
        self.input_qty = QLineEdit()
        self.input_qty.setStyleSheet(styles.get_input_style())
        c1.addWidget(self.input_qty)
        
        lbl3 = QLabel("Дата сдачи")
        lbl3.setStyleSheet(f"font-size: 12px; {styles.get_text_sub()}")
        c1.addWidget(lbl3)
        self.date_deadline = QDateEdit()
        self.date_deadline.setDate(QDate.currentDate().addDays(3))
        self.date_deadline.setCalendarPopup(True)
        self.date_deadline.setStyleSheet(styles.get_input_style())
        c1.addWidget(self.date_deadline)
        
        left_col.addWidget(card1)

        card2 = QFrame()
        card2.setStyleSheet(styles.get_card_style())
        c2 = QVBoxLayout(card2)
        c2.setContentsMargins(25, 25, 25, 25)
        c2.setSpacing(10)
        
        lbl_title2 = QLabel("02 Бумага и печать")
        lbl_title2.setStyleSheet(f"font-size: 16px; {styles.get_text_main()}")
        c2.addWidget(lbl_title2)
        
        self.combo_paper = QComboBox()
        self.combo_paper.setStyleSheet(styles.get_input_style())
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
        lbl_price_title.setStyleSheet("color:#DBEAFE; font-size:14px; border:none; font-weight: bold;")
        pc.addWidget(lbl_price_title)
        self.lbl_price = QLabel("0.00 ₽")
        self.lbl_price.setStyleSheet("color: white; font-size: 38px; font-weight: 900; border: none;")
        pc.addWidget(self.lbl_price)
        right_col.addWidget(price_card)

        btn_calc = QPushButton("Рассчитать")
        btn_calc.setStyleSheet(styles.STYLE_BTN_GREEN)
        btn_calc.clicked.connect(self.do_calculate)
        right_col.addWidget(btn_calc)

        btn_save = QPushButton("Сохранить заказ")
        btn_save.setStyleSheet(styles.STYLE_BTN_BLUE)
        btn_save.clicked.connect(self.do_save)
        right_col.addWidget(btn_save)

        right_col.addStretch()
        layout.addLayout(right_col, 40)
        
        self.load_papers()

    def load_papers(self):
        self.combo_paper.clear()
        for p in db.get_papers():
            self.combo_paper.addItem(p[1], p[0])

    def do_calculate(self):
        try:
            qty = int(self.input_qty.text())
            paper_id = self.combo_paper.currentData()
            price = next(p[2] for p in db.get_papers() if p[0] == paper_id)
            total = calculate_price(qty, 4, price)
            self.lbl_price.setText(f"{total:.2f} ₽")
        except Exception:
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
            
            papers = db.get_papers()
            current_paper = next(p for p in papers if p[0] == paper_id)
            stock_available = current_paper[3]
            
            if stock_available < qty:
                QMessageBox.warning(
                    self, 
                    "Внимание: мало бумаги!", 
                    f"На складе недостаточно бумаги!\n\n"
                    f"На складе: {stock_available} л.\n"
                    f"Требуется: {qty} л.\n\n"
                    f"Заказ сохранен. На складе образовался долг, "
                    f"который нужно будет покрыть при следующей закупке."
                )
                
            db.update_stock(paper_id, qty)
            db.save_order(client, qty, total, paper_id, deadline)
            
            QMessageBox.information(self, "Успех", "Заказ сохранен в очередь!")
            
            self.input_client.clear()
            self.input_qty.clear()
            self.lbl_price.setText("0.00 ₽")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))