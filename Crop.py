from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, \
    QComboBox, QFileDialog, QLineEdit
import sys
from random import randint
from moviepy.video.io.VideoFileClip import VideoFileClip
from VideoSelf import VideoWindow


class CropWindow(QWidget):
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

        self.layout = QVBoxLayout()
        self.changesizey = QLineEdit()
        self.changesizey.setPlaceholderText("height")
        self.changesizex = QLineEdit()
        self.changesizey.setPlaceholderText("width")
        self.ok = QPushButton("Set New Size")
        self.layoutyx = QHBoxLayout()
        self.layoutyx.addWidget(self.changesizex)
        self.layoutyx.addWidget(self.changesizey)

        self.layout.addLayout(self.layoutyx)
        self.layout.addWidget(self.ok)
        self.ok.clicked.connect(lambda: self.window.crop_video(self, self.changesizex.text(),
                                                                      self.changesizey.text()))

        self.setLayout(self.layout)