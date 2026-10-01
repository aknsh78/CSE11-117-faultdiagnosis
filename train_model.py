import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# -----------------------------
# 1. Load all valve1 CSV files
# -----------------------------

DATA_PATH = Path("archive/SKAB/valve1")

csv_files = sorted(DATA_PATH.glob("*.csv"))

dataframes = []

for file in csv_files:
    df = pd.read_csv(file, sep=";")
    dataframes.append(df)

data = pd.concat(dataframes, ignore_index=True)

print("Dataset shape:", data.shape)


# -----------------------------
# 2. Select features and target
# -----------------------------

features = [
    "Accelerometer1RMS",
    "Accelerometer2RMS",
    "Current",
    "Pressure",
    "Temperature",
    "Thermocouple",
    "Voltage",
    "Volume Flow RateRMS"
]

X = data[features]
y = data["anomaly"]


# -----------------------------
# 3. Handle missing values
# -----------------------------

X = X.fillna(X.median())


# -----------------------------
# 4. Time-based split
# -----------------------------

data["datetime"] = pd.to_datetime(data["datetime"])

# Sort chronologically
data = data.sort_values("datetime")

X = data[features].fillna(data[features].median())
y = data["anomaly"]

split_index = int(len(data) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# -----------------------------
# 5. Scale the features
# -----------------------------

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# -----------------------------
# 6. Train Random Forest
# -----------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train_scaled, y_train)


# -----------------------------
# 7. Evaluate
# -----------------------------

predictions = model.predict(X_test_scaled)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions))


# -----------------------------
# 8. Save model and scaler
# -----------------------------

joblib.dump(model, "fault_model.joblib")
joblib.dump(scaler, "scaler.joblib")

print("\nModel saved as fault_model.joblib")
print("Scaler saved as scaler.joblib")
# -----------------------------
# 9. Feature importance
# -----------------------------

importance = pd.Series(
    model.feature_importances_,
    index=features
).sort_values(ascending=False)

print("\nFeature Importance:")
print(importance)