import joblib
import pandas as pd

# Load trained model and scaler
model = joblib.load("fault_model.joblib")
scaler = joblib.load("scaler.joblib")

FEATURES = [
    "Accelerometer1RMS",
    "Accelerometer2RMS",
    "Current",
    "Pressure",
    "Temperature",
    "Thermocouple",
    "Voltage",
    "Volume Flow RateRMS"
]


def detect_fault(sensor_data):

    # Convert incoming sensor data to DataFrame
    df = pd.DataFrame([sensor_data])

    # Make sure features are in exactly the same order
    X = df[FEATURES]

    # Apply the same scaling used during training
    X_scaled = scaler.transform(X)

    # Make prediction
    prediction = model.predict(X_scaled)[0]

    # Get probability
    probability = model.predict_proba(X_scaled)[0]

    if prediction == 1:
        status = "ANOMALY"
    else:
        status = "NORMAL"

    return {
        "prediction": int(prediction),
        "status": status,
        "normal_probability": round(float(probability[0]), 4),
        "anomaly_probability": round(float(probability[1]), 4)
    }


# Test example
if __name__ == "__main__":

    sample = {
        "Accelerometer1RMS": 0.026,
        "Accelerometer2RMS": 0.040,
        "Current": 1.2,
        "Pressure": 0.05,
        "Temperature": 79.5,
        "Thermocouple": 26.0,
        "Voltage": 230.0,
        "Volume Flow RateRMS": 32.0
    }

    result = detect_fault(sample)

    print("Sensor data:")
    print(sample)

    print("\nPrediction:")
    print(result)