# ColorMe - AI-Powered Personal Color Analysis
An AI-powered web application that analyzes your face and skin tone to provide personalized color recommendations for clothing, jewelry, and styling choices.

✨ Features
- AI-powered face detection using MediaPipe
- Skin tone analysis with K-means clustering
- Seasonal color analysis (Spring, Summer, Autumn, Winter)
- Undertone detection (warm, cool, neutral)
- Personalized color palettes and styling tips
- User authentication and analysis history
- Interactive dashboard with saved results

🛠️ Technology Stack
- Frontend: HTML5, CSS3, JavaScript
- Backend: Python 3.8+, Flask, Flask-CORS
- AI/ML: MediaPipe, OpenCV, NumPy, scikit-learn
- Authentication: Werkzeug, PyJWT

📦 Prerequisites
Python 3.8 or higher
pip (Python package installer)

# Run on Visual Studio Code

# Start server
python (or python3) app.py
Expected Output:
==================================================
ColorMe Application Starting...
==================================================
Frontend: http://localhost:5001
 * Running on http://127.0.0.1:5001
3. Open in Browser
Navigate to: http://localhost:5001
4. Test the Application

Upload a clear, front-facing photo
Click Skin, Hair, Eyes circles, then click colors in your photo
Click "Analyze My Colors"
View your season, undertone, and color recommendations
Sign up to save results and access dashboard

5. Stop Server
Press Ctrl + C in terminal

# Example Output
python3 app.py                                                                  
✓ Successfully imported colorpalette and undertone modules

==================================================
ColorMe Application Starting...
==================================================
Frontend: http://localhost:5001
API Endpoints:
  - GET  /health
  - POST /analyze
  - POST /palette
  - POST /login
  - POST /signup
  - POST /user/results
  - POST /user/save-result
  - POST /get-user-info
  - POST /update-password
==================================================

 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
 * Running on http://192.168.1.122:5001
Press CTRL+C to quit