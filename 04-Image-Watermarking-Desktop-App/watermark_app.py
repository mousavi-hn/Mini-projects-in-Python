import sys
from PySide6.QtGui import QPixmap, QPainter, QFont
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QSplitter, QLabel, QFrame, QVBoxLayout, QPushButton, \
    QFileDialog, QMessageBox, QSlider, QLineEdit


def load_main_image():
    file_path, _ = QFileDialog.getOpenFileName(window, "Open File", filter="Image Files (*.jpg *.png *.bmp)")
    if file_path:
        global main_image
        main_image = QPixmap(file_path)

        image_display_part.clear()
        image_display_part.setPixmap(main_image.scaled(image_display_part.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

def load_watermark_image(opacity):
    global current_image_opacity, rendered_image, watermark_image_file_path
    current_opacity = opacity / 100.0
    if main_image is not None and watermark_image_file_path == "":
        watermark_image_file_path, _ = QFileDialog.getOpenFileName(window, "Open File", filter="Image Files (*.jpg *.png *.bmp)")

    if watermark_image_file_path != "":
        watermark = QPixmap(watermark_image_file_path)
        base_image = main_image.copy()

        painter = QPainter(base_image)
        painter.setOpacity(current_opacity)

        x = base_image.width() - watermark.width() - 20
        y = base_image.height() - watermark.height() - 20

        painter.drawPixmap(x, y, watermark)
        painter.end()

        rendered_image = base_image.copy()

        image_display_part.clear()
        image_display_part.setPixmap(
            base_image.scaled(image_display_part.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    if main_image is None:
        msg = QMessageBox()
        msg.setWindowTitle("Error!")
        msg.setText("Base image must be chosen first! Please use Load Image button!")
        msg.exec()

def load_watermark_text(opacity):
    global current_text_opacity, rendered_image
    current_text_opacity = opacity / 100.0
    if main_image is not None:
        base_image = main_image.copy()

        painter = QPainter(base_image)
        font = QFont("Arial", 40, QFont.Bold)
        painter.setFont(font)
        painter.setOpacity(current_text_opacity)

        painter.drawText(base_image.rect(), Qt.AlignCenter, text_watermark.text())
        painter.end()

        rendered_image = base_image.copy()

        image_display_part.clear()
        image_display_part.setPixmap(
            base_image.scaled(image_display_part.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    else:
        msg = QMessageBox()
        msg.setWindowTitle("Error!")
        msg.setText("Base image must be chosen first! Please use Load Image button!")
        msg.exec()


def save_image():
    if main_image is not None:
        rendered_image.save("rendered_image.png")
        msg = QMessageBox()
        msg.setWindowTitle("Success!")
        msg.setText("Saved successfully!")
        msg.exec()
    else:
        msg = QMessageBox()
        msg.setWindowTitle("Error!")
        msg.setText("No image found!")
        msg.exec()

def clear():
    image_display_part.clear()
    global main_image, watermark_image_file_path
    main_image = None
    watermark_image_file_path = ""
    text_watermark.clear()

app = QApplication(sys.argv)

main_image = None
watermark_image_file_path = ""
rendered_image = None

window = QWidget()
window.setWindowTitle("Watermarking Desktop")
window.setFixedSize(1200, 600)

main_layout = QHBoxLayout(window)
splitter = QSplitter(Qt.Horizontal)

image_display_part = QLabel()
image_display_part.setAlignment(Qt.AlignCenter)
image_display_part.setFrameStyle(QFrame.Panel | QFrame.Sunken)

control_panel = QWidget()
control_panel_layout = QVBoxLayout(control_panel)

load_image_button = QPushButton("Load Base Image")
load_image_button.clicked.connect(load_main_image)

image_opacity_slider = QSlider(Qt.Orientation.Horizontal)
image_opacity_slider.setMinimum(0)
image_opacity_slider.setMaximum(100)
image_opacity_slider.setValue(50)
current_image_opacity = image_opacity_slider.value()
image_opacity_slider.valueChanged.connect(load_watermark_image)

text_opacity_slider = QSlider(Qt.Orientation.Horizontal)
text_opacity_slider.setMinimum(0)
text_opacity_slider.setMaximum(100)
text_opacity_slider.setValue(50)
current_text_opacity = text_opacity_slider.value()
text_opacity_slider.valueChanged.connect(load_watermark_text)

text_watermark = QLineEdit()
text_watermark.setPlaceholderText("Put the text watermark here!")

load_watermark_text_button = QPushButton("Load Watermark Text")
load_watermark_text_button.clicked.connect(
    lambda checked=False, opacity=current_text_opacity: load_watermark_text(opacity)
)

load_watermark_image_button = QPushButton("Load Watermark Image")
load_watermark_image_button.clicked.connect(
    lambda checked=False, opacity=current_image_opacity: load_watermark_image(opacity)
)

save_image_button = QPushButton("Save Image")
save_image_button.clicked.connect(save_image)

clear_button = QPushButton("Clear")
clear_button.clicked.connect(clear)

control_panel_layout.addWidget(load_image_button)
control_panel_layout.addSpacing(100)

control_panel_layout.addWidget(load_watermark_image_button)
control_panel_layout.addWidget(QLabel("Choose the image opacity: "))
control_panel_layout.addWidget(image_opacity_slider)
control_panel_layout.addSpacing(100)

control_panel_layout.addWidget(text_watermark)
control_panel_layout.addWidget(load_watermark_text_button)
control_panel_layout.addWidget(QLabel("Choose the text opacity: "))
control_panel_layout.addWidget(text_opacity_slider)
control_panel_layout.addStretch()

control_panel_layout.addWidget(save_image_button)
control_panel_layout.addWidget(clear_button)

splitter.addWidget(image_display_part)
splitter.addWidget(control_panel)
splitter.setSizes([800, 400])

main_layout.addWidget(splitter)

window.show()
sys.exit(app.exec())