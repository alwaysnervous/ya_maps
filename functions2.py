# Масштабирование
def scaling_up(sl):
    if sl.spn[0] <= 100:
        sl.spn = (sl.spn[0] + 1, sl.spn + 1)
    get_map(sl.lat, sl.lot, sl.spn)


def scaling_down(sl):
    if sl.spn[0] >= 0:
        sl.spn = (sl.spn[0] - 1, sl.spn - 1)
    get_map(sl.lat, sl.lot, sl.spn)


def up(sl):
    if -7.483765 >= sl.lot >= -47.483765:
        sl.lat += sl.height
    get_map(sl.lat, sl.lot, sl.spn)


def down(sl):
    if -7.483765 >= sl.lot >= -47.483765:
        sl.lat -= sl.height
    get_map(sl.lat, sl.lot, sl.spn)


def right(sl):
    if 155.746181 >= sl.lat >= 115.746181:
        sl.lat += sl.width
    get_map(sl.lat, sl.lot, sl.spn)


def left(sl):
    if 155.746181 >= sl.lat >= 115.746181:
        sl.lat -= sl.width
    get_map(sl.lat, sl.lot, sl.spn)
