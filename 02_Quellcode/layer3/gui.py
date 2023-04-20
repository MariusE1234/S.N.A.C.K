#File-imports
from layer2.interfaces import IDatabase
from layer2.core_functions import CoinSlot, ProductList, TransactionLog
from layer2.vending_machine import VendingMachine
from layer3.factorys import ProductButtonFactory, DialogFactory
#libraries-imports
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QGridLayout, QWidget, QMessageBox, QGroupBox

class VendingMachineGUI(QWidget):
    def __init__(self, db: IDatabase, product_button_factory: ProductButtonFactory, dialog_factory: DialogFactory):
        super().__init__()
        self.product_button_factory = product_button_factory
        self.dialog_factory = dialog_factory
        self.product_data_access = db.get_ProductDataAccess()
        self.transaction_data_access = db.get_TransactionDataAccess()
        self.config_data_access = db.get_ConfigDataAccess()
        self.product_list = ProductList(self.product_data_access)
        self.coin_slot = CoinSlot()
        self.transaction_log = TransactionLog(self.transaction_data_access)
        self.vending_machine = VendingMachine(self.product_list, self.coin_slot, self.transaction_log)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("S.N.A.C.K Verkaufsautomat")
        self.setWindowIcon(QIcon("04_Images//vm_icon.png"))
        self.product_buttons = []
        layout = QGridLayout()

        # Platzieren Sie das status_label über der QGroupBox
        self.status_label = QLabel("Bitte wählen Sie ein Produkt aus.")
        layout.addWidget(self.status_label, 0, 0, 1, 3)

        # Erstellen Sie die QGroupBox für die Produkt-Buttons
        self.products_groupbox = QGroupBox("Produkte")
        products_layout = QGridLayout()
        self.products_groupbox.setLayout(products_layout)

        for i, product in enumerate(self.vending_machine.get_products()):
            button = self.create_product_button(product)
            self.product_buttons.append(button)
            products_layout.addWidget(button, i // 3, i % 3)

        layout.addWidget(self.products_groupbox, 1, 0, 1, 3)

        # Restlichen Widgets hinzufügen (coin_button, config_button, buy_button, coin_label)
        self.coin_button = QPushButton("Münzen einwerfen")
        self.coin_button.clicked.connect(self.show_coin_dialog)
        layout.addWidget(self.coin_button, 2, 3)

        self.config_button = QPushButton("Konfigurationsmenü")
        self.config_button.clicked.connect(self.show_config_dialog)
        layout.addWidget(self.config_button, 3, 3)

        self.buy_button = QPushButton("Kaufen")
        self.buy_button.clicked.connect(self.buy_product)
        layout.addWidget(self.buy_button, 4, 3)

        self.coin_label = QLabel("0.0 €")
        layout.addWidget(self.coin_label, 5, 0)

        # Fügen Sie den Info-Button hinzu
        self.info_button = QPushButton("Info")
        self.info_button.clicked.connect(self.show_info_dialog)
        layout.addWidget(self.info_button, 6, 3)

        self.setLayout(layout)

    def create_product_button(self, product):
        button = self.product_button_factory.create_product_button(product)
        button.clicked.connect(lambda _, p=product: self.select_product(p))
        return button

    def select_product(self, product):
        self.vending_machine.select_product(product)
        self.status_label.setText(f"Bitte werfen Sie {product.price} € ein.")


    def buy_product(self):
        message = self.vending_machine.buy_product()
        self.status_label.setText(message)
        amount = f"{self.coin_slot.get_total_amount()} €"
        self.coin_label.setText(str(amount))

    def show_coin_dialog(self):
        dialog = self.dialog_factory.create_coins_dialog()
        if dialog.exec_() == QDialog.Accepted:
            self.coin_slot.add_coin(dialog.selected_coin)
            self.coin_label.setText(f"{self.coin_slot.get_total_amount()} €")

    def update_product_buttons(self):
        for i, product in enumerate(self.vending_machine.get_products()):
            button = self.product_buttons[i]
            button.setText(str(product.name) + "\n" + str(product.price))
            button.setIcon(QIcon(product.image_path))
            button.setIconSize(QSize(100, 100))
            button.clicked.disconnect()
            button.clicked.connect(lambda _, p=product: self.select_product(p))

    def show_config_dialog(self):
        if self.show_pin_dialog():
            dialog = self.dialog_factory.create_config_dialog(self.product_list, self.transaction_data_access, self.product_data_access, self.config_data_access)
            if dialog.exec_() == QDialog.Accepted:
                new_products = dialog.get_products_from_table()
                self.product_list.delete_products()
                self.product_list.save_products(new_products)
                self.refresh_product_buttons()

    def refresh_product_buttons(self):
        # Löschen Sie alle Produkt-Buttons und entfernen Sie sie aus dem Layout
        for button in self.product_buttons:
            button.deleteLater()
            button.setParent(None)

        self.product_buttons = []

        # Erhalten Sie das products_layout aus der QGroupBox im Hauptlayout
        products_layout = self.products_groupbox.layout()  # Hier das products_layout abrufen
        for i, product in enumerate(self.vending_machine.get_products()):
            button = self.create_product_button(product)
            self.product_buttons.append(button)
            products_layout.addWidget(button, i // 3, i % 3)

    def show_pin_dialog(self):
        pin_dialog = self.dialog_factory.create_pin_dialog()
        result = pin_dialog.exec_()

        if result == QDialog.Accepted:
            entered_pin = pin_dialog.get_pin()
            correct_pin = str(self.config_data_access.get_config("pin"))

            if entered_pin == correct_pin:
                return True
            else:
                QMessageBox.warning(self, "Falscher Pin", "Zugriff verweigert")
                return False
        else:
             return False
         
    def show_info_dialog(self):
        info_dialog = self.dialog_factory.create_info_dialog()
        info_dialog.exec_()
