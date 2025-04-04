

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS  # Added CORS import
import pandas as pd
import os
import numpy as np

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)  # This enables CORS for all routes

# Custom JSON encoder to handle NaN values
def handle_nans(obj):
    if isinstance(obj, (float, np.floating)):
        return None if pd.isna(obj) else obj
    elif isinstance(obj, (list, tuple)):
        return [handle_nans(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: handle_nans(v) for k, v in obj.items()}
    return obj

# Load the dataset
try:
    csv_path = os.path.join(os.path.dirname(__file__), 'kindle_data-v2.csv')
    print(f"Loading CSV from: {csv_path}")
    
    df = pd.read_csv(csv_path)
    df = df.where(pd.notnull(df), None)
    print(f"Successfully loaded {len(df)} records")
except Exception as e:
    print(f"Error loading dataset: {str(e)}")
    df = pd.DataFrame()

@app.route('/')
def home():
    return render_template('index.html')

# Route for about page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api/books')
def get_books():
    if df.empty:
        return jsonify({"error": "Dataset not loaded"}), 500
    
    try:
        # Return all books without pagination or sorting
        return jsonify({
            "books": handle_nans(df.to_dict('records')),
            "total": len(df)
        })
    except Exception as e:
        print(f"API Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Run the app
    app.run(debug=True, port=5000, host='0.0.0.0')

