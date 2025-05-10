import sys
import os
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                            QWidget, QFileDialog, QProgressBar, QLabel, QSlider, QHBoxLayout)
from PySide6.QtCore import Qt, QThread, Signal, QMimeData
from PySide6.QtGui import QFont, QIcon, QPalette, QColor, QDragEnterEvent, QDropEvent
from PIL import Image
from app_icon import create_app_icon

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
                    # Convert palette images to RGBA
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    elif img.mode in ('RGBA', 'LA'):
                        # Already in RGBA or LA mode, no conversion needed
                        pass
                    else:
                        # Convert other modes to RGB
                        img = img.convert('RGB')
                    
                    # Save as WebP
                    img.save(output_path, 'WEBP', quality=self.quality, lossless=False)
                
                self.progress.emit(int((i + 1) / total_files * 100))
            
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

class DropZone(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent  # Store reference to main window
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(150)
        self.setAcceptDrops(True)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #7263f2;
                border-radius: 10px;
                background-color: #0c1826;
                color: #687683;
            }
            QLabel:hover {
                border-color: #8a7df4;
                background-color: #122b40;
            }
        """)
        self.setText("Drop folder here\nor click to select")
        self.setFont(QFont('Arial', 12))
        self.setCursor(Qt.PointingHandCursor)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                QLabel {
                    border: 2px dashed #1d966d;
                    border-radius: 10px;
                    background-color: #122b40;
                    color: #687683;
                }
            """)

    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #7263f2;
                border-radius: 10px;
                background-color: #0c1826;
                color: #687683;
            }
            QLabel:hover {
                border-color: #8a7df4;
                background-color: #122b40;
            }
        """)

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            path = url.toLocalFile()
            if os.path.isdir(path):
                if hasattr(self.main_window, 'handle_folder_selected'):
                    self.main_window.handle_folder_selected(path)
                else:
                    print("Error: Main window doesn't have handle_folder_selected method")
            self.setStyleSheet("""
                QLabel {
                    border: 2px dashed #7263f2;
                    border-radius: 10px;
                    background-color: #0c1826;
                    color: #687683;
                }
                QLabel:hover {
                    border-color: #8a7df4;
                    background-color: #122b40;
                }
            """)

class WebPConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WebP Converter")
        self.setMinimumSize(500, 400)
        self.setup_ui()
        self.setup_dark_theme()
        self.input_dir = None  # Initialize input_dir

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

        # Drop zone
        self.drop_zone = DropZone(self)
        self.drop_zone.mousePressEvent = self.show_folder_dialog
        layout.addWidget(self.drop_zone)

        # Add spacer for margin
        layout.addSpacing(30)  # Add 30 pixels of vertical space

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

        # Add spacer to push footer to bottom
        layout.addStretch()

        # Footer
        footer = QLabel("Powered by Nikba Creative Studio")
        footer.setFont(QFont('Arial', 10))
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #687683; margin-top: 20px;")
        layout.addWidget(footer)

    def show_folder_dialog(self, event):
        try:
            folder = QFileDialog.getExistingDirectory(self, "Select Folder")
            if folder:
                self.handle_folder_selected(folder)
        except Exception as e:
            print(f"Error selecting folder: {str(e)}")

    def handle_folder_selected(self, folder):
        try:
            self.input_dir = folder
            self.convert_btn.setEnabled(True)
            self.status_label.setText(f"Selected folder: {folder}")
            self.progress_bar.setValue(0)
            self.progress_bar.hide()
            self.drop_zone.setText(f"Selected: {os.path.basename(folder)}\nDrop another folder or click to change")
        except Exception as e:
            print(f"Error handling folder selection: {str(e)}")

    def update_quality_label(self, value):
        self.quality_value_label.setText(str(value))

    def start_conversion(self):
        if not self.input_dir:
            self.status_label.setText("Error: No folder selected")
            return

        try:
            self.convert_btn.setEnabled(False)
            self.progress_bar.setValue(0)
            self.progress_bar.show()
            self.status_label.setText("Converting images...")

            self.worker = ConversionWorker(self.input_dir, self.quality_slider.value())
            self.worker.progress.connect(self.update_progress)
            self.worker.finished.connect(self.conversion_finished)
            self.worker.error.connect(self.conversion_error)
            self.worker.start()
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            self.convert_btn.setEnabled(True)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def conversion_finished(self):
        self.status_label.setText("Conversion completed successfully!")
        self.convert_btn.setEnabled(True)

    def conversion_error(self, error_msg):
        self.status_label.setText(f"Error: {error_msg}")
        self.convert_btn.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Create and set the app icon
    icon_path = create_app_icon()
    app_icon = QIcon(icon_path)
    app.setWindowIcon(app_icon)
    
    window = WebPConverter()
    window.setWindowIcon(app_icon)
    window.show()
    sys.exit(app.exec()) 