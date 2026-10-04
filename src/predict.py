"""
Prediction Module for College Placement Prediction
===================================================
This module provides the interface for predicting whether a student is likely
to be Placed or Not Placed based on their academic and skill inputs.

It loads:
- The winning trained model (best_model.pkl)
- The exact fitted StandardScaler (scaler.pkl)
- The list of trained features (feature_names.json)
"""

import os
import json
import joblib
import pandas as pd
import numpy as np

# Default paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(CURRENT_DIR, "..", "models")

class PlacementPredictor:
    def __init__(self, models_dir=MODELS_DIR):
        self.models_dir = models_dir
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.load_artifacts()

    def load_artifacts(self):
        """
        Loads the trained model, scaler, and feature names.
        """
        model_path = os.path.join(self.models_dir, "best_model.pkl")
        scaler_path = os.path.join(self.models_dir, "scaler.pkl")
        features_path = os.path.join(self.models_dir, "feature_names.json")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Trained model not found at {model_path}. Please run train_model.py first.")
        if not os.path.exists(scaler_path):
            raise FileNotFoundError(f"Scaler not found at {scaler_path}. Please run train_model.py first.")
        if not os.path.exists(features_path):
            raise FileNotFoundError(f"Feature names file not found at {features_path}.")

        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        with open(features_path, "r") as f:
            self.feature_names = json.load(f)

        print("[OK] Predictor artifacts loaded successfully.")

    def validate_inputs(self, student_data):
        """
        Validates form inputs against realistic educational bounds.
        Raises ValueError with clear message if invalid.
        """
        errors = []
        
        # 1. CGPA
        try:
            cgpa = float(student_data.get('CGPA', 0))
            if not (0.0 <= cgpa <= 10.0):
                errors.append("CGPA must be between 0.0 and 10.0.")
        except (ValueError, TypeError):
            errors.append("CGPA must be a valid decimal number.")

        # 2. 10th Percentage
        try:
            tenth = float(student_data.get('Tenth_Percentage', 0))
            if not (0.0 <= tenth <= 100.0):
                errors.append("10th Percentage must be between 0.0% and 100.0%.")
        except (ValueError, TypeError):
            errors.append("10th Percentage must be a valid number.")

        # 3. 12th Percentage
        try:
            twelfth = float(student_data.get('Twelfth_Percentage', 0))
            if not (0.0 <= twelfth <= 100.0):
                errors.append("12th Percentage must be between 0.0% and 100.0%.")
        except (ValueError, TypeError):
            errors.append("12th Percentage must be a valid number.")

        # 4. Internships
        try:
            internships = int(student_data.get('Internships', 0))
            if internships < 0 or internships > 10:
                errors.append("Internships count must be between 0 and 10.")
        except (ValueError, TypeError):
            errors.append("Internships must be a valid integer.")

        # 5. Projects
        try:
            projects = int(student_data.get('Projects', 0))
            if projects < 0 or projects > 20:
                errors.append("Projects count must be between 0 and 20.")
        except (ValueError, TypeError):
            errors.append("Projects must be a valid integer.")

        # 6. Technical Skills (1 to 5)
        try:
            tech = int(student_data.get('Technical_Skills', 1))
            if not (1 <= tech <= 5):
                errors.append("Technical Skills rating must be between 1 and 5.")
        except (ValueError, TypeError):
            errors.append("Technical Skills rating must be an integer between 1 and 5.")

        # 7. Communication Skills (1 to 5)
        try:
            comm = int(student_data.get('Communication_Skills', 1))
            if not (1 <= comm <= 5):
                errors.append("Communication Skills rating must be between 1 and 5.")
        except (ValueError, TypeError):
            errors.append("Communication Skills rating must be an integer between 1 and 5.")

        # 8. Backlogs
        try:
            backlogs = int(student_data.get('Backlogs', 0))
            if backlogs < 0 or backlogs > 20:
                errors.append("Backlogs count must be a non-negative number.")
        except (ValueError, TypeError):
            errors.append("Backlogs must be a valid integer.")

        # 9. Work Experience
        work_exp = str(student_data.get('Work_Experience', '')).strip().lower()
        if work_exp not in ['yes', 'no', '1', '0', 'true', 'false']:
            errors.append("Work Experience must be either 'Yes' or 'No'.")

        if errors:
            raise ValueError(" | ".join(errors))

    def predict(self, student_data):
        """
        Executes prediction pipeline for a student profile:
        1. Validates inputs
        2. Prepares feature vector
        3. Scales features with scaler
        4. Predicts class (Placed / Not Placed)
        5. Computes placement probability
        6. Generates analytical profile feedback
        """
        self.validate_inputs(student_data)

        # Parse and encode values into ordered feature list
        row_dict = {}
        for feature in self.feature_names:
            val = student_data[feature]
            if feature == 'Work_Experience':
                encoded_val = 1 if str(val).strip().lower() in ['yes', '1', 'true'] else 0
                row_dict[feature] = [encoded_val]
            else:
                row_dict[feature] = [float(val)]

        input_df = pd.DataFrame(row_dict)

        # Scale using training scaler and preserve feature names
        scaled_input = self.scaler.transform(input_df)
        scaled_df = pd.DataFrame(scaled_input, columns=self.feature_names)

        # Predict class
        prediction = int(self.model.predict(scaled_df)[0])
        label = "PLACED" if prediction == 1 else "NOT PLACED"

        # Compute probability
        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba(scaled_df)[0]
            placed_prob = round(float(probabilities[1]) * 100, 2)
            not_placed_prob = round(float(probabilities[0]) * 100, 2)
        else:
            placed_prob = 100.0 if prediction == 1 else 0.0
            not_placed_prob = 100.0 - placed_prob

        # Generate student insights
        cgpa_val = float(student_data['CGPA'])
        backlogs_val = int(student_data['Backlogs'])
        internships_val = int(student_data['Internships'])
        tech_val = int(student_data['Technical_Skills'])
        comm_val = int(student_data['Communication_Skills'])
        work_exp_val = 1 if str(student_data['Work_Experience']).strip().lower() in ['yes', '1', 'true'] else 0

        positive_factors = []
        improvement_areas = []

        if cgpa_val >= 8.0:
            positive_factors.append(f"Strong academic CGPA ({cgpa_val}) significantly enhances placement chances.")
        elif cgpa_val < 6.5:
            improvement_areas.append(f"CGPA is currently {cgpa_val}. Aiming for 7.0+ unlocks more campus placement drives.")

        if backlogs_val == 0:
            positive_factors.append("Zero active backlogs satisfies all eligibility criteria of top IT recruiters.")
        else:
            improvement_areas.append(f"{backlogs_val} backlog(s) recorded. Clearing backlogs before drive is strongly recommended.")

        if internships_val >= 1:
            positive_factors.append(f"Completed {internships_val} internship(s), demonstrating industry readiness.")
        else:
            improvement_areas.append("Completing at least 1 internship provides a notable competitive advantage.")

        if tech_val >= 4:
            positive_factors.append("High technical skill rating (4+/5) increases clearing probability in coding rounds.")
        if comm_val >= 4:
            positive_factors.append("Good communication skills rating (4+/5) benefits HR and technical interviews.")

        if work_exp_val == 1:
            positive_factors.append("Prior work or freelance experience is highly valued by hiring managers.")

        return {
            "prediction": label,
            "prediction_code": prediction,
            "probability": placed_prob,
            "not_placed_probability": not_placed_prob,
            "positive_factors": positive_factors,
            "improvement_areas": improvement_areas,
            "input_summary": {k: student_data[k] for k in self.feature_names}
        }

# Global singleton helper
_predictor_instance = None

def get_predictor():
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = PlacementPredictor()
    return _predictor_instance

if __name__ == "__main__":
    predictor = get_predictor()

    # Test sample 1: Strong candidate
    sample_placed = {
        "CGPA": 8.65,
        "Tenth_Percentage": 88.0,
        "Twelfth_Percentage": 85.0,
        "Internships": 2,
        "Projects": 3,
        "Technical_Skills": 4,
        "Communication_Skills": 4,
        "Backlogs": 0,
        "Work_Experience": "Yes"
    }
    result1 = predictor.predict(sample_placed)
    print("\n--- Test Candidate 1 (Strong Profile) ---")
    print(f"Prediction: {result1['prediction']}")
    print(f"Model predicted probability: {result1['probability']}%")

    # Test sample 2: High backlogs, low CGPA
    sample_not_placed = {
        "CGPA": 5.4,
        "Tenth_Percentage": 55.0,
        "Twelfth_Percentage": 52.0,
        "Internships": 0,
        "Projects": 1,
        "Technical_Skills": 2,
        "Communication_Skills": 2,
        "Backlogs": 3,
        "Work_Experience": "No"
    }
    result2 = predictor.predict(sample_not_placed)
    print("\n--- Test Candidate 2 (At Risk Profile) ---")
    print(f"Prediction: {result2['prediction']}")
    print(f"Model predicted probability: {result2['probability']}%")
