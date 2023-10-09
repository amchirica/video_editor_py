from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, \
    QComboBox, QLineEdit

import sys

from random import randint
from VideoSelf import VideoWindow


class AddTextWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, window, w, h):
        super().__init__()
        self.window = window
        self.resize(w, h)
        self.setBaseSize(w, h)

        self.layout = QVBoxLayout()
        self.final = QPushButton('Add Text')
        self.text = QLineEdit()
        self.text.setPlaceholderText("Enter Text")
        self.font_size = QLineEdit()
        self.font_size.setPlaceholderText("Enter Font Size")
        self.text_color = QComboBox()
        colors = ['black', 'white', 'red', 'blue']
        self.text_color.addItems(colors)
        self.poslayout = QHBoxLayout()


        self.x = QLineEdit()
        self.x.setPlaceholderText("x")
        self.y = QLineEdit()
        self.y.setPlaceholderText("y")

        self.note = QLabel("Pos:")
        self.align = QComboBox()
        places = ['center', 'East', 'West', 'South', 'North']
        self.align.addItems(places)
        self.poslayout.addWidget(self.note)
        self.poslayout.addWidget(self.align)
        self.poslayout.addWidget(self.x)
        self.poslayout.addWidget(self.y)

        self.layout.addWidget(self.text)
        self.layout.addWidget(self.font_size)
        self.layout.addWidget(self.text_color)
        self.layout.addLayout(self.poslayout)
        self.layout.addWidget(self.final)
        self.final.clicked.connect(lambda: self.window.add_text_video(self, self.text.text(), self.font_size.text(),
                                                                      self.text_color.currentText(), 
                                                                      self.align.currentText()
                                                                      ))

        self.setLayout(self.layout)