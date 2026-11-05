from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt
from ui.add_material import AddPaperDialog
from ui import styles
import database as db

class StockPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.table_stock = QTableWidget()
        self.table_stock.setColumnCount(3)
        self.table_stock.setHorizontalHeaderLabels(["Бумага", "Цена (₽)", "Остаток (л.)"])
        self.table_stock.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_stock.verticalHeader().setVisible(False)
        self.table_stock.setShowGrid(False)
        self.table_stock.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_stock.verticalHeader().setDefaultSectionSize(50)
        self.table_stock.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        
        header = self.table_stock.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        self.table_stock.setStyleSheet(styles.STYLE_TABLE)
        self.table_stock.cellDoubleClicked.connect(self.edit_paper)
        layout.addWidget(self.table_stock)
        
        self.load_stock()

    def load_stock(self):
        papers = db.get_papers()
        self.table_stock.setRowCount(len(papers))
        for row, p in enumerate(papers):
            item_name = QTableWidgetItem(str(p[1]))
            item_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_name.setData(Qt.ItemDataRole.UserRole, p[0])
            
            item_price = QTableWidgetItem(f"{p[2]} ₽")
            item_price.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            item_stock = QTableWidgetItem(f"{p[3]} л.")
            item_stock.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table_stock.setItem(row, 0, item_name)
            self.table_stock.setItem(row, 1, item_price)
            self.table_stock.setItem(row, 2, item_stock)

    def edit_paper(self, row, column):
        paper_id = self.table_stock.item(row, 0).data(Qt.ItemDataRole.UserRole)
        papers = db.get_papers()
        paper_data = next((p for p in papers if p[0] == paper_id), None)
        
        if paper_data:
            dialog = AddPaperDialog(self, paper_data)
            if dialog.exec():
                self.load_stock()