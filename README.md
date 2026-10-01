# FaultGuard AI

## AI-Powered Predictive Maintenance & Fault Diagnosis System

FaultGuard AI is an industrial predictive-maintenance system designed to monitor machine sensor data, detect abnormal operating conditions, identify possible fault patterns, and present the results through an interactive dashboard.

The system combines **IoT-style sensor data transmission, MQTT communication, machine learning, PostgreSQL, and Streamlit** to create an end-to-end fault-monitoring workflow.

---

## 🚀 Live Dashboard

**Streamlit Cloud:** https://faultguard-ai.streamlit.app/

---

## 📌 Project Overview

Industrial machines continuously generate sensor data such as temperature, voltage, current, pressure, vibration, and flow rate. Detecting abnormal behavior early can help identify potential machine problems before they become more serious.

FaultGuard AI processes these sensor readings through a machine-learning pipeline and provides:

- Real-time-style sensor monitoring
- Anomaly/fault detection
- Anomaly probability
- Fault severity
- Possible cause
- Recommended action
- Sensor trend visualization
- Historical fault records
- Model validation and performance metrics

---

## 🏗️ System Architecture

```text
                 Sensor / Dataset Data
                         │
                         ▼
                  MQTT Publisher
                         │
                         ▼
                    HiveMQ Broker
                         │
                         ▼
                  MQTT Subscriber
                         │
                         ▼
             ┌─────────────────────────┐
             │   Fault Detection Model │
             │    Random Forest +      │
             │    StandardScaler       │
             └─────────────────────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
        Fault Diagnosis       Anomaly Probability
              │                     │
              └──────────┬──────────┘
                         ▼
                  PostgreSQL
                         │
                         ▼
                 Streamlit Dashboard
```

---

## ✨ Key Features

### 1. Sensor Monitoring

FaultGuard AI monitors multiple machine parameters:

- Accelerometer 1 RMS
- Accelerometer 2 RMS
- Current
- Pressure
- Temperature
- Thermocouple
- Voltage
- Volume Flow Rate RMS

### 2. AI-Based Fault Detection

A **Random Forest Classifier** is used to classify sensor observations as:

- `NORMAL`
- `ANOMALY`

The system also reports the model's probability for the detected state.

### 3. Dynamic Fault Diagnosis

When abnormal behavior is detected, the system analyzes abnormal sensor patterns and maps them to possible machine subsystems.

Examples include:

| Sensor Pattern | Possible Cause |
|---|---|
| Pressure | Pressure abnormality |
| Volume Flow Rate RMS | Flow-system abnormality |
| Accelerometer 1/2 RMS | Mechanical vibration abnormality |
| Current / Voltage | Electrical abnormality |
| Temperature / Thermocouple | Thermal abnormality |

If a single sensor does not explain the anomaly, the system can report:

> Abnormal multivariate sensor pattern detected

### 4. Severity & Recommended Action

The dashboard provides a severity level and a corresponding recommended action to help interpret detected abnormalities.

### 5. Historical Monitoring

The system stores and displays historical sensor/fault records so that previous machine behavior can be reviewed.

### 6. Model Validation

The dashboard displays:

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

---

## 🤖 Machine Learning Model

### Model

**Random Forest Classifier**

Configuration:

```python
RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)
```

### Preprocessing

The sensor features are standardized using:

```text
StandardScaler
```

### Features Used

```text
Accelerometer1RMS
Accelerometer2RMS
Current
Pressure
Temperature
Thermocouple
Voltage
Volume Flow RateRMS
```

### Dataset

The project uses the **SKAB Valve 1** data for model development and testing.

The training process uses a time-based 80/20 split.

---

## 📊 Model Performance

The current trained model produced the following validation results:

| Metric | Result |
|---|---:|
| Accuracy | 93.17% |
| Anomaly Precision | 99.80% |
| Anomaly Recall | 80.08% |
| Anomaly F1 Score | 88.86% |

### Confusion Matrix

```text
                 Predicted
                 Normal  Anomaly

Actual Normal      2396       2
Actual Anomaly     246     989
```

The model produces very few false positives, while some actual anomalies are still missed. Therefore, the recall value is important when interpreting the model's performance.

---

## 🔄 End-to-End Workflow

### Step 1 — Sensor Data

Machine/simulated sensor values are generated or obtained from the dataset.

### Step 2 — MQTT Communication

The sensor data is published to the MQTT topic:

```text
factory/machine1/sensors
```

using HiveMQ as the MQTT broker.

### Step 3 — Data Reception

The MQTT subscriber receives the sensor message.

### Step 4 — ML Inference

The received sensor values are passed through:

```text
StandardScaler
        ↓
Random Forest
        ↓
NORMAL / ANOMALY
```

### Step 5 — Diagnosis

The system identifies abnormal sensor patterns and generates:

```text
Fault
Severity
Possible Cause
Recommended Action
```

### Step 6 — Storage

Processed records are stored in PostgreSQL during the local real-time workflow.

### Step 7 — Dashboard

Streamlit displays the machine condition, sensor values, trends, diagnosis, model performance, and historical records.

---

## 🖥️ Dashboard

The FaultGuard AI dashboard provides an industrial control-room style interface containing:

- System health status
- Machine indicators
- Sensor monitoring
- Live sensor trends
- Anomaly probability
- Diagnosis and recommended action
- Model validation
- Model performance
- Confusion matrix
- Historical fault records
- System information

The deployed dashboard is available at:

**https://faultguard-ai.streamlit.app/**

---

## 📁 Project Structure

```text
faultdiagnosis/
│
├── dashboard.py
├── mqtt_publisher.py
├── mqtt_subscriber.py
├── fault_detector.py
├── database.py
│
├── fault_model.joblib
├── scaler.joblib
├── model_metrics.json
├── latest_data.json
├── faults.json
├── historical_data.csv
│
├── archive/
│   └── SKAB/
│
├── requirements.txt
├── .gitignore
└── README.md
```

> File names may vary slightly depending on the local development version of the project.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application and ML pipeline |
| Pandas | Data processing |
| Scikit-learn | Machine learning |
| Random Forest | Fault/anomaly classification |
| StandardScaler | Feature scaling |
| Joblib | Model serialization |
| MQTT | Sensor-data communication |
| HiveMQ | MQTT broker |
| PostgreSQL | Historical data storage |
| Streamlit | Interactive dashboard |
| Git & GitHub | Version control and deployment |
| Streamlit Community Cloud | Dashboard deployment |

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd faultdiagnosis
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file and add the required MQTT/database configuration used by the project.

Do **not** commit passwords, API keys, MQTT credentials, or other secrets to GitHub.

### 5. Start the dashboard

```bash
streamlit run dashboard.py
```

The dashboard will normally open at:

```text
http://localhost:8501
```

---

## 📡 Running the MQTT Pipeline

For the local real-time workflow:

### Start the MQTT subscriber

```bash
python mqtt_subscriber.py
```

### Start the MQTT publisher

In another terminal:

```bash
python mqtt_publisher.py
```

The publisher sends sensor data to HiveMQ, while the subscriber receives the data, performs ML inference, generates diagnosis information, and stores the processed result.

---

## 🗄️ PostgreSQL

PostgreSQL is used in the local implementation to store processed sensor and fault records.

The database layer is handled through:

```text
database.py
```

The dashboard can use the PostgreSQL history when the database connection is available.

For the deployed Streamlit Cloud dashboard, historical records are also available through the committed:

```text
historical_data.csv
```

This allows the public dashboard to display historical sensor data without requiring access to the local PostgreSQL instance.

---

## 🔄 Dashboard Refresh

The dashboard includes a **Refresh Dashboard** control.

In the deployed demonstration environment, the refresh mechanism can cycle through records from `historical_data.csv` so that the dashboard can demonstrate changing machine readings without requiring the cloud application to connect directly to the local MQTT broker or PostgreSQL server.

---

## 🔐 Security

Sensitive configuration should remain outside the Git repository.

Use:

```text
.env
```

for local secrets and add it to `.gitignore`.

Never commit:

- MQTT passwords
- Database passwords
- API keys
- Authentication tokens
- Private credentials

---

## 🎯 Project Scope

### In Scope

- Sensor-data ingestion
- MQTT-based communication
- Machine-learning anomaly detection
- Fault diagnosis
- Severity classification
- Recommended actions
- Historical sensor/fault monitoring
- PostgreSQL data storage
- Interactive Streamlit dashboard
- Model performance visualization

### Out of Scope

- Direct physical control of industrial machinery
- Automatic repair of machine faults
- Safety-critical autonomous decisions
- Guaranteed prediction of every future machine failure

---

## 🔮 Future Enhancements

Possible future improvements include:

- More industrial datasets and machine types
- More detailed fault classification
- Real-time cloud IoT data ingestion
- Cloud-hosted PostgreSQL
- Automated alerts through email/SMS
- Explainable AI for individual predictions
- More advanced predictive-maintenance models
- Remaining Useful Life (RUL) prediction
- Role-based access control
- Deployment on an industrial IoT platform

---

## 👩‍💻 Project

**FaultGuard AI**  
AI-powered predictive maintenance and fault diagnosis system.

Built using Python, Machine Learning, MQTT, PostgreSQL, and Streamlit.
