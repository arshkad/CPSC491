from flask import Flask, request, jsonify
import colorsys
import numpy as np

app = Flask(__name__)

# Convert HEX <-> RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % tuple(int(x) for x in rgb)


