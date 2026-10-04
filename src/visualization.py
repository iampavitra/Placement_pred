"""
Exploratory Data Analysis (EDA) and Visualization Module
========================================================
This module generates clean, publication-ready graphs for the College Placement
Prediction project suitable for college presentations, reports, and the web dashboard.

Generated Visualizations:
1. Placement Distribution (Count and Percentage)
2. CGPA Distribution & Boxplot vs Placement Status
3. 10th and 12th Percentage vs Placement Status
4. Internship Experience and Projects vs Placement Status
5. Backlogs vs Placement Status
6. Feature Correlation Heatmap
7. Model Performance Comparison Chart
"""

import os
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server environments
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set cohesive educational aesthetic
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
PRIMARY_BLUE = "#1e40af"
ACCENT_GREEN = "#10b981"
ACCENT_RED = "#ef4444"
PALETTE = [PRIMARY_BLUE, ACCENT_GREEN, "#f59e0b", "#6366f1", "#ec4899"]

def setup_plot_style():
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.labelweight': 'bold',
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'figure.titlesize': 16,
        'figure.dpi': 200
    })

def generate_eda_visualizations(df, output_dir):
    """
    Generates all exploratory data analysis charts and saves them to output_dir.
    """
    os.makedirs(output_dir, exist_ok=True)
    setup_plot_style()
    print("Generating EDA visualizations...")

    # 1. Placement Distribution (Pie + Bar Chart)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    status_counts = df['Placement_Status'].value_counts()
    colors = ['#2563eb', '#f87171']
    
    # Donut chart
    axes[0].pie(
        status_counts,
        labels=status_counts.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2)
    )
    axes[0].set_title("Placement Distribution (%)", pad=15)
    
    # Bar count chart
    bars = axes[1].bar(status_counts.index, status_counts.values, color=colors, width=0.5, edgecolor='#1e293b')
    for bar in bars:
        yval = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2.0, yval + 10, f"{int(yval)} ({yval/len(df)*100:.1f}%)", ha='center', va='bottom', fontweight='bold')
    axes[1].set_title("Student Count by Placement Status", pad=15)
    axes[1].set_ylabel("Number of Students")
    axes[1].set_ylim(0, max(status_counts.values) * 1.15)
    
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "placement_distribution.png"), dpi=200, bbox_inches='tight')
    plt.close(fig)

    # 2. CGPA Distribution & Boxplot vs Placement
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    
    sns.histplot(
        data=df, x='CGPA', hue='Placement_Status',
        kde=True, element="step", palette={'Placed': '#2563eb', 'Not Placed': '#ef4444'},
        ax=axes[0], bins=25
    )
    axes[0].set_title("CGPA Distribution by Placement Outcome", pad=15)
    axes[0].set_xlabel("CGPA (0 - 10)")
    axes[0].set_ylabel("Student Count")
    
    sns.boxplot(
        data=df, x='Placement_Status', y='CGPA', hue='Placement_Status', legend=False,
        palette={'Placed': '#3b82f6', 'Not Placed': '#f87171'},
        ax=axes[1], width=0.4
    )
    axes[1].set_title("CGPA Spread vs Placement Status", pad=15)
    axes[1].set_xlabel("Placement Status")
    axes[1].set_ylabel("CGPA")
    
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "cgpa_vs_placement.png"), dpi=200, bbox_inches='tight')
    plt.close(fig)

    # 3. 10th and 12th Percentage vs Placement
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    
    sns.boxplot(
        data=df, x='Placement_Status', y='Tenth_Percentage', hue='Placement_Status', legend=False,
        palette={'Placed': '#3b82f6', 'Not Placed': '#f87171'},
        ax=axes[0], width=0.4
    )
    axes[0].set_title("10th Percentage vs Placement", pad=15)
    axes[0].set_ylabel("10th Percentage (%)")
    
    sns.boxplot(
        data=df, x='Placement_Status', y='Twelfth_Percentage', hue='Placement_Status', legend=False,
        palette={'Placed': '#3b82f6', 'Not Placed': '#f87171'},
        ax=axes[1], width=0.4
    )
    axes[1].set_title("12th Percentage vs Placement", pad=15)
    axes[1].set_ylabel("12th Percentage (%)")
    
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "percentage_vs_placement.png"), dpi=200, bbox_inches='tight')
    plt.close(fig)

    # 4. Internships and Projects vs Placement
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Internship placement rate
    intern_rate = df.groupby('Internships')['Placement_Status'].apply(lambda s: (s == 'Placed').mean() * 100).reset_index()
    sns.barplot(data=intern_rate, x='Internships', y='Placement_Status', color='#2563eb', ax=axes[0], edgecolor='#1e293b')
    axes[0].set_title("Placement Rate (%) by Number of Internships", pad=15)
    axes[0].set_xlabel("Number of Internships Completed")
    axes[0].set_ylabel("Placement Success Rate (%)")
    axes[0].set_ylim(0, 105)
    for p in axes[0].patches:
        axes[0].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height() + 2),
                         ha='center', va='bottom', fontweight='bold')

    # Project placement rate
    proj_rate = df.groupby('Projects')['Placement_Status'].apply(lambda s: (s == 'Placed').mean() * 100).reset_index()
    sns.barplot(data=proj_rate, x='Projects', y='Placement_Status', color='#0ea5e9', ax=axes[1], edgecolor='#1e293b')
    axes[1].set_title("Placement Rate (%) by Number of Academic Projects", pad=15)
    axes[1].set_xlabel("Number of Projects Completed")
    axes[1].set_ylabel("Placement Success Rate (%)")
    axes[1].set_ylim(0, 105)
    for p in axes[1].patches:
        axes[1].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height() + 2),
                         ha='center', va='bottom', fontweight='bold')
                         
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "projects_internships_vs_placement.png"), dpi=200, bbox_inches='tight')
    plt.close(fig)

    # 5. Backlogs vs Placement
    fig, ax = plt.subplots(figsize=(8, 5))
    backlog_rate = df.groupby('Backlogs')['Placement_Status'].apply(lambda s: (s == 'Placed').mean() * 100).reset_index()
    bars = ax.bar(backlog_rate['Backlogs'], backlog_rate['Placement_Status'], color='#e11d48', width=0.5, edgecolor='#1e293b')
    ax.set_title("Placement Rate (%) vs Academic Backlogs", pad=15)
    ax.set_xlabel("Number of Backlogs")
    ax.set_ylabel("Placement Success Rate (%)")
    ax.set_ylim(0, 105)
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold')
        
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "backlogs_vs_placement.png"), dpi=200, bbox_inches='tight')
    plt.close(fig)

    # 6. Correlation Heatmap
    # Create numeric copy for correlation
    num_df = df.copy()
    if 'Student_ID' in num_df.columns:
        num_df = num_df.drop(columns=['Student_ID'])
    if 'Work_Experience' in num_df.columns:
        num_df['Work_Experience'] = num_df['Work_Experience'].map({'Yes': 1, 'No': 0, 1: 1, 0: 0})
    if 'Placement_Status' in num_df.columns:
        num_df['Placement_Status'] = num_df['Placement_Status'].map({'Placed': 1, 'Not Placed': 0, 1: 1, 0: 0})
        
    fig, ax = plt.subplots(figsize=(10, 8))
    corr = num_df.corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", square=True, linewidths=0.5, cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title("Correlation Heatmap of Student Features & Placement", pad=15)
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "correlation_heatmap.png"), dpi=200, bbox_inches='tight')
    plt.close(fig)

    print("All EDA visualizations successfully created in:", output_dir)

def plot_model_comparison(comparison_df, output_dir):
    """
    Plots a multi-metric bar chart comparing all evaluated ML models.
    """
    os.makedirs(output_dir, exist_ok=True)
    setup_plot_style()
    
    fig, ax = plt.subplots(figsize=(11, 6))
    
    # Reshape dataframe for grouped barplot
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1_Score']
    df_melted = pd.melt(
        comparison_df,
        id_vars=['Model'],
        value_vars=metrics,
        var_name='Metric',
        value_name='Score'
    )
    
    sns.barplot(data=df_melted, x='Model', y='Score', hue='Metric', palette='viridis', ax=ax, edgecolor='#1e293b')
    ax.set_title("Machine Learning Models Evaluation Comparison", pad=15)
    ax.set_ylabel("Score (0.0 to 1.0)")
    ax.set_ylim(0, 1.15)
    ax.legend(loc='lower right', frameon=True)
    
    # Annotate bar values
    for p in ax.patches:
        val = p.get_height()
        if not np.isnan(val) and val > 0:
            ax.annotate(f"{val:.3f}", (p.get_x() + p.get_width() / 2., val + 0.01),
                        ha='center', va='bottom', fontsize=8, rotation=90)
            
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "model_comparison.png"), dpi=200, bbox_inches='tight')
    plt.close(fig)
    print("Model comparison chart saved to:", os.path.join(output_dir, "model_comparison.png"))

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_dir, "..", "data", "placement_data.csv")
    img_dir = os.path.join(current_dir, "..", "app", "static", "images")
    
    if os.path.exists(csv_file):
        df_sample = pd.read_csv(csv_file)
        generate_eda_visualizations(df_sample, img_dir)
    else:
        print(f"Data file not found at: {csv_file}")
