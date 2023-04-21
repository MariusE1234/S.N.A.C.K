class UIUpdater:
    def __init__(self, products_groupbox, product_buttons, status_label, coin_label, product_button_factory):
        self.products_groupbox = products_groupbox
        self.product_buttons = product_buttons
        self.status_label = status_label
        self.coin_label = coin_label
        self.product_button_factory = product_button_factory

    def update_product_buttons(self, vending_machine, select_product_callback):
        # Löschen Sie alle Produkt-Buttons und entfernen Sie sie aus dem Layout
        for button in self.product_buttons:
            button.deleteLater()
            button.setParent(None)

        self.product_buttons = []

        # Erhalten Sie das products_layout aus der QGroupBox im Hauptlayout
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
