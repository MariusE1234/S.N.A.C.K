#File-imports
from layer3.dialogs import CoinsDialog, PinDialog, ConfigDialog, InfoDialog
#libraries-imports
from abc import ABC, abstractmethod
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

class ProductButtonFactory(ABC):

    @abstractmethod
    def create_product_button(self, product):
        pass

class DefaultProductButtonFactory(ProductButtonFactory):

    def create_product_button(self, product):
        button = QPushButton(str(product.name) + "\n" + str(product.price))
        button.setIcon(QIcon(product.image_path))
        button.setIconSize(QSize(100, 100))
        return button

class DialogFactory(ABC):

    @abstractmethod
    def create_coins_dialog(self):
        pass

    @abstractmethod
    def create_pin_dialog(self):
        pass

    @abstractmethod
    def create_config_dialog(self, product_list, transaction_data_access, product_data_access, config_data_access):
        pass

    @abstractmethod
    def create_info_dialog(self):
        pass

class DefaultDialogFactory(DialogFactory):

    def create_coins_dialog(self):
        return CoinsDialog()

    def create_pin_dialog(self):
        return PinDialog()

    def create_config_dialog(self, product_list, transaction_data_access, product_data_access, config_data_access):
        return ConfigDialog(product_list, transaction_data_access, product_data_access, config_data_access)

    def create_info_dialog(self):
        return InfoDialog()

