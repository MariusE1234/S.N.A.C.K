#Datei dialogs.py
#File-imports
from layer2.interfaces import IConfigDataAccess,IProductDataAccess, ITransactionDataAccess, IProductList
from layer2.validator import DefaultProductValidator
from layer2.core_functions import ProductList
from layer3.controllers import ConfigController, StatController, CoinController, ProductController
#libraries-imports
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator,QIcon,QPixmap
from PyQt5.QtWidgets import QLabel, QDialog, QTableWidgetItem, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QTableWidget, QScrollArea, QListWidget, QLineEdit, QMessageBox, QSpinBox, QDoubleSpinBox,QFileDialog, QSlider
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

class PinButton(QPushButton):
    def __init__(self, number, pin_dialog):
        super().__init__(str(number))
        self.number = number
        self.pin_dialog = pin_dialog
        self.clicked.connect(self.add_number)

    def add_number(self):
        current_text = self.pin_dialog.pin_input.text()
        self.pin_dialog.pin_input.setText(current_text + str(self.number))

class PinDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PIN eingeben")
        self.setWindowIcon(QIcon("04_Images//lock_icon.png"))
        self.setup_ui()
        self.user_canceled = False

    def setup_ui(self):
        layout = QVBoxLayout()
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.Password)

        # RegExpValidator erstellen, um nur Zahlen von 1-9 zuzulassen
        regex = QRegExp("[1-9]+")
        validator = QRegExpValidator(regex)
        self.pin_input.setValidator(validator)
        # PIN-Länge auf 6 Zeichen beschränken
        self.pin_input.setMaxLength(6)

        layout.addWidget(self.pin_input)

        buttons_layout = QGridLayout()
        for i in range(1, 10):
            button = PinButton(i, self)
            buttons_layout.addWidget(button, (i - 1) // 3, (i - 1) % 3)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        buttons_layout.addWidget(ok_button, 3, 1)

        cancel_button = QPushButton("Abbrechen")
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button, 3, 0)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def get_pin(self):
        return self.pin_input.text()

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

    def setup_ui(self):
        layout = QGridLayout()

        self.name_label, self.name_edit = self.create_input_field(layout, "Produktname:", QLineEdit(), 0)
        self.price_label, self.price_edit = self.create_input_field(layout, "Preis:", QDoubleSpinBox(), 1)
        self.stock_label, self.stock_edit = self.create_input_field(layout, "Bestand:", QSpinBox(), 2)

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

    @abstractmethod
    def get_submit_button_text(self):
        pass

    @abstractmethod
    def save_product(self):
        pass

    @abstractmethod
    def validate_input(self, name, image_path):
        pass

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

class FeedbackDialog(QDialog):
    def __init__(self, satisfaction_value, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Zufriedenheit")

        layout = QVBoxLayout()

        emoji_label = QLabel()
        if satisfaction_value < 50:
            emoji_pixmap = QPixmap("04_Images//sad.png")
            message = "Es tut uns leid, dass dir unser Verkaufsautomat nicht gefallen hat."
        elif 50 <= satisfaction_value < 75:
            emoji_pixmap = QPixmap("04_Images//neutral.png")
            message = "Danke für dein Feedback. Wir werden daran arbeiten, unseren Verkaufsautomaten zu verbessern."
        else:
            emoji_pixmap = QPixmap("04_Images//happy.png")
            message = "Wir freuen uns, dass dir unser Verkaufsautomat gefällt. Danke für dein positives Feedback!"

        scaled_pixmap = emoji_pixmap.scaled(100, 100, Qt.KeepAspectRatio)
        emoji_label.setPixmap(scaled_pixmap)
        layout.addWidget(emoji_label)
        emoji_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(emoji_label)

        message_label = QLabel(message)
        layout.addWidget(message_label)

        close_button = QPushButton("Schließen")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

class InfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Info - S.N.A.C.K")
        self.setWindowIcon(QIcon("04_Images//info_icon.png"))

        layout = QVBoxLayout()

        info_label = QLabel()
        info_label.setText("<h2><u>S.N.A.C.K – das stilvolle neue attraktive coole Knabbersystem</u></h2>"
                           "<p><b>Namen der Entwickler:</b></p>"
                           "<ul>"
                           "<li>Burak Özkan</li>"
                           "<li>Marius Engelmeier</li>"
                           "</ul>"
                           "<p><b>Beschreibung:</b></p>"
                           "<p>S.N.A.C.K ist ein virtueller Verkaufsautomat der verschiedensten Snacks und Getränke anbietet. "
                           "Der Automat funktioniert wie ein normaler Verkaufsautomat, Münzen werden eingeworfen und der "
                           "entsprechende Snack/Getränke wird ausgewählt. Zu dem ist es möglich den Automaten zu bearbeiten, "
                           "die Preise oder das Sortiment können festgelegt werden.</p>"
                           "<p><b>Ziel:</b></p>"
                           "<p>Unerfahrene Automatenbenutzer können sich mit dem virtuellen S.N.A.C.K auf die Benutzung von "
                           "Automaten in der Realwelt vorbereiten. Zu dem können Besitzer von Automaten lernen, wie dieser "
                           "zu initialisieren ist.</p>"
                           "<p><b>Repository:</b></p>"
                           "<p><a href='https://github.com/MariusE1234/S.N.A.C.K.git'>https://github.com/MariusE1234/S.N.A.C.K.git</a></p>")
        info_label.setWordWrap(True)
        info_label.setTextFormat(Qt.RichText)
        layout.addWidget(info_label)

        satisfaction_label = QLabel("Zufriedenheit mit dem Snack-Automaten:")
        layout.addWidget(satisfaction_label)

        satisfaction_slider = QSlider(Qt.Horizontal)
        layout.addWidget(satisfaction_slider)

        send_satisfaction_button = QPushButton("Zufriedenheit senden")
        send_satisfaction_button.clicked.connect(lambda: self.show_feedback(satisfaction_slider.value()))
        layout.addWidget(send_satisfaction_button)

        close_button = QPushButton("Schließen")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)
    
    def show_feedback(self, satisfaction_value):
        feedback_dialog = FeedbackDialog(satisfaction_value, self)
        feedback_dialog.exec()

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
