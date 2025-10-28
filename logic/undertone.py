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
# Define skin color range in YCrCb space
   skin_mask = cv2.inRange(img_ycrcb, (0, 133, 77), (255, 173, 127))
   skin = cv2.bitwise_and(image, image, mask=skin_mask)


   # Convert to RGB and flatten for clustering
   skin_rgb = cv2.cvtColor(skin, cv2.COLOR_BGR2RGB)
   pixels = skin_rgb.reshape((-1, 3))
   pixels = pixels[np.any(pixels != [0, 0, 0], axis=1)]  # remove black background


   if len(pixels) == 0:
       raise ValueError("No skin pixels detected")


   # Cluster to find dominant skin colors
   kmeans = KMeans(n_clusters=num_colors, n_init=10)
   kmeans.fit(pixels)
   dominant_colors = kmeans.cluster_centers_.astype(int)
   return dominant_colors
