import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import joblib
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PhishingDetector:
    """Class for detecting phishing emails using ML"""
    
    def __init__(self):
        """Initialize the phishing detector"""
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.model = None
        self.feature_importance = None
    
    def load_model(self, model_path, vectorizer_path):
        """Load a pre-trained model and vectorizer"""
        try:
            self.model = joblib.load(model_path)
            self.vectorizer = joblib.load(vectorizer_path)
            logger.info("Model and vectorizer loaded successfully")
            
            # Store feature importance for explanation
            if hasattr(self.model, 'feature_importances_'):
                self.feature_importance = dict(zip(
                    self.vectorizer.get_feature_names_out(),
                    self.model.feature_importances_
                ))
                
            return True
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False
    
    def save_model(self, model_path, vectorizer_path):
        """Save the trained model and vectorizer"""
        try:
            joblib.dump(self.model, model_path)
            joblib.dump(self.vectorizer, vectorizer_path)
            logger.info("Model and vectorizer saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            return False
    
    def train(self, data_path=None, X=None, y=None, test_size=0.2, random_state=42):
        """Train the phishing detection model"""
        try:
            # Load dataset if path is provided, otherwise use provided X and y
            if data_path:
                # Load dataset
                data = pd.read_csv(data_path)
                
                # Check if dataset has required columns
                required_cols = ['content', 'is_phishing']
                for col in required_cols:
                    if col not in data.columns:
                        raise ValueError(f"Dataset missing required column: {col}")
                
                # Prepare data
                X = data['content'].fillna('')
                y = data['is_phishing']
            elif X is None or y is None:
                raise ValueError("Either data_path or both X and y must be provided")
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state
            )
            
            # Vectorize text data
            X_train_vectors = self.vectorizer.fit_transform(X_train)
            X_test_vectors = self.vectorizer.transform(X_test)
            
            # Train model
            self.model = RandomForestClassifier(n_estimators=100, random_state=random_state)
            self.model.fit(X_train_vectors, y_train)
            
            # Make predictions
            y_pred = self.model.predict(X_test_vectors)
            
            # Calculate metrics
            metrics = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred),
                'recall': recall_score(y_test, y_pred),
                'f1_score': f1_score(y_test, y_pred),
                'classification_report': classification_report(y_test, y_pred)
            }
            
            # Store feature importance for explanation
            if hasattr(self.model, 'feature_importances_'):
                self.feature_importance = dict(zip(
                    self.vectorizer.get_feature_names_out(),
                    self.model.feature_importances_
                ))
            
            logger.info(f"Model trained successfully. Metrics: {metrics}")
            return metrics
            
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise
    
    def predict(self, email_content):
        """Predict if an email is phishing or not"""
        try:
            if self.model is None:
                raise ValueError("Model not trained yet")
            
            # Vectorize the input
            content_vector = self.vectorizer.transform([email_content])
            
            # Make prediction
            prediction = self.model.predict(content_vector)[0]
            confidence = np.max(self.model.predict_proba(content_vector)[0])
            
            # Generate explanation
            explanation = self._generate_explanation(email_content, prediction)
            
            return prediction, confidence, explanation
            
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            raise
    
    def _generate_explanation(self, email_content, prediction):
        """Generate an explanation for the prediction"""
        if not self.feature_importance:
            return "No feature importance available for explanation."
        
        # Get top features from the email that influenced the prediction
        words = email_content.lower().split()
        relevant_features = {}
        
        for word in set(words):
            if word in self.feature_importance:
                relevant_features[word] = self.feature_importance[word]
        
        # Sort by importance
        sorted_features = sorted(relevant_features.items(), key=lambda x: x[1], reverse=True)[:5]
        
        if prediction == 1:
            explanation = "This email was classified as phishing because it contains suspicious elements such as: "
            explanation += ", ".join([f"\"{word}\"" for word, _ in sorted_features])
        else:
            explanation = "This email was classified as legitimate. "
            if sorted_features:
                explanation += "Key words that indicate legitimacy: "
                explanation += ", ".join([f"\"{word}\"" for word, _ in sorted_features])
        
        return explanation