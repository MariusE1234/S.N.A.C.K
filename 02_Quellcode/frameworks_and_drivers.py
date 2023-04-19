
from PyQt5.QtCore import Qt,QSize, QRegExp
from PyQt5.QtGui import QRegExpValidator,QIcon,QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QDialog, QTableWidgetItem, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QTableWidget, QScrollArea, QListWidget, QWidget, QLineEdit, QMessageBox, QSpinBox, QDoubleSpinBox,QFileDialog,QGroupBox, QSlider
from use_cases import Transaction, Product, Coin, CoinSlot, VendingMachine, IProductList, ITransactionLog, ProductList
from interface_adapters import IDataAccess, Database

class CoinsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Münzen einwerfen")
        self.setWindowIcon(QIcon("02_Quellcode//images//money_icon.jpg"))
        self.coins = [Coin(value) for value in Coin.available_coins]
        self.selected_coin = None
        self.setup_ui()

    def setup_ui(self):
        self.coin_buttons = []
        layout = QVBoxLayout()

        coins_layout = QHBoxLayout()  # Ändern Sie das Layout von QGridLayout zu QHBoxLayout
        for i, coin in enumerate(self.coins):
            pixmap = QPixmap(f"02_Quellcode//images//coin_{coin.value}.jpg")  # Pfad zum Bild der jeweiligen Münze
            pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio)  # Skalieren Sie das Bild auf die gewünschte Größe
            icon = QIcon(pixmap)
            button = QPushButton()
            button.setIcon(icon)
            button.setIconSize(pixmap.rect().size())
            button.setFixedSize(60, 60)  # Setzen Sie eine feste Größe für den Button
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

class PinDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PIN eingeben")
        self.setWindowIcon(QIcon("02_Quellcode//images//lock_icon.png"))
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
        #PIN-Länge auf 6 Zeichen beschränken
        self.pin_input.setMaxLength(6)

        layout.addWidget(self.pin_input)

        buttons_layout = QGridLayout()
        for i in range(1, 10):
            button = QPushButton(str(i))
            button.clicked.connect(lambda _, num=i: self.add_number(num))
            buttons_layout.addWidget(button, (i - 1) // 3, (i - 1) % 3)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        buttons_layout.addWidget(ok_button, 3, 1)

        cancel_button = QPushButton("Abbrechen")  # Hinzufügen einer Schaltfläche "Abbrechen"
        cancel_button.clicked.connect(self.reject)  # Verbinden der Schaltfläche "Abbrechen" mit dem Signal "rejected"
        buttons_layout.addWidget(cancel_button, 3, 0)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def add_number(self, number):
        current_text = self.pin_input.text()
        self.pin_input.setText(current_text + str(number))

    def get_pin(self):
        return self.pin_input.text()

    def reject(self):
        self.user_canceled = True  # Setzen Sie user_canceled auf True, wenn der Benutzer auf "Abbrechen" klickt
        super().reject()

class ConfigDialog(QDialog):
    def __init__(
        self,
        parent=None,
        transaction_log: ITransactionLog = None,
        product_list: IProductList = None,
        data_access: IDataAccess = None,  # Hinzufügen des IDataAccess-Interfaces
    ):
        super().__init__(parent)
        self.setWindowTitle("Konfigurationsmenü")
        self.setWindowIcon(QIcon("02_Quellcode//images//config_icon.png"))
        self.product_list = product_list
        self.transaction_log = transaction_log
        self.data_access = data_access  # Speichern des data_access-Objekts
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()

        # Produkte
        product_layout = QVBoxLayout()
        product_label = QLabel("Produkte")
        product_layout.addWidget(product_label)
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(4)
        self.product_table.setColumnWidth(0, 400)
        self.product_table.setColumnWidth(1, 200)
        self.product_table.setColumnWidth(2, 200)
        self.product_table.setColumnWidth(3, 400)
        self.product_table.setRowCount(len(self.product_list.products))
        self.product_table.setHorizontalHeaderLabels(["Produktname", "Preis", "Bestand", "Bildpfad"])
        self.product_table.verticalHeader().setVisible(False)

        for i, product in enumerate(self.product_list.products):
            name_item = QTableWidgetItem(product.name)
            price_item = QTableWidgetItem(str(product.price))
            stock_item = QTableWidgetItem(str(product.stock))
            image_path_item = QTableWidgetItem(product.image_path)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            price_item.setFlags(price_item.flags() & ~Qt.ItemIsEditable)
            stock_item.setFlags(stock_item.flags() & ~Qt.ItemIsEditable)
            image_path_item.setFlags(image_path_item.flags() & ~Qt.ItemIsEditable)  # Bildpfad sollte nicht bearbeitbar sein
            self.product_table.setItem(i, 0, name_item)
            self.product_table.setItem(i, 1, price_item)
            self.product_table.setItem(i, 2, stock_item)
            self.product_table.setItem(i, 3, image_path_item)  # Bildpfad-Element setzen

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
        if self.transaction_log:
            for transaction in self.transaction_log.get_transactions():
                self.transaction_list.addItem(str(transaction))

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.transaction_list)
        transaction_layout.addWidget(scroll_area)

        layout.addLayout(transaction_layout)
        self.setLayout(layout)


    def is_name_unique(self, name, exclude_row=None):
        for row in range(self.product_table.rowCount()):
            if row != exclude_row and self.product_table.item(row, 0).text() == name:
                return False
        return True

    def add_product(self):
        add_product_dialog = AddProductDialog(self)
        result = add_product_dialog.exec_()

        if result == QDialog.Accepted:
            new_product = add_product_dialog.get_product()
            if self.is_name_unique(new_product.name):
                self.data_access.add_product(new_product)  # Verwenden von data_access statt database
                row = self.product_table.rowCount()
                self.product_table.setRowCount(row + 1)
                name_item = QTableWidgetItem(new_product.name)
                price_item = QTableWidgetItem(str(new_product.price))
                stock_item = QTableWidgetItem(str(new_product.stock))
                image_item = QTableWidgetItem(new_product.image_path)
                name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
                price_item.setFlags(price_item.flags() & ~Qt.ItemIsEditable)
                stock_item.setFlags(stock_item.flags() & ~Qt.ItemIsEditable)
                image_item.setFlags(image_item.flags() & ~Qt.ItemIsEditable)
                self.product_table.setItem(row, 0, name_item)
                self.product_table.setItem(row, 1, price_item)
                self.product_table.setItem(row, 2, stock_item)
                self.product_table.setItem(row, 3, image_item)
            else:
                QMessageBox.warning(self, "Fehler", "Ein Produkt mit diesem Namen existiert bereits.")

    def edit_product(self):
        row = self.product_table.currentRow()
        if row != -1:
            edit_product_dialog = EditProductDialog(self, current_product=Product(self.product_table.item(row, 0).text(), float(self.product_table.item(row, 1).text()), int(self.product_table.item(row, 2).text()),self.product_table.item(row, 3).text()))
            result = edit_product_dialog.exec_()

            if result == QDialog.Accepted:
                edited_product = edit_product_dialog.get_product()
                if self.is_name_unique(edited_product.name, exclude_row=row):
                    current_product = Product(self.product_table.item(row, 0).text(), float(self.product_table.item(row, 1).text()), int(self.product_table.item(row, 2).text()),self.product_table.item(row, 3).text())
                    self.data_access.update_product(current_product, edited_product)
                    name_item = QTableWidgetItem(edited_product.name)
                    price_item = QTableWidgetItem(str(edited_product.price))
                    stock_item = QTableWidgetItem(str(edited_product.stock))
                    image_item = QTableWidgetItem(edited_product.image_path)
                    name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
                    price_item.setFlags(price_item.flags() & ~Qt.ItemIsEditable)
                    stock_item.setFlags(stock_item.flags() & ~Qt.ItemIsEditable)
                    image_item.setFlags(image_item.flags() & ~Qt.ItemIsEditable)
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
            self.data_access.delete_product(product_name)  # Verwenden von data_access statt database
            self.product_table.removeRow(row)


    def get_products(self):
        products = []
        for i in range(self.product_table.rowCount()):
            name_item = self.product_table.item(i, 0)
            price_item = self.product_table.item(i, 1)
            stock_item = self.product_table.item(i, 2)
            image_item = self.product_table.item(i, 3)
            if name_item is not None and price_item is not None and stock_item is not None:
                products.append(Product(name_item.text(), float(price_item.text()), int(stock_item.text()),image_item.text()))
        return products
    
    def change_pin(self):
        new_pin_dialog = PinDialog(self)
        new_pin_dialog.setWindowTitle("Neue PIN eingeben")
        
        result = new_pin_dialog.exec_()
        
        if result == QDialog.Accepted:
            new_pin = new_pin_dialog.get_pin()
            self.data_access.update_config("pin", new_pin)  
            QMessageBox.information(self, "Erfolg", "Die PIN wurde erfolgreich geändert.")

class AddProductDialog(QDialog):
    def __init__(self, parent=None, existing_names=None):
        super().__init__(parent)
        self.existing_names = existing_names if existing_names else []
        self.setWindowTitle("Produkt hinzufügen")
        self.setWindowIcon(QIcon("02_Quellcode//images//add_icon.png"))
        self.setup_ui()

    def setup_ui(self):
        layout = QGridLayout()

        self.name_label = QLabel("Produktname:")
        layout.addWidget(self.name_label, 0, 0)
        self.name_edit = QLineEdit()
        layout.addWidget(self.name_edit, 0, 1)

        self.price_label = QLabel("Preis:")
        layout.addWidget(self.price_label, 1, 0)
        self.price_edit = QDoubleSpinBox()
        self.price_edit.setRange(0.00, 999.99)
        self.price_edit.setSingleStep(0.50)
        layout.addWidget(self.price_edit, 1, 1)

        self.stock_label = QLabel("Bestand:")
        layout.addWidget(self.stock_label, 2, 0)
        self.stock_edit = QSpinBox()
        self.stock_edit.setRange(0, 999)
        layout.addWidget(self.stock_edit, 2, 1)

        self.image_label = QLabel("Bild:")
        layout.addWidget(self.image_label, 3, 0)
        self.image_path_edit = QLineEdit()
        self.image_path_edit.setReadOnly(True)
        layout.addWidget(self.image_path_edit, 3, 1)
        self.choose_image_button = QPushButton("Bild auswählen")
        self.choose_image_button.clicked.connect(self.choose_image)
        layout.addWidget(self.choose_image_button, 3, 2)

        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button, 4, 0)

        self.add_button = QPushButton("Hinzufügen")
        self.add_button.clicked.connect(self.add_product)
        layout.addWidget(self.add_button, 4, 1)

        self.setLayout(layout)

    def choose_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Bild auswählen", "",
                                                   "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)", options=options)
        if file_name:
            self.image_path_edit.setText(file_name)

    def add_product(self):
        name = self.name_edit.text().strip()
        price = self.price_edit.value()
        stock = self.stock_edit.value()
        image_path = self.image_path_edit.text().strip()

        if not name:
            QMessageBox.warning(self, "Fehler", "Bitte geben Sie einen Produktnamen ein.")
            return

        if name in self.existing_names:
            QMessageBox.warning(self, "Fehler", "Ein Produkt mit diesem Namen existiert bereits.")
            return

        if not image_path:
            QMessageBox.warning(self, "Fehler", "Bitte wählen Sie ein Bild aus.")
            return

        self.accept()

    def get_product(self):
        name = self.name_edit.text().strip()
        price = self.price_edit.value()
        stock = self.stock_edit.value()
        image_path = self.image_path_edit.text().strip()
        return Product(name, price, stock, image_path)

class EditProductDialog(AddProductDialog):
    def __init__(self, parent=None, existing_names=None, current_product=None):
        super().__init__(parent, existing_names)
        self.setWindowTitle("Produkt bearbeiten")
        self.setWindowIcon(QIcon("02_Quellcode//images//edit_icon.png"))
        self.current_product = current_product
        if current_product:
            self.name_edit.setText(current_product.name)
            self.price_edit.setValue(current_product.price)
            self.stock_edit.setValue(current_product.stock)
            # Setzen des Bildpfads des aktuellen Produkts im image_path_edit-Textfeld
            self.image_path_edit.setText(current_product.image_path)
        self.add_button.setText("Speichern")
        self.add_button.clicked.disconnect(self.add_product)
        self.add_button.clicked.connect(self.edit_product)

        layout = self.layout()
        self.image_label = QLabel("Bild:")
        layout.addWidget(self.image_label, 3, 0)
        self.image_path_edit.setReadOnly(False)
        layout.addWidget(self.image_path_edit, 3, 1)
        self.choose_image_button = QPushButton("Bild auswählen")
        self.choose_image_button.clicked.connect(self.choose_image)
        layout.addWidget(self.choose_image_button, 3, 2)
        

    def edit_product(self):
        name = self.name_edit.text().strip()
        price = self.price_edit.value()
        stock = self.stock_edit.value()
        image_path = self.image_path_edit.text().strip()

        if not name:
            QMessageBox.warning(self, "Fehler", "Bitte geben Sie einen Produktnamen ein.")
            return

        if name != self.current_product.name and name in self.existing_names:
            QMessageBox.warning(self, "Fehler", "Ein Produkt mit diesem Namen existiert bereits.")
            return

        self.current_product.name = name
        self.current_product.price = price
        self.current_product.stock = stock
        self.current_product.image_path = image_path
        print(self.current_product.image_path)
        self.accept()

    def browse_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Bild auswählen", "", "Image Files (*.png *.jpg *.bmp *.gif *.jpeg)", options=options)
        if file_path:
            self.image_path_edit.setText(file_path)
    
    def get_product(self):
        name = self.name_edit.text().strip()
        price = self.price_edit.value()
        stock = self.stock_edit.value()
        image_path = self.image_path_edit.text().strip()
        return Product(name, price, stock, image_path)

class InfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Info - S.N.A.C.K")
        self.setWindowIcon(QIcon("02_Quellcode//images//info_icon.png"))

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
        feedback_dialog = QDialog(self)
        feedback_dialog.setWindowTitle("Zufriedenheit")

        layout = QVBoxLayout()

        emoji_label = QLabel()
        if satisfaction_value < 50:
            emoji_pixmap = QPixmap("02_Quellcode//images//sad.png")
            message = "Es tut uns leid, dass dir unser Verkaufsautomat nicht gefallen hat."
        elif 50 <= satisfaction_value < 75:
            emoji_pixmap = QPixmap("02_Quellcode//images//neutral.png")
            message = "Danke für dein Feedback. Wir werden daran arbeiten, unseren Verkaufsautomaten zu verbessern."
        else:
            emoji_pixmap = QPixmap("02_Quellcode//images//happy.png")
            message = "Wir freuen uns, dass dir unser Verkaufsautomat gefällt. Danke für dein positives Feedback!"

        # Skaliere das Bild auf die gewünschte Größe
        scaled_pixmap = emoji_pixmap.scaled(100, 100, Qt.KeepAspectRatio)
        emoji_label.setPixmap(scaled_pixmap)
        layout.addWidget(emoji_label)
        
        # Zentriere das Bild im QLabel
        emoji_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(emoji_label)

        message_label = QLabel(message)
        layout.addWidget(message_label)

        close_button = QPushButton("Schließen")
        close_button.clicked.connect(feedback_dialog.close)
        layout.addWidget(close_button)

        feedback_dialog.setLayout(layout)
        feedback_dialog.exec()

class VendingMachineGUI(QWidget):
    def __init__(
        self,
        db_path: str,
    ):
        super().__init__()
        self.data_access = Database(db_path)  # Erstellen und Speichern des data_access-Objekts
        self.product_list = ProductList(self.data_access)  # Erstellen des product_list-Objekts
        self.coin_slot = CoinSlot()  # Erstellen des coin_slot-Objekts

        self.vending_machine = VendingMachine(self.product_list, self.coin_slot, self.data_access)  # Dependency Injection
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("S.N.A.C.K Verkaufsautomat")
        self.setWindowIcon(QIcon("02_Quellcode//images//vm_icon.png"))
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
            button = QPushButton(str(product.name) + "\n" + str(product.price))
            button.setIcon(QIcon(product.image_path))
            button.setIconSize(QSize(100, 100))
            button.clicked.connect(lambda _, p=product: self.select_product(p))
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



    def select_product(self, product):
        self.vending_machine.select_product(product)
        self.status_label.setText(f"Bitte werfen Sie {self.vending_machine.selected_product.price} € ein.")

    def buy_product(self):
        message = self.vending_machine.buy_product()
        self.status_label.setText(message)
        amount = f"{self.vending_machine.coin_slot.get_total_amount()} €"
        self.coin_label.setText(str(amount))

    def show_coin_dialog(self):
        dialog = CoinsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.vending_machine.coin_slot.add_coin(dialog.selected_coin)
            self.coin_label.setText(f"{self.vending_machine.coin_slot.get_total_amount()} €")

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
            dialog = ConfigDialog(self, transaction_log=self.vending_machine.transaction_log, product_list=self.vending_machine.product_list, data_access=self.vending_machine.data_access)
            if dialog.exec_() == QDialog.Accepted:
                new_products = dialog.get_products()
                self.vending_machine.product_list.save_products(new_products)
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
            button = QPushButton(str(product.name) + "\n" + str(product.price))
            button.setIcon(QIcon(product.image_path))
            button.setIconSize(QSize(100, 100))
            button.clicked.connect(lambda _, p=product: self.select_product(p))
            self.product_buttons.append(button)
            products_layout.addWidget(button, i // 3, i % 3)

       

    def show_pin_dialog(self):
        class CustomPinDialog(PinDialog):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.user_canceled = False

            def reject(self):
                self.user_canceled = True
                super().reject()

        pin_dialog = CustomPinDialog(self)
        result = pin_dialog.exec_()

        if result == QDialog.Accepted:
            entered_pin = pin_dialog.get_pin()
            correct_pin = str(self.data_access.get_config("pin"))  # Verwenden von data_access statt database

            if entered_pin == correct_pin:
                return True
            else:
                QMessageBox.warning(self, "Falscher Pin", "Zugriff verweigert")
                return False
        else:
             return False
         
    def show_info_dialog(self):
        info_dialog = InfoDialog(self)
        info_dialog.exec_()