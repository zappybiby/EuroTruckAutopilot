from screeninfo import get_monitors
import re


def get():
    monitors = []

    for m in get_monitors():
        x = (str(m))
        monitors.append(re.sub(r'([?!^monitor()])', '', x))

    return monitors


def get_window_x_position(offset):
    monitors = get()
    return int(get_x_offset(monitors[1])) + offset if len(monitors) > 1 else offset


def get_x_offset(monitor):
    return monitor[monitor.find('+') + 1:monitor.rfind('+')]
