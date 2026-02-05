from collections import Counter

import webcolors
from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtGui import QColor


class WorkerThread(QObject):
    finished = Signal(list)

    def __init__(self, image, progress_bar):
        super().__init__()
        self.image = image
        self.progress_bar = progress_bar
        self.detected_colors = []

    def get_detected_colors(self):
        return self.detected_colors

    @Slot()
    def run(self):
        pixels = []
        self.progress_bar.setMaximum(self.image.height() * self.image.width())
        self.progress_bar.setValue(0)

        for y in range(self.image.height()):
            for x in range(self.image.width()):
                color = QColor(self.image.pixel(x, y))
                pixels.append((color.red(), color.green(), color.blue()))
                self.progress_bar.setValue(self.progress_bar.value() + 1)

        most_common = Counter(pixels).most_common(100)
        top_ten_colors = []
        for color, count in most_common:
            top_ten_colors.append(self.closest_color(color))

        self.detected_colors = list(dict.fromkeys(top_ten_colors))
        self.finished.emit(self.detected_colors)

    def closest_color(self, requested_color):
        min_distance = float("inf")
        closest_name = None

        for name in webcolors.names("css3"):
            hex_code = webcolors.name_to_hex(name)
            rgb_common = webcolors.hex_to_rgb(hex_code)

            rd = (rgb_common[0] - requested_color[0]) ** 2
            gd = (rgb_common[1] - requested_color[1]) ** 2
            bd = (rgb_common[2] - requested_color[2]) ** 2

            distance = rd + gd + bd

            if distance < min_distance:
                min_distance = distance
                closest_name = name

        return closest_name




