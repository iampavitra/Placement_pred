"""
Model Training and Evaluation Module
====================================
This module:
1. Loads preprocessed training and testing data without data leakage.
2. Trains multiple classification models:
   - Logistic Regression
   - Decision Tree Classifier
   - Random Forest Classifier
   - K-Nearest Neighbors Classifier
3. Evaluates each model using:
   - Accuracy
   - Precision
   - Recall
   - F1-Score
   - Confusion Matrix
4. Ranks models fairly based on test performance.
5. Automatically saves the best model, scaler, feature metadata, and metrics.
6. Generates a comparative performance visualization.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from data_preprocessing import prepare_data, FEATURE_COLUMNS, TARGET_COLUMN
from visualization import plot_model_comparison

def train_and_evaluate_models(data_path, models_dir, images_dir):
    """
    Trains multiple models, evaluates their performance, saves the best model
    and exports summary statistics for the web application dashboard.
    """
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    print("=" * 60)
    print("STEP 1: PREPARING DATA (Train/Test Split & Feature Scaling)")
    print("=" * 60)
    X_train_scaled, X_test_scaled, y_train, y_test, scaler, feature_names, raw_df = prepare_data(data_path)

    # Define candidate models with fixed random states for reproducibility
    models = {
        "Logistic Regression": LogisticRegression(random_state=42, max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(random_state=42, max_depth=5),
        "Random Forest": RandomForestClassifier(random_state=42, n_estimators=100, max_depth=6),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5)
    }

    results = []
    trained_model_objects = {}

    print("\n" + "=" * 60)
    print("STEP 2: TRAINING AND EVALUATING CANDIDATE MODELS")
    print("=" * 60)

    for name, model in models.items():
        print(f"\nTraining [{name}]...")
        # Fit model on training data
        model.fit(X_train_scaled, y_train)
        trained_model_objects[name] = model

        # Predict on holdout test set
        y_pred = model.predict(X_test_scaled)

        # Compute classification metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='binary', zero_division=0)
        rec = recall_score(y_test, y_pred, average='binary', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='binary', zero_division=0)
        cm = confusion_matrix(y_test, y_pred).tolist()

        results.append({
            "Model": name,
            "Accuracy": round(float(acc), 4),
            "Precision": round(float(prec), 4),
            "Recall": round(float(rec), 4),
            "F1_Score": round(float(f1), 4),
            "Confusion_Matrix": cm
        })

        print(f" -> Accuracy:  {acc * 100:.2f}%")
        print(f" -> Precision: {prec * 100:.2f}%")
        print(f" -> Recall:    {rec * 100:.2f}%")
        print(f" -> F1-Score:  {f1:.4f}")
        print(f" -> Confusion Matrix [TN, FP], [FN, TP]: {cm}")

    # Build comparison DataFrame
    comparison_df = pd.DataFrame(results)

    print("\n" + "=" * 60)
    print("STEP 3: MODEL PERFORMANCE COMPARISON TABLE")
    print("=" * 60)
    display_df = comparison_df[['Model', 'Accuracy', 'Precision', 'Recall', 'F1_Score']]
    print(display_df.to_string(index=False))

    # Select best model based on F1-Score (balances precision and recall)
    best_row = comparison_df.sort_values(by=['F1_Score', 'Accuracy'], ascending=False).iloc[0]
    best_model_name = best_row['Model']
    best_model_obj = trained_model_objects[best_model_name]

    print("\n" + "=" * 60)
    print("STEP 4: MODEL SELECTION RESULT")
    print("=" * 60)
    print(f"BEST MODEL SELECTED: {best_model_name}")
    print(f"Highest F1-Score:    {best_row['F1_Score']}")
    print(f"Test Set Accuracy:   {best_row['Accuracy'] * 100:.2f}%")

    # Save artifacts
    print("\n" + "=" * 60)
    print("STEP 5: SAVING MODEL ARTIFACTS AND METRICS")
    print("=" * 60)

    # 1. Save Best Model
    model_path = os.path.join(models_dir, "best_model.pkl")
    joblib.dump(best_model_obj, model_path)
    print(f"[OK] Saved best model to: {model_path}")

    # 2. Save Scaler
    scaler_path = os.path.join(models_dir, "scaler.pkl")
    joblib.dump(scaler, scaler_path)
    print(f"[OK] Saved scaler to: {scaler_path}")

    # 3. Save Feature Names
    features_path = os.path.join(models_dir, "feature_names.json")
    with open(features_path, "w") as f:
        json.dump(feature_names, f, indent=4)
    print(f"[OK] Saved feature names to: {features_path}")

    # 4. Save Model Comparison JSON
    metrics_path = os.path.join(models_dir, "model_comparison.json")
    metrics_data = {
        "best_model": best_model_name,
        "best_accuracy": float(best_row['Accuracy']),
        "best_f1": float(best_row['F1_Score']),
        "models": results
    }
    with open(metrics_path, "w") as f:
        json.dump(metrics_data, f, indent=4)
    print(f"[OK] Saved metrics comparison to: {metrics_path}")

    # 5. Save Dataset Summary for Dashboard
    total_students = len(raw_df)
    placed_count = int((raw_df[TARGET_COLUMN] == 'Placed').sum())
    not_placed_count = total_students - placed_count
    placement_rate = round((placed_count / total_students) * 100, 2)
    avg_cgpa = round(float(raw_df['CGPA'].mean()), 2)
    avg_tenth = round(float(raw_df['Tenth_Percentage'].mean()), 2)
    avg_twelfth = round(float(raw_df['Twelfth_Percentage'].mean()), 2)

    summary_data = {
        "total_students": total_students,
        "placed_students": placed_count,
        "not_placed_students": not_placed_count,
        "placement_percentage": placement_rate,
        "avg_cgpa": avg_cgpa,
        "avg_tenth": avg_tenth,
        "avg_twelfth": avg_twelfth,
        "best_model_name": best_model_name,
        "best_model_accuracy": round(float(best_row['Accuracy']) * 100, 2)
    }

    summary_path = os.path.join(models_dir, "dataset_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary_data, f, indent=4)
    print(f"[OK] Saved dashboard dataset summary to: {summary_path}")

    # 6. Plot model comparison chart
    plot_model_comparison(comparison_df, images_dir)

    print("\nTraining and evaluation pipeline completed successfully!")
    return metrics_data

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, "..", "data", "placement_data.csv")
    models_directory = os.path.join(current_dir, "..", "models")
    images_directory = os.path.join(current_dir, "..", "app", "static", "images")

    train_and_evaluate_models(data_file, models_directory, images_directory)
