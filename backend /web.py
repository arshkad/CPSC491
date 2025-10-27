from flask import Flask, request, jsonify
from sklearn.cluster import KMeans
import cv2
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Extract colors using kmeans 
def extract_dominant_colors(image, num_colors=3):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((-1, 3))
    kmeans = KMeans(n_clusters=num_colors, n_init=10)
    kmeans.fit(image)
    colors = kmeans.cluster_centers_.astype(int)
    return colors.tolist()

# Home route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Color Extraction API!"})

# Extract dominant colors
@app.route('/extract_colors', methods=['POST'])
def extract_colors():
    # Expect an image file from client
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    file = request.files['image']
    image_stream = np.array(Image.open(io.BytesIO(file.read())))
    image_cv = cv2.cvtColor(image_stream, cv2.COLOR_RGB2BGR)

    num_colors = int(request.form.get('num_colors', 3))
    colors = extract_dominant_colors(image_cv, num_colors=num_colors)

    return jsonify({"dominant_colors": colors})

# Health check
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "Backend running", "model": "KMeans color extraction"})

if __name__ == '__main__':
    app.run(debug=True)
