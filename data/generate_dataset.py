"""
Dataset Generator for College Placement Prediction
==================================================
This script generates a realistic benchmark dataset (1,200 student records)
with relevant academic and skill metrics for machine learning classification.

NOTE: This is a synthetic benchmark dataset generated for academic and demonstration
purposes for the BCA mini-project. It simulates real-world college recruitment patterns.
"""

import numpy as np
import pandas as pd
import os

def generate_placement_dataset(num_samples=1200, random_seed=42):
    np.random.seed(random_seed)
    
    # 1. Student ID
    student_ids = [f"STU{1000 + i}" for i in range(num_samples)]
    
    # 2. 10th Percentage (Range: 50% - 98%, mean ~75%, std ~10%)
    tenth_pct = np.clip(np.random.normal(75, 10, num_samples), 50.0, 98.0).round(2)
    
    # 3. 12th Percentage (Correlated with 10th percentage, mean ~72%, std ~10%)
    twelfth_noise = np.random.normal(0, 5, num_samples)
    twelfth_pct = np.clip(tenth_pct * 0.85 + 10 + twelfth_noise, 48.0, 98.0).round(2)
    
    # 4. CGPA (Scale 0-10, mean ~7.4, std ~1.1, range 5.0 - 9.9)
    cgpa_noise = np.random.normal(0, 0.6, num_samples)
    cgpa = np.clip((twelfth_pct / 10.0) * 0.7 + 2.3 + cgpa_noise, 5.0, 9.9).round(2)
    
    # 5. Internships (0 to 3 internships)
    internship_probs = [0.35, 0.40, 0.18, 0.07]
    internships = np.random.choice([0, 1, 2, 3], size=num_samples, p=internship_probs)
    
    # 6. Projects (0 to 5 projects)
    project_probs = [0.10, 0.25, 0.35, 0.20, 0.07, 0.03]
    projects = np.random.choice([0, 1, 2, 3, 4, 5], size=num_samples, p=project_probs)
    
    # 7. Technical Skills (Rating 1 to 5)
    tech_base = np.clip(np.round((cgpa - 5) / 1.0 + np.random.normal(0, 0.7, num_samples)), 1, 5).astype(int)
    technical_skills = tech_base
    
    # 8. Communication Skills (Rating 1 to 5)
    comm_base = np.random.choice([1, 2, 3, 4, 5], size=num_samples, p=[0.08, 0.22, 0.40, 0.22, 0.08])
    communication_skills = comm_base
    
    # 9. Number of Backlogs (0 to 5)
    # Higher CGPA students tend to have fewer backlogs
    backlogs = []
    for g in cgpa:
        if g >= 8.5:
            b = np.random.choice([0, 1], p=[0.95, 0.05])
        elif g >= 7.0:
            b = np.random.choice([0, 1, 2], p=[0.75, 0.20, 0.05])
        elif g >= 6.0:
            b = np.random.choice([0, 1, 2, 3], p=[0.50, 0.30, 0.15, 0.05])
        else:
            b = np.random.choice([0, 1, 2, 3, 4, 5], p=[0.20, 0.30, 0.25, 0.15, 0.07, 0.03])
        backlogs.append(b)
    backlogs = np.array(backlogs)
    
    # 10. Work Experience (Yes / No)
    work_exp_prob = 0.22  # ~22% of college students had part-time/freelance work experience
    work_exp = np.random.choice(["Yes", "No"], size=num_samples, p=[work_exp_prob, 1 - work_exp_prob])
    
    # 11. Calculate Placement Probability using realistic log-odds equation
    # Factors that positively impact placement:
    # - High CGPA
    # - Good 10th & 12th marks
    # - Having internships and projects
    # - Strong technical and communication skills
    # - Previous work experience
    # Factors that negatively impact placement:
    # - Academic backlogs
    
    log_odds = (
        1.10 * (cgpa - 7.2) +
        0.03 * (tenth_pct - 70) +
        0.03 * (twelfth_pct - 70) +
        0.75 * internships +
        0.40 * (projects - 1.5) +
        0.65 * (technical_skills - 3.0) +
        0.45 * (communication_skills - 3.0) +
        0.80 * (work_exp == "Yes").astype(int) -
        1.05 * backlogs +
        np.random.normal(0, 0.65, num_samples) # Natural variance
    )
    
    # Sigmoid function to convert log_odds to probability
    placement_prob = 1.0 / (1.0 + np.exp(-log_odds))
    
    # Determine placement status (threshold 0.50)
    placement_status = ["Placed" if p >= 0.50 else "Not Placed" for p in placement_prob]
    
    # Build DataFrame
    df = pd.DataFrame({
        "Student_ID": student_ids,
        "CGPA": cgpa,
        "Tenth_Percentage": tenth_pct,
        "Twelfth_Percentage": twelfth_pct,
        "Internships": internships,
        "Projects": projects,
        "Technical_Skills": technical_skills,
        "Communication_Skills": communication_skills,
        "Backlogs": backlogs,
        "Work_Experience": work_exp,
        "Placement_Status": placement_status
    })
    
    return df

if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(output_dir, "placement_data.csv")
    
    print("Generating benchmark college placement dataset...")
    df = generate_placement_dataset(num_samples=1200, random_seed=42)
    
    df.to_csv(csv_path, index=False)
    print(f"Dataset successfully saved to: {csv_path}")
    print(f"Total Rows: {len(df)}")
    print(f"Placement Distribution:\n{df['Placement_Status'].value_counts(normalize=True).round(3) * 100}%")
    print("\nFirst 5 Records:")
    print(df.head())
