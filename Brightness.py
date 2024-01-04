from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QSlider, QLabel, QFileDialog
from PyQt5.QtCore import Qt
import sys
from moviepy.editor import VideoFileClip, clips_array
from moviepy.editor import vfx
import os

class BrightnessWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Brightness & Contrast Adjuster")
        self.setGeometry(100, 100, 250, 250)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(-50, 50)
        self.slider.setValue(0)

        self.label = QLabel("Brightness: 0", alignment=Qt.AlignCenter)

        self.ok_button = QPushButton("Set Brightness & Contrast")
        self.ok_button.clicked.connect(self.adjust_brightness)

        layout = QVBoxLayout()
        layout.addWidget(self.slider)
        layout.addWidget(self.label)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

        # Variabila de instanță pentru a reține clipul video curent
        self.current_video_clip = None

        # Încarcă clipul video inițial la deschiderea ferestrei
        file_dialog = QFileDialog()
        input_video_path, _ = file_dialog.getOpenFileName(None, "Select Video File", "", "Video Files (*.mp4 *.avi)")
        if input_video_path:
            self.load_video(input_video_path)

    def change_brightness_video(self, videoclip, brightness_value: float):
        # Mapare intervalului [-50, 50] la [0, 1]
        brightness_factor = (brightness_value + 50) / 100
        contrast_factor = 1.0  # Menținerea contrastului la o valoare constantă

        # Calcularea factorului de ajustare pentru luminanță
        if brightness_value > 0:
            # Dacă este o valoare pozitivă, să se mapeze în intervalul [1, 2]
            brightness_factor = 1 + brightness_value / 50

        # Asigură că valorile sunt în intervalul corespunzător pentru moviepy
        brightness_factor = max(0.5, min(brightness_factor, 2.0))
        contrast_factor = max(0.5, min(contrast_factor, 2.0))

        modified_clip = videoclip.fx(vfx.colorx, brightness_factor).fx(vfx.colorx, contrast_factor)
        return modified_clip

    def load_video(self, file_path):
        self.current_video_clip = VideoFileClip(file_path)

    def adjust_brightness(self):
        try:
            brightness = float(self.slider.value())
            
            if self.current_video_clip is not None:
                # Folosește clipul video curent
                modified_clip = self.change_brightness_video(self.current_video_clip, brightness)
                
                # Exportă videoclipul modificat în același director cu sursa
                output_video_path = os.path.splitext(self.current_video_clip.filename)[0] + "_modified.mp4"
                modified_clip.write_videofile(output_video_path, codec='libx264')
        except ValueError:
            self.label.setText("Invalid brightness value")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrightnessWindow()
    window.show()
    sys.exit(app.exec_())
