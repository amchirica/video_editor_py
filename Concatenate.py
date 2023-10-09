from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, \
    QComboBox, QFileDialog, QRadioButton
import sys
from random import randint
from moviepy.video.io.VideoFileClip import VideoFileClip
from VideoSelf import VideoWindow


class ConcatenateWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, window, w, h, videoSamples):
        super().__init__()
        self.window = window
        self.resize(w, h)
        self.setBaseSize(w, h)
        print(len(videoSamples))
        if len(videoSamples) < 2:
            self.layout = QVBoxLayout()
            self.note = QLabel("Choose at least two video")
            self.done = QPushButton("Close")
            self.layout.addWidget(self.note)
            self.layout.addWidget(self.done)
            self.done.clicked.connect(self.destroy_it)
            self.setLayout(self.layout)

        else:
            self.layout = QVBoxLayout()
            self.slide_out = QRadioButton()
            self.slidelayout = QHBoxLayout()
            self.note = QLabel("Is concatenation slided:")
            self.slidelayout.addWidget(self.note)
            self.slidelayout.addWidget(self.slide_out)
            self.done = QPushButton("Concatenate")

            self.layout.addLayout(self.slidelayout)
            self.layout.addWidget(self.done)
            self.done.clicked.connect(lambda: self.window.concatenate_video(self, videoSamples,
                                                                            True if self.slide_out.isChecked()
                                                                            else False))
            self.setLayout(self.layout)

    def destroy_it(self):
        self.destroy()
