import tempfile
from base64 import b64encode
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint, QLine, QRect, QRectF, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPalette, QPen, QPolygon, QPainterPath, QPixmap
from PyQt5.QtWidgets import QWidget, QFrame, QScrollArea, QVBoxLayout
import sys
import os
from PyQt5.QtCore import pyqtSignal
from numpy import load
import subprocess
from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QApplication, QPushButton
from PyQt5.QtWidgets import QFileDialog


__textColor__ = QColor(187, 100, 70)
__backgroudColor__ = QColor(60, 63, 65)
__font__ = QFont('Decorative', 10)


class VideoSample:

    def __init__(self, duration, color=Qt.darkYellow, picture=None, audio=None):
        self.duration = duration
        self.color = color  # Floating color
        self.defColor = color  # DefaultColor
        if picture is not None:
            self.picture = picture.scaledToHeight(45)
        else:
            self.picture = None
        self.startPos = 0  # Inicial position
        self.endPos = self.duration  # End position


class QTimeLine(QWidget):
    timeUpdated = pyqtSignal(float)
    positionChanged = pyqtSignal(int)
    selectionChanged = pyqtSignal(VideoSample)

    def __init__(self, duration, length):
        super(QWidget, self).__init__()
        self.duration = duration
        self.length = length

        # Setarea variabilelor
        self.backgroundColor = __backgroudColor__
        self.textColor = __textColor__
        self.font = __font__
        self.pos = None
        self.pointerPos = None
        self.pointerTimePos = None
        self.selectedSample = None
        self.clicking = False  # Check if mouse left button is being pressed
        self.is_in = False  # check if user is in the widget
        self.videoSamples = []  # List of videos samples

        self.setMouseTracking(True)  # Mouse events
        self.setAutoFillBackground(True)  # background

        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, self.length, 200)
        self.setWindowTitle("TESTE")

        # Setăm fundalul
        pal = QPalette()
        pal.setColor(QPalette.Background, self.backgroundColor)
        self.setPalette(pal)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(self.textColor)
        qp.setFont(self.font)
        qp.setRenderHint(QPainter.Antialiasing)
        w = 0
        # Draw time
        scale = self.getScale()
        while w <= self.width():
            qp.drawText(w - 50, 0, 100, 100, Qt.AlignHCenter, self.get_time_string(w * scale))
            w += 100
        # Draw down line
        qp.setPen(QPen(Qt.darkCyan, 5, Qt.SolidLine))
        qp.drawLine(0, 40, self.width(), 40)

        # Draw dash lines
        point = 0
        qp.setPen(QPen(self.textColor))
        qp.drawLine(0, 40, self.width(), 40)
        while point <= self.width():
            if point % 30 != 0:
                qp.drawLine(3 * point, 40, 3 * point, 30)
            else:
                qp.drawLine(3 * point, 40, 3 * point, 20)
            point += 10

        if self.pos is not None and self.is_in:
            qp.drawLine(self.pos.x(), 0, self.pos.x(), 40)

        if self.pointerPos is not None:
            line = QLine(QPoint(int(self.pointerTimePos/self.getScale()), 40),
                         QPoint(int(self.pointerTimePos/self.getScale()), self.height()))
            poly = QPolygon([QPoint(int(self.pointerTimePos/self.getScale()) - 10, 20),
                             QPoint(int(self.pointerTimePos/self.getScale()) + 10, 20),
                             QPoint(int(self.pointerTimePos/self.getScale()), 40)])
        else:
            line = QLine(QPoint(0, 0), QPoint(0, self.height()))
            poly = QPolygon([QPoint(-10, 20), QPoint(10, 20), QPoint(0, 40)])

        # Draw samples
        t = 0
        for sample in self.videoSamples:
            # Clear clip path
            path = QPainterPath()
            path.addRoundedRect(QRectF(t / scale, 50, sample.duration / scale, 200), 10, 10)
            qp.setClipPath(path)

            # Draw sample
            path = QPainterPath()
            qp.setPen(sample.color)
            path.addRoundedRect(QRectF(t/scale, 50, sample.duration/scale, 50), 10, 10)
            sample.startPos = t/scale
            sample.endPos = t/scale + sample.duration/scale
            qp.fillPath(path, sample.color)
            qp.drawPath(path)

            # Draw preview pictures
            if sample.picture is not None:
                if sample.picture.size().width() < sample.duration/scale:
                    path = QPainterPath()
                    path.addRoundedRect(QRectF(t/scale, 52.5, sample.picture.size().width(), 45), 10, 10)
                    qp.setClipPath(path)
                    qp.drawPixmap(QRect(t/scale, 52.5, sample.picture.size().width(), 45), sample.picture)
                else:
                    path = QPainterPath()
                    path.addRoundedRect(QRectF(t / scale, 52.5, sample.duration/scale, 45), 10, 10)
                    qp.setClipPath(path)
                    pic = sample.picture.copy(0, 0, sample.duration/scale, 45)
                    qp.drawPixmap(QRect(t / scale, 52.5, sample.duration/scale, 45), pic)
            t += sample.duration

        # Curață calea clipului
        path = QPainterPath()
        path.addRect(self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height())
        qp.setClipPath(path)

        # Draw pointer
        qp.setPen(Qt.darkCyan)
        qp.setBrush(QBrush(Qt.darkCyan))

        qp.drawPolygon(poly)
        qp.drawLine(line)
        qp.end()

    # Mouse movement
    def mouseMoveEvent(self, e):
        self.pos = e.pos()

        # if mouse is being pressed, update pointer
        if self.clicking:
            x = self.pos.x()
            self.pointerPos = x
            self.positionChanged.emit(x)
            self.checkSelection(x)
            self.pointerTimePos = self.pointerPos*self.getScale()

        self.update()

    # Mouse pressed
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            x = e.pos().x()
            self.pointerPos = x
            self.positionChanged.emit(x)
            self.pointerTimePos = self.pointerPos * self.getScale()

            self.checkSelection(x)

            self.update()
            self.clicking = True  # Set clicking check to true

    # Mouse release
    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicking = False  # Set clicking check to false

    # Enter
    def enterEvent(self, e):
        self.is_in = True

    # Leave
    def leaveEvent(self, e):
        self.is_in = False
        self.update()

    # check selection
    def checkSelection(self, x):
        # Check if user clicked in video sample
        for sample in self.videoSamples:
            if sample.startPos < x < sample.endPos:
                sample.color = Qt.darkCyan
                if self.selectedSample is not sample:
                    self.selectedSample = sample
                    self.selectionChanged.emit(sample)
            else:
                sample.color = sample.defColor

    # Get time string from seconds
    def get_time_string(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)


    # Get scale from length
    def getScale(self):
        return float(self.duration)/float(self.width())

    # Get duration
    def getDuration(self):
        return self.duration

    # Get selected sample
    def getSelectedSample(self):
        return self.selectedSample

    # Set background color
    def setBackgroundColor(self, color):
        self.backgroundColor = color

    # Set text color
    def setTextColor(self, color):
        self.textColor = color

    # Set Font
    def setTextFont(self, font):
        self.font = font


class VideoRenderingTerminal(QWidget):
    def __init__(self, parent=None):
        super(VideoRenderingTerminal, self).__init__(parent)

        self.terminal_output = QTextEdit(self)
        self.terminal_output.setReadOnly(True)

        self.render_button = QPushButton("Render Video", self)
        self.render_button.clicked.connect(self.start_rendering)

        layout = QVBoxLayout(self)
        layout.addWidget(self.terminal_output)
        layout.addWidget(self.render_button)

    def start_rendering(self):
    # Deschide fereastra de dialog pentru export
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Video", "", "Video Files (*.mp4);;All Files (*)", options=options)

        if file_name:
            # Actualizează comanda de randare cu calea selectată
            render_command = f"python path_to_your_render_script.py --output {file_name}"

            process = subprocess.Popen(render_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            output, _ = process.communicate()

        # Afisează output-ul în terminal
        self.terminal_output.append(output.strip())
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                self.terminal_output.append(output.strip())
                QApplication.processEvents()  # Asigură-te că ai această linie

                process.communicate()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    terminal_widget = VideoRenderingTerminal()
    terminal_widget.show()
    sys.exit(app.exec_())
