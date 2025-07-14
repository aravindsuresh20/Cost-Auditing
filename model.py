import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Load the dataset
file_path = 'full_audit_dataset_with_security_operational.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')

# Drop rows with missing 'AuditScore'
df = df.dropna(subset=['AuditScore'])

# One-hot encode categorical features
df = pd.get_dummies(df)

# Separate features and target variable
X = df.drop('AuditScore', axis=1)
y = df['AuditScore']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Print evaluation metrics
print(f"Mean Squared Error (MSE): {mse}")
print(f"R-squared (R²): {r2}")

# Save the trained model to a file
joblib.dump(model, 'linear_regression_model.pkl')
