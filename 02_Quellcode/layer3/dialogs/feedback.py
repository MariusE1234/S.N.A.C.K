#Datei feedback.py
#libraries-imports
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QVBoxLayout

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
