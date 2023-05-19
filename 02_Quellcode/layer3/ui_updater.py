#Datei ui_updater.py
from layer3.observer import Observer
PRODUCT_BUTTONS="product_buttons"
STATUS_LABEL= "status_label"
COIN_LABEL= "coin_label"

class UIUpdater(Observer):
    def __init__(self, products_groupbox, product_buttons, status_label, coin_label, product_button_factory):
        self.products_groupbox = products_groupbox
        self.product_buttons = product_buttons
        self.status_label = status_label
        self.coin_label = coin_label
        self.product_button_factory = product_button_factory

    def update(self, notification_type, *args):
        if notification_type == PRODUCT_BUTTONS:
            self.update_product_buttons(*args)
        elif notification_type == STATUS_LABEL:
            self.update_status_label(*args)
        elif notification_type == COIN_LABEL:
            self.update_coin_label(*args)
            
    def update_product_buttons(self, vending_machine, select_product_callback):
        # Löschen Sie alle Produkt-Buttons und entfernen Sie sie aus dem Layout
        for button in self.product_buttons:
            button.deleteLater()
            button.setParent(None)

        self.product_buttons = []

        # Erhalten des products_layout aus der QGroupBox im Hauptlayout
        products_layout = self.products_groupbox.layout()  # Hier das products_layout abrufen
        for i, product in enumerate(vending_machine.get_products()):
            button = self.create_product_button(product, select_product_callback)
            self.product_buttons.append(button)
            products_layout.addWidget(button, i // 3, i % 3)

    def create_product_button(self, product, select_product_callback):
        button = self.product_button_factory.create_product_button(product)
        button.clicked.connect(lambda _, p=product: select_product_callback(p))
        return button

    def update_status_label(self, text):
        self.status_label.setText(text)

    def update_coin_label(self, amount):
        self.coin_label.setText(f"{amount} €")
