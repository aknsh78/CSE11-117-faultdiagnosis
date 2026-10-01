import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_BASE = os.path.join(BASE_DIR, "faults.json")


with open(KNOWLEDGE_BASE, "r") as file:
    fault_knowledge = json.load(file)


def diagnose(data):

    temperature = data["temperature"]
    vibration = data["vibration"]
    voltage = data["voltage"]
    current = data["current"]
    pressure = data["pressure"]

    # Detect fault from sensor values
    if vibration > 5:
        fault = "BEARING_FAULT"

    elif current > 9:
        fault = "OVERLOAD"

    elif voltage < 210 or voltage > 240:
        fault = "VOLTAGE_FAULT"

    elif pressure < 4 or pressure > 6:
        fault = "PRESSURE_FAULT"

    else:
        fault = "NORMAL"

    # Get explanation from knowledge base
    knowledge = fault_knowledge[fault]

    return {
        "fault": fault,
        "severity": knowledge["severity"],
        "cause": knowledge["cause"],
        "recommendation": knowledge["recommendation"]
    }