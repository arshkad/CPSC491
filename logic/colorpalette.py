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

# Rotate hue (in HSV space)
def adjust_hue(rgb, degree_shift):
   r, g, b = [x/255.0 for x in rgb]
   h, s, v = colorsys.rgb_to_hsv(r, g, b)
   h = (h + degree_shift / 360.0) % 1.0
   r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v)
   return [r2 * 255, g2 * 255, b2 * 255]


# Generate palette from one color
def generate_palette(base_color, palette_type="complementary"):
   """
   palette_type: 'complementary', 'analogous', 'triadic', 'monochromatic', 'split_complementary'
   base_color: [R, G, B] or '#RRGGBB'
   """
   if isinstance(base_color, str):
       base_rgb = np.array(hex_to_rgb(base_color))
   else:
       base_rgb = np.array(base_color)


   palette = []


   if palette_type == "complementary":
       palette = [base_rgb, adjust_hue(base_rgb, 180)]
   elif palette_type == "analogous":
       palette = [adjust_hue(base_rgb, -30), base_rgb, adjust_hue(base_rgb, 30)]
   elif palette_type == "triadic":
       palette = [base_rgb, adjust_hue(base_rgb, 120), adjust_hue(base_rgb, 240)]
   elif palette_type == "split_complementary":
       palette = [base_rgb, adjust_hue(base_rgb, 150), adjust_hue(base_rgb, 210)]
   elif palette_type == "monochromatic":
       # Generate lighter/darker variations of the same hue
       r, g, b = base_rgb
       for factor in [0.5, 0.75, 1.0, 1.25, 1.5]:
           new_color = np.clip(base_rgb * factor, 0, 255)
           palette.append(new_color)
   else:
       raise ValueError("Palette type not specified.") 

