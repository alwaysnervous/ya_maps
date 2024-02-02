import requests
import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from switch_map_layer import switch_map_layer

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
    def __init__(self, image_path):
        super().__init__()
        self.lat, self.lot = '135.746181', '-27.483765'
        self.spn = (20, 20)

        # Загружаем изображение с помощью QPixmap
        pixmap = QPixmap(image_path)

        # Создаем QLabel и устанавливаем в него изображение
        label = QLabel(self)
        label.setPixmap(pixmap)

        # Создаем вертикальный layout и добавляем QLabel в него
        layout = QVBoxLayout(self)
        layout.addWidget(label)

        # Создаем кнопку
        button = QPushButton("Смена слоя карты", self)

        # Добавляем кнопку в вертикальный layout
        layout.addWidget(button)

        button.clicked.connect(switch_map_layer)

        self.setLayout(layout)


# Выполняем запрос.
map_response = get_map('135.746181', '-27.483765', (20, 20))
if map_response:
    # Запрос успешно выполнен, печатаем полученные данные.

    map_filename = "map.png"
    with open(map_filename, "wb") as file:
        file.write(map_response)

    app = QApplication(sys.argv)

    image_display_widget = ImageDisplayWidget(map_filename)

    image_display_widget.show()
    os.remove(map_filename)

    sys.exit(app.exec_())
else:
    # Произошла ошибка выполнения запроса. Обрабатываем http-статус.
    print("Ошибка выполнения запроса:")
