import requests
import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap

# Готовим запрос.
geocoder_request = f"http://static-maps.yandex.ru/1.x/?ll=135.746181,-27.483765&spn=20,20&l=map"


class ImageDisplayWidget(QWidget):
    def __init__(self, image_path):
        super().__init__()

        # Загружаем изображение с помощью QPixmap
        pixmap = QPixmap(image_path)

        # Создаем QLabel и устанавливаем в него изображение
        label = QLabel(self)
        label.setPixmap(pixmap)

        # Создаем вертикальный layout и добавляем QLabel в него
        layout = QVBoxLayout(self)
        layout.addWidget(label)

        self.setLayout(layout)


# Выполняем запрос.
response = requests.get(geocoder_request)
if response:
    # Запрос успешно выполнен, печатаем полученные данные.

    map_filename = "map.png"
    with open(map_filename, "wb") as file:
        file.write(response.content)

    app = QApplication(sys.argv)

    image_display_widget = ImageDisplayWidget(map_filename)

    image_display_widget.show()
    os.remove(map_filename)

    sys.exit(app.exec_())

    # os.remove(map_filename)
else:
    # Произошла ошибка выполнения запроса. Обрабатываем http-статус.
    print("Ошибка выполнения запроса:")
    print(geocoder_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
