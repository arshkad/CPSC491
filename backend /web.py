from flask import Flask, request, jsonify
from sklearn.cluster import KMeans
import cv2
import numpy as np
from PIL import Image

app = Flask(__name__)

def extract_dominant_colors(image, num_colors=3):
    # Convert to RGB and reshape
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((-1, 3))
    
    # KMeans to find dominant colors
    kmeans = KMeans(n_clusters=num_colors, n_init=10)
    kmeans.fit(image)
    
    colors = kmeans.cluster_centers_.astype(int)
    return colors