from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash
from app.forms.upload_form import UploadForm
from app.forms.train_form import TrainForm
from werkzeug.utils import secure_filename
import os
import requests
import json

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def index():
    """Render the home page"""
    return render_template('index.html')

@frontend_bp.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """Page for analyzing emails"""
    form = UploadForm()
    result = None
    
    if form.validate_on_submit():
        if form.email_file.data:
            # Handle file upload
            file = form.email_file.data
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Make API call to our own backend
            files = {'file': open(file_path, 'rb')}
            response = requests.post(f"{request.url_root}api/upload", files=files)
            
            if response.status_code == 200:
                result = response.json()
            else:
                flash(f"Error: {response.text}", 'danger')
        
        elif form.email_content.data:
            # Handle text input
            data = {'email_content': form.email_content.data}
            response = requests.post(f"{request.url_root}api/detect", json=data)
            
            if response.status_code == 200:
                result = response.json()
            else:
                flash(f"Error: {response.text}", 'danger')
    
    return render_template('analyze.html', form=form, result=result)

@frontend_bp.route('/train', methods=['GET', 'POST'])
def train():
    """Page for training the model"""
    form = TrainForm()
    result = None
    
    if form.validate_on_submit():
        data = {
            'dataset_path': form.dataset_path.data,
            'test_size': form.test_size.data,
            'random_state': form.random_state.data
        }
        
        response = requests.post(f"{request.url_root}api/train", json=data)
        
        if response.status_code == 200:
            result = response.json()
            flash("Model trained successfully!", 'success')
        else:
            flash(f"Error: {response.text}", 'danger')
    
    # Get model info
    try:
        model_info_response = requests.get(f"{request.url_root}api/model-info")
        model_info = model_info_response.json()
    except:
        model_info = {'model_loaded': False}
    
    return render_template('train.html', form=form, result=result, model_info=model_info)

@frontend_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')