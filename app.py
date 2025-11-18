# from flask import Flask, request, jsonify, render_template
# from logic.colorpalette import generate_palette
# from logic.undertone import extract_dominant_skin_colors
# from logic.web import extract_dominant_colors
# import cv2
# import numpy as np
# from PIL import Image
# import io

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template("index.html")

# @app.route('/api/palette', methods=['POST'])
# def palette():
#     data = request.json
#     base = data.get("base_color")
#     ptype = data.get("palette_type", "complementary")
    
#     result = generate_palette(base, ptype)
#     return jsonify({"palette": result})

# @app.route('/api/extract_colors', methods=['POST'])
# def extract_colors_route():
#     file = request.files["image"]
#     img = np.array(Image.open(io.BytesIO(file.read())))
#     img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
#     colors = extract_dominant_colors(img_bgr)
#     return jsonify({"dominant_colors": colors})

# @app.route('/api/skin_tone', methods=['POST'])
# def skin_tone():
#     file = request.files["image"]
#     img = np.array(Image.open(io.BytesIO(file.read())))
#     img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
#     dominant = extract_dominant_skin_colors(img_bgr)
#     return jsonify({"skin_colors": dominant.tolist()})

# if __name__ == "__main__":
#     app.run(debug=True)

# from flask import Flask
# from flask_cors import CORS

# from colorpalette import generate_palette
# from undertone import extract_dominant_skin_colors
# from web import extract_dominant_colors

# app = Flask(__name__)
# CORS(app)   # very important 🔥 for frontend → backend requests

# ---- test

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from web import extract_dominant_colors
# from undertone import extract_dominant_skin_colors
# from colorpalette import generate_palette
# import numpy as np
# import cv2
# from PIL import Image
# import io

# app = Flask(__name__)
# CORS(app)  # allow frontend to call backend

# @app.route("/health")
# def health():
#     return jsonify({"status": "Backend running"})

# # Upload + extract 3 dominant colors
# @app.route("/extract_colors", methods=["POST"])
# def extract_colors_route():
#     if "image" not in request.files:
#         return jsonify({"error": "No image uploaded"}), 400

#     image_file = request.files["image"]
#     img_arr = np.array(Image.open(io.BytesIO(image_file.read())))
#     img_cv = cv2.cvtColor(img_arr, cv2.COLOR_RGB2BGR)

#     colors = extract_dominant_colors(img_cv, num_colors=3)
#     return jsonify({"dominant_colors": colors})

# # Extract only SKIN tones
# @app.route("/extract_skin", methods=["POST"])
# def extract_skin_route():
#     if "image" not in request.files:
#         return jsonify({"error": "No image uploaded"}), 400

#     image_file = request.files["image"]
#     img_arr = np.array(Image.open(io.BytesIO(image_file.read())))
#     img_cv = cv2.cvtColor(img_arr, cv2.COLOR_RGB2BGR)

#     skin_colors = extract_dominant_skin_colors(img_cv)
#     return jsonify({
#         "skin_colors": skin_colors.tolist()
#     })

# # Generate palette
# @app.route("/palette", methods=["POST"])
# def palette_route():
#     data = request.json
#     base_color = data.get("base_color")
#     palette_type = data.get("palette_type", "complementary")

#     palette = generate_palette(base_color, palette_type)
#     return jsonify({"palette": palette})


# if __name__ == "__main__":
#     app.run(debug=True)


# --------------- TEST
# """
# ColorMe - Main Application Entry Point
# This is the main Flask application that serves the frontend and handles all API endpoints
# """

# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import os
# import sys

# # Add the logic folder to the Python path
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'logic'))

# # Import analysis modules
# try:
#     from colorpalette import determine_season, get_season_description, generate_palette, get_season_palette
#     from undertone import analyze_undertone, get_undertone_recommendations, analyze_detailed_undertone
# except ImportError as e:
#     print(f"Warning: Could not import analysis modules: {e}")
#     print("Make sure colorpalette.py and undertone.py are in the 'logic' folder")
    
#     # Provide fallback functions
#     def determine_season(skin_rgb, hair_rgb, eye_rgb):
#         return "Spring"
    
#     def get_season_description(season):
#         return {"characteristics": "Season analysis module not loaded"}
    
#     def analyze_undertone(skin_rgb):
#         return "warm"
    
#     def get_undertone_recommendations(undertone):
#         return {"jewelry": "Analysis module not loaded"}
    
#     def generate_palette(base_color, palette_type):
#         return ["#FF0000", "#00FF00", "#0000FF"]
    
#     def get_season_palette(season, base_color=None):
#         return ["#FF0000", "#00FF00", "#0000FF"]
    
#     def analyze_detailed_undertone(skin_rgb):
#         return {"undertone": "warm", "warm_percentage": 50, "cool_percentage": 30, "neutral_percentage": 20}

# app = Flask(__name__, static_folder='frontend', static_url_path='')
# CORS(app)  # Enable CORS for all routes

# def parse_rgb(rgb_string):
#     """Convert 'rgb(255, 255, 255)' to (255, 255, 255)"""
#     try:
#         rgb_string = rgb_string.replace('rgb(', '').replace(')', '').strip()
#         r, g, b = map(int, [x.strip() for x in rgb_string.split(',')])
#         return (r, g, b)
#     except Exception as e:
#         raise ValueError(f"Invalid RGB format: {rgb_string}")

# # ============ FRONTEND ROUTES ============

# @app.route('/')
# def index():
#     """Serve the main index.html page"""
#     return send_from_directory('frontend', 'index.html')

# @app.route('/<path:path>')
# def serve_static(path):
#     """Serve static files from the frontend folder"""
#     try:
#         return send_from_directory('frontend', path)
#     except:
#         # If file not found, return index.html for client-side routing
#         return send_from_directory('frontend', 'index.html')

# # ============ API ROUTES ============

# @app.route('/health', methods=['GET'])
# def health():
#     """Health check endpoint"""
#     return jsonify({
#         "status": "Backend running",
#         "version": "1.0.0",
#         "modules": {
#             "colorpalette": "loaded",
#             "undertone": "loaded"
#         }
#     })

# @app.route('/analyze', methods=['POST'])
# def analyze_colors():
#     """
#     Main color analysis endpoint
#     Receives skin, hair, and eye colors from the frontend
#     Returns seasonal analysis and undertone
#     """
#     try:
#         data = request.get_json()
        
#         if not data:
#             return jsonify({'error': 'No data provided'}), 400
        
#         # Get RGB colors from frontend
#         skin_color = data.get('skin')
#         hair_color = data.get('hair')
#         eye_color = data.get('eyes')
        
#         if not all([skin_color, hair_color, eye_color]):
#             return jsonify({'error': 'Missing color data. Please select all three colors.'}), 400
        
#         # Convert RGB strings to tuples
#         skin_rgb = parse_rgb(skin_color)
#         hair_rgb = parse_rgb(hair_color)
#         eye_rgb = parse_rgb(eye_color)
        
#         print(f"Analyzing colors - Skin: {skin_rgb}, Hair: {hair_rgb}, Eyes: {eye_rgb}")
        
#         # Perform analysis
#         season = determine_season(skin_rgb, hair_rgb, eye_rgb)
#         undertone = analyze_undertone(skin_rgb)
#         season_info = get_season_description(season)
#         undertone_info = get_undertone_recommendations(undertone)
#         detailed_undertone = analyze_detailed_undertone(skin_rgb)
        
#         # Generate recommended color palette
#         palette = get_season_palette(season, skin_rgb)
        
#         # Return comprehensive results
#         return jsonify({
#             'success': True,
#             'season': season,
#             'undertone': undertone,
#             'skin_rgb': skin_rgb,
#             'hair_rgb': hair_rgb,
#             'eye_rgb': eye_rgb,
#             'message': f'Your color season is {season} with {undertone} undertones!',
#             'season_info': {
#                 'characteristics': season_info.get('characteristics', ''),
#                 'best_colors': season_info.get('best_colors', []),
#                 'avoid_colors': season_info.get('avoid_colors', []),
#                 'metals': season_info.get('metals', ''),
#             },
#             'undertone_info': {
#                 'jewelry': undertone_info.get('jewelry', ''),
#                 'best_colors': undertone_info.get('best_colors', []),
#                 'makeup_tips': undertone_info.get('makeup_tips', []),
#             },
#             'detailed_undertone': detailed_undertone,
#             'recommended_palette': palette
#         })
        
#     except ValueError as e:
#         print(f"ValueError in analyze_colors: {str(e)}")
#         return jsonify({'error': f'Invalid color format: {str(e)}'}), 400
#     except Exception as e:
#         print(f"Error in analyze_colors: {str(e)}")
#         return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

# @app.route('/palette', methods=['POST'])
# def palette_route():
#     """
#     Generate color palette from a base color
#     Supports different palette types
#     """
#     try:
#         data = request.get_json()
        
#         base_color = data.get('base_color', [255, 0, 0])  # Default = red
#         palette_type = data.get('palette_type', 'complementary')
        
#         # Generate palette
#         palette = generate_palette(base_color, palette_type)
        
#         return jsonify({
#             "success": True,
#             "base_color": base_color,
#             "palette_type": palette_type,
#             "generated_palette": palette
#         })
        
#     except Exception as e:
#         print(f"Error in palette_route: {str(e)}")
#         return jsonify({"error": str(e)}), 400

# @app.route('/login', methods=['POST'])
# def login():
#     """Login endpoint - TODO: Implement proper authentication"""
#     try:
#         data = request.get_json()
#         username = data.get('username')
#         password = data.get('password')
        
#         # TODO: Add your authentication logic here
#         # For now, just a simple check
#         if username and password:
#             return jsonify({
#                 'success': True,
#                 'message': 'Login successful',
#                 'username': username
#             })
#         else:
#             return jsonify({
#                 'success': False,
#                 'message': 'Invalid credentials'
#             }), 401
            
#     except Exception as e:
#         print(f"Error in login: {str(e)}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/signup', methods=['POST'])
# def signup():
#     """Signup endpoint - TODO: Implement user registration"""
#     try:
#         data = request.get_json()
#         username = data.get('username')
#         password = data.get('password')
#         email = data.get('email')
        
#         # TODO: Add your user registration logic here
#         # - Validate input
#         # - Hash password
#         # - Store in database
        
#         if username and password and email:
#             return jsonify({
#                 'success': True,
#                 'message': 'Account created successfully',
#                 'username': username
#             })
#         else:
#             return jsonify({
#                 'success': False,
#                 'message': 'Missing required fields'
#             }), 400
            
#     except Exception as e:
#         print(f"Error in signup: {str(e)}")
#         return jsonify({'error': str(e)}), 500

# # Error handlers
# @app.errorhandler(404)
# def not_found(e):
#     """Handle 404 errors"""
#     return jsonify({'error': 'Resource not found'}), 404

# @app.errorhandler(500)
# def internal_error(e):
#     """Handle 500 errors"""
#     return jsonify({'error': 'Internal server error'}), 500

# if __name__ == '__main__':
#     # Check if frontend folder exists
#     if not os.path.exists('frontend'):
#         print("Warning: 'frontend' folder not found!")
#         print("Please make sure your HTML files are in a 'frontend' folder")
    
#     # Check if logic folder exists
#     if not os.path.exists('logic'):
#         print("Warning: 'logic' folder not found!")
#         print("Please make sure colorpalette.py and undertone.py are in a 'logic' folder")
    
#     print("\n" + "="*50)
#     print("ColorMe Application Starting...")
#     print("="*50)
#     print("Frontend: http://localhost:5000")
#     print("API Endpoints:")
#     print("  - GET  /health")
#     print("  - POST /analyze")
#     print("  - POST /palette")
#     print("  - POST /login")
#     print("  - POST /signup")
#     print("="*50 + "\n")
    
#     # Run the Flask app
#     app.run(debug=True, port=5001, host='0.0.0.0')



# -------- RECENT TEST
# """
# ColorMe - Main Application Entry Point
# This is the main Flask application that serves the frontend and handles all API endpoints
# """

# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import os
# import sys

# # Add the logic folder to the Python path
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'logic'))

# # Import analysis modules
# try:
#     from colorpalette import determine_season, get_season_description, generate_palette, get_season_palette
#     from undertone import analyze_undertone, get_undertone_recommendations, analyze_detailed_undertone
# except ImportError as e:
#     print(f"Warning: Could not import analysis modules: {e}")
#     print("Make sure colorpalette.py and undertone.py are in the 'logic' folder")
    
#     # Provide fallback functions
#     def determine_season(skin_rgb, hair_rgb, eye_rgb):
#         return "Spring"
    
#     def get_season_description(season):
#         return {"characteristics": "Season analysis module not loaded"}
    
#     def analyze_undertone(skin_rgb):
#         return "warm"
    
#     def get_undertone_recommendations(undertone):
#         return {"jewelry": "Analysis module not loaded"}
    
#     def generate_palette(base_color, palette_type):
#         return ["#FF0000", "#00FF00", "#0000FF"]
    
#     def get_season_palette(season, base_color=None):
#         return ["#FF0000", "#00FF00", "#0000FF"]
    
#     def analyze_detailed_undertone(skin_rgb):
#         return {"undertone": "warm", "warm_percentage": 50, "cool_percentage": 30, "neutral_percentage": 20}

# app = Flask(__name__, static_folder='frontend', static_url_path='')
# CORS(app)  # Enable CORS for all routes

# def parse_rgb(rgb_string):
#     """Convert 'rgb(255, 255, 255)' to (255, 255, 255)"""
#     try:
#         rgb_string = rgb_string.replace('rgb(', '').replace(')', '').strip()
#         r, g, b = map(int, [x.strip() for x in rgb_string.split(',')])
#         return (r, g, b)
#     except Exception as e:
#         raise ValueError(f"Invalid RGB format: {rgb_string}")

# # ============ FRONTEND ROUTES ============

# @app.route('/')
# def index():
#     """Serve the main index.html page"""
#     return send_from_directory('frontend', 'index.html')

# @app.route('/<path:path>')
# def serve_static(path):
#     """Serve static files from the frontend folder"""
#     try:
#         return send_from_directory('frontend', path)
#     except:
#         # If file not found, return index.html for client-side routing
#         return send_from_directory('frontend', 'index.html')

# # ============ API ROUTES ============

# @app.route('/health', methods=['GET'])
# def health():
#     """Health check endpoint"""
#     return jsonify({
#         "status": "Backend running",
#         "version": "1.0.0",
#         "modules": {
#             "colorpalette": "loaded",
#             "undertone": "loaded"
#         }
#     })

# @app.route('/analyze', methods=['POST'])
# def analyze_colors():
#     """
#     Main color analysis endpoint
#     Receives skin, hair, and eye colors from the frontend
#     Returns seasonal analysis and undertone
#     """
#     try:
#         data = request.get_json()
        
#         if not data:
#             return jsonify({'error': 'No data provided'}), 400
        
#         # Get RGB colors from frontend
#         skin_color = data.get('skin')
#         hair_color = data.get('hair')
#         eye_color = data.get('eyes')
        
#         if not all([skin_color, hair_color, eye_color]):
#             return jsonify({'error': 'Missing color data. Please select all three colors.'}), 400
        
#         # Convert RGB strings to tuples
#         skin_rgb = parse_rgb(skin_color)
#         hair_rgb = parse_rgb(hair_color)
#         eye_rgb = parse_rgb(eye_color)
        
#         print("\n" + "="*60)
#         print("🎨 COLOR ANALYSIS DEBUG")
#         print("="*60)
#         print(f"Input Colors:")
#         print(f"  Skin RGB:  {skin_rgb}")
#         print(f"  Hair RGB:  {hair_rgb}")
#         print(f"  Eye RGB:   {eye_rgb}")
        
#         # Perform analysis
#         season = determine_season(skin_rgb, hair_rgb, eye_rgb)
#         undertone = analyze_undertone(skin_rgb)
#         season_info = get_season_description(season)
#         undertone_info = get_undertone_recommendations(undertone)
#         detailed_undertone = analyze_detailed_undertone(skin_rgb)
        
#         print(f"\nResults:")
#         print(f"  Season:    {season}")
#         print(f"  Undertone: {undertone}")
#         print(f"  Breakdown: Warm {detailed_undertone['warm_percentage']}%, "
#               f"Cool {detailed_undertone['cool_percentage']}%, "
#               f"Neutral {detailed_undertone['neutral_percentage']}%")
#         print("="*60 + "\n")
        
#         # Generate recommended color palette
#         palette = get_season_palette(season, skin_rgb)
        
#         # Return comprehensive results
#         return jsonify({
#             'success': True,
#             'season': season,
#             'undertone': undertone,
#             'skin_rgb': skin_rgb,
#             'hair_rgb': hair_rgb,
#             'eye_rgb': eye_rgb,
#             'message': f'Your color season is {season} with {undertone} undertones!',
#             'season_info': {
#                 'characteristics': season_info.get('characteristics', ''),
#                 'best_colors': season_info.get('best_colors', []),
#                 'avoid_colors': season_info.get('avoid_colors', []),
#                 'metals': season_info.get('metals', ''),
#             },
#             'undertone_info': {
#                 'jewelry': undertone_info.get('jewelry', ''),
#                 'best_colors': undertone_info.get('best_colors', []),
#                 'makeup_tips': undertone_info.get('makeup_tips', []),
#             },
#             'detailed_undertone': detailed_undertone,
#             'recommended_palette': palette
#         })
        
#     except ValueError as e:
#         print(f"ValueError in analyze_colors: {str(e)}")
#         return jsonify({'error': f'Invalid color format: {str(e)}'}), 400
#     except Exception as e:
#         print(f"Error in analyze_colors: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

# @app.route('/palette', methods=['POST'])
# def palette_route():
#     """
#     Generate color palette from a base color
#     Supports different palette types
#     """
#     try:
#         data = request.get_json()
        
#         base_color = data.get('base_color', [255, 0, 0])  # Default = red
#         palette_type = data.get('palette_type', 'complementary')
        
#         # Generate palette
#         palette = generate_palette(base_color, palette_type)
        
#         return jsonify({
#             "success": True,
#             "base_color": base_color,
#             "palette_type": palette_type,
#             "generated_palette": palette
#         })
        
#     except Exception as e:
#         print(f"Error in palette_route: {str(e)}")
#         return jsonify({"error": str(e)}), 400

# @app.route('/login', methods=['POST'])
# def login():
#     """Login endpoint - TODO: Implement proper authentication"""
#     try:
#         data = request.get_json()
#         username = data.get('username')
#         password = data.get('password')
        
#         # TODO: Add your authentication logic here
#         # For now, just a simple check
#         if username and password:
#             return jsonify({
#                 'success': True,
#                 'message': 'Login successful',
#                 'username': username
#             })
#         else:
#             return jsonify({
#                 'success': False,
#                 'message': 'Invalid credentials'
#             }), 401
            
#     except Exception as e:
#         print(f"Error in login: {str(e)}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/signup', methods=['POST'])
# def signup():
#     """Signup endpoint - TODO: Implement user registration"""
#     try:
#         data = request.get_json()
#         username = data.get('username')
#         password = data.get('password')
#         email = data.get('email')
        
#         # TODO: Add your user registration logic here
#         # - Validate input
#         # - Hash password
#         # - Store in database
        
#         if username and password and email:
#             return jsonify({
#                 'success': True,
#                 'message': 'Account created successfully',
#                 'username': username
#             })
#         else:
#             return jsonify({
#                 'success': False,
#                 'message': 'Missing required fields'
#             }), 400
            
#     except Exception as e:
#         print(f"Error in signup: {str(e)}")
#         return jsonify({'error': str(e)}), 500

# # Error handlers
# @app.errorhandler(404)
# def not_found(e):
#     """Handle 404 errors"""
#     return jsonify({'error': 'Resource not found'}), 404

# @app.errorhandler(500)
# def internal_error(e):
#     """Handle 500 errors"""
#     return jsonify({'error': 'Internal server error'}), 500

# if __name__ == '__main__':
#     # Check if frontend folder exists
#     if not os.path.exists('frontend'):
#         print("Warning: 'frontend' folder not found!")
#         print("Please make sure your HTML files are in a 'frontend' folder")
    
#     # Check if logic folder exists
#     if not os.path.exists('logic'):
#         print("Warning: 'logic' folder not found!")
#         print("Please make sure colorpalette.py and undertone.py are in a 'logic' folder")
    
#     print("\n" + "="*50)
#     print("ColorMe Application Starting...")
#     print("="*50)
#     print("Frontend: http://localhost:5000")
#     print("API Endpoints:")
#     print("  - GET  /health")
#     print("  - POST /analyze")
#     print("  - POST /palette")
#     print("  - POST /login")
#     print("  - POST /signup")
#     print("="*50 + "\n")
    
#     # Run the Flask app
#     app.run(debug=True, port=5001, host='0.0.0.0')
"""
ColorMe - Main Application Entry Point
This is the main Flask application that serves the frontend and handles all API endpoints
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

# Add the logic folder to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'logic'))

# Import analysis modules
try:
    from colorpalette import determine_season, get_season_description, generate_palette, get_season_palette
    from undertone import analyze_undertone, get_undertone_recommendations, analyze_detailed_undertone
except ImportError as e:
    print(f"Warning: Could not import analysis modules: {e}")
    print("Make sure colorpalette.py and undertone.py are in the 'logic' folder")
    
    # Provide fallback functions
    def determine_season(skin_rgb, hair_rgb, eye_rgb):
        return "Spring"
    
    def get_season_description(season):
        return {"characteristics": "Season analysis module not loaded"}
    
    def analyze_undertone(skin_rgb):
        return "warm"
    
    def get_undertone_recommendations(undertone):
        return {"jewelry": "Analysis module not loaded"}
    
    def generate_palette(base_color, palette_type):
        return ["#FF0000", "#00FF00", "#0000FF"]
    
    def get_season_palette(season, base_color=None):
        return ["#FF0000", "#00FF00", "#0000FF"]
    
    def analyze_detailed_undertone(skin_rgb):
        return {"undertone": "warm", "warm_percentage": 50, "cool_percentage": 30, "neutral_percentage": 20}

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)  # Enable CORS for all routes

def parse_rgb(rgb_string):
    """Convert 'rgb(255, 255, 255)' to (255, 255, 255)"""
    try:
        rgb_string = rgb_string.replace('rgb(', '').replace(')', '').strip()
        r, g, b = map(int, [x.strip() for x in rgb_string.split(',')])
        return (r, g, b)
    except Exception as e:
        raise ValueError(f"Invalid RGB format: {rgb_string}")

# ============ FRONTEND ROUTES ============

@app.route('/')
def index():
    """Serve the main index.html page"""
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from the frontend folder"""
    try:
        return send_from_directory('frontend', path)
    except:
        # If file not found, return index.html for client-side routing
        return send_from_directory('frontend', 'index.html')

# ============ API ROUTES ============

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "Backend running",
        "version": "1.0.0",
        "modules": {
            "colorpalette": "loaded",
            "undertone": "loaded"
        }
    })

@app.route('/analyze', methods=['POST'])
def analyze_colors():
    """
    Main color analysis endpoint
    Receives skin, hair, and eye colors from the frontend
    Returns seasonal analysis and undertone
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Get RGB colors from frontend
        skin_color = data.get('skin')
        hair_color = data.get('hair')
        eye_color = data.get('eyes')
        
        if not all([skin_color, hair_color, eye_color]):
            return jsonify({'error': 'Missing color data. Please select all three colors.'}), 400
        
        # Convert RGB strings to tuples
        skin_rgb = parse_rgb(skin_color)
        hair_rgb = parse_rgb(hair_color)
        eye_rgb = parse_rgb(eye_color)
        
        # Calculate some debug values
        from colorpalette import rgb_to_hsv, calculate_contrast
        skin_hsv = rgb_to_hsv(skin_rgb)
        hair_hsv = rgb_to_hsv(hair_rgb)
        contrast_skin_hair = calculate_contrast(skin_rgb, hair_rgb)
        
        print("\n" + "="*60)
        print("🎨 COLOR ANALYSIS DEBUG")
        print("="*60)
        print(f"Input Colors:")
        print(f"  Skin RGB:  {skin_rgb} (Brightness: {skin_hsv[2]:.2f})")
        print(f"  Hair RGB:  {hair_rgb} (Brightness: {hair_hsv[2]:.2f})")
        print(f"  Eye RGB:   {eye_rgb}")
        print(f"\nAnalysis Factors:")
        print(f"  Skin-Hair Contrast: {contrast_skin_hair:.3f}")
        print(f"  Warm Score: {((skin_rgb[0] + skin_rgb[1])/2 - skin_rgb[2])/255:.3f}")
        print(f"  Hair Darkness: {'Very Dark' if hair_hsv[2] < 0.25 else 'Dark' if hair_hsv[2] < 0.35 else 'Medium' if hair_hsv[2] < 0.55 else 'Light'}")
        
        # Perform analysis
        season = determine_season(skin_rgb, hair_rgb, eye_rgb)
        undertone = analyze_undertone(skin_rgb)
        
        # CRITICAL: Season ALWAYS determines undertone in 12-season system
        # Winter/Summer = Cool undertones ALWAYS
        # Spring/Autumn = Warm undertones ALWAYS
        
        if "Winter" in season or "Summer" in season:
            # Cool seasons MUST have cool undertones
            original_undertone = undertone
            undertone = "cool"
            if original_undertone != "cool":
                print(f"  → Undertone FORCED to 'cool' for {season} (was {original_undertone})")
        
        elif "Spring" in season or "Autumn" in season:
            # Warm seasons MUST have warm undertones
            original_undertone = undertone
            undertone = "warm"
            if original_undertone != "warm":
                print(f"  → Undertone FORCED to 'warm' for {season} (was {original_undertone})")
        
        season_info = get_season_description(season)
        undertone_info = get_undertone_recommendations(undertone)
        detailed_undertone = analyze_detailed_undertone(skin_rgb)
        
        print(f"\nResults:")
        print(f"  Season:    {season}")
        print(f"  Undertone: {undertone}")
        print(f"  Breakdown: Warm {detailed_undertone['warm_percentage']}%, "
              f"Cool {detailed_undertone['cool_percentage']}%, "
              f"Neutral {detailed_undertone['neutral_percentage']}%")
        print("="*60 + "\n")
        
        # Generate recommended color palette
        palette = get_season_palette(season, skin_rgb)
        
        # Return comprehensive results
        return jsonify({
            'success': True,
            'season': season,
            'undertone': undertone,
            'skin_rgb': skin_rgb,
            'hair_rgb': hair_rgb,
            'eye_rgb': eye_rgb,
            'message': f'Your color season is {season} with {undertone} undertones!',
            'season_info': {
                'characteristics': season_info.get('characteristics', ''),
                'best_colors': season_info.get('best_colors', []),
                'avoid_colors': season_info.get('avoid_colors', []),
                'metals': season_info.get('metals', ''),
            },
            'undertone_info': {
                'jewelry': undertone_info.get('jewelry', ''),
                'best_colors': undertone_info.get('best_colors', []),
                'makeup_tips': undertone_info.get('makeup_tips', []),
            },
            'detailed_undertone': detailed_undertone,
            'recommended_palette': palette
        })
        
    except ValueError as e:
        print(f"ValueError in analyze_colors: {str(e)}")
        return jsonify({'error': f'Invalid color format: {str(e)}'}), 400
    except Exception as e:
        print(f"Error in analyze_colors: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/palette', methods=['POST'])
def palette_route():
    """
    Generate color palette from a base color
    Supports different palette types
    """
    try:
        data = request.get_json()
        
        base_color = data.get('base_color', [255, 0, 0])  # Default = red
        palette_type = data.get('palette_type', 'complementary')
        
        # Generate palette
        palette = generate_palette(base_color, palette_type)
        
        return jsonify({
            "success": True,
            "base_color": base_color,
            "palette_type": palette_type,
            "generated_palette": palette
        })
        
    except Exception as e:
        print(f"Error in palette_route: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    """Login endpoint - TODO: Implement proper authentication"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # TODO: Add your authentication logic here
        # For now, just a simple check
        if username and password:
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'username': username
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
            
    except Exception as e:
        print(f"Error in login: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/signup', methods=['POST'])
def signup():
    """Signup endpoint - TODO: Implement user registration"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        # TODO: Add your user registration logic here
        # - Validate input
        # - Hash password
        # - Store in database
        
        if username and password and email:
            return jsonify({
                'success': True,
                'message': 'Account created successfully',
                'username': username
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
            
    except Exception as e:
        print(f"Error in signup: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Check if frontend folder exists
    if not os.path.exists('frontend'):
        print("Warning: 'frontend' folder not found!")
        print("Please make sure your HTML files are in a 'frontend' folder")
    
    # Check if logic folder exists
    if not os.path.exists('logic'):
        print("Warning: 'logic' folder not found!")
        print("Please make sure colorpalette.py and undertone.py are in a 'logic' folder")
    
    print("\n" + "="*50)
    print("ColorMe Application Starting...")
    print("="*50)
    print("Frontend: http://localhost:5000")
    print("API Endpoints:")
    print("  - GET  /health")
    print("  - POST /analyze")
    print("  - POST /palette")
    print("  - POST /login")
    print("  - POST /signup")
    print("="*50 + "\n")
    
    # Run the Flask app
    app.run(debug=True, port=5001, host='0.0.0.0')