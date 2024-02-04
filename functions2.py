from main import get_map


# Масштабирование
def scaling_up(sl):
    if sl.spn[0] <= 90 and sl.spn[1] <= 90:
        sl.spn = (sl.spn[0] + 1, sl.spn[1] + 1)
    sl.map_response = get_map(sl.lat, sl.lot, sl.spn)
    sl.map_view()


def scaling_down(sl):
    if sl.spn[0] >= 0 and sl.spn[1] >= 0:
        sl.spn = (sl.spn[0] - 1, sl.spn[1] - 1)
    sl.map_response = get_map(sl.lat, sl.lot, sl.spn)
    sl.map_view()


# Движение
def up(sl):
    if float(sl.lot) + 38.5 <= 90:
        sl.lot = str(float(sl.lot) + 38.5)
    sl.map_response = get_map(sl.lat, sl.lot, sl.spn)
    sl.map_view()


def down(sl):
    if float(sl.lot) - 38.5 >= -90:
        sl.lot = str(float(sl.lot) - 38.5)
    sl.map_response = get_map(sl.lat, sl.lot, sl.spn)
    sl.map_view()


def right(sl):
    if float(sl.lat) + 51.3 <= 180:
        sl.lat = str(float(sl.lat) + 51.3)
    sl.map_response = get_map(sl.lat, sl.lot, sl.spn)
    sl.map_view()


def left(sl):
    if float(sl.lat) - 51.3 >= -180:
        sl.lat = str(float(sl.lat) - 51.3)
    sl.map_response = get_map(sl.lat, sl.lot, sl.spn)
    sl.map_view()
