<div align="center">
  <img src="app/static/images/disha-logo.jpg" alt="DISHA Logo" height="120">
</div>

# DISHA: Career Intelligence Using Machine Learning

> **A Complete Final Year BCA Mini-Project**  
> Developed using Python, Scikit-Learn, Pandas, NumPy, Matplotlib, Seaborn, and Flask.

---

## 1. Project Title

**College Placement Prediction Using Machine Learning**  
*Machine Learning Based Student Placement Prediction System*

---

## 2. Project Objective

The primary objective of this project is to build an interactive, accurate web-based application that predicts whether an undergraduate college student (such as a BCA, B.Sc., or B.Tech candidate) is likely to be **Placed** or **Not Placed** in campus recruitment drives.

By leveraging machine learning classification techniques, the system:
* Helps students understand their current placement probability early in their academic journey.
* Highlights specific areas for improvement (such as clearing backlogs, pursuing internships, or improving technical skills).
* Provides college training and placement officers (TPO) with objective, data-backed analytical tools to identify students who need mentoring.

---

## 3. Key Features

* **Empirical Multi-Model Comparison:** Evaluates Logistic Regression, Decision Tree, Random Forest, and K-Nearest Neighbors on the exact same holdout test set.
* **Leakage-Free Preprocessing Pipeline:** Uses a stratified 80/20 train-test split and fits `StandardScaler` strictly on the training set only.
* **Interactive Prediction Web App:** A clean, responsive user interface designed with an academic blue-and-white theme.
* **Real-Time Probability Estimation:** Displays calculated placement probability alongside transparent academic disclaimers.
* **Profile Diagnostic Feedback:** Dynamically pinpoints student strengths and recommendations for improvement.
* **Exploratory Data Analysis Dashboard:** Displays key dataset metrics, model evaluation comparison table, and publication-ready statistical graphs.
* **REST API Endpoint:** Programmatic `/api/predict` route accepting JSON payloads for developer integration.
* **Viva-Ready Documentation:** In-depth explanations of algorithms, metrics, and frequently asked viva questions.

---

## 4. Technologies Used

| Technology | Purpose |
| :--- | :--- |
| **Python 3.11** | Core programming language for data processing, ML, and web backend. |
| **Pandas** | Tabular data manipulation, CSV ingestion, missing values handling, and encoding. |
| **NumPy** | Multi-dimensional array operations, mathematical transformations, and vectorization. |
| **Scikit-Learn** | ML modeling, feature scaling (`StandardScaler`), train-test splitting, and evaluation metrics. |
| **Matplotlib & Seaborn** | Creation of EDA distributions, correlation heatmaps, and model comparison bar charts. |
| **Flask** | Lightweight Python web framework serving routes, Jinja2 templates, and REST API. |
| **HTML5 & Vanilla CSS** | Responsive frontend UI designed around an academic blue-and-white aesthetic. |
| **Joblib** | Serialization and loading of trained model weights and preprocessing scalers. |

---

## 5. Dataset Information

The project utilizes a dedicated benchmark college placement dataset located at [`data/placement_data.csv`](data/placement_data.csv).

> **Academic Transparency Note:**  
> This dataset contains 1,200 student records generated as a synthetic benchmark dataset for educational demonstration in the BCA mini-project. It simulates real-world campus recruitment dynamics observed in Indian colleges. The dataset is decoupled from application code and can easily be replaced by substituting another CSV file.

### Dataset Features:
1. **`CGPA`** (Float, 0.0 - 10.0): Cumulative Grade Point Average.
2. **`Tenth_Percentage`** (Float, 0.0% - 100.0%): 10th standard secondary school board marks.
3. **`Twelfth_Percentage`** (Float, 0.0% - 100.0%): 12th standard higher secondary / diploma marks.
4. **`Internships`** (Integer, 0 - 3+): Number of industry internships completed.
5. **`Projects`** (Integer, 0 - 5+): Count of software, web, or hardware academic projects.
6. **`Technical_Skills`** (Integer, 1 - 5): Rating in programming, databases, and problem solving.
7. **`Communication_Skills`** (Integer, 1 - 5): Rating in verbal, written, and interview communication.
8. **`Backlogs`** (Integer, 0 - 5+): Number of pending or history of academic backlogs.
9. **`Work_Experience`** (Categorical, "Yes" / "No"): Whether the student has prior part-time or freelance work experience.
10. **`Placement_Status`** (Target Variable, "Placed" / "Not Placed"): Ground truth recruitment outcome.

---

## 6. Machine Learning Algorithms

We implemented and compared four diverse classification algorithms:

### 1. Logistic Regression (Selected Deployed Model)
* **Concept:** Calculates a weighted linear sum of input features and maps it to a probability between 0 and 1 using the Sigmoid (logistic) curve:
  $$\sigma(z) = \frac{1}{1 + e^{-z}}$$
* **Result:** Achieved **92.50% Accuracy** and **0.9423 F1-Score**. Selected as the winning model because of its superior generalization on the test set and well-calibrated output probabilities.

### 2. Decision Tree Classifier
* **Concept:** Hierarchical model that asks a series of sequential questions (e.g., "Is CGPA ≥ 7.5?") using Gini Impurity to split data into decision nodes.
* **Result:** Achieved **85.83% Accuracy** and **0.8924 F1-Score**.

### 3. Random Forest Classifier
* **Concept:** An ensemble meta-estimator that fits 100 bootstrap decision trees on random subsets of features and samples, combining their votes to avoid individual tree overfitting.
* **Result:** Achieved **90.42% Accuracy** and **0.9283 F1-Score** (with 96.75% recall).

### 4. K-Nearest Neighbors (KNN)
* **Concept:** Instance-based algorithm that measures Euclidean distance between a candidate student vector and stored training instances, assigning the majority class among the closest $k=5$ neighbors.
* **Result:** Achieved **90.83% Accuracy** and **0.9308 F1-Score**.

---

## 7. Project Structure

```text
college-placement-prediction/
│
├── data/
│   ├── placement_data.csv          # 1,200 student records benchmark dataset
│   └── generate_dataset.py         # Reproducible dataset generator script
│
├── models/
│   ├── best_model.pkl              # Serialized winning ML model (Logistic Regression)
│   ├── scaler.pkl                  # Fitted StandardScaler object
│   ├── feature_names.json          # Ordered list of trained feature columns
│   ├── model_comparison.json       # Exact computed metrics for all 4 models
│   └── dataset_summary.json        # Dashboard summary statistics
│
├── notebooks/
│   └── analysis.ipynb              # Complete EDA and model training Jupyter Notebook
│
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py       # Data cleaning, encoding, splitting, and scaling
│   ├── visualization.py            # Generates publication-ready EDA & comparison charts
│   ├── train_model.py              # Multi-model training and evaluation script
│   └── predict.py                  # Prediction inference engine and input validator
│
├── app/
│   ├── __init__.py
│   ├── app.py                      # Flask web application controller
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css           # Custom academic blue/white theme styling
│   │   ├── js/
│   │   │   └── main.js             # Form validation & preset demo loader
│   │   └── images/                 # Exported EDA & model comparison charts
│   │       ├── placement_distribution.png
│   │       ├── cgpa_vs_placement.png
│   │       ├── percentage_vs_placement.png
│   │       ├── projects_internships_vs_placement.png
│   │       ├── backlogs_vs_placement.png
│   │       ├── correlation_heatmap.png
│   │       └── model_comparison.png
│   └── templates/
│       ├── base.html               # Shared master layout with navbar & footer
│       ├── index.html              # Home landing page with overview & stats
│       ├── predict.html            # Prediction form & dynamic result card
│       ├── dashboard.html          # Analytics KPIs, metrics table & EDA gallery
│       └── about.html              # Project documentation & BCA viva guide
│
├── requirements.txt                # Required Python packages
├── run.bat                         # 1-Click Windows execution script
├── run_instructions.txt            # Command-line execution guide
└── README.md                       # Comprehensive documentation
```

---

## 8. Installation

1. **Clone or Open the Project Folder:**
   ```bash
   cd c:\Users\naidu\Desktop\project
   ```

2. **Verify Python Installation (Python 3.10 or 3.11):**
   ```bash
   python --version
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 9. How to Run the Application

### Option A: 1-Click Windows Launch (Recommended)
Simply double-click the [`run.bat`](run.bat) file located in the root directory.

### Option B: Manual Command Line Launch
1. Open PowerShell or Command Prompt in the project directory.
2. (Optional) Re-train the models to generate fresh weights:
   ```bash
   python src/train_model.py
   ```
3. Run the web server:
   ```bash
   python app/app.py
   ```
4. Open your web browser and navigate to:
   ```text
   http://127.0.0.1:5000
   ```

---

## 10. How Prediction Works

When a student's profile is submitted via the web form:
1. **Validation:** `src/predict.py` verifies that all 9 inputs are present and fall within logical academic bounds (e.g., CGPA $0.0 \le \text{CGPA} \le 10.0$, backlogs $\ge 0$).
2. **Encoding:** Categorical values (such as `Work_Experience: Yes/No`) are encoded to binary digits (1/0).
3. **Scaling:** The single-row vector is transformed using the exact pre-fitted `StandardScaler` from training:
   $$z = \frac{x - \mu}{\sigma}$$
4. **Classification:** The transformed vector is fed into `best_model.pkl`, which predicts the class:
   * Class 1 $\rightarrow$ **PLACED**
   * Class 0 $\rightarrow$ **NOT PLACED**
5. **Probability Computation:** `model.predict_proba()` calculates the confidence percentage (e.g., 94.2%).
6. **Insight Extraction:** The system inspects feature values to generate custom diagnostic tips (e.g., identifying zero backlogs as a strength or suggesting internships).

---

## 11. Model Evaluation Results

All candidate models were evaluated on the holdout test set (240 unseen students):

| Algorithm | Accuracy | Precision | Recall | F1-Score | Confusion Matrix [TN, FP / FN, TP] |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Selected)** | **92.50%** | **93.04%** | **95.45%** | **0.9423** | `[[75, 11], [7, 147]]` |
| **K-Nearest Neighbors (KNN)** | 90.83% | 90.24% | 96.10% | 0.9308 | `[[70, 16], [6, 148]]` |
| **Random Forest Classifier** | 90.42% | 89.22% | 96.75% | 0.9283 | `[[68, 18], [5, 149]]` |
| **Decision Tree Classifier** | 85.83% | 87.04% | 91.56% | 0.8924 | `[[65, 21], [13, 141]]` |

### Why Logistic Regression Was Selected:
* **Highest Measured Performance:** Outperformed other models with a 92.50% test accuracy and a 0.9423 F1-score.
* **Low False Negatives:** Only 7 placed candidates were mistakenly predicted as not placed (Recall: 95.45%).
* **Calibrated Probabilities:** The sigmoid output offers a mathematically sound probability estimate rather than an arbitrary binary cutoff.

---

## 12. Limitations

* **Soft Skills Quantification:** Communication and technical skills are represented on a 1-5 numerical scale, which involves human subjectivity.
* **Company-Specific Variance:** Different recruiting companies have distinct eligibility criteria (e.g., some product companies prioritize coding rounds over 10th/12th marks).
* **Cross-University Differences:** Grading scales (CGPA vs percentage) and curriculum rigors differ across colleges.

---

## 13. Future Enhancements

* **Resume Parser (NLP):** Automatically extract CGPA, internships, and skill tags directly from uploaded student PDF resumes using Natural Language Processing.
* **Company Tier Recommendations:** Recommend specific hiring company categories (e.g., Mass Recruiters vs Product Firms) based on student profile strengths.
* **Personalized Skill Roadmaps:** Generate custom learning paths and coding challenge recommendations to help at-risk students boost their placement chances.
* **Multi-College Database Integration:** Train models on multi-institutional datasets to generalize predictions across different universities.

---

## 14. Viva Examination Preparation Guide

### Quick Answers to Potential Viva Questions:

1. **What is the problem statement of your project?**  
   *Answer:* To forecast whether a college student is likely to be placed during campus interviews by applying machine learning classification models on their academic and extracurricular profile.

2. **How did you prevent data leakage?**  
   *Answer:* We split the data into training (80%) and testing (20%) sets *before* performing feature scaling. The `StandardScaler` was fitted *only* on `X_train`, and then used to transform `X_test` and all new web inputs.

3. **Why did you use F1-Score rather than just Accuracy?**  
   *Answer:* Accuracy can be deceptive if the dataset has class imbalance. F1-Score is the harmonic mean of Precision and Recall, ensuring the model balances false alarms (False Positives) and missed placements (False Negatives).

4. **What does the confusion matrix represent?**  
   *Answer:* It summarizes classification results:
   * **True Negatives (TN = 75):** Unplaced students correctly predicted as Unplaced.
   * **False Positives (FP = 11):** Unplaced students incorrectly predicted as Placed.
   * **False Negatives (FN = 7):** Placed students incorrectly predicted as Unplaced.
   * **True Positives (TP = 147):** Placed students correctly predicted as Placed.

5. **Can the model be used with another dataset?**  
   *Answer:* Yes. The preprocessing and training scripts are decoupled from the web application. Any new CSV matching the feature schema can be placed into `data/` and trained using `python src/train_model.py`.
