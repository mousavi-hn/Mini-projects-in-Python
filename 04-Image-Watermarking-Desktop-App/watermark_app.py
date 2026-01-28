import sys
from PySide6.QtGui import QPixmap, QPainter, QFont
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QSplitter, QLabel, QFrame, QVBoxLayout, QPushButton, \
    QFileDialog, QMessageBox, QSlider, QLineEdit

class WatermarkApp(QWidget):
    def __init__(self):
        super().__init__()
        self.base_pixmap = None
        self.watermark_pixmap = None
        self.watermark_text = ""
        self.first_temp_watermarked_image = None
        self.second_temp_watermarked_image = None
        self.rendered_pixmap = None

        self.setWindowTitle("Watermarking Desktop")
        self.setFixedSize(1200, 600)

        main_layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)

        self.image_display_part = QLabel()
        self.image_display_part.setAlignment(Qt.AlignCenter)
        self.image_display_part.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        control_panel = QWidget()
        control_panel_layout = QVBoxLayout(control_panel)

        load_image_button = QPushButton("Load Base Image")
        load_image_button.clicked.connect(self.load_main_image)

        self.image_opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.image_opacity_slider.setMinimum(0)
        self.image_opacity_slider.setMaximum(100)
        self.image_opacity_slider.setValue(50)
        self.current_image_opacity = self.image_opacity_slider.value() / 100.0
        self.image_opacity_slider.valueChanged.connect(self.choose_image_opacity)

        self.text_opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.text_opacity_slider.setMinimum(0)
        self.text_opacity_slider.setMaximum(100)
        self.text_opacity_slider.setValue(50)
        self.current_text_opacity = self.text_opacity_slider.value() / 100.0
        self.text_opacity_slider.valueChanged.connect(self.choose_text_opacity)

        self.watermark_text_field = QLineEdit()
        self.watermark_text_field.setPlaceholderText("Put the text watermark here!")

        self.load_watermark_text_button = QPushButton("Load Watermark Text")
        self.load_watermark_text_button.clicked.connect(self.load_watermark)

        distance_label = QLabel("Distance between texts: ")
        self.horizontal_distance_text_field = QLineEdit()
        self.horizontal_distance_text_field.setPlaceholderText("Distance between texts horizontally: ")
        self.vertical_distance_text_field = QLineEdit()
        self.vertical_distance_text_field.setPlaceholderText("Distance between texts vertically: ")

        self.load_watermark_image_button = QPushButton("Load Watermark Image")
        self.load_watermark_image_button.clicked.connect(self.load_watermark)

        save_image_button = QPushButton("Save Image")
        save_image_button.clicked.connect(self.save_image)

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear)

        control_panel_layout.addWidget(load_image_button)
        control_panel_layout.addSpacing(100)

        control_panel_layout.addWidget(self.load_watermark_image_button)
        control_panel_layout.addWidget(QLabel("Choose the image opacity: "))
        control_panel_layout.addWidget(self.image_opacity_slider)
        control_panel_layout.addSpacing(100)

        control_panel_layout.addWidget(self.watermark_text_field)
        control_panel_layout.addWidget(self.load_watermark_text_button)
        control_panel_layout.addWidget(QLabel("Choose the text opacity: "))
        control_panel_layout.addWidget(self.text_opacity_slider)
        control_panel_layout.addWidget(distance_label)
        control_panel_layout.addWidget(self.horizontal_distance_text_field)
        control_panel_layout.addWidget(self.vertical_distance_text_field)
        control_panel_layout.addStretch()

        control_panel_layout.addWidget(save_image_button)
        control_panel_layout.addWidget(clear_button)

        splitter.addWidget(self.image_display_part)
        splitter.addWidget(control_panel)
        splitter.setSizes([800, 400])

        main_layout.addWidget(splitter)

    def load_main_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", filter="Image Files (*.jpg *.png *.bmp)")
        if file_path:
            self.base_pixmap = QPixmap(file_path)
            self.first_temp_watermarked_image = self.base_pixmap.copy()
            self.second_temp_watermarked_image = self.base_pixmap.copy()
            self.image_display_part.setPixmap(self.base_pixmap.scaled(self.image_display_part.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def load_watermark(self):
        if self.base_pixmap is None and (self.sender() == self.text_opacity_slider or self.sender() == self.image_opacity_slider):
            return

        if self.base_pixmap is None:
            self.show_message_box("Error!", "Please choose a base image!")
            return

        if self.sender() == self.load_watermark_image_button:
            watermark_image_file_path, _ = QFileDialog.getOpenFileName(self, "Open File",
                                                                           filter="Image Files (*.jpg *.png *.bmp)")
            if watermark_image_file_path:
                self.watermark_pixmap = QPixmap(watermark_image_file_path)

        if self.sender() == self.load_watermark_image_button or self.sender() == self.image_opacity_slider:
            if self.watermark_pixmap is None:
                return

            self.first_temp_watermarked_image = self.second_temp_watermarked_image.copy()

            painter = QPainter(self.first_temp_watermarked_image)
            painter.setOpacity(self.current_image_opacity)

            x = self.first_temp_watermarked_image.width() - self.watermark_pixmap.width() - 20
            y = self.first_temp_watermarked_image.height() - self.watermark_pixmap.height() - 20

            painter.drawPixmap(x, y, self.watermark_pixmap)
            painter.end()

            self.rendered_pixmap = self.first_temp_watermarked_image.copy()

        if self.sender() == self.load_watermark_text_button or self.sender() == self.text_opacity_slider:
            self.second_temp_watermarked_image = self.first_temp_watermarked_image.copy()

            self.watermark_text = self.watermark_text_field.text()
            if self.watermark_text == "" and self.sender() == self.text_opacity_slider:
                return

            if self.watermark_text == "" and self.sender() == self.load_watermark_text_button:
                self.show_message_box("Error!", "Please choose a watermark text!")
                return

            try:
                horizontal_step = int(self.horizontal_distance_text_field.text())
                vertical_step = int(self.vertical_distance_text_field.text())
            except ValueError:
                self.show_message_box("Error!", "Please choose a valid distance between texts!")
                return

            if horizontal_step <= 0 or vertical_step <= 0:
                self.show_message_box("Error!", "Distances must be positive integers!")
                return

            painter = QPainter(self.second_temp_watermarked_image)
            font = QFont("Arial", 40, QFont.Bold)
            painter.setFont(font)
            painter.setOpacity(self.current_text_opacity)

            for x in range(0, self.second_temp_watermarked_image.width(), horizontal_step):
                for y in range(0, self.second_temp_watermarked_image.height(), vertical_step):
                    painter.drawText(x, y, self.watermark_text)
            painter.end()

            self.rendered_pixmap = self.second_temp_watermarked_image.copy()

        if self.rendered_pixmap is not None:
            self.image_display_part.setPixmap(
                self.rendered_pixmap.scaled(self.image_display_part.size(), Qt.KeepAspectRatio,
                                               Qt.SmoothTransformation))


    def save_image(self):
        if self.base_pixmap is None:
            self.show_message_box("Error!", "Please choose a base image!")
            return

        if self.rendered_pixmap is None:
            self.show_message_box("Error!", "Nothing to save yet. Apply a watermark first!")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "watermarked_image.png")
        if file_path:
            self.rendered_pixmap.save(f"{file_path}")
            self.show_message_box("Success!", "Image saved successfully!")

    def clear(self):
        self.image_display_part.clear()
        self.base_pixmap = None
        self.watermark_pixmap = None
        self.watermark_text = ""
        self.rendered_pixmap = None
        self.first_temp_watermarked_image = None
        self.second_temp_watermarked_image = None
        self.watermark_text_field.clear()
        self.horizontal_distance_text_field.clear()
        self.vertical_distance_text_field.clear()

    def show_message_box(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

    def choose_image_opacity(self, opacity):
        self.current_image_opacity = opacity / 100.0
        self.load_watermark()

    def choose_text_opacity(self, opacity):
        self.current_text_opacity = opacity / 100.0
        self.load_watermark()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WatermarkApp()
    window.show()
    sys.exit(app.exec())