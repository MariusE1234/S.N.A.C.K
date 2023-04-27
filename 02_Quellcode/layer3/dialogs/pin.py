#Datei pin.py
#libraries-imports
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator,QIcon
from PyQt5.QtWidgets import QDialog, QPushButton, QGridLayout, QVBoxLayout, QLineEdit

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
