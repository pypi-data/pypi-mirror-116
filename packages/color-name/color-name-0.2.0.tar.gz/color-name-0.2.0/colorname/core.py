
from PIL import ImageGrab
import colorsys

def get_color_name(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    h *= 360
    if l < .1:
        return "black"
    elif l > .9:
        return "white"
    elif s < .1:
        return "gray"
    elif h < 30 or h >= 330:
        return "red"
    elif 30 <= h < 90:
        return "yellow"
    elif 90 <= h < 150:
        return "green"
    elif 150 <= h < 210:
        return "cyan"
    elif 210 <= h < 270:
        return "blue"
    elif 270 <= h < 330:
        return "magenta"
    else:
        return "unknown"

def get_pixel_color(x, y):
    '''Returns RGB data from the given pixel coordinates'''
    return ImageGrab.grab(bbox=(x, y, x + 1, y + 1)).getdata()[0]

def get_pixel_color_name(x, y):
    '''Returns the name of a color at the given pixel coordinates'''
    color = get_pixel_color(x, y)
    return get_color_name(*color)

