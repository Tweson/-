from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
                             QComboBox, QDateEdit, QPushButton)
from PyQt6.QtCore import QDate
import database as db
from ui import styles

class StatsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(15)
        
        top_bar = QHBoxLayout()
        
        self.lbl_period = QLabel("Период:")
        self.lbl_period.setStyleSheet(f"font-weight: bold; font-size: 14px; {styles.get_text_main()}")
        top_bar.addWidget(self.lbl_period)
        
        self.combo_period = QComboBox()
        self.combo_period.addItems(["Сегодня", "Вчера", "За всё время", "Свой период"])
        self.combo_period.setStyleSheet(styles.get_input_style())
        self.combo_period.currentIndexChanged.connect(self.on_period_change)
        top_bar.addWidget(self.combo_period)
        
        self.lbl_from = QLabel("С:")
        self.lbl_from.setStyleSheet(styles.get_text_main())
        self.lbl_from.hide()
        top_bar.addWidget(self.lbl_from)
        
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addDays(-2))
        self.date_from.setCalendarPopup(True)
        self.date_from.setStyleSheet(styles.get_input_style())
        self.date_from.hide()
        top_bar.addWidget(self.date_from)
        
        self.lbl_to = QLabel("По:")
        self.lbl_to.setStyleSheet(styles.get_text_main())
        self.lbl_to.hide()
        top_bar.addWidget(self.lbl_to)
        
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        self.date_to.setStyleSheet(styles.get_input_style())
        self.date_to.hide()
        top_bar.addWidget(self.date_to)
        
        self.btn_apply = QPushButton("Применить")
        self.btn_apply.setStyleSheet(styles.STYLE_BTN_BLUE)
        self.btn_apply.hide()
        self.btn_apply.clicked.connect(self.load_stats)
        top_bar.addWidget(self.btn_apply)

        top_bar.addStretch()
        self.layout.addLayout(top_bar)

        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(10)
        
        self.card_rev = self.create_card("Выручка", "0 ₽", "#10B981")
        self.card_tot = self.create_card("Всего заказов", "0", "#2563EB")
        self.card_work = self.create_card("В работе", "0", "#F59E0B")
        self.card_ready = self.create_card("Готово", "0", "#8B5CF6")
        self.card_issued = self.create_card("Выдано", "0", "#64748B")
        self.card_due_today = self.create_card("Сдать сегодня!", "0", "#EF4444")
        
        self.cards_layout.addWidget(self.card_rev)
        self.cards_layout.addWidget(self.card_tot)
        self.cards_layout.addWidget(self.card_work)
        self.cards_layout.addWidget(self.card_ready)
        self.cards_layout.addWidget(self.card_issued)
        self.cards_layout.addWidget(self.card_due_today)
        
        self.layout.addLayout(self.cards_layout)
        self.load_stats()

    def create_card(self, title, value, color):
        card = QFrame()
        card.setStyleSheet(styles.get_stats_card_style())
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"font-size: 12px; font-weight: bold; {styles.get_text_sub()}")
        layout.addWidget(lbl_title)
        
        lbl_value = QLabel(value)
        lbl_value.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: 900; border: none;")
        lbl_value.setObjectName("value_label")
        layout.addWidget(lbl_value)
        
        return card

    def on_period_change(self, index):
        if self.combo_period.currentText() == "Свой период":
            self.lbl_from.show()
            self.date_from.show()
            self.lbl_to.show()
            self.date_to.show()
            self.btn_apply.show()
        else:
            self.lbl_from.hide()
            self.date_from.hide()
            self.lbl_to.hide()
            self.date_to.hide()
            self.btn_apply.hide()
            self.load_stats()

    def load_stats(self):
        period = self.combo_period.currentText()
        
        if period == "Свой период":
            date_start = self.date_from.date().toString("yyyy-MM-dd")
            date_end = self.date_to.date().toString("yyyy-MM-dd")
            stats = db.get_stats_filtered(period, date_start, date_end)
        else:
            stats = db.get_stats_filtered(period)
        
        self.card_rev.findChild(QLabel, "value_label").setText(f"{stats['revenue']:,.2f} ₽".replace(",", " "))
        self.card_tot.findChild(QLabel, "value_label").setText(str(stats['total_orders']))
        self.card_work.findChild(QLabel, "value_label").setText(str(stats['in_work']))
        self.card_ready.findChild(QLabel, "value_label").setText(str(stats['ready']))
        self.card_issued.findChild(QLabel, "value_label").setText(str(stats['issued']))
        self.card_due_today.findChild(QLabel, "value_label").setText(str(stats['due_today']))