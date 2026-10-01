import pandas as pd
import time
from pathlib import Path
from datetime import datetime

# -----------------------------------------
# Dataset location
# -----------------------------------------

DATA_PATH = Path("archive/SKAB/valve1")

csv_files = sorted(
    DATA_PATH.glob("*.csv"),
    key=lambda x: int(x.stem)
)

if not csv_files:
    raise FileNotFoundError(
        f"No CSV files found in {DATA_PATH}"
    )

# -----------------------------------------
# Load all files in order
# -----------------------------------------

dataframes = []

for file in csv_files:
    df = pd.read_csv(file, sep=";")
    df["source_file"] = file.stem
    dataframes.append(df)

data = pd.concat(
    dataframes,
    ignore_index=True
)

print(f"Loaded {len(data)} SKAB sensor records.")


# -----------------------------------------
# Current position in dataset
# -----------------------------------------

current_index = 740


# -----------------------------------------
# Generate next sensor record
# -----------------------------------------

def generate_sensor_data():

    global current_index

    # Restart from beginning when dataset ends
    if current_index >= len(data):
        current_index = 0

    row = data.iloc[current_index]

    current_index += 1

    # Ground truth
    if int(row["anomaly"]) == 1:
        fault_type = "ANOMALY"
    else:
        fault_type = "NORMAL"

    sensor_data = {
        "device_id": "ESP32_001",

        "timestamp": datetime.now().isoformat(),

        "Accelerometer1RMS": float(
            row["Accelerometer1RMS"]
        ),

        "Accelerometer2RMS": float(
            row["Accelerometer2RMS"]
        ),

        "Current": float(
            row["Current"]
        ),

        "Pressure": float(
            row["Pressure"]
        ),

        "Temperature": float(
            row["Temperature"]
        ),

        "Thermocouple": float(
            row["Thermocouple"]
        ),

        "Voltage": float(
            row["Voltage"]
        ),

        "Volume Flow RateRMS": float(
            row["Volume Flow RateRMS"]
        ),

        "power_factor": 0.92,

        "power": round(
            float(row["Voltage"])
            * float(row["Current"])
            * 0.92,
            2
        ),

        # Ground truth
        "fault_type": fault_type,
        "anomaly": int(row["anomaly"]),
        "changepoint": int(row["changepoint"]),

        "source_file": str(row["source_file"])
    }

    return sensor_data


# -----------------------------------------
# Test simulator
# -----------------------------------------

if __name__ == "__main__":

    while True:

        sensor_data = generate_sensor_data()

        print("\nSensor data:")
        print(sensor_data)

        time.sleep(2)