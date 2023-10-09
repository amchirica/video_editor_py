import functools
import sys
from PyQt5.QtGui import QPalette, QColor, QPixmap, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QToolBar, QAction, QStatusBar, QCheckBox, QComboBox, \
    QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QStackedLayout, QPushButton, QTabWidget, QDialog, \
    QDialogButtonBox, QMessageBox, QFileDialog, QTextEdit, QFrame, QStyle, QSizePolicy, QSlider, \
    QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt, QSize, QDir, QRect
from PyQt5.QtMultimediaWidgets import QVideoWidget
from moviepy.editor import VideoFileClip
from Photo import AddPhotoWindow
from AddText import AddTextWindow
from Concatenate import ConcatenateWindow
from Crop import CropWindow
from Importaudio import AudioWindow
from Rotate import RotateWindow
from Size import SizeWindow
from Speed import SpeedWindow
from Subwindow import SUBWindow
from VideoCut import *
from Brightness import BrightnessWindow
from Contrast import ContrastWindow
import TimeLine
from FadeInOut import FadeWindow
from TimeLine import QTimeLine
from VideoSelf import VideoWindow


class MainWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)
        main_layout = QVBoxLayout()
        self.file_name = ""
        layout = QHBoxLayout()
        layout1 = QVBoxLayout()
        self.menuLayout = QGridLayout()
        for i in range(10):
            for j in range(10):
                self.menuLayout.addWidget(QLabel(), i, j)
        self.i = 0
        self.j = 0
        self.videoSamples = []
        self.icons = []

        layout3 = QVBoxLayout()
        self.VideoPlay = VideoWindow()
        layout3.addWidget(self.VideoPlay)

        self.imp = QPushButton('Import Video')
        self.imp.clicked.connect(self.import_vid)
        layout1.addWidget(self.imp)

        self.add_photo = QPushButton('Add Photo')
        self.add_photo.clicked.connect(lambda: AddPhotoWindow(self.VideoPlay, 200, 100).show())
        layout1.addWidget(self.add_photo)

        self.cut = QPushButton('Cut')
        self.cut.clicked.connect(lambda: self.VideoPlay.record_subclip_video())
        layout1.addWidget(self.cut)

        self.remove = QPushButton('Remove Video Piece')
        self.remove.clicked.connect(lambda: self.VideoPlay.remove_piece_video())
        layout1.addWidget(self.remove)

        self.rotate = QPushButton('Rotate')
        self.rotate.clicked.connect(lambda: self.show_sub_window(RotateWindow(self.VideoPlay, 200, 100)))
        layout1.addWidget(self.rotate)

        self.subvid = QPushButton('Add Subvideo')
        self.subvid.clicked.connect(lambda: self.show_sub_window(SUBWindow(self.VideoPlay, 200, 100)))
        layout1.addWidget(self.subvid)

        self.concatenate = QPushButton('Concatenate')
        self.concatenate.clicked.connect(lambda: self.show_sub_window(ConcatenateWindow(self.VideoPlay, 200, 100,
                                                                                        self.videoSamples)))
        layout1.addWidget(self.concatenate)

        self.fade = QPushButton('Fade in/Fade out')
        self.fade.clicked.connect(lambda: self.show_sub_window(FadeWindow(self.VideoPlay, 200, 100)))
        layout1.addWidget(self.fade)

        self.changesize = QPushButton('Size')
        self.changesize.clicked.connect(lambda: self.show_sub_window(SizeWindow(self.VideoPlay, 200, 100)))
        layout1.addWidget(self.changesize)

        self.speed = QPushButton('Speed')
        self.speed.clicked.connect(lambda: self.show_sub_window(SpeedWindow(self.VideoPlay, 200, 100)))
        layout1.addWidget(self.speed)

        self.add_text = QPushButton('Text')
        self.add_text.clicked.connect(lambda: self.show_sub_window(AddTextWindow(self.VideoPlay, 200, 100)))
        layout1.addWidget(self.add_text)

        self.audi = QPushButton('Extract Audio')
        self.audi.clicked.connect(lambda: self.VideoPlay.record_subclip_audio())
        layout1.addWidget(self.audi)

        self.silentvid = QPushButton('Extract Video Without Audio')
        self.silentvid.clicked.connect(lambda: self.VideoPlay.remove_audio())
        layout1.addWidget(self.silentvid)

        self.audadd = QPushButton('Concatenate with Audio')
        self.audadd.clicked.connect(lambda: self.show_sub_window(AudioWindow(self.VideoPlay, 200, 100)))
        layout1.addWidget(self.audadd)

        self.crop = QPushButton('Crop Video')
        self.crop.clicked.connect(lambda: self.show_sub_window(CropWindow(self.VideoPlay, 200, 100)))
        layout1.addWidget(self.crop)

        self.brightness = QPushButton('Brightness')
        self.brightness.clicked.connect(lambda: self.show_sub_window(BrightnessWindow(self.VideoPlay)))
        layout1.addWidget(self.brightness)


        self.contrast = QPushButton('Contrast')
        self.contrast.clicked.connect(lambda: self.show_sub_window(ContrastWindow(self.VideoPlay, 200, 100)))
        layout1.addWidget(self.contrast)

        layout1.addStretch()

        layout.addLayout(layout1, 2)

        layout.addLayout(self.menuLayout, 6)
        layout.addLayout(layout3, 10)
        main_layout.addLayout(layout, 2)
        lay = QVBoxLayout()
        self.time_l = TimeLine.QTimeLine(300, 10)
        lay.addWidget(self.time_l)

        main_layout.addLayout(lay, 1)
        self.setLayout(main_layout)

    def import_vid(self, file_name=None):
        if not file_name:
            file_name, _ = QFileDialog.getOpenFileName(self, 'Open Video', '', 'Video files (*.mp4 *.MP4 *.avi *.mov)')
        if file_name != '':
            clip = VideoFileClip(file_name)
            dot_index = file_name.rfind('.')
            cut_frame_name = file_name[: dot_index] + '_{}.png'.format(1)
            clip.save_frame(cut_frame_name, 10)
            icon = QLabel()

            icon.mouseDoubleClickEvent = functools.partial(self.playSelectedItem, filename=file_name)
            icon.mouseReleaseEvent = functools.partial(self.add_to_concatenate, filename=file_name, label=icon)
            w = icon.width()
            h = icon.height()
            pixmap = QPixmap(cut_frame_name)
            icon.setPixmap(pixmap.scaled(int(w / 10), int(h / 10)))
            self.menuLayout.addWidget(icon, self.j, self.i)
            if self.i == 9:
                self.i = 0
                self.j += 1
            else:
                self.i += 1
            if self.i == 9 and self.j == 9:
                self.i = 0
                self.j = 0

            self.clipchik = TimeLine.VideoSample(clip.duration)
            self.time_l.videoSamples.append(self.clipchik)

    def playSelectedItem(self, event, filename):
        self.VideoPlay.openFile(filename)
        self.VideoPlay.video_name = filename
        self.VideoPlay.record_start_time = 0
        if filename != '':
            clip = VideoFileClip(filename)
            self.VideoPlay.record_end_time = clip.duration
            self.VideoPlay.video_duration = clip.duration
            self.VideoPlay.indices_list = [(0, clip.duration)]
        for v in self.icons:
            v.setStyleSheet("border: 0px solid blue;")
        self.videoSamples.clear()
        self.icons.clear()

    def add_to_concatenate(self, event, filename, label):
        self.videoSamples.append(filename)
        self.icons.append(label)
        label.setStyleSheet("border: 3px solid blue;")

    def show_sub_window(self, window):
        window.show()


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("VideoPy")

        # Add a favicon
        favicon_path = "favicon.ico"
        self.setWindowIcon(QIcon(favicon_path))
        
        w = 700

        h = 500

        self.resize(w, h)

        main_widget = MainWidget()

        self.setCentralWidget(main_widget)


app = QApplication(sys.argv)

window = MainWindow()
window.showMaximized()

app.exec_()
