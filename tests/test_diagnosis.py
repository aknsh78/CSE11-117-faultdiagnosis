from diagnosis.diagnosis_engine import diagnose


def test_normal():
    data = {
        "temperature": 40,
        "vibration": 2,
        "voltage": 230,
        "current": 5,
        "pressure": 5
    }

    result = diagnose(data)

    assert result["fault"] == "NORMAL"
    print("NORMAL test: PASS")


def test_bearing_fault():
    data = {
        "temperature": 70,
        "vibration": 8,
        "voltage": 230,
        "current": 6,
        "pressure": 5
    }

    result = diagnose(data)

    assert result["fault"] == "BEARING_FAULT"
    print("BEARING_FAULT test: PASS")


def test_overload():
    data = {
        "temperature": 70,
        "vibration": 4,
        "voltage": 225,
        "current": 12,
        "pressure": 5
    }

    result = diagnose(data)

    assert result["fault"] == "OVERLOAD"
    print("OVERLOAD test: PASS")


def test_voltage_fault():
    data = {
        "temperature": 45,
        "vibration": 3,
        "voltage": 190,
        "current": 6,
        "pressure": 5
    }

    result = diagnose(data)

    assert result["fault"] == "VOLTAGE_FAULT"
    print("VOLTAGE_FAULT test: PASS")


def test_pressure_fault():
    data = {
        "temperature": 45,
        "vibration": 3,
        "voltage": 230,
        "current": 6,
        "pressure": 2
    }

    result = diagnose(data)

    assert result["fault"] == "PRESSURE_FAULT"
    print("PRESSURE_FAULT test: PASS")


if __name__ == "__main__":
    test_normal()
    test_bearing_fault()
    test_overload()
    test_voltage_fault()
    test_pressure_fault()

    print("\nAll diagnosis tests passed!")