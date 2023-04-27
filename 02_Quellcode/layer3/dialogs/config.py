#Datei config.py
#File-imports
from layer3.dialogs.product import AddProductDialog, EditProductDialog
from layer3.dialogs.pin import PinDialog
from layer3.dialogs.statistic import StatDialog
#libraries-imports
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QDialog, QTableWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QScrollArea, QListWidget, QMessageBox

class ConfigDialog(QDialog):
    def __init__(
        self,
        vmcontroller,
        configcontroller,
        productcontroller,
        transactioncontroller,
        parent=None
    ):
        super().__init__(parent)
        self.setWindowTitle("Konfigurationsmenü")
        self.setWindowIcon(QIcon("04_Images//config_icon.png"))
        self.vmcontroller = vmcontroller
        self.configcontroller = configcontroller
        self.productcontroller = productcontroller
        self.transactioncontroller = transactioncontroller
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()

        # Produkte
        product_list = self.productcontroller.get_products()
        product_layout = QVBoxLayout()
        product_label = QLabel("Produkte")
        product_layout.addWidget(product_label)
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(4)
        self.product_table.setColumnWidth(0, 400)
        self.product_table.setColumnWidth(1, 200)
        self.product_table.setColumnWidth(2, 200)
        self.product_table.setColumnWidth(3, 400)
        self.product_table.setRowCount(len(product_list))
        self.product_table.setHorizontalHeaderLabels(["Produktname", "Preis", "Bestand", "Bildpfad"])
        self.product_table.verticalHeader().setVisible(False)

        for i, product in enumerate(product_list):
            name_item = self.create_non_editable_table_item(product.name)
            price_item = self.create_non_editable_table_item(str(product.price))
            stock_item = self.create_non_editable_table_item(str(product.stock))
            image_path_item = self.create_non_editable_table_item(product.image_path)
            self.product_table.setItem(i, 0, name_item)
            self.product_table.setItem(i, 1, price_item)
            self.product_table.setItem(i, 2, stock_item)
            self.product_table.setItem(i, 3, image_path_item)

        self.product_table.resizeColumnsToContents()
        product_layout.addWidget(self.product_table)

        # Schaltflächen zum Hinzufügen, Bearbeiten und Löschen von Produkten
        button_row1_layout = QHBoxLayout()
        self.add_button = QPushButton("Produkt hinzufügen")
        self.add_button.clicked.connect(self.add_product)
        button_row1_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Produkt bearbeiten")
        self.edit_button.clicked.connect(self.edit_product)
        button_row1_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Produkt löschen")
        self.delete_button.clicked.connect(self.delete_product)
        button_row1_layout.addWidget(self.delete_button)

        product_layout.addLayout(button_row1_layout)

        # Schaltfläche für weitere Buttons
        button_row2_layout = QHBoxLayout()
        self.change_pin_button = QPushButton("PIN ändern")
        self.change_pin_button.clicked.connect(self.change_pin)
        button_row2_layout.addWidget(self.change_pin_button)

        self.stat_button = QPushButton("Statistik")
        self.stat_button.clicked.connect(self.show_stat_dialog)
        button_row2_layout.addWidget(self.stat_button)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        button_row2_layout.addWidget(self.ok_button)

        product_layout.addLayout(button_row2_layout)

        layout.addLayout(product_layout)

        # Transaktionen
        transaction_layout = QVBoxLayout()
        transaction_label = QLabel("Transaktionen")
        transaction_layout.addWidget(transaction_label)

        self.transaction_list = QListWidget()
        transaction_log = self.transactioncontroller.get_transactions()
        if transaction_log:
            for transaction in transaction_log:
                self.transaction_list.addItem(str(transaction))

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.transaction_list)
        transaction_layout.addWidget(scroll_area)

        layout.addLayout(transaction_layout)
        self.setLayout(layout)

    def create_non_editable_table_item(self, text):
        item = QTableWidgetItem(text)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        return item

    def add_product(self):
        add_product_dialog = AddProductDialog(productcontroller=self.productcontroller)
        result = add_product_dialog.exec_()

        if result == QDialog.Accepted:
            new_product = add_product_dialog.get_product()
            success = self.productcontroller.add_product(new_product, self.product_table)
            if success:
                row = self.product_table.rowCount()
                self.product_table.setRowCount(row + 1)
                name_item = self.create_non_editable_table_item(new_product.name)
                price_item = self.create_non_editable_table_item(str(new_product.price))
                stock_item = self.create_non_editable_table_item(str(new_product.stock))
                image_item = self.create_non_editable_table_item(new_product.image_path)
                self.product_table.setItem(row, 0, name_item)
                self.product_table.setItem(row, 1, price_item)
                self.product_table.setItem(row, 2, stock_item)
                self.product_table.setItem(row, 3, image_item)
            else:
                QMessageBox.warning(self, "Fehler", "Ein Produkt mit diesem Namen existiert bereits.")

    def edit_product(self):
        row = self.product_table.currentRow()
        if row != -1:
            edit_product_dialog = EditProductDialog(productcontroller=self.productcontroller, current_product=self.productcontroller.create_product(self.product_table.item(row, 0).text(), float(self.product_table.item(row, 1).text()), int(self.product_table.item(row, 2).text()), self.product_table.item(row, 3).text()))
            result = edit_product_dialog.exec_()

            if result == QDialog.Accepted:
                edited_product = edit_product_dialog.get_product()
                current_product = self.productcontroller.create_product(self.product_table.item(row, 0).text(), float(self.product_table.item(row, 1).text()), int(self.product_table.item(row, 2).text()), self.product_table.item(row, 3).text())
                success = self.productcontroller.edit_product(current_product, edited_product, self.product_table, exclude_row=row)
                if success:
                    name_item = self.create_non_editable_table_item(edited_product.name)
                    price_item = self.create_non_editable_table_item(str(edited_product.price))
                    stock_item = self.create_non_editable_table_item(str(edited_product.stock))
                    image_item = self.create_non_editable_table_item(edited_product.image_path)
                    self.product_table.setItem(row, 0, name_item)
                    self.product_table.setItem(row, 1, price_item)
                    self.product_table.setItem(row, 2, stock_item)
                    self.product_table.setItem(row, 3, image_item)
                else:
                    QMessageBox.warning(self, "Fehler", "Ein Produkt mit diesem Namen existiert bereits.")
    
    def delete_product(self):
        row = self.product_table.currentRow()
        if row != -1:
            product_name = self.product_table.item(row, 0).text()
            self.productcontroller.delete_product(product_name)
            self.product_table.removeRow(row)

    def change_pin(self):
        new_pin_dialog = PinDialog(self)
        new_pin_dialog.setWindowTitle("Neue PIN eingeben")
        
        result = new_pin_dialog.exec_()
        
        if result == QDialog.Accepted:
            new_pin = new_pin_dialog.get_pin()
            self.configcontroller.update_config("pin", new_pin)  
            QMessageBox.information(self, "Erfolg", "Die PIN wurde erfolgreich geändert.")

    def get_products_from_table(self):
        return self.productcontroller.get_products_from_table(self.product_table)
        
    def show_stat_dialog(self):
        stat_dialog = StatDialog(self, self.transactioncontroller)
        stat_dialog.exec_()
