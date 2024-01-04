from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtGui import QIcon, QPainter, QColor
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QAction, QComboBox, QFileDialog, QHBoxLayout,
                             QLabel, QMainWindow, QPushButton, QShortcut,
                             QSlider, QStyle, QVBoxLayout, QWidget, QSizePolicy, QApplication)
from PyQt5.QtMultimedia import QMediaContent
from moviepy.video.io.VideoFileClip import VideoFileClip
import sys
from moviepy.video.io.VideoFileClip import VideoFileClip
from Thread import Thread

class Labelik(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._slider = None
        self._values = []

    def setSlider(self, slider):
        self._slider = slider
        self.update()

    def set_values(self, values):
        self._values = values
        self.update()

    def paintEvent(self, event):
        if self._slider is None:
            return
        painter = QPainter(self)
        X1 = self.get_pos_by_value(self._slider.minimum())
        X2 = self.get_pos_by_value(self._slider.maximum())
        R = QtCore.QRect(QtCore.QPoint(X1, 0), QtCore.QPoint(X2, self.height()))
        painter.fillRect(R, QColor("#000000"))
        for start, end in self._values:
            x1 = int(self.get_pos_by_value(start))
            x2 = self.get_pos_by_value(end)
            r = QtCore.QRect(QtCore.QPoint(x1, 0), QtCore.QPoint(x2, self.height()))
            painter.fillRect(r, QColor("#2600ff"))

    def get_pos_by_value(self, value):
        opt = QtWidgets.QStyleOptionSlider()
        self._slider.initStyleOption(opt)
        opt.sliderPosition = int(value)
        r = self._slider.style().subControlRect(
            QtWidgets.QStyle.CC_Slider,
            opt,
            QtWidgets.QStyle.SC_SliderHandle,
            self._slider
        )
        return r.center().x()


class VideoWindow(QWidget):

    def __init__(self):
        super().__init__()


        self.video_player = QMediaPlayer()
        self.video_slider = QSlider(self)
        self.label = Labelik(self.video_slider)


        videoWidget = QVideoWidget()

        self.record_start_time = None
        self.record_end_time = None
        self.video_name = ""

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        #self.video_slider = QSlider(Qt.Horizontal)
        #self.video_slider.setRange(0, 0)
        #self.video_slider.sliderMoved.connect(self.setPosition)
        #self.video_slider.setStyleSheet()
        self.video_duration = 0


        self.labellay = QHBoxLayout()
        self.note = QLabel("Layer")
        self.labellay.addWidget(self.note, 0)
        self.indices_list = [(0, self.video_duration)]
        self.label = Labelik(self.video_slider)
        self.video_slider = QtWidgets.QSlider(
            orientation=QtCore.Qt.Horizontal,
            minimum=0,
            maximum=0,
            singleStep=1,
            pageStep=1
        )
        self.video_slider.sliderMoved.connect(self.setPosition)
        self.label.setSlider(self.video_slider)
        self.label.set_values(self.indices_list)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.video_slider)

        self.layout_record = QHBoxLayout()
        self.layout_record.setContentsMargins(0, 0, 0, 0)
        self.button_start = QPushButton('From')
        self.button_start.setStyleSheet("QPushButton"
                                      "{"
                                      "background-color : lightgray;"
                                      "}"
                                      )
        self.button_end = QPushButton('To')
        self.button_end.setStyleSheet("QPushButton"
                                      "{"
                                      "background-color : lightgray;"
                                      "}"
                                      )
        self.layout_record.addWidget(self.button_start)
        self.layout_record.addWidget(self.button_end)

        self.button_start.clicked.connect(self.record_start)
        self.button_end.clicked.connect(self.record_end)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget, 8)
        layout.addLayout(self.layout_record, 1)
        self.labellay.addWidget(self.label, 13)
        layout.addLayout(self.labellay, 1)
        layout.addLayout(controlLayout, 1)
        layout.addWidget(self.errorLabel,1)

        # Set widget to contain window contents
        self.setLayout(layout)

        self.video_player.setVideoOutput(videoWidget)
        self.video_player.stateChanged.connect(self.mediaStateChanged)
        self.video_player.positionChanged.connect(self.positionChanged)
        self.video_player.durationChanged.connect(self.durationChanged)
        self.video_player.error.connect(self.handleError)

        QShortcut(Qt.Key_Up, self, self.arrow_up)
        QShortcut(Qt.Key_Down, self, self.arrow_down)
        QShortcut(Qt.Key_Left, self, self.arrow_left_event)
        QShortcut(Qt.Key_Right, self, self.arrow_right_event)
        QShortcut(Qt.Key_Space, self, self.play)

    def arrow_up(self):
        if self.video_player.state() != QMediaPlayer.StoppedState:
            self.video_player.setVolume(min(self.video_player.volume() + 10, 100))

    def arrow_down(self):
        if self.video_player.state() != QMediaPlayer.StoppedState:
            self.video_player.setVolume(max(self.video_player.volume() - 10, 0))

    def arrow_left_event(self):
        self.set_position(self.video_slider.value() - 10 * 1000)

    def arrow_right_event(self):
        self.set_position(self.video_slider.value() + 10 * 1000)

    def openFile(self, fileName):
        if fileName != '':
            self.video_player.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.video_player.state() == QMediaPlayer.PlayingState:
            self.video_player.pause()
        else:
            self.video_player.play()

    def mediaStateChanged(self, state):
        if self.video_player.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.video_slider.setValue(position)

    def durationChanged(self, duration):
        self.video_slider.setRange(0, duration)
        self.video_duration = duration
        self.record_start_time = 0
        self.record_end_time = 0
        self.indices_list = [(0, self.video_duration)]

    def setPosition(self, position):
        self.video_player.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error for play " + self.video_player.errorString())

    def record_start(self):
        end_pos = self.indices_list[0][1]
        if self.record_start_time != 0:
            self.record_start_time = 0
            self.button_start.setStyleSheet("QPushButton"
                                          "{"
                                          "background-color : lightgray;"
                                          "}"
                                          )
            self.indices_list.clear()
            self.indices_list.append((0, end_pos))
            self.label.set_values(self.indices_list)

        else:
            self.record_start_time = self.video_slider.sliderPosition()

            if self.record_end_time is not None and self.record_end_time != 0 and self.record_start_time > self.record_end_time:
                self.record_start_time, self.record_end_time = self.record_end_time, self.record_start_time

            self.button_start.setStyleSheet("QPushButton"
                                            "{"
                                            "background-color : lightblue;"
                                            "}"
                                            )

            pos = self.video_slider.sliderPosition()
            self.indices_list.clear()
            self.indices_list.append((pos, end_pos))
            self.label.set_values(self.indices_list)

        self._show_record_time()

    def record_end(self):
        st_pos = self.indices_list[0][0]
        if self.record_end_time != 0:
            self.record_end_time = 0
            self.button_end.setStyleSheet("QPushButton"
                                          "{"
                                          "background-color : lightgray;"
                                          "}"
                                          )
            self.indices_list.clear()
            self.indices_list.append((st_pos, self.video_duration))
            self.label.set_values(self.indices_list)

        else:
            self.record_end_time = self.video_slider.sliderPosition()

            if self.record_start_time is not None and self.record_start_time > self.record_end_time:
                self.record_start_time, self.record_end_time = self.record_end_time, self.record_start_time

            self.button_end.setStyleSheet("QPushButton"
                                          "{"
                                          "background-color : lightblue;"
                                          "}"
                                          )
            pos = self.video_slider.sliderPosition()
            self.indices_list.clear()
            self.indices_list.append((st_pos, pos))
            self.label.set_values(self.indices_list)

        self._show_record_time()

    def _show_record_time(self):
        if self.record_start_time is not None and self.record_end_time is not None:
            cut = 0

    def _check_duration(self):
        if self.video_name == "":
            print(2)
            return False
        elif self.record_start_time == self.record_end_time:
            print(4)
            return False
        elif self.record_start_time > self.record_end_time:
            print(3)
            return False
        else:
            return True

        return False

    def record_subclip_video(self):
        if self._check_duration():
            self.thread = Thread()
            self.thread.set_params(Thread.MSG_CUT_VIDEO, self.video_name,
                                   self.record_start_time / 1000, self.record_end_time / 1000)
            self.thread.signal_return_value.connect(self.thread_done)
            self.thread.start()
            self.thread.wait()


    def record_rotate_video(self, wind, degree):
        if self._check_duration():
            self.thread = Thread()
            self.thread.set_params(Thread.MSG_ROTATE_VIDEO, self.video_name,
                                   self.record_start_time / 1000, self.record_end_time / 1000,
                                   degree)
            self.thread.signal_return_value.connect(self.thread_done)
            self.thread.start()
            self.thread.wait()
            wind.destroy()
            #return self.video_name

    def record_subclip_audio(self):
        if self._check_duration():
            self.thread = Thread()
            self.thread.set_params(Thread.MSG_EXTRACT_AUDIO, self.video_name,
                                   self.record_start_time / 1000, self.record_end_time / 1000)
            self.thread.signal_return_value.connect(self.thread_done)
            self.thread.start()
            self.thread.wait()

    def fade_in_video(self, wind, duration):
        self.thread = Thread()
        self.thread.set_params(Thread.MSG_FADE_IN_VIDEO, self.video_name,
                               self.record_start_time / 1000, self.record_end_time / 1000,
                               0, duration)
        self.thread.signal_return_value.connect(self.thread_done)
        self.thread.start()
        self.thread.wait()
        wind.destroy()

    def fade_out_video(self, wind, duration):
        self.thread = Thread()
        self.thread.set_params(Thread.MSG_FADE_OUT_VIDEO, self.video_name,
                                   self.record_start_time / 1000, self.record_end_time / 1000,
                                   0, duration)
        self.thread.signal_return_value.connect(self.thread_done)
        self.thread.start()
        self.thread.wait()
        wind.destroy()

    def add_text_video(self, wind, text, fontsize, color, align):
        if self._check_duration():
            try:
                fontsize1 = int(fontsize)
            except ValueError:
                print("Invalid font size. Please enter a valid numerical value.")
                return

            print(f"Adding text: {text}, Font size: {fontsize1}, Color: {color}, Alignment: {align}")

            self.thread = Thread()
            self.thread.set_params(Thread.MSG_ADD_TEXT_VIDEO, self.video_name,
                                self.record_start_time / 1000, self.record_end_time / 1000,
                                0, 0, text, fontsize1, color, align)
            self.thread.signal_return_value.connect(self.thread_done)
            self.thread.start()
            self.thread.wait()
            wind.destroy()


    def concatenate_video(self, wind, videoSamples, slide_out):
        self.thread = Thread()
        #clip = VideoFileClip(self.video_name)
        self.thread.set_params(Thread.MSG_CONCATENATE_VIDEO, self.video_name,
                                   0, 1000,
                                   videoSamples=videoSamples, slide_out=slide_out)
        self.thread.signal_return_value.connect(self.thread_done)
        self.thread.start()
        self.thread.wait()
        wind.destroy()

    def remove_piece_video(self):
        if self._check_duration():
            self.thread = Thread()
            self.thread.set_params(Thread.MSG_REMOVE_PIECE_VIDEO, self.video_name,
                                   self.record_start_time / 1000, self.record_end_time / 1000)
            self.thread.signal_return_value.connect(self.thread_done)
            self.thread.start()
            self.thread.wait()

    def add_photo_video(self, wind, photo_name):
        if self._check_duration():
            self.thread = Thread()
            self.thread.set_params(Thread.MSG_ADD_PHOTO_VIDEO, self.video_name,
                                   self.record_start_time / 1000, self.record_end_time / 1000, photo_name=photo_name)
            self.thread.signal_return_value.connect(self.thread_done)
            self.thread.start()
            self.thread.wait()
            wind.destroy()

    def change_speed_video(self, wind, speed):
        self.thread = Thread()
        speed1 = float(speed)
        self.thread.set_params(Thread.MSG_CHANGE_SPEED_VIDEO, self.video_name,
                                   self.record_start_time / 1000, self.record_end_time / 1000, speed=speed1)
        self.thread.signal_return_value.connect(self.thread_done)
        self.thread.start()
        self.thread.wait()
        wind.destroy()

    def change_size_video(self, wind, ratioy, ratiox):
        self.thread = Thread()
        self.thread.set_params(Thread.MSG_RATIO_VIDEO, self.video_name,
                                   self.record_start_time / 1000, self.record_end_time / 1000, ratioy=ratioy, ratiox=ratiox)
        self.thread.signal_return_value.connect(self.thread_done)
        self.thread.start()
        self.thread.wait()
        wind.destroy()

    def remove_audio(self):
        self.thread = Thread()
        self.thread.set_params(Thread.MSG_REMOVE_AUDIO_VIDEO, self.video_name,
                               self.record_start_time / 1000, self.record_end_time / 1000)
        self.thread.signal_return_value.connect(self.thread_done)
        self.thread.start()
        self.thread.wait()

    def concatenate_audio(self, wind, audio_name):
        self.thread = Thread()
        self.thread.set_params(Thread.MSG_CONCATENATE_AUDIO_VIDEO, self.video_name,
                               self.record_start_time / 1000, self.record_end_time / 1000, audio_name=audio_name)
        self.thread.signal_return_value.connect(self.thread_done)
        self.thread.start()
        self.thread.wait()
        wind.destroy()

    def subclip_video(self, wind, video_name1):
        self.thread = Thread()
        self.thread.set_params(Thread.MSG_ADD_VIDEO_VIDEO, self.video_name,
                               self.record_start_time / 1000, self.record_end_time / 1000, video_name2=video_name1)
        self.thread.signal_return_value.connect(self.thread_done)
        self.thread.start()
        self.thread.wait()
        wind.destroy()

    def crop_video(self, wind, w, h):
        self.thread = Thread()
        wid = float(w)
        hei = float(h)
        self.thread.set_params(Thread.MSG_CROP_VIDEO, self.video_name,
                               self.record_start_time / 1000, self.record_end_time / 1000, subheight=hei, subwidth=wid)
        self.thread.signal_return_value.connect(self.thread_done)
        self.thread.start()
        self.thread.wait()
        wind.destroy()

    def change_brightness_video(self, w, h):
        if self.record_start_time is None or self.record_end_time is None:
            # Verificăm dacă valorile sunt None și gestionăm cazul corespunzător
            print("Eroare: Timpul de început sau timpul de încheiere nu au fost setate.")
            return

        self.thread = Thread()
        wid = float(w)
        hei = float(h)
        start_time = float(self.record_start_time) / 1000
        end_time = float(self.record_end_time) / 1000
        self.thread.set_params(Thread.MSG_BRIGHTNESS_VIDEO, self.video_name, start_time, end_time, subheight=hei, subwidth=wid)
        self.thread.signal_return_value.connect(self.thread_done)
        self.thread.start()
        self.thread.wait()
        self.destroy()


    def thread_done(self, return_value, video_name):
        if return_value:
            self.openFile(video_name)
            self.video_name = video_name
            return True
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    videoWindow = VideoWindow()
    videoWindow.show()
    sys.exit(app.exec_())
