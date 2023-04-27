#Datei info.py
#File-imports
from layer3.dialogs.feedback import FeedbackDialog
#libraries-imports
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QVBoxLayout, QSlider

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
