import sys
import os
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                            QWidget, QFileDialog, QProgressBar, QLabel, QSlider, QHBoxLayout)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QIcon, QPalette, QColor
from PIL import Image

class ConversionWorker(QThread):
    progress = Signal(int)
    finished = Signal()
    error = Signal(str)

    def __init__(self, input_dir, quality):
        super().__init__()
        self.input_dir = input_dir
        self.quality = quality

    def run(self):
        try:
            image_files = [f for f in os.listdir(self.input_dir) 
                         if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))]
            total_files = len(image_files)
            
            for i, image_file in enumerate(image_files):
                input_path = os.path.join(self.input_dir, image_file)
                output_path = os.path.join(self.input_dir, 
                                         f"{os.path.splitext(image_file)[0]}.webp")
                
                with Image.open(input_path) as img:
                    if img.mode in ('RGBA', 'LA'):
                        img.save(output_path, 'WEBP', quality=self.quality, lossless=False)
                    else:
                        img.convert('RGB').save(output_path, 'WEBP', quality=self.quality, lossless=False)
                
                self.progress.emit(int((i + 1) / total_files * 100))
            
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

class WebPConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WebP Converter")
        self.setMinimumSize(500, 400)
        self.setup_ui()
        self.setup_dark_theme()

    def setup_dark_theme(self):
        # Set the application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0c1826;
            }
            QWidget {
                background-color: #0c1826;
                color: #687683;
            }
            QPushButton {
                background-color: #7263f2;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8a7df4;
            }
            QPushButton:pressed {
                background-color: #5a4bd1;
            }
            QPushButton:disabled {
                background-color: #122b40;
                color: #757575;
            }
            QPushButton#convert_btn {
                background-color: #1d966d;
                color: #ffffff;
            }
            QPushButton#convert_btn:hover {
                background-color: #22b07f;
            }
            QPushButton#convert_btn:pressed {
                background-color: #187c5a;
            }
            QPushButton#convert_btn:disabled {
                background-color: #122b40;
                color: #757575;
            }
            QProgressBar {
                border: 2px solid #7263f2;
                border-radius: 5px;
                text-align: center;
                background-color: #0c1826;
                color: #687683;
            }
            QProgressBar::chunk {
                background-color: #7263f2;
                border-radius: 3px;
            }
            QLabel {
                color: #687683;
            }
            QSlider::groove:horizontal {
                border: 1px solid #7263f2;
                height: 8px;
                background: #0c1826;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #7263f2;
                border: none;
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #8a7df4;
            }
            QSlider::sub-page:horizontal {
                background: #7263f2;
                border-radius: 4px;
            }
        """)

    def setup_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("WebP Converter")
        title.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Quality selector
        quality_layout = QVBoxLayout()
        quality_label = QLabel("Quality:")
        quality_label.setFont(QFont('Arial', 12))
        
        # Create horizontal layout for slider and value label
        quality_control_layout = QHBoxLayout()
        
        # Quality slider
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(1, 100)
        self.quality_slider.setValue(85)
        self.quality_slider.setMinimumWidth(200)
        self.quality_slider.valueChanged.connect(self.update_quality_label)
        
        # Quality value label
        self.quality_value_label = QLabel("85")
        self.quality_value_label.setFont(QFont('Arial', 12))
        self.quality_value_label.setMinimumWidth(30)
        self.quality_value_label.setAlignment(Qt.AlignRight)
        
        quality_control_layout.addWidget(self.quality_slider)
        quality_control_layout.addWidget(self.quality_value_label)
        
        quality_layout.addWidget(quality_label)
        quality_layout.addLayout(quality_control_layout)
        layout.addLayout(quality_layout)

        # Select folder button
        self.select_btn = QPushButton("Select Folder")
        self.select_btn.setFont(QFont('Arial', 12))
        self.select_btn.setMinimumHeight(50)
        self.select_btn.clicked.connect(self.select_folder)
        layout.addWidget(self.select_btn)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFont(QFont('Arial', 12))
        self.progress_bar.setMinimumHeight(30)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setFont(QFont('Arial', 12))
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # Convert button
        self.convert_btn = QPushButton("Convert to WebP")
        self.convert_btn.setObjectName("convert_btn")
        self.convert_btn.setFont(QFont('Arial', 12))
        self.convert_btn.setMinimumHeight(50)
        self.convert_btn.clicked.connect(self.start_conversion)
        self.convert_btn.setEnabled(False)
        layout.addWidget(self.convert_btn)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.input_dir = folder
            self.convert_btn.setEnabled(True)
            self.status_label.setText(f"Selected folder: {folder}")
            self.progress_bar.setValue(0)
            self.progress_bar.hide()

    def update_quality_label(self, value):
        self.quality_value_label.setText(str(value))

    def start_conversion(self):
        self.convert_btn.setEnabled(False)
        self.select_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        self.status_label.setText("Converting images...")

        self.worker = ConversionWorker(self.input_dir, self.quality_slider.value())
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.conversion_finished)
        self.worker.error.connect(self.conversion_error)
        self.worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def conversion_finished(self):
        self.status_label.setText("Conversion completed successfully!")
        self.convert_btn.setEnabled(True)
        self.select_btn.setEnabled(True)

    def conversion_error(self, error_msg):
        self.status_label.setText(f"Error: {error_msg}")
        self.convert_btn.setEnabled(True)
        self.select_btn.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WebPConverter()
    window.show()
    sys.exit(app.exec()) 