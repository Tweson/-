from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QComboBox)
import database as db

class StatsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(15)
        
        top_bar = QHBoxLayout()
        
        lbl_period = QLabel("Период:")
        lbl_period.setStyleSheet("color: #0F172A; font-weight: bold; font-size: 14px;")
        top_bar.addWidget(lbl_period)
        
        self.combo_period = QComboBox()
        self.combo_period.addItems(["Сегодня", "Вчера", "За всё время"])
        self.combo_period.setStyleSheet("padding: 6px; border: 1px solid #D1D5DB; border-radius: 6px; color: #0F172A; font-weight: bold;")
        self.combo_period.currentIndexChanged.connect(self.load_stats)
        top_bar.addWidget(self.combo_period)
        
        top_bar.addStretch()
        self.layout.addLayout(top_bar)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)
        
        self.card_rev = self.create_card("Выручка (Выдано)", "0 ₽", "#10B981")
        self.card_tot = self.create_card("Всего заказов", "0", "#0F172A")
        self.card_work = self.create_card("В работе", "0", "#2563EB")
        self.card_ready = self.create_card("Готово", "0", "#F59E0B")
        self.card_issued = self.create_card("Выдано", "0", "#64748B")
        
        cards_layout.addWidget(self.card_rev)
        cards_layout.addWidget(self.card_tot)
        cards_layout.addWidget(self.card_work)
        cards_layout.addWidget(self.card_ready)
        cards_layout.addWidget(self.card_issued)
        
        self.layout.addLayout(cards_layout)
        self.load_stats()

    def create_card(self, title, value, color):
        card = QFrame()
        card.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #E2E8F0;")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(5)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #64748B; font-size: 13px; font-weight: bold; border: none;")
        layout.addWidget(lbl_title)
        
        lbl_value = QLabel(value)
        lbl_value.setStyleSheet(f"color: {color}; font-size: 26px; font-weight: 900; border: none;")
        lbl_value.setObjectName("value_label")
        layout.addWidget(lbl_value)
        
        return card

    def load_stats(self):
        period = self.combo_period.currentText()
        stats = db.get_stats_filtered(period)
        
        self.card_rev.findChild(QLabel, "value_label").setText(f"{stats['revenue']:,.2f} ₽".replace(",", " "))
        self.card_tot.findChild(QLabel, "value_label").setText(str(stats['total_orders']))
        self.card_work.findChild(QLabel, "value_label").setText(str(stats['in_work']))
        self.card_ready.findChild(QLabel, "value_label").setText(str(stats['ready']))
        self.card_issued.findChild(QLabel, "value_label").setText(str(stats['issued']))