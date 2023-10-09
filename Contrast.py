from PyQt5.QtWidgets import QWidget, QDialog, QVBoxLayout, QLabel, QSlider, QDialogButtonBox
from PyQt5.QtCore import Qt

class ContrastWindow(QDialog, QWidget):
    def __init__(self, video_player, width, height):
        super().__init__()
        self.setWindowTitle("Contrast")
        self.resize(width, height)
        self.video_player = video_player
        
        layout = QVBoxLayout()
        
        self.contrast_label = QLabel("Contrast: 0")
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setMinimum(-100)
        self.contrast_slider.setMaximum(100)
        self.contrast_slider.setTickPosition(QSlider.TicksBelow)
        self.contrast_slider.setTickInterval(10)
        self.contrast_slider.valueChanged.connect(self.update_contrast_label)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.apply_contrast)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(self.contrast_label)
        layout.addWidget(self.contrast_slider)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def update_contrast_label(self, value):
        self.contrast_label.setText(f"Contrast: {value}")
    
    def apply_contrast(self):
        contrast_value = self.contrast_slider.value()
        self.video_player.contrast_video(contrast_value)
        self.accept()
