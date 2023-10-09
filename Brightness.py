from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QSlider, QLabel, QFileDialog
from PyQt5.QtCore import Qt
import sys
from moviepy.editor import VideoFileClip
from moviepy.editor import *
import os

class BrightnessWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Brightness & Contrast Adjuster")
        self.setGeometry(100, 100, 400, 150)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(-20, 20)
        self.slider.setValue(0)

        self.label = QLabel("Brightness: 0", alignment=Qt.AlignCenter)

        self.ok_button = QPushButton("Set Brightness")
        self.ok_button.clicked.connect(self.adjust_brightness)

        layout = QVBoxLayout()
        layout.addWidget(self.slider)
        layout.addWidget(self.label)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def change_brightness_video(self, videoclip, brightness_value: float):
        modified_clip = videoclip.fx(vfx.colorx, brightness_value)
        return modified_clip

    def adjust_brightness(self):
        try:
            brightness = float(self.slider.value())
            if self.parent() is not None:
                # Alege fișierul video sursă utilizând File Dialog
                file_dialog = QFileDialog()
                input_video_path, _ = file_dialog.getOpenFileName(None, "Select Video File", "", "Video Files (*.mp4 *.avi)")
                
                if input_video_path:
                    my_video_clip = VideoFileClip(input_video_path)
                    modified_clip = self.change_brightness_video(my_video_clip, brightness)
                    
                    # Exportă videoclipul modificat în același director cu sursa
                    output_video_path = os.path.splitext(input_video_path)[0] + "_modified.mp4"
                    modified_clip.write_videofile(output_video_path, codec='libx264')
        except ValueError:
            self.label.setText("Invalid brightness value")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrightnessWindow()
    window.show()
    sys.exit(app.exec_())
