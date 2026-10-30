# FaultGuard AI – Test Results

## 1. Environment
- Python: 3.13.14
- Operating System: Windows
- MQTT Broker: HiveMQ Cloud
- Database: PostgreSQL 18
- Dashboard: Streamlit

## 2. Test Results

| Test ID | Test Description | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| T01 | Python dependency check | Required packages installed | Packages found in virtual environment | PASS |
| T02 | HiveMQ connection | Successful broker connection | Connection successful | PASS |
| T03 | MQTT publisher | Sensor messages published | Repeated JSON messages published | PASS |
| T04 | MQTT subscriber | Messages received | Sensor messages received | PASS |
| T05 | ML inference | Normal/anomaly prediction | Predictions displayed with probabilities | PASS |
| T06 | Fault diagnosis | Cause and severity generated | Diagnosis and recommendation displayed | PASS |
| T07 | PostgreSQL connection | Database connection successful | Database connected successfully | PASS |
| T08 | Database storage | Sensor records saved | Subscriber reported saved to PostgreSQL; records retrieved | PASS |
| T09 | Dashboard | Sensor readings displayed | Dashboard displayed sensor readings | PASS |
| T10 | Dashboard refresh | Values update | Changing values observed after refresh | OBSERVED |

## 3. Test Evidence
Screenshots are stored in the tests/evidence folder:
- MQTT publisher output
- MQTT subscriber output
- Anomaly prediction and diagnosis
- PostgreSQL records
- Streamlit dashboard

## 4. Limitations
- Input data is generated using the SKAB dataset and a software simulator.
- Physical ESP32 hardware deployment has not been verified.
- Model metrics have not been independently recalculated.
- Dashboard data sources have not been independently traced for every displayed component.
- Diagnostic causes are rule-based suggestions, not confirmed physical faults.

## 5. Conclusion
The observed tests demonstrate successful MQTT communication, subscriber-side inference, diagnosis output, PostgreSQL access, and dashboard display during the test session.