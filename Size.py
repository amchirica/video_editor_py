from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, \
    QComboBox, QFileDialog, QLineEdit, QSlider
import sys
from random import randint
from moviepy.video.io.VideoFileClip import VideoFileClip
from VideoSelf import VideoWindow
from PyQt5.QtCore import Qt


class SizeWindow(QWidget):
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

        self.slider = QSlider(
            orientation=Qt.Horizontal,
            minimum=0,
            maximum=10,
            singleStep=1,
            pageStep=1
        )
        self.slider.setValue(5)

        self.slider1 = QSlider(
            orientation=Qt.Horizontal,
            minimum=0,
            maximum=10,
            singleStep=1,
            pageStep=1
        )
        self.slider1.setValue(5)

        label_value = QLabel(alignment=Qt.AlignCenter)
        self.slider.valueChanged.connect(lambda: label_value.setNum(self.slider.value() / 5))
        label_value.setNum(self.slider.value() / 5)

        label_value1 = QLabel(alignment=Qt.AlignCenter)
        self.slider1.valueChanged.connect(lambda: label_value1.setNum(self.slider1.value() / 5))
        label_value1.setNum(self.slider1.value() / 5)


        self.ok = QPushButton("Set New Size")

        self.layout.addWidget(QLabel('height'))
        self.layout.addWidget(self.slider1)
        self.layout.addWidget(label_value1)
        self.layout.addWidget(QLabel('width'))
        self.layout.addWidget(self.slider)
        self.layout.addWidget(label_value)
        self.layout.addWidget(self.ok)
        self.ok.clicked.connect(lambda: self.window.change_size_video(self, self.slider.value(), self.slider1.value()))

        self.setLayout(self.layout)