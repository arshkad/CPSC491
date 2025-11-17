# from flask import Flask, request, jsonify
# import colorsys
# import numpy as np

# app = Flask(__name__)

# # Convert HEX <-> RGB
# def hex_to_rgb(hex_color):
#     hex_color = hex_color.lstrip('#')
#     return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# def rgb_to_hex(rgb):
#     return '#%02x%02x%02x' % tuple(int(x) for x in rgb)

# # Rotate hue (in HSV space)
# def adjust_hue(rgb, degree_shift):
#    r, g, b = [x/255.0 for x in rgb]
#    h, s, v = colorsys.rgb_to_hsv(r, g, b)
#    h = (h + degree_shift / 360.0) % 1.0
#    r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v)
#    return [r2 * 255, g2 * 255, b2 * 255]


# # Generate palette from one color
# def generate_palette(base_color, palette_type="complementary"):
#    """
#    palette_type: 'complementary', 'analogous', 'triadic', 'monochromatic', 'split_complementary'
#    base_color: [R, G, B] or '#RRGGBB'
#    """
#    if isinstance(base_color, str):
#        base_rgb = np.array(hex_to_rgb(base_color))
#    else:
#        base_rgb = np.array(base_color)


#    palette = []


#    if palette_type == "complementary":
#        palette = [base_rgb, adjust_hue(base_rgb, 180)]
#    elif palette_type == "analogous":
#        palette = [adjust_hue(base_rgb, -30), base_rgb, adjust_hue(base_rgb, 30)]
#    elif palette_type == "triadic":
#        palette = [base_rgb, adjust_hue(base_rgb, 120), adjust_hue(base_rgb, 240)]
#    elif palette_type == "split_complementary":
#        palette = [base_rgb, adjust_hue(base_rgb, 150), adjust_hue(base_rgb, 210)]
#    elif palette_type == "monochromatic":
#        # Generate lighter/darker variations of the same hue
#        r, g, b = base_rgb
#        for factor in [0.5, 0.75, 1.0, 1.25, 1.5]:
#            new_color = np.clip(base_rgb * factor, 0, 255)
#            palette.append(new_color)
#    else:
#        raise ValueError("Palette type not specified.") 

# # Convert to HEX for frontend readability
#    palette_hex = [rgb_to_hex(color) for color in palette]
#    return palette_hex


# # Flask Route: /palette
# @app.route('/palette', methods=['POST'])
# def palette_route():
#    data = request.get_json()


#    base_color = data.get('base_color', [255, 0, 0])  # Default = red
#    palette_type = data.get('palette_type', 'complementary')


#    try:
#        palette = generate_palette(base_color, palette_type)
#        return jsonify({
#            "base_color": base_color,
#            "palette_type": palette_type,
#            "generated_palette": palette
#        })
#    except Exception as e:
#        return jsonify({"error": str(e)}), 400


# if __name__ == '__main__':
#    app.run(debug=True)

# ----------- TEST

"""
Color Palette and Season Analysis Module
Combines color palette generation with seasonal color analysis
"""

import colorsys
import numpy as np

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

    # Convert to HEX for frontend readability
    palette_hex = [rgb_to_hex(color) for color in palette]
    return palette_hex

# ========== SEASONAL COLOR ANALYSIS FUNCTIONS ==========

def rgb_to_hsv(rgb):
    """Convert RGB tuple to HSV"""
    r, g, b = [x / 255.0 for x in rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return (h * 360, s, v)  # Return hue in degrees

def calculate_contrast(color1_rgb, color2_rgb):
    """Calculate contrast between two colors"""
    def luminance(rgb):
        r, g, b = [x / 255.0 for x in rgb]
        return 0.299 * r + 0.587 * g + 0.114 * b
    
    lum1 = luminance(color1_rgb)
    lum2 = luminance(color2_rgb)
    
    return abs(lum1 - lum2)

def determine_season(skin_rgb, hair_rgb, eye_rgb):
    """
    Determine color season based on skin, hair, and eye colors
    Returns: 'Spring', 'Summer', 'Autumn', or 'Winter'
    
    Theory:
    - Spring: Warm, bright, clear colors (warm undertone, high contrast)
    - Summer: Cool, soft, muted colors (cool undertone, low contrast)
    - Autumn: Warm, deep, muted colors (warm undertone, low-medium contrast)
    - Winter: Cool, bright, clear colors (cool undertone, high contrast)
    """
    
    # Convert to HSV for better color analysis
    skin_hsv = rgb_to_hsv(skin_rgb)
    hair_hsv = rgb_to_hsv(hair_rgb)
    eye_hsv = rgb_to_hsv(eye_rgb)
    
    # Analyze skin undertone
    skin_r, skin_g, skin_b = skin_rgb
    
    # Warm undertone indicators: more red/yellow
    # Cool undertone indicators: more blue/pink
    warm_score = (skin_r - skin_b) / 255.0  # Positive = warm, negative = cool
    
    # Calculate overall saturation (color intensity)
    avg_saturation = (skin_hsv[1] + hair_hsv[1] + eye_hsv[1]) / 3
    
    # Calculate contrast between features
    contrast_skin_hair = calculate_contrast(skin_rgb, hair_rgb)
    contrast_skin_eye = calculate_contrast(skin_rgb, eye_rgb)
    overall_contrast = (contrast_skin_hair + contrast_skin_eye) / 2
    
    # Calculate brightness
    skin_brightness = skin_hsv[2]
    hair_brightness = hair_hsv[2]
    
    # Decision tree for season determination
    is_warm = warm_score > 0.05  # Warm undertone
    is_high_contrast = overall_contrast > 0.3
    is_bright = avg_saturation > 0.4 or skin_brightness > 0.6
    
    # Determine season
    if is_warm:
        if is_high_contrast and is_bright:
            return "Spring"
        else:
            return "Autumn"
    else:  # Cool
        if is_high_contrast and is_bright:
            return "Winter"
        else:
            return "Summer"

def get_season_description(season):
    """Get detailed description of each season's characteristics"""
    descriptions = {
        "Spring": {
            "colors": ["Warm, clear, bright colors", "Peachy pinks", "Coral", "Golden yellow", "Bright green"],
            "best_colors": ["Peach", "Coral", "Golden yellow", "Warm pink", "Turquoise", "Light orange"],
            "avoid_colors": ["Black", "Pure white", "Dark navy", "Burgundy"],
            "metals": "Gold jewelry suits you best",
            "characteristics": "Warm undertone with bright, clear coloring",
            "palette_type": "analogous"
        },
        "Summer": {
            "colors": ["Cool, soft, muted colors", "Rose pink", "Lavender", "Soft blue", "Mauve"],
            "best_colors": ["Soft pink", "Lavender", "Powder blue", "Rose", "Soft white", "Light gray"],
            "avoid_colors": ["Orange", "Bright yellow", "True black"],
            "metals": "Silver jewelry suits you best",
            "characteristics": "Cool undertone with soft, muted coloring",
            "palette_type": "monochromatic"
        },
        "Autumn": {
            "colors": ["Warm, deep, muted colors", "Rust", "Olive green", "Camel", "Deep orange"],
            "best_colors": ["Rust", "Olive", "Camel", "Warm brown", "Terracotta", "Forest green"],
            "avoid_colors": ["Pastel colors", "Cool pinks", "Bright white"],
            "metals": "Gold jewelry suits you best",
            "characteristics": "Warm undertone with rich, earthy coloring",
            "palette_type": "analogous"
        },
        "Winter": {
            "colors": ["Cool, bright, clear colors", "True red", "Navy blue", "Pure white", "Hot pink"],
            "best_colors": ["True red", "Royal blue", "Pure white", "Black", "Hot pink", "Emerald green"],
            "avoid_colors": ["Orange", "Gold", "Warm browns"],
            "metals": "Silver jewelry suits you best",
            "characteristics": "Cool undertone with high contrast coloring",
            "palette_type": "complementary"
        }
    }
    return descriptions.get(season, {})

def get_season_palette(season, base_color=None):
    """
    Generate a color palette suitable for the given season
    Returns hex color codes
    """
    season_colors = {
        "Spring": ["#FFB6C1", "#FF7F50", "#FFD700", "#98FB98", "#87CEEB"],
        "Summer": ["#E6B8E6", "#B0C4DE", "#FFB6C1", "#D8BFD8", "#F5F5DC"],
        "Autumn": ["#CD853F", "#808000", "#D2691E", "#8B4513", "#556B2F"],
        "Winter": ["#FF0000", "#000080", "#FFFFFF", "#FF1493", "#50C878"]
    }
    
    # If a base color is provided, generate a palette based on season's recommended type
    if base_color:
        season_info = get_season_description(season)
        palette_type = season_info.get("palette_type", "complementary")
        return generate_palette(base_color, palette_type)
    
    return season_colors.get(season, season_colors["Spring"])

# Example usage and testing
if __name__ == "__main__":
    # Test seasonal analysis
    print("=== Testing Seasonal Color Analysis ===")
    
    test_cases = [
        ((220, 180, 150), (50, 30, 20), (100, 80, 60), "Light peachy skin, dark hair, brown eyes"),
        ((240, 220, 210), (200, 180, 150), (150, 180, 200), "Light cool skin, light hair, blue eyes"),
        ((180, 140, 110), (70, 40, 20), (80, 60, 40), "Medium warm skin, dark hair, brown eyes"),
        ((200, 190, 190), (40, 40, 50), (100, 120, 140), "Light cool skin, dark hair, blue eyes")
    ]
    
    for skin, hair, eyes, description in test_cases:
        season = determine_season(skin, hair, eyes)
        print(f"\n{description}")
        print(f"RGB - Skin: {skin}, Hair: {hair}, Eyes: {eyes}")
        print(f"Season: {season}")
        print(f"Characteristics: {get_season_description(season)['characteristics']}")
        print(f"Best metals: {get_season_description(season)['metals']}")
    
    # Test palette generation
    print("\n\n=== Testing Palette Generation ===")
    base_color = [255, 100, 100]
    for palette_type in ["complementary", "analogous", "triadic", "monochromatic"]:
        palette = generate_palette(base_color, palette_type)
        print(f"\n{palette_type.title()}: {palette}")