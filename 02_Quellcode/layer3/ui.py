# File-imports
from layer3.controllers import VendingMachineController
from layer3.factories import ProductButtonFactory, CoinsDialogFactory, PinDialogFactory, ConfigDialogFactory, InfoDialogFactory
from layer3.ui_updater import UIUpdater
from layer3.dialogs.coins import CoinsDialog
from layer3.dialogs.pin import PinDialog
from layer3.dialogs.config import ConfigDialog
from layer3.dialogs.info import InfoDialog
# Libraries-imports
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QGridLayout, QWidget, QMessageBox, QGroupBox

class VendingMachineGUI(QWidget):
    def __init__(self,
                 vmcontroller: VendingMachineController,
                 configcontroller,
                 statcontroller,
                 coincontroller,
                 productcontroller,
                 transactioncontroller,
                 product_button_factory: ProductButtonFactory,
                 coins_dialog_factory: CoinsDialogFactory,
                 pin_dialog_factory: PinDialogFactory,
                 config_dialog_factory: ConfigDialogFactory,
                 info_dialog_factory: InfoDialogFactory):
        super().__init__()
        self.vmcontroller = vmcontroller
        self.configcontroller = configcontroller
        self.statcontroller = statcontroller
        self.coincontroller = coincontroller
        self.productcontroller = productcontroller
        self.transactioncontroller = transactioncontroller
        self.product_button_factory = product_button_factory
        self.coins_dialog_factory = coins_dialog_factory
        self.pin_dialog_factory = pin_dialog_factory
        self.config_dialog_factory = config_dialog_factory
        self.info_dialog_factory = info_dialog_factory
        self.product_buttons = []
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("S.N.A.C.K Verkaufsautomat")
        self.setWindowIcon(QIcon("04_Images//vm_icon.png"))
        self.product_buttons = []
        layout = QGridLayout()

        self.status_label = QLabel("Bitte wählen Sie ein Produkt aus.")
        layout.addWidget(self.status_label, 0, 0, 1, 3)

        self.products_groupbox = QGroupBox("Produkte")
        products_layout = QGridLayout()
        self.products_groupbox.setLayout(products_layout)
        layout.addWidget(self.products_groupbox, 1, 0, 1, 3)

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

        self.info_button = QPushButton("Info")
        self.info_button.clicked.connect(self.show_info_dialog)
        layout.addWidget(self.info_button, 6, 3)

        self.ui_updater = UIUpdater(self.products_groupbox, self.product_buttons, self.status_label, self.coin_label, self.product_button_factory)
        self.ui_updater.update_product_buttons(self.vmcontroller, self.select_product)

        self.setLayout(layout)
        self.vmcontroller.add_observer(self.ui_updater)

    def select_product(self, product):
        self.vmcontroller.notify_observers("status_label", f"Bitte werfen Sie {product.price} € ein.")
        self.vmcontroller.select_product(product)
        self.ui_updater.update_status_label(f"Bitte werfen Sie {product.price} € ein.")

    def buy_product(self):
        message = self.vmcontroller.buy_product()
        self.ui_updater.update_status_label(message)
        amount = self.coincontroller.get_total_amount()
        self.ui_updater.update_coin_label(amount)

    def show_coin_dialog(self):
        dialog = self.coins_dialog_factory.create_coins_dialog(self.coincontroller, CoinsDialog)
        if dialog.exec_() == QDialog.Accepted:
            self.coincontroller.add_coin(dialog.selected_coin)
            amount = self.coincontroller.get_total_amount()
            self.vmcontroller.notify_observers("coin_label", amount)
            self.ui_updater.update_coin_label(amount)

    def show_config_dialog(self):
        if self.show_pin_dialog():
            dialog = self.config_dialog_factory.create_config_dialog(self.vmcontroller, self.configcontroller, self.productcontroller, self.transactioncontroller, ConfigDialog)
            if dialog.exec_() == QDialog.Accepted:
                new_products = dialog.get_products_from_table()
                self.vmcontroller.product_list.delete_products()
                self.vmcontroller.product_list.save_products(new_products)
                self.vmcontroller.notify_observers("product_buttons", self.vmcontroller, self.select_product)
                self.refresh_product_buttons()

    def refresh_product_buttons(self):
        self.vmcontroller.notify_observers("product_buttons", self.vmcontroller, self.select_product)
        self.ui_updater.update_product_buttons(self.vmcontroller, self.select_product)

    def show_pin_dialog(self):
        pin_dialog = self.pin_dialog_factory.create_pin_dialog(PinDialog)
        result = pin_dialog.exec_()

        if result == QDialog.Accepted:
            entered_pin = pin_dialog.get_pin()
            correct_pin = str(self.vmcontroller.config_data_access.get_config("pin"))

            if entered_pin == correct_pin:
                return True
            else:
                QMessageBox.warning(self, "Falscher Pin", "Zugriff verweigert")
                return False
        else:
            return False

    def show_info_dialog(self):
        info_dialog = self.info_dialog_factory.create_info_dialog(InfoDialog)
        info_dialog.exec_()


