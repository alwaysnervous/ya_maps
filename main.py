import requests
import sys
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from functions2 import *

MAP_LAYER_NUMBER = 0


def get_map(lat, lon, spn, l):
    spn = ','.join(map(str, spn))
    map_params = {
        "ll": ",".join([lat, lon]),
        "spn": spn,
        "l": l,
        # "pt": ",".join([lat, lon])
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    return response.content


class ImageDisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.lat, self.lot = '135.746181', '-27.483765'
        self.spn = [34, 34]
        self.layer_number = 0
        self.layers = ['map', 'sat', 'sat,skl']
        self.image_path = 'map.png'

        pixmap = QPixmap(self.image_path)
        self.label = QLabel(self)
        self.label.setPixmap(pixmap)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        self.map_view()

        button = QPushButton("Смена слоя карты", self)
        layout.addWidget(button)
        button.clicked.connect(self.switch_map_layer)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.spn = tuple(map(lambda x: max(x - 17, 0), self.spn))
        elif event.key() == Qt.Key_PageDown:
            self.spn = tuple(map(lambda x: min(x + 17, 68), self.spn))
        self.map_view()

    def map_view(self):
        map_response = get_map('135.746181', '-27.483765', self.spn, self.layers[self.layer_number])
        if map_response:
            with open(self.image_path, "wb") as file:
                file.write(map_response)
        else:
            print("Ошибка выполнения запроса:")
        pixmap = QPixmap(self.image_path)
        self.label.setPixmap(pixmap)

    def switch_map_layer(self):
        self.layer_number = (self.layer_number + 1) % 3
        self.map_view()
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_display_widget = ImageDisplayWidget()
    image_display_widget.show()
    sys.exit(app.exec_())

