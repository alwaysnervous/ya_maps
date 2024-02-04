import requests
import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from switch_map_layer import switch_map_layer
from functions2 import *

MAP_LAYER_NUMBER = 0


def get_map(lat, lon, spn):
    spn = ','.join(map(str, spn))
    map_params = {
        "ll": ",".join([lat, lon]),
        "spn": spn,
        "l": "map",
        # "pt": ",".join([lat, lon])
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    return response.content


class ImageDisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.lat, self.lot = '135.746181', '-27.483765'
        self.spn = (20, 20)
        self.layer_number = 0
        self.map_response = get_map('135.746181', '-27.483765', (20, 20))
        self.image_path = 'map.png'
        pixmap = QPixmap(self.image_path)
        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.map_view()
        button = QPushButton("Смена слоя карты", self)
        layout.addWidget(button)
        button.clicked.connect(lambda: switch_map_layer(self))
        self.setLayout(layout)

    def map_view(self):
        if self.map_response:
            with open(self.image_path, "wb") as file:
                file.write(self.map_response)
        else:
            print("Ошибка выполнения запроса:")
        pixmap = QPixmap(self.image_path)
        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_display_widget = ImageDisplayWidget()
    image_display_widget.show()
    sys.exit(app.exec_())

