# Cost-Auditing
Markdown
### Exploratory Data Analysis (EDA) for AuditScore Prediction

This section outlines the exploratory data analysis performed on the audit dataset for predicting `AuditScore` using a linear regression model. The analysis is integrated into a Flask web application, allowing for interactive visualization and data exploration based on selected `AuditType`.

### Features

* **Automated EDA Summary**: Generates a summary of descriptive statistics, missing values, and data types for the audit dataset at application startup.
* **Interactive Data Filtering**: Allows users to filter the dataset by `AuditType` through a web interface.
* **Dynamic Table Display**: Presents filtered data in a sortable and searchable HTML table.
* **Visualizations**: Generates and displays bar charts for `AuditScore` frequency and `DataValue` comparisons for the selected `AuditType`.

### Requirements

The application and EDA process rely on the following key dependencies:

* **Python 3.6+**
* **Flask**: For building the web application.
* **Pandas**: For data manipulation and analysis.
* **Matplotlib**: For generating plots.
* **scikit-learn**: (Used in `model.py` for model training, but relevant for understanding the overall project context).
* **joblib**: (Used in `model.py` for saving/loading the trained model).
* **openpyxl**: For reading Excel files.

You can install these dependencies using `pip`:

```bash
pip install -r requirements.txt
(Note: A requirements.txt file would need to be created containing the above libraries.)
Installation and Setup
1.	Project Structure:
2.	/your-project-directory
3.	│── /inputfile
4.	│   └── full_audit_dataset_with_security_operational.xlsx  # Your dataset
5.	│── /output
6.	│   └── eda_summary.txt # EDA summary generated at startup
7.	│── /templates
8.	│   ├── homepage.html
9.	│   ├── index.html
10.	│   └── results.html
11.	│── app.py           # Flask application for EDA and dashboard
12.	│── model.py         # Script for training the linear regression model
13.	│── requirements.txt # List of Python dependencies
14.	Place your dataset: Ensure full_audit_dataset_with_security_operational.xlsx is located in the inputfile directory, relative to app.py.
15.	Run the Flask app:
Bash
python app.py
This will start the Flask development server.
16.	Access the application: Open your web browser and navigate to http://127.0.0.1:5000.
Project Structure (Detailed)
•	/inputfile/: Contains the Excel dataset (full_audit_dataset_with_security_operational.xlsx) used for analysis and model training.
•	/output/: Stores the generated EDA summary file (eda_summary.txt). This directory is created if it doesn't exist.
•	/templates/: Houses the HTML templates for the web application:
o	homepage.html: The initial landing page.
o	index.html: The dashboard where users select audit types.
o	results.html: Displays the filtered data table and generated plots.
•	app.py: The main Flask application. It handles:
o	Loading the dataset.
o	Performing initial EDA and saving the summary.
o	Routing for the homepage, dashboard, and data upload.
o	Filtering data based on AuditType.
o	Generating HTML tables for display.
o	Creating and encoding AuditScore frequency and DataValue comparison plots.
•	model.py: A separate script responsible for:
o	Loading the dataset.
o	Precomputing the data (handling missing values, one-hot encoding).
o	Splitting data into training and testing sets.
o	Training a LinearRegression model.
o	Evaluating the model's performance (MSE, R-squared).
o	Saving the trained model as linear_regression_model.pkl using joblib.
•	requirements.txt: Lists all Python packages required to run the application and model training script.
Usage
1.	Upon running app.py, an EDA summary (eda_summary.txt) will be generated in the output directory, providing insights into the dataset's structure, missing values, and data types.
2.	Navigate to the homepage in your browser.
3.	Select an "Audit Type" from the dropdown menu on the dashboard.
4.	Submit your selection to view:
o	A table displaying AuditType, AuditScore, DataValue, and RiskLevel for the selected audit type.
o	A bar chart showing the frequency distribution of AuditScore.
o	A bar chart illustrating the DataValue comparison.
