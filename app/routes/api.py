from flask import Blueprint, request, jsonify, current_app
from app.ml.model import PhishingDetector
import os
import json
from werkzeug.utils import secure_filename
from app.utils.email_parser import parse_email_content

api_bp = Blueprint('api', __name__)
detector = None

# Initialize the model on first request
@api_bp.before_app_first_request
def load_model():
    global detector
    try:
        if os.path.exists(current_app.config['MODEL_PATH']) and os.path.exists(current_app.config['VECTORIZER_PATH']):
            detector = PhishingDetector()
            detector.load_model(current_app.config['MODEL_PATH'], current_app.config['VECTORIZER_PATH'])
        else:
            # No pre-trained model exists yet
            detector = PhishingDetector()
    except Exception as e:
        print(f"Error loading model: {e}")
        detector = PhishingDetector()

@api_bp.route('/detect', methods=['POST'])
def detect_phishing():
    """Endpoint to detect phishing in email content"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    if 'email_content' not in data:
        return jsonify({"error": "Missing email_content field"}), 400
    
    email_content = data['email_content']
    
    # Parse the email to extract features
    email_features = parse_email_content(email_content)
    
    # Make prediction
    if detector and hasattr(detector, 'model') and detector.model is not None:
        prediction, confidence, explanation = detector.predict(email_features)
        return jsonify({
            "is_phishing": bool(prediction),
            "confidence": float(confidence),
            "explanation": explanation
        })
    else:
        return jsonify({"error": "Model not loaded or not trained yet"}), 503

@api_bp.route('/upload', methods=['POST'])
def upload_email():
    """Endpoint to upload an email file for analysis"""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Read and analyze the email
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            email_content = f.read()
        
        # Parse the email
        email_features = parse_email_content(email_content)
        
        # Make prediction if model is loaded
        if detector and hasattr(detector, 'model') and detector.model is not None:
            prediction, confidence, explanation = detector.predict(email_features)
            return jsonify({
                "is_phishing": bool(prediction),
                "confidence": float(confidence),
                "explanation": explanation,
                "filename": filename
            })
        else:
            return jsonify({"error": "Model not loaded or not trained yet"}), 503

@api_bp.route('/train', methods=['POST'])
def train_model():
    """Endpoint to train the model with new data"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    if 'dataset_path' not in data:
        return jsonify({"error": "Missing dataset_path field"}), 400
    
    dataset_path = data['dataset_path']
    
    # Optional parameters
    test_size = data.get('test_size', 0.2)
    random_state = data.get('random_state', 42)
    
    try:
        global detector
        if detector is None:
            detector = PhishingDetector()
        
        # Train the model
        metrics = detector.train(dataset_path, test_size, random_state)
        
        # Save the model
        detector.save_model(current_app.config['MODEL_PATH'], current_app.config['VECTORIZER_PATH'])
        
        return jsonify({
            "success": True,
            "message": "Model trained successfully",
            "metrics": metrics
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/model-info', methods=['GET'])
def model_info():
    """Endpoint to get information about the current model"""
    if detector and hasattr(detector, 'model') and detector.model is not None:
        return jsonify({
            "model_loaded": True,
            "model_type": detector.model.__class__.__name__,
            "feature_count": detector.vectorizer.get_feature_names_out().shape[0] if hasattr(detector, 'vectorizer') else None,
            "last_trained": os.path.getmtime(current_app.config['MODEL_PATH']) if os.path.exists(current_app.config['MODEL_PATH']) else None
        })
    else:
        return jsonify({"model_loaded": False})