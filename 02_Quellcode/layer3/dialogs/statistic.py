#Datei statistic.py
#File-imports
from layer3.controllers import StatController
#libraries-imports
from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QGridLayout

class StatDialog(QDialog):
    def __init__(self, parent, transactioncontroller):
        statController = StatController(transactioncontroller)
        super().__init__(parent)
        self.setWindowTitle("Statistik")
        layout = QGridLayout()

        sales_label = QLabel(f"Gesamteinnahmen: {statController.get_total_sales()} €")
        layout.addWidget(sales_label)

        product_label = QLabel(f"verkaufte Produkte: {statController.get_sold_products()}")
        layout.addWidget(product_label)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)
