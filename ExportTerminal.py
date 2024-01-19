from PyQt5.QtWidgets import QFileDialog, QPushButton, QWidget, QVBoxLayout, QTextEdit
from moviepy.editor import VideoFileClip

class ExportTerminal(QWidget):
    def __init__(self, parent=None):
        super(ExportTerminal, self).__init__()
        w = 200
        h = 500
        self.resize(w, h)

        self.terminal_output = QTextEdit(self)
        self.terminal_output.setReadOnly(True)
        self.setFixedSize(200, 500)  # Setează dimensiunile fixe ale ferestrei (schimbă dimensiunile după nevoie)

        self.select_file_button = QPushButton("Select Video File", self)
        self.select_file_button.clicked.connect(self.select_video_file)

        self.export_button = QPushButton("Export Video", self)
        self.export_button.clicked.connect(self.start_export)

        layout = QVBoxLayout(self)
        layout.addWidget(self.terminal_output)
        layout.addWidget(self.select_file_button)
        layout.addWidget(self.export_button)

        self.setLayout(layout)

        self.selected_file_path = None  # Variabilă pentru a stoca calea către fișierul video selectat

    def set_position(self, main_window_rect):
        # Plasează fereastra în colțul din dreapta jos al ferestrei principale
        x = main_window_rect.right() - self.width()
        y = main_window_rect.bottom() - self.height()
        self.move(x, y)

    def select_video_file(self):
        # Deschide fereastra de dialog pentru selectarea fișierului video
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Video File", "", "Video Files (*.mp4);;All Files (*)", options=options)

        if file_name:
            # Salvează calea către fișierul video selectat
            self.selected_file_path = file_name
            self.terminal_output.append(f"Selected video file: {self.selected_file_path}")

    def start_export(self):
        if not self.selected_file_path:
            self.terminal_output.append("Please select a video file.")
            return

        try:
            # Creează un obiect VideoFileClip folosind calea către fișierul video selectat
            video_clip = VideoFileClip(self.selected_file_path)

            # Deschide fereastra de dialog pentru export
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getSaveFileName(self, "Export Video", "", "Video Files (*.mp4);;All Files (*)", options=options)

            if file_name:
                # Salvează clipul video
                video_clip.write_videofile(file_name, codec="libx264", audio_codec="aac")

                # Afisează mesajul în terminal
                self.terminal_output.append(f"Export successful. Video saved at: {file_name}")
        except Exception as e:
            # În caz de eroare, afișează mesajul în terminal
            self.terminal_output.append(f"Export failed. Error: {str(e)}")
