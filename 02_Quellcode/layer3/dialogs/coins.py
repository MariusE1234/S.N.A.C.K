#Datei coins.py
#libraries-imports
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QHBoxLayout
from abc import abstractmethod

class CoinsDialog(QDialog):
    def __init__(self, coinController, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Münzen einwerfen")
        self.setWindowIcon(QIcon("04_Images//money_icon.jpg"))
        self.coinController = coinController
        self.selected_coin = None
        self.setup_ui()

    def setup_ui(self):
        self.coin_buttons = []
        layout = QVBoxLayout()

        coins_layout = QHBoxLayout()  # Ändern Sie das Layout von QGridLayout zu QHBoxLayout
        for i, coin in enumerate(self.coinController.get_availableCoins()):
            pixmap = QPixmap(f"04_Images//coin_{coin.value}.jpg")  # Pfad zum Bild der jeweiligen Münze
            pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio)  # Skalieren Sie das Bild auf die gewünschte Größe
            icon = QIcon(pixmap)
            button = QPushButton()
            button.setIcon(icon)
            button.setIconSize(pixmap.rect().size())
            button.setFixedSize(60, 60)  
            button.clicked.connect(lambda _, c=coin: self.select_coin(c))
            self.coin_buttons.append(button)
            coins_layout.addWidget(button)

        layout.addLayout(coins_layout)

        buttons_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        buttons_layout.addWidget(self.ok_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)


    def select_coin(self, coin):
        self.selected_coin = coin
