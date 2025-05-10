# WebP Converter

A modern Python application for converting images to WebP format while maintaining high quality.

## Features

- Convert multiple images to WebP format in one go
- Adjustable quality settings (1-100)
- Modern and user-friendly interface
- Progress tracking
- Supports PNG, JPG, JPEG, TIFF, and BMP formats
- Maintains transparency for PNG images

## Requirements

- Python 3.8 or higher
- PySide6
- Pillow

## Installation

1. Clone this repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python webp_converter.py
   ```
2. Click "Select Folder" to choose the directory containing your images
3. Adjust the quality setting if needed (default is 85)
4. Click "Convert to WebP" to start the conversion
5. Wait for the process to complete

The converted WebP images will be saved in the same folder as the original images.

## Notes

- The application preserves transparency for PNG images
- Higher quality settings result in larger file sizes
- The default quality of 85 provides a good balance between quality and file size
- The application uses PySide6 for better macOS compatibility 