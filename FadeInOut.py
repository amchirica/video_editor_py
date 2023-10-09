from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QComboBox
import sys
from random import randint
from VideoSelf import VideoWindow

class FadeWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, window, w, h):
        super().__init__()
        self.window = window
        self.resize(w, h)
        self.setBaseSize(w, h)

        self.layout = QHBoxLayout()
        self.fade_in = QPushButton('Fade In')
        self.fade_out = QPushButton('Fade Out')
        self.combobox_duration = QComboBox()
        duration = ['1', '3', '5', '7']
        self.combobox_duration.addItems(duration)

        self.layout.addWidget(self.fade_in)
        self.layout.addWidget(self.fade_out)
        self.layout.addWidget(self.combobox_duration)
        self.fade_in.clicked.connect(lambda: self.window.fade_in_video(self, self.combobox_duration.currentText()))
        self.fade_out.clicked.connect(lambda: self.window.fade_out_video(self, self.combobox_duration.currentText()))

        self.setLayout(self.layout)
