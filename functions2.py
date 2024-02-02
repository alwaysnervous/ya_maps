# Масштабирование
def scaling_up(sl):
    if sl.spn[0] <= 100:
        sl.spn = (sl.spn[0] + 1, sl.spn + 1)
    get_map(sl.lat, sl.lot, sl.spn)


def scaling_down(sl):
    if sl.spn[0] >= 0:
        sl.spn = (sl.spn[0] - 1, sl.spn - 1)
    get_map(sl.lat, sl.lot, sl.spn)


