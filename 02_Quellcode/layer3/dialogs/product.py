#Datei product.py
#File-imports
from layer2.validator import DefaultProductValidator
#libraries-imports
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QGridLayout, QLineEdit, QMessageBox, QSpinBox, QDoubleSpinBox,QFileDialog
from abc import abstractmethod

class ProductDialog(QDialog):
    def __init__(self, productcontroller, parent=None, existing_names=None, current_product=None):
        super().__init__(parent)
        self.existing_names = existing_names if existing_names else []
        self.current_product = current_product
        self.productcontroller = productcontroller
        self.setWindowTitle(self.get_dialog_title())
        self.setWindowIcon(QIcon(self.get_dialog_icon()))
        self.setup_ui()

    @abstractmethod
    def get_dialog_title(self):
        pass

    @abstractmethod
    def get_dialog_icon(self):
        pass

    @abstractmethod
    def get_submit_button_text(self):
        pass

    @abstractmethod
    def save_product(self):
        pass

    @abstractmethod
    def validate_input(self, name, image_path):
        pass

    def setup_ui(self):
        layout = QGridLayout()

        self.name_label, self.name_edit = self.create_input_field(layout, "Produktname:", QLineEdit(), 0)
        self.price_label, self.price_edit = self.create_input_field(layout, "Preis:", QDoubleSpinBox(), 1)
        self.price_edit.setSingleStep(0.5)  
        self.price_edit.setDecimals(2)  
        self.price_edit.setMinimum(0.00) 
        self.price_edit.setMaximum(500) 
        self.stock_label, self.stock_edit = self.create_input_field(layout, "Bestand:", QSpinBox(), 2)
        self.stock_edit.setMinimum(0) 
        self.stock_edit.setMaximum(999) 

        self.image_label, self.image_path_edit = self.create_input_field(layout, "Bild:", QLineEdit(), 3)
        self.image_path_edit.setReadOnly(True)
        self.choose_image_button = QPushButton("Bild auswählen")
        self.choose_image_button.clicked.connect(self.choose_image)
        layout.addWidget(self.choose_image_button, 3, 2)

        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button, 4, 0)

        self.add_button = QPushButton(self.get_submit_button_text())
        self.add_button.clicked.connect(self.save_product)
        layout.addWidget(self.add_button, 4, 1)

        self.setLayout(layout)

        if self.current_product:
            self.name_edit.setText(self.current_product.name)
            self.price_edit.setValue(self.current_product.price)
            self.stock_edit.setValue(self.current_product.stock)
            self.image_path_edit.setText(self.current_product.image_path)

    def create_input_field(self, layout, label_text, input_widget, row):
        label = QLabel(label_text)
        layout.addWidget(label, row, 0)
        layout.addWidget(input_widget, row, 1)
        return label, input_widget

    def choose_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Bild auswählen", "",
                                                   "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)", options=options)
        if file_name:
            self.image_path_edit.setText(file_name)

    def get_product(self):
        name = self.name_edit.text().strip()
        price = self.price_edit.value()
        stock = self.stock_edit.value()
        image_path = self.image_path_edit.text().strip()
        return self.productcontroller.create_product(name, price, stock, image_path)

class AddProductDialog(ProductDialog):
    def get_dialog_title(self):
        return "Produkt hinzufügen"

    def get_dialog_icon(self):
        return "04_Images//add_icon.png"

    def get_submit_button_text(self):
        return "Hinzufügen"

    def validate_input(self, name, image_path):
        valid_name, name_error_msg = DefaultProductValidator.is_valid_name(name, self.existing_names)
        if not valid_name:
            QMessageBox.warning(self, "Fehler", name_error_msg)
            return False

        valid_image_path, image_path_error_msg = DefaultProductValidator.is_valid_image_path(image_path)
        if not valid_image_path:
            QMessageBox.warning(self, "Fehler", image_path_error_msg)
            return False

        return True

    def save_product(self):
        name = self.name_edit.text().strip()
        price = self.price_edit.value()
        stock = self.stock_edit.value()
        image_path = self.image_path_edit.text().strip()

        if not self.validate_input(name, image_path):
            return

        self.accept()

class EditProductDialog(ProductDialog):
    def get_dialog_title(self):
        return "Produkt bearbeiten"

    def get_dialog_icon(self):
        return "04_Images//edit_icon.png"

    def get_submit_button_text(self):
        return "Speichern"

    def validate_input(self, name, image_path):
        valid_name, name_error_msg = DefaultProductValidator.is_valid_name(name, self.existing_names, self.current_product)
        if not valid_name:
            QMessageBox.warning(self, "Fehler", name_error_msg)
            return False

        return True

    def save_product(self):
        name = self.name_edit.text().strip()
        price = self.price_edit.value()
        stock = self.stock_edit.value()
        image_path = self.image_path_edit.text().strip()

        if not self.validate_input(name, image_path):
            return

        self.current_product.name = name
        self.current_product.price = price
        self.current_product.stock = stock
        self.current_product.image_path = image_path
        self.accept()
