import pandas as pd
import numpy as np
import os
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from sklearn.preprocessing import MinMaxScaler

# Load the processed dataset
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
file_path = os.path.join(data_dir, "INDUSINDBK.BSE_stock_data_processed.csv")


if not os.path.exists(file_path):
    print(f"❌ Error: Processed data file not found: {file_path}")
    exit()

df = pd.read_csv(file_path, index_col=0, parse_dates=True)

# 🔧 Clean the data: replace infinities and NaNs
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.bfill(inplace=True)

# Optional: clip extreme values to avoid overflows
df = df.clip(lower=-1e6, upper=1e6)

# 🎯 Define the target: predict if next day's open > today's close
df["Target"] = np.where(df["Open"].shift(-1) > df["Close"], 1, 0)

# ✅ Define features including advanced indicators
features = [
    "Daily Change %", "Volatility", "MA_5", "MA_10",
    "MA_20", "Momentum", "Volume_Change", "RSI_14"
]

# Ensure all required features are present
missing_features = [f for f in features if f not in df.columns]
if missing_features:
    print(f"❌ Missing features in dataset: {missing_features}")
    exit()

X = df[features]
y = df["Target"]

# 🧪 Scale the features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# 💾 Save the scaler
scaler_path = os.path.join(data_dir, "scaler.pkl")
joblib.dump(scaler, scaler_path)
print(f"✅ Scaler saved: {scaler_path}")

# 📊 Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, shuffle=False, random_state=42)

# 🤖 Train the XGBoost model
model = xgb.XGBClassifier(
    n_estimators=150,
    learning_rate=0.05,
    use_label_encoder=False,
    eval_metric='logloss'
)
model.fit(X_train, y_train)

# 💾 Save trained model
model_path = os.path.join(data_dir, "stock_prediction_model.pkl")
joblib.dump(model, model_path)
print(f"✅ Model saved: {model_path}")
