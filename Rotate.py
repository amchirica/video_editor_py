from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, \
    QComboBox, QFileDialog, QLineEdit
import sys
from random import randint
from moviepy.video.io.VideoFileClip import VideoFileClip
from VideoSelf import VideoWindow


class RotateWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, window, w, h):
        super().__init__()
        self.file_name = ""
        self.window = window
        self.resize(w, h)
        self.setBaseSize(w, h)

        self.mini_menu = QHBoxLayout()
        self.label_rotate = QLabel('Degree of rotation (counterclockwise)')
        self.combobox_degree = QComboBox()
        degrees = ['0', '90', '180', '270']
        self.combobox_degree.addItems(degrees)
        self.mini_menu.addWidget(self.label_rotate)
        self.mini_menu.addWidget(self.combobox_degree)

        self.ok = QPushButton("Rotate")

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.mini_menu)
        self.layout.addWidget(self.ok)
        self.ok.clicked.connect(lambda: self.window.record_rotate_video(self, self.combobox_degree.currentText()))

        self.setLayout(self.layout)