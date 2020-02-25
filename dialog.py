import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Dialog(QDialog):

    def __init__(self, parent=None, state=None):
        """Fenêtre en cas de victoire ou égalité"""
        super(Dialog, self).__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Fin")

        layout = QGridLayout(self)

        pixmapLabel = QLabel("")
        label = QLabel("")
        okButton = QPushButton("Ok")


        if state == 1:
            label.setText("Joueur 1 gagnant")
            layout.addWidget(pixmapLabel, 0, 0)
            layout.addWidget(label, 0, 1)
            layout.addWidget(okButton, 1, 1)

        elif state == 2:
            label.setText("Joueur 2 gagnant")
            layout.addWidget(pixmapLabel, 0, 0)
            layout.addWidget(label, 0, 1)
            layout.addWidget(okButton, 1, 1)

        else:
            label.setText("Egalité")
            layout.addWidget(pixmapLabel, 0, 0)
            layout.addWidget(label, 0, 1)
            layout.addWidget(okButton, 1, 1)

        okButton.clicked.connect(self.hide)


if __name__ == "__main__":
    app = QApplication([])
    dialog = Dialog(state=3)
    dialog.show()
    app.exec_()
