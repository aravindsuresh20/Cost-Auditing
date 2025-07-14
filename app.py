# app.py

import matplotlib
matplotlib.use('Agg') # MUST BE CALLED BEFORE importing pyplot
import matplotlib.pyplot as plt
import pandas as pd
import os
import io # Import io module for BytesIO
import base64 # Import base64 module for encoding images

from flask import Flask, request, render_template

app = Flask(__name__)

# Load the dataset
# Ensure 'inputfile/full_audit_dataset_with_security_operational.xlsx' exists relative to app.py
try:
    df = pd.read_excel('inputfile/full_audit_dataset_with_security_operational.xlsx', engine='openpyxl')
except FileNotFoundError:
    print("Error: 'full_audit_dataset_with_security_operational.xlsx' not found. Please ensure it's in the 'inputfile' directory.")
    df = pd.DataFrame() # Create an empty DataFrame to prevent further errors
audit_types = df['AuditType'].dropna().unique() if not df.empty else []

# Function to perform EDA and save to a file
def perform_eda(dataframe, filename='output/eda_summary.txt'):
    eda_summary = {
        "Summary Statistics": dataframe.describe().to_string(),
        "Missing Values": dataframe.isnull().sum().to_string(),
        "Data Types": dataframe.dtypes.to_string()
    }

    os.makedirs('output', exist_ok=True)
    with open(filename, 'w') as f:
        for key, value in eda_summary.items():
            f.write(f"{key}:\n{value}\n\n")

# Perform EDA at startup
if not df.empty:
    perform_eda(df)

# Route for homepage
@app.route('/')
def homepage():
    return render_template('homepage.html', audit_types=audit_types)

# Route for dashboard (index.html)
@app.route('/dashboard')
def dashboard():
    return render_template('index.html', audit_types=audit_types)

# Upload route
@app.route('/upload', methods=['POST'])
def upload():
    selected_audit_type = request.form['audit_type']
    filtered = df[df['AuditType'] == selected_audit_type].copy() # Use .copy() to avoid SettingWithCopyWarning

    # Define the columns you want to display in the table
    desired_columns = ['AuditType', 'AuditScore', 'DataValue', 'RiskLevel']
    
    # Filter the DataFrame to include only the desired columns
    # Check if columns exist before selecting them to avoid KeyError
    columns_to_display = [col for col in desired_columns if col in filtered.columns]
    df_for_display = filtered[columns_to_display]

    # Generate table_html from the DataFrame with only desired columns
    table_html = df_for_display.to_html(classes="display compact", index=False, table_id="myDataTable")

    # Initialize Base64 variables for images
    audit_score_img_base64 = ""
    data_value_img_base64 = ""

    # Plot 1: Frequency vs AuditScore
    audit_score_counts = filtered['AuditScore'].value_counts()
    if not filtered['AuditScore'].dropna().empty:
        audit_score_counts = audit_score_counts.reindex(filtered['AuditScore'].dropna().unique())
    else:
        audit_score_counts = pd.Series()

    if not audit_score_counts.empty:
        plt.figure(figsize=(8, 5))
        audit_score_counts.plot(kind='bar', color='skyblue', edgecolor='white')
        plt.title('Frequency vs AuditScore')
        plt.xlabel('AuditScore')
        plt.ylabel('Frequency')
        plt.tight_layout()
        
        img_buffer_audit_score = io.BytesIO()
        plt.savefig(img_buffer_audit_score, format='png')
        img_buffer_audit_score.seek(0)
        audit_score_img_base64 = base64.b64encode(img_buffer_audit_score.read()).decode('utf-8')
        plt.close()

    # Plot 2: DataValue Comparison
    if not filtered.empty and 'DataValue' in filtered.columns:
        plt.figure(figsize=(8, 5))
        ax = filtered['DataValue'].plot(kind='bar', color='orange', edgecolor='white')
        plt.title('DataValue Comparison')
        plt.xlabel('Index')
        plt.ylabel('DataValue')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        if len(ax.get_xticks()) > 0:
            ax.set_xticks(ax.get_xticks()[::max(1, len(ax.get_xticks()) // 10)])
        plt.xticks(rotation=45)
        plt.tight_layout()

        img_buffer_data_value = io.BytesIO()
        plt.savefig(img_buffer_data_value, format='png')
        img_buffer_data_value.seek(0)
        data_value_img_base64 = base64.b64encode(img_buffer_data_value.read()).decode('utf-8')
        plt.close()

    # Render results.html, passing the Base64 encoded images
    # Pass df_for_display.columns.values for titles to ensure they match displayed columns
    return render_template('results.html', tables=[table_html], titles=df_for_display.columns.values,
                           audit_score_img=f"data:image/png;base64,{audit_score_img_base64}",
                           data_value_img=f"data:image/png;base64,{data_value_img_base64}")


if __name__ == '__main__':
    app.run(debug=True)