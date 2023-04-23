#Datei factorys.py
# Libraries-imports
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


class CoinsDialogFactory(ABC):

    @abstractmethod
    def create_coins_dialog(self, CoinsDialog):
        pass


class DefaultCoinsDialogFactory(CoinsDialogFactory):

    def create_coins_dialog(self, CoinsDialog):
        return CoinsDialog()


class PinDialogFactory(ABC):

    @abstractmethod
    def create_pin_dialog(self, PinDialog):
        pass


class DefaultPinDialogFactory(PinDialogFactory):

    def create_pin_dialog(self, PinDialog):
        return PinDialog()


class ConfigDialogFactory(ABC):

    @abstractmethod
    def create_config_dialog(self, product_list, transaction_data_access, product_data_access, config_data_access, ConfigDialog):
        pass


class DefaultConfigDialogFactory(ConfigDialogFactory):

    def create_config_dialog(self, product_list, transaction_data_access, product_data_access, config_data_access, ConfigDialog):
        return ConfigDialog(product_list, transaction_data_access, product_data_access, config_data_access)


class InfoDialogFactory(ABC):

    @abstractmethod
    def create_info_dialog(self, InfoDialog):
        pass


class DefaultInfoDialogFactory(InfoDialogFactory):

    def create_info_dialog(self, InfoDialog):
        return InfoDialog()
