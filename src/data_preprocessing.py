"""
Data Preprocessing Module for College Placement Prediction
===========================================================
This module handles:
1. Loading the student placement dataset.
2. Checking dataset information and summary statistics.
3. Handling missing values and duplicates.
4. Dropping non-predictive columns (e.g. Student_ID).
5. Encoding categorical features and target variable.
6. Train-test splitting without data leakage (stratified split).
7. Feature scaling using StandardScaler (fit on training data only).
"""

import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Define features used for model training and prediction
FEATURE_COLUMNS = [
    'CGPA',
    'Tenth_Percentage',
    'Twelfth_Percentage',
    'Internships',
    'Projects',
    'Technical_Skills',
    'Communication_Skills',
    'Backlogs',
    'Work_Experience'
]

TARGET_COLUMN = 'Placement_Status'

def load_data(csv_path):
    """
    Loads dataset from CSV file into a pandas DataFrame.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset file not found at: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"Data loaded successfully. Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def clean_data(df):
    """
    Cleans dataset:
    - Removes duplicate rows
    - Handles missing values (imputes median for numerical, mode for categorical)
    - Removes unnecessary identification columns like 'Student_ID'
    """
    df_clean = df.copy()
    
    # 1. Check and remove duplicates
    duplicates_count = df_clean.duplicated().sum()
    if duplicates_count > 0:
        print(f"Removing {duplicates_count} duplicate records...")
        df_clean = df_clean.drop_duplicates()
    
    # 2. Check and handle missing values
    missing_counts = df_clean.isnull().sum()
    if missing_counts.sum() > 0:
        print("Handling missing values:")
        for col in df_clean.columns:
            if df_clean[col].isnull().sum() > 0:
                if df_clean[col].dtype in ['float64', 'int64']:
                    median_val = df_clean[col].median()
                    df_clean[col] = df_clean[col].fillna(median_val)
                    print(f" - Filled missing values in '{col}' with median: {median_val}")
                else:
                    mode_val = df_clean[col].mode()[0]
                    df_clean[col] = df_clean[col].fillna(mode_val)
                    print(f" - Filled missing values in '{col}' with mode: {mode_val}")
    else:
        print("No missing values found in the dataset.")
        
    # 3. Drop non-predictive identifier columns if present
    if 'Student_ID' in df_clean.columns:
        df_clean = df_clean.drop(columns=['Student_ID'])
        print("Dropped non-predictive column: 'Student_ID'")
        
    return df_clean

def encode_features_and_target(df):
    """
    Encodes categorical features and the target column:
    - Work_Experience: 'Yes' -> 1, 'No' -> 0
    - Placement_Status: 'Placed' -> 1, 'Not Placed' -> 0
    """
    df_encoded = df.copy()
    
    # Encode Work_Experience
    if 'Work_Experience' in df_encoded.columns:
        df_encoded['Work_Experience'] = (
            df_encoded['Work_Experience']
            .astype(str)
            .str.strip()
            .map({'Yes': 1, 'No': 0, 'yes': 1, 'no': 0, '1': 1, '0': 0, 1: 1, 0: 0})
            .fillna(0)
            .astype(int)
        )
    
    # Encode Target: Placement_Status
    if TARGET_COLUMN in df_encoded.columns:
        df_encoded[TARGET_COLUMN] = (
            df_encoded[TARGET_COLUMN]
            .astype(str)
            .str.strip()
            .map({'Placed': 1, 'Not Placed': 0, 'placed': 1, 'not placed': 0, '1': 1, '0': 0, 1: 1, 0: 0})
            .fillna(0)
            .astype(int)
        )
            
    return df_encoded

def prepare_data(csv_path, test_size=0.2, random_state=42):
    """
    Complete end-to-end preprocessing pipeline:
    1. Loads dataset
    2. Cleans data
    3. Encodes categorical variables
    4. Separates X (features) and y (target)
    5. Performs stratified Train/Test split
    6. Fits StandardScaler on X_train ONLY, transforms X_train and X_test
    
    Returns:
        X_train_scaled, X_test_scaled, y_train, y_test, scaler, feature_names, raw_df
    """
    raw_df = load_data(csv_path)
    df_clean = clean_data(raw_df)
    df_encoded = encode_features_and_target(df_clean)
    
    # Ensure all required features are present
    for col in FEATURE_COLUMNS:
        if col not in df_encoded.columns:
            raise ValueError(f"Required feature '{col}' missing from dataset!")
            
    X = df_encoded[FEATURE_COLUMNS]
    y = df_encoded[TARGET_COLUMN]
    
    # Stratified Train/Test split to maintain identical class ratios in train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )
    
    print(f"Data split: Training samples = {X_train.shape[0]}, Test samples = {X_test.shape[0]}")
    
    # Fit scaler ONLY on training data to prevent data leakage!
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=FEATURE_COLUMNS,
        index=X_train.index
    )
    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test),
        columns=FEATURE_COLUMNS,
        index=X_test.index
    )
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, FEATURE_COLUMNS, df_clean

def preprocess_single_input(input_dict, scaler, feature_names=FEATURE_COLUMNS):
    """
    Preprocesses a single user input from the web form for real-time model prediction.
    Ensures input is transformed with the exact same scaler used during training.
    """
    # Create single-row DataFrame
    row = {}
    for col in feature_names:
        val = input_dict.get(col)
        if col == 'Work_Experience':
            if isinstance(val, str):
                val = 1 if val.lower() in ['yes', '1', 'true'] else 0
            else:
                val = int(val)
        else:
            val = float(val)
        row[col] = [val]
        
    df_input = pd.DataFrame(row)
    
    # Scale input using the saved scaler
    scaled_input = scaler.transform(df_input)
    return scaled_input, df_input

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(current_dir, "..", "data", "placement_data.csv")
    
    print("Testing Preprocessing Pipeline...")
    X_tr, X_te, y_tr, y_te, sc, feats, df_c = prepare_data(dataset_path)
    print("Preprocessing successful!")
    print("Feature columns:", feats)
    print("Sample scaled training row:")
    print(X_tr.iloc[0])
