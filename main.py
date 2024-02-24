import sys

import math
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QLineEdit, QCheckBox


def get_map(lat, lon, l, z, pts: list[tuple[float, float]] = None):
    map_params = {
        "ll": ",".join([lon, lat]),
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
    coordinates = map(float, geo_object['Point']['pos'].split(' '))
    return coordinates


def get_address(lat, lon, include_postal_code=False):
    url = (f'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&'
           f'geocode={lon},{lat}&format=json')
    data = requests.get(url).json()
    try:
        geo_object = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    except IndexError:
        return
    address = geo_object["metaDataProperty"]["GeocoderMetaData"]["text"]
    if include_postal_code:
        try:
            address += ", " + geo_object["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
        except KeyError:
            address += ", Почтовый индекс отсутствует"
    return address


def get_organization(lat, lon):
    url = (f'https://search-maps.yandex.ru/v1/?apikey=73961a13-a537-4463-a34a-bff0205a48e8&'
           f'text=организации&lang=ru_RU&ll={lon},{lat}&type=biz&results=1&spn=0.45,0.45')
    response = requests.get(url).json()
    organization = response['features'][0]['properties']['CompanyMetaData']['name'] if response['features'] else ''
    return organization


class ImageDisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.lat, self.lot = 55.75, 37.61
        self.layer_number = 0
        self.z = 10
        self.layers = ['map', 'sat', 'sat,skl']
        self.image_path = 'map.png'
        self.points = []

        layout = QVBoxLayout(self)

        pixmap = QPixmap(self.image_path)
        self.image_label = QLabel(self)
        self.image_label.setPixmap(pixmap)
        self.image_label.mousePressEvent = self.getPos
        layout.addWidget(self.image_label)

        self.switch_map_layer_button = QPushButton("Смена слоя карты", self)
        self.switch_map_layer_button.clicked.connect(self.switch_map_layer)
        layout.addWidget(self.switch_map_layer_button)

        self.search_line_edit = QLineEdit(self)
        layout.addWidget(self.search_line_edit)

        self.search_button = QPushButton("Искать", self)
        self.search_button.clicked.connect(self.search)
        layout.addWidget(self.search_button)

        self.focus_button = QPushButton("Сделать фокус на картинке (ПОСЛЕ ВВОДА)", self)
        self.focus_button.clicked.connect(self.focus)
        layout.addWidget(self.focus_button)

        self.reset_search_result_button = QPushButton("Сброс поискового результата", self)
        self.reset_search_result_button.clicked.connect(self.reset_search_result)
        layout.addWidget(self.reset_search_result_button)

        self.address_line_edit = QLineEdit(self)
        self.address_line_edit.setPlaceholderText("Адрес найденого объекта")
        self.address_line_edit.setReadOnly(True)
        layout.addWidget(self.address_line_edit)

        self.include_postal_code_checkbox = QCheckBox("Включать приписывание почтового индекса", self)
        self.include_postal_code_checkbox.clicked.connect(self.include_postal_code)
        layout.addWidget(self.include_postal_code_checkbox)

        self.focus()
        self.map_view()
        self.setLayout(layout)

    def getPos(self, event):
        x = event.pos().x()
        y = event.pos().y()
        event_button = event.button()
        clicked_lot = max(min(self.lot + (x - 300) * 1.4 / (2 ** self.z),
                              180), -180)
        clicked_lat = max(min(self.lat + (225 - y) * 1.4 * math.cos(math.radians(self.lat)) / (2 ** self.z),
                              80), -80)
        self.points = [(clicked_lot, clicked_lat, 'org')]
        if event_button == 1:
            self.address_line_edit.setText(get_address(clicked_lat, clicked_lot,
                                                       self.include_postal_code_checkbox.isChecked()))

        elif event_button == 2:
            self.address_line_edit.setText(get_organization(clicked_lat, clicked_lot))
        self.map_view()

    def focus(self):
        self.image_label.setFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.z = min(self.z + 1, 21)
            self.map_view()
        elif event.key() == Qt.Key_PageDown:
            self.z = max(self.z - 1, 3)
            self.map_view()
        if event.key() == Qt.Key_Up:
            self.lat = min(self.lat + 634 / (2 ** self.z), 80)
            self.map_view()
        if event.key() == Qt.Key_Down:
            self.lat = max(self.lat - 634 / (2 ** self.z), -80)
            self.map_view()
        if event.key() == Qt.Key_Right:
            self.lot = min(self.lot + 842 / (2 ** self.z), 180)
            self.map_view()
        if event.key() == Qt.Key_Left:
            self.lot = max(self.lot - 842 / (2 ** self.z), -180)
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
        self.lot, self.lat = get_coordinates(search_query)
        self.points = [(self.lat, self.lot, 'org')]
        self.address_line_edit.setText(get_address(self.lat, self.lot, self.include_postal_code_checkbox.isChecked()))
        self.map_view()

    def reset_search_result(self):
        self.points = [()]
        self.address_line_edit.clear()
        self.map_view()

    def include_postal_code(self):
        x, y = get_coordinates(self.address_line_edit.text())
        self.address_line_edit.setText(get_address(y, x, self.include_postal_code_checkbox.isChecked()))
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
