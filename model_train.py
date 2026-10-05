import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# 1. Load Dataset
df = pd.read_csv('phone_usage_india.csv')

# Clean column names (strip trailing spaces)
df.columns = df.columns.str.strip()

# 2. Separate Target and Features
# Replace 'Daily_Screen_Time' with the exact target column name in your CSV file
target_col = 'Daily_Screen_Time'
X = df.drop(columns=[target_col])
y = df[target_col]

# Identify numerical and categorical columns
num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
cat_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

# 3. Create Preprocessing & Model Pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
    ]
)

model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# 4. Train-Test Split and Model Training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model_pipeline.fit(X_train, y_train)

# 5. Model Evaluation
y_pred = model_pipeline.predict(X_test)
print(f"Model R² Score: {r2_score(y_test, y_pred):.2f}")
print(f"Root Mean Squared Error: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f} hours")

# 6. Save Model Pipeline
joblib.dump(model_pipeline, 'screen_time_model.pkl')
print("Model saved successfully as 'screen_time_model.pkl'")