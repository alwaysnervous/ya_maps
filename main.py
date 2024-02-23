import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QLineEdit


def get_map(lat, lon, l, z, pts: list[tuple[float, float]] = None):
    map_params = {
        "ll": ",".join([lat, lon]),
        "l": l,
        "z": z
    }
    if pts:
        map_params["pt"] = "~".join([",".join([str(coord) for coord in point]) for point in pts])
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    return response.content


def get_coordinates(address):
    url = (f'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&'
           f'geocode={address}&format=json')
    data = requests.get(url).json()
    geo_object = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    coordinates = map(float, geo_object['Point']
                                       ['pos'].split(' '))
    return coordinates


def get_address(lat, lon):
    url = (f'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&'
           f'geocode={lat},{lon}&format=json')
    data = requests.get(url).json()
    geo_object = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    address = geo_object["metaDataProperty"]["GeocoderMetaData"]["text"]
    return address


class ImageDisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.lat, self.lot = 135.746181, -27.483765
        self.layer_number = 0
        self.z = 4
        self.layers = ['map', 'sat', 'sat,skl']
        self.image_path = 'map.png'
        self.points = []

        pixmap = QPixmap(self.image_path)
        self.image_label = QLabel(self)
        self.image_label.setPixmap(pixmap)

        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)

        self.switch_map_layer_button = QPushButton("Смена слоя карты", self)
        self.switch_map_layer_button.clicked.connect(self.switch_map_layer)
        layout.addWidget(self.switch_map_layer_button)

        self.search_line_edit = QLineEdit(self)
        layout.addWidget(self.search_line_edit)

        self.search_button = QPushButton("Искать")
        self.search_button.clicked.connect(self.search)
        layout.addWidget(self.search_button)

        self.focus_button = QPushButton("Сделать фокус на картинке (ПОСЛЕ ВВОДА)")
        self.focus_button.clicked.connect(self.focus)
        layout.addWidget(self.focus_button)

        self.reset_search_result_button = QPushButton("Сброс поискового результата")
        self.reset_search_result_button.clicked.connect(self.reset_search_result)
        layout.addWidget(self.reset_search_result_button)

        self.address_line_edit = QLineEdit(self)
        self.address_line_edit.setPlaceholderText("Адрес найденого объекта")
        self.address_line_edit.setReadOnly(True)
        layout.addWidget(self.address_line_edit)

        self.focus()
        self.map_view()
        self.setLayout(layout)

    def focus(self):
        self.image_label.setFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.z = min(self.z + 1, 21)
            self.map_view()
        elif event.key() == Qt.Key_PageDown:
            self.z = max(self.z - 1, 0)
            self.map_view()
        if event.key() == Qt.Key_Up:
            self.lot = min(self.lot + 630 / (2 ** self.z), 80)
            self.map_view()
        if event.key() == Qt.Key_Down:
            self.lot = max(self.lot - 630 / (2 ** self.z), -80)
            self.map_view()
        if event.key() == Qt.Key_Right:
            self.lat = min(self.lat + 840 / (2 ** self.z), 180)
            self.map_view()
        if event.key() == Qt.Key_Left:
            self.lat = max(self.lat - 840 / (2 ** self.z), -180)
            self.map_view()

    def map_view(self):
        map_response = get_map(str(self.lat), str(self.lot), self.layers[self.layer_number], self.z, self.points)
        if map_response:
            with open(self.image_path, "wb") as file:
                file.write(map_response)
        else:
            print("Ошибка выполнения запроса:")
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(pixmap)
        self.focus()

    def switch_map_layer(self):
        self.layer_number = (self.layer_number + 1) % 3
        self.map_view()

    def search(self):
        search_query = self.search_line_edit.text()
        if not search_query:
            return
        self.z = 14
        self.lat, self.lot = get_coordinates(search_query)
        self.points = [[self.lat, self.lot]]
        self.address_line_edit.setText(get_address(self.lat, self.lot))
        self.map_view()

    def reset_search_result(self):
        self.points = [[]]
        self.address_line_edit.clear()
        self.map_view()


def except_hook(cls, exception, traceback):
    # Отлавливание исключений
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_display_widget = ImageDisplayWidget()
    image_display_widget.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
