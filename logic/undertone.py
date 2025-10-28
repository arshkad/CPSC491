from flask import Flask, request, jsonify
from sklearn.cluster import KMeans
from PIL import Image
import numpy as np
import cv2
import io


app = Flask(__name__)


#Convert RGB <-> HEX
def rgb_to_hex(rgb):
   return '#%02x%02x%02x' % tuple(int(x) for x in rgb)


# Extract dominant colors (skin only)
def extract_dominant_skin_colors(image, num_colors=3):
   # Convert to RGB → YCrCb (helps isolate skin tones)
   img_ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
   (y, cr, cb) = cv2.split(img_ycrcb)

