import functools
import sys
from PyQt5.QtGui import QPalette, QColor, QPixmap, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QToolBar, QAction, QStatusBar, QCheckBox, QComboBox, \
    QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QStackedLayout, QPushButton, QTabWidget, QDialog, \
    QDialogButtonBox, QMessageBox, QFileDialog, QTextEdit, QFrame, QStyle, QSizePolicy, QSlider, \
    QListWidget, QListWidgetItem, QToolButton, QSizePolicy
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
import TimeLine
from FadeInOut import FadeWindow
from TimeLine import QTimeLine
from VideoSelf import VideoWindow
from ExportTerminal import ExportTerminal



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

        # Adaugă o etichetă pentru informații despre videoclip
        self.video_info_label = QLabel("Video: None\nDuration: 0 seconds\nResolution: N/A\nCodec: N/A")
        layout1.addWidget(self.video_info_label)


        layout3 = QVBoxLayout()
        self.VideoPlay = VideoWindow()
        layout3.addWidget(self.VideoPlay)

        self.imp = QPushButton('Import Video')
        self.imp.clicked.connect(self.import_vid)
        layout1.addWidget(self.imp)

        self.add_photo = QPushButton('Add Photo')
        self.add_photo.clicked.connect(lambda: AddPhotoWindow(self.VideoPlay, 200, 100).show())
        layout1.addWidget(self.add_photo)

        self.cut = QPushButton('Cut Fragment')
        self.cut.clicked.connect(lambda: self.VideoPlay.record_subclip_video())
        layout1.addWidget(self.cut)

        self.remove = QPushButton('Remove Fragment')
        self.remove.clicked.connect(lambda: self.VideoPlay.remove_piece_video())
        layout1.addWidget(self.remove)

        self.rotate = QPushButton('Rotate')
        self.rotate.clicked.connect(lambda: self.show_sub_window(RotateWindow(self.VideoPlay, 200, 100)))
        layout1.addWidget(self.rotate)

        self.subvid = QPushButton('Add Subvideo')
        self.subvid.clicked.connect(lambda: self.show_sub_window(SUBWindow(self.VideoPlay, 200, 100)))
        layout1.addWidget(self.subvid)

        self.concatenate = QPushButton('Concatenate')
        self.concatenate.clicked.connect(lambda: self.show_sub_window(ConcatenateWindow(self.VideoPlay, 200, 100, self.videoSamples)))
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

        self.audadd = QPushButton('Import/Rewrite Audio')
        self.audadd.clicked.connect(lambda: self.show_sub_window(AudioWindow(self.VideoPlay, 200, 100)))
        layout1.addWidget(self.audadd)

        self.crop = QPushButton('Optimize Resolution')
        self.crop.clicked.connect(lambda: self.show_sub_window(CropWindow(self.VideoPlay, 200, 100)))
        layout1.addWidget(self.crop)

        self.brightness = QPushButton('Brightness and Contrast')
        self.brightness.clicked.connect(lambda: self.show_sub_window(BrightnessWindow(self.VideoPlay, 200, 100)))
        layout1.addWidget(self.brightness)

        self.audi = QPushButton('Export Audio Wihtout Video')
        self.audi.clicked.connect(lambda: self.VideoPlay.record_subclip_audio())
        layout1.addWidget(self.audi)

        self.silentvid = QPushButton('Export Video Without Audio')
        self.silentvid.clicked.connect(lambda: self.VideoPlay.remove_audio())
        layout1.addWidget(self.silentvid)
        
        self.export_terminal = ExportTerminal(self)
        layout.addWidget(self.export_terminal)



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
            file_name, _ = QFileDialog.getOpenFileName(self, 'Open Video', '', 'Video files (*.mp4 *.MP4 *.avi *.mov *.mp3)')
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

            # Afișează informații despre videoclip în eticheta video_info_label
            video_info = (
                f"Video: {file_name}\n"
                f"Duration: {clip.duration} seconds\n"
                f"Resolution: {clip.size}\n"
                f"Codec: {clip.fps}\n"
            )
            self.video_info_label.setText(video_info)


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
            if v in self.icons:
                v.setStyleSheet("border: 0px solid blue;")
        self.videoSamples.clear()
        self.icons.clear()

    def add_to_concatenate(self, event, filename, label):
        self.videoSamples.append(filename)
        self.icons.append(label)
        label.setStyleSheet("border: 3px solid blue;")
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.delete_last_clip()

    def delete_last_clip(self):
        if self.videoSamples:
            # Ia ultimul element din lista și șterge-l
            last_clip = self.videoSamples.pop()
            last_icon = self.icons.pop()

            # Șterge QLabel din layout
            layout = self.layout()
            layout.removeWidget(last_icon)
            last_icon.deleteLater()

    def show_sub_window(self, window):
        window.show()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("VideoPy")

        # Adauga favicon
        favicon_path = "favicon.ico"
        self.setWindowIcon(QIcon(favicon_path))
        
        
        w = 700
        h = 500

        self.resize(w, h)

        main_widget = MainWidget()

        #Crează un buton de imp si seteaza stilul
        self.imp = QPushButton('Import Video')
        self.imp.setStyleSheet("QPushButton { width: 100px; height: 50px; background-color: red; color: white; }")
        self.imp.clicked.connect(main_widget.import_vid)
        main_widget.layout().addWidget(self.imp)

        self.setCentralWidget(main_widget)


app = QApplication(sys.argv)

window = MainWindow()
window.showMaximized()

app.exec_()