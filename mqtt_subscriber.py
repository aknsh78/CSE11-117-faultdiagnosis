import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv

from fault_detector import detect_fault
from database import get_connection

load_dotenv()

BROKER = "a932b4866647456da95d3f085cde84fb.s1.eu.hivemq.cloud"
PORT = 8883

USERNAME = os.getenv("HIVEMQ_USERNAME")
PASSWORD = os.getenv("HIVEMQ_PASSWORD")

TOPIC = "factory/machine1/sensors"


def on_connect(client, userdata, flags, rc):

    print("Connection result:", rc)

    if rc == 0:
        print("Connected to HiveMQ Cloud")

        result = client.subscribe(TOPIC)

        print("Subscribe result:", result[0])
        print("Subscribed to:", TOPIC)

    else:
        print("Connection failed. Error code:", rc)


def on_message(client, userdata, msg):

    message = msg.payload.decode()

    print("\nReceived:")
    print(message)

    try:

        data = json.loads(message)

        # ------------------------------------------------
        # 1. Run ML fault detection
        # ------------------------------------------------

        ml_result = detect_fault(data)

        print("\n========== ML PREDICTION ==========")
        print("Status:", ml_result["status"])
        print("Normal probability:",
              ml_result["normal_probability"])
        print("Anomaly probability:",
              ml_result["anomaly_probability"])
        print("===================================")


        # ------------------------------------------------
        # 2. Create fault information
        # ------------------------------------------------

        if ml_result["prediction"] == 1:

            fault = "ANOMALY"
            severity = "HIGH"
            cause = "Abnormal sensor pattern detected"
            recommendation = "Inspect machine condition and sensor readings"

        else:

            fault = "NORMAL"
            severity = "LOW"
            cause = "No abnormal sensor pattern detected"
            recommendation = "Continue monitoring"


        # ------------------------------------------------
        # 3. Save data to PostgreSQL
        # ------------------------------------------------

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
    """
    INSERT INTO sensor_readings (
        device_id,
        timestamp,

        temperature,
        vibration,
        voltage,
        current,
        pressure,
        power,
        power_factor,

        accelerometer1_rms,
        accelerometer2_rms,
        thermocouple,
        volume_flow_rate_rms,

        fault,
        severity,
        cause,
        recommendation,

        anomaly_probability,
        ground_truth_fault
    )
    VALUES (
        %s, %s,
        %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s
    )
    """,
    (
        data.get("device_id"),
        data.get("timestamp"),

        # Existing fields
        data.get("Temperature"),
        data.get("Accelerometer1RMS"),
        data.get("Voltage"),
        data.get("Current"),
        data.get("Pressure"),
        data.get("power"),
        data.get("power_factor"),

        # Actual SKAB fields
        data.get("Accelerometer1RMS"),
        data.get("Accelerometer2RMS"),
        data.get("Thermocouple"),
        data.get("Volume Flow RateRMS"),

        # ML diagnosis
        fault,
        severity,
        cause,
        recommendation,

        ml_result["anomaly_probability"],

        # Ground truth from SKAB
        data.get("fault_type")
    )
)

        connection.commit()

        cursor.close()
        connection.close()

        print("Saved to PostgreSQL")


        # ------------------------------------------------
        # 4. Save latest data for dashboard
        # ------------------------------------------------

        dashboard_data = {

            "device_id": data.get("device_id"),

            "timestamp": data.get("timestamp"),

            "temperature": data.get("Temperature"),

            "accelerometer1_rms":
                data.get("Accelerometer1RMS"),

            "accelerometer2_rms":
                data.get("Accelerometer2RMS"),

            "current":
                data.get("Current"),

            "pressure":
                data.get("Pressure"),

            "thermocouple":
                data.get("Thermocouple"),

            "voltage":
                data.get("Voltage"),

            "volume_flow_rate_rms":
                data.get("Volume Flow RateRMS"),

            "fault":
                fault,

            "severity":
                severity,

            "cause":
                cause,

            "recommendation":
                recommendation,

            "normal_probability":
                ml_result["normal_probability"],

            "anomaly_probability":
                ml_result["anomaly_probability"],

            "ground_truth":
                data.get("fault_type"),

            "anomaly":
                data.get("anomaly"),

            "source_file":
                 data.get("source_file")
        }


        with open("latest_data.json", "w") as file:

            json.dump(
                dashboard_data,
                file,
                indent=4
            )


        # ------------------------------------------------
        # 5. Display diagnosis
        # ------------------------------------------------

        print("\n========== DIAGNOSIS ==========")

        print("Detected Fault:", fault)

        print("Severity:", severity)

        print("Possible Cause:", cause)

        print("Recommended Action:",
              recommendation)

        print("Anomaly Probability:",
              ml_result["anomaly_probability"])

        print("================================")


    except json.JSONDecodeError:

        print(
            "Error: Received message is not valid JSON"
        )

    except KeyError as e:

        print("Missing sensor field:", e)

    except Exception as e:

        print("Diagnosis error:", e)


# ------------------------------------------------
# MQTT CLIENT
# ------------------------------------------------

client = mqtt.Client()

client.username_pw_set(
    USERNAME,
    PASSWORD
)

client.tls_set()

client.on_connect = on_connect

client.on_message = on_message


print("Username loaded:", USERNAME)

print(
    "Password loaded:",
    bool(PASSWORD)
)

print("Connecting...")


client.connect(
    BROKER,
    PORT,
    60
)


client.loop_forever()