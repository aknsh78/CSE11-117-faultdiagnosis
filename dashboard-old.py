import textwrap
import streamlit as st
import json
import os
import math
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="FaultGuard AI",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(textwrap.dedent("""
<style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #0b1120;
        color: #e5e7eb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    /* ---------- SIDEBAR ---------- */

    [data-testid="stSidebar"] {
        background: #080d18;
        border-right: 1px solid #1e293b;
    }

    [data-testid="stSidebar"] h1 {
        color: #f8fafc;
    }

    /* ---------- HEADER ---------- */

    .main-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 22px 26px;
        margin-bottom: 24px;
        border-radius: 16px;
        background: linear-gradient(
            135deg,
            #111827,
            #172033
        );
        border: 1px solid #263449;
    }

    .brand-title {
        font-size: 30px;
        font-weight: 800;
        color: #f8fafc;
        margin: 0;
    }

    .brand-subtitle {
        color: #94a3b8;
        font-size: 14px;
        margin-top: 5px;
    }

    .live-badge {
        padding: 8px 15px;
        border-radius: 30px;
        background: #052e24;
        color: #34d399;
        border: 1px solid #065f46;
        font-size: 13px;
        font-weight: 700;
    }

    /* ---------- STATUS ---------- */

    .status-card {
        padding: 25px;
        border-radius: 16px;
        margin-bottom: 20px;
        border: 1px solid #334155;
    }

    .status-normal {
        background: linear-gradient(
            135deg,
            #052e24,
            #071f1a
        );
        border-color: #065f46;
    }

    .status-anomaly {
        background: linear-gradient(
            135deg,
            #3b1111,
            #210b0b
        );
        border-color: #7f1d1d;
    }

    .status-unknown {
        background: linear-gradient(
            135deg,
            #3b2a11,
            #21180b
        );
        border-color: #854d0e;
    }

    .status-label {
        font-size: 13px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .status-value {
        font-size: 32px;
        font-weight: 800;
        margin-top: 5px;
    }

    .status-description {
        color: #cbd5e1;
        margin-top: 8px;
        font-size: 14px;
    }

    /* ---------- METRIC CARDS ---------- */

    .metric-card {
        background: #111827;
        border: 1px solid #263449;
        border-radius: 14px;
        padding: 18px;
        height: 125px;
    }

    .metric-title {
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 10px;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 27px;
        font-weight: 750;
    }

    .metric-unit {
        color: #64748b;
        font-size: 12px;
        margin-left: 4px;
    }

    /* ---------- SECTION ---------- */

    .section-title {
        font-size: 19px;
        font-weight: 750;
        color: #f8fafc;
        margin-top: 25px;
        margin-bottom: 14px;
    }

    /* ---------- SENSOR CARDS ---------- */

    .sensor-card {
        background: #111827;
        border: 1px solid #263449;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }

    .sensor-name {
        color: #94a3b8;
        font-size: 12px;
    }

    .sensor-value {
        color: #e2e8f0;
        font-size: 21px;
        font-weight: 700;
        margin-top: 5px;
    }

    /* ---------- AI PANEL ---------- */

    .ai-panel {
        background: linear-gradient(
            135deg,
            #111827,
            #151e31
        );
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 22px;
    }

    .probability-number {
        font-size: 42px;
        font-weight: 800;
        color: #f8fafc;
    }

    .probability-label {
        color: #94a3b8;
        font-size: 13px;
    }

    /* ---------- INFO BOX ---------- */

    .info-box {
        background: #111827;
        border: 1px solid #263449;
        border-radius: 12px;
        padding: 17px;
        margin-bottom: 12px;
    }

    .info-title {
        color: #64748b;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: .7px;
    }

    .info-value {
        color: #e2e8f0;
        font-size: 15px;
        margin-top: 6px;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #475569;
        font-size: 12px;
        padding: 25px;
        margin-top: 35px;
        border-top: 1px solid #1e293b;
    }

</style>
"""), unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

DATA_FILE = "latest_data.json"

if not os.path.exists(DATA_FILE):

    st.error("No sensor data available.")

    st.info(
        "Start the MQTT publisher and subscriber "
        "to generate latest_data.json."
    )

    st.stop()


try:

    with open(DATA_FILE, "r") as file:
        data = json.load(file)

except Exception as e:

    st.error(f"Unable to read sensor data: {e}")
    st.stop()


# =========================================================
# SAFE VALUE FUNCTION
# =========================================================

def value(key, default=0):

    result = data.get(key, default)

    if result is None:
        return default

    return result


def number(key, digits=2):

    try:
        return f"{float(value(key)):.{digits}f}"
    except:
        return "—"


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        "## ⚙️ FaultGuard AI"
    )

    st.caption(
        "Predictive Maintenance System"
    )

    st.markdown("---")

    st.markdown("### Machine")

    st.write(
        f"**Device:** {value('device_id', 'Unknown')}"
    )

    st.write(
        "**Status:** Connected"
    )

    st.markdown("---")

    st.markdown("### Data Source")

    st.write("SKAB Valve Dataset")

    st.write("Random Forest")

    st.write("MQTT + HiveMQ")

    st.write("PostgreSQL")

    st.markdown("---")

    if st.button(
        "🔄 Refresh Dashboard",
        use_container_width=True
    ):
        st.rerun()


# =========================================================
# HEADER
# =========================================================

st.html("""
<div class="main-header">

    <div>
        <div class="brand-title">
            ⚙️ FaultGuard AI
        </div>

        <div class="brand-subtitle">
            Intelligent Industrial Fault Detection & Predictive Maintenance
        </div>
    </div>

    <div class="live-badge">
        ● LIVE MONITORING
    </div>

</div>
""")


# =========================================================
# MACHINE STATUS
# =========================================================

fault = value("fault", "UNKNOWN")
severity = value("severity", "UNKNOWN")
fault_status = str(fault).strip().upper()

if fault_status == "NORMAL":

    status_class = "status-normal"
    status_icon = "🟢"
    status_text = "SYSTEM NORMAL"
    status_description = (
        "No abnormal sensor pattern detected."
    )

elif fault_status == "UNKNOWN":

    status_class = "status-unknown"
    status_icon = "⚪"
    status_text = "STATUS UNAVAILABLE"
    status_description = (
        "No valid machine health status is available."
    )

else:

    status_class = "status-anomaly"
    status_icon = "🔴"
    status_text = "ANOMALY DETECTED"
    status_description = (
        "The AI model detected an abnormal sensor pattern."
    )


st.html(f"""
<div class="status-card {status_class}">

    <div class="status-label">
        Machine Health Status
    </div>

    <div class="status-value">
        {status_icon} {status_text}
    </div>

    <div class="status-description">
        {status_description}
    </div>

</div>
""")


# =========================================================
# TOP METRICS
# =========================================================

st.markdown(
    '<div class="section-title">Key Machine Indicators</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.markdown(textwrap.dedent(f"""
    <div class="metric-card">
        <div class="metric-title">TEMPERATURE</div>
        <div class="metric-value">
            {number("temperature")}
            <span class="metric-unit">°C</span>
        </div>
    </div>
    """), unsafe_allow_html=True)


with c2:

    st.markdown(textwrap.dedent(f"""
    <div class="metric-card">
        <div class="metric-title">CURRENT</div>
        <div class="metric-value">
            {number("current")}
            <span class="metric-unit">A</span>
        </div>
    </div>
    """), unsafe_allow_html=True)


with c3:

    st.markdown(textwrap.dedent(f"""
    <div class="metric-card">
        <div class="metric-title">VOLTAGE</div>
        <div class="metric-value">
            {number("voltage")}
            <span class="metric-unit">V</span>
        </div>
    </div>
    """), unsafe_allow_html=True)


with c4:

    st.markdown(textwrap.dedent(f"""
    <div class="metric-card">
        <div class="metric-title">FLOW RATE</div>
        <div class="metric-value">
            {number("volume_flow_rate_rms")}
        </div>
    </div>
    """), unsafe_allow_html=True)


# =========================================================
# SENSOR MONITORING
# =========================================================

st.markdown(
    '<div class="section-title">Sensor Monitoring</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)


with left:

    sensors_left = [
        ("Accelerometer 1 RMS", "accelerometer1_rms"),
        ("Accelerometer 2 RMS", "accelerometer2_rms"),
        ("Temperature", "temperature"),
        ("Thermocouple", "thermocouple")
    ]

    for sensor_name, key in sensors_left:

        st.markdown(textwrap.dedent(f"""
        <div class="sensor-card">
            <div class="sensor-name">{sensor_name}</div>
            <div class="sensor-value">
                {number(key)}
            </div>
        </div>
        """), unsafe_allow_html=True)


with right:

    sensors_right = [
        ("Current", "current"),
        ("Pressure", "pressure"),
        ("Voltage", "voltage"),
        ("Volume Flow Rate RMS", "volume_flow_rate_rms")
    ]

    for sensor_name, key in sensors_right:

        st.markdown(textwrap.dedent(f"""
        <div class="sensor-card">
            <div class="sensor-name">{sensor_name}</div>
            <div class="sensor-value">
                {number(key)}
            </div>
        </div>
        """), unsafe_allow_html=True)


# =========================================================
# AI ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">AI Fault Analysis</div>',
    unsafe_allow_html=True
)

ai_left, ai_right = st.columns([1, 1])


with ai_left:

    try:
        anomaly_probability = float(value("anomaly_probability", 0))
        if not math.isfinite(anomaly_probability):
            anomaly_probability = 0.0
    except (TypeError, ValueError, OverflowError):
        anomaly_probability = 0.0

    anomaly_probability = min(max(anomaly_probability, 0.0), 1.0)
    probability_percent = anomaly_probability * 100

    st.markdown(textwrap.dedent(f"""
    <div class="ai-panel">

        <div class="probability-label">
            ANOMALY PROBABILITY
        </div>

        <div class="probability-number">
            {probability_percent:.1f}%
        </div>

    </div>
    """), unsafe_allow_html=True)

    st.progress(
        min(max(anomaly_probability, 0.0), 1.0)
    )


with ai_right:

    st.markdown(textwrap.dedent(f"""
    <div class="info-box">

        <div class="info-title">
            Detected Condition
        </div>

        <div class="info-value">
            {fault}
        </div>

    </div>

    <div class="info-box">

        <div class="info-title">
            Severity
        </div>

        <div class="info-value">
            {severity}
        </div>

    </div>
    """), unsafe_allow_html=True)


# =========================================================
# DIAGNOSIS
# =========================================================

st.markdown(
    '<div class="section-title">Diagnosis & Recommended Action</div>',
    unsafe_allow_html=True
)

d1, d2 = st.columns(2)


with d1:

    st.markdown(textwrap.dedent(f"""
    <div class="info-box">

        <div class="info-title">
            Possible Cause
        </div>

        <div class="info-value">
            {value("cause", "No information available")}
        </div>

    </div>
    """), unsafe_allow_html=True)


with d2:

    st.markdown(textwrap.dedent(f"""
    <div class="info-box">

        <div class="info-title">
            Recommended Action
        </div>

        <div class="info-value">
            {value("recommendation", "No recommendation available")}
        </div>

    </div>
    """), unsafe_allow_html=True)


# =========================================================
# GROUND TRUTH
# =========================================================

ground_truth = data.get("ground_truth")

if ground_truth is not None:

    st.markdown(
        '<div class="section-title">Model Validation</div>',
        unsafe_allow_html=True
    )

    v1, v2, v3 = st.columns(3)

    with v1:

        st.markdown(textwrap.dedent(f"""
        <div class="info-box">

            <div class="info-title">
                AI Prediction
            </div>

            <div class="info-value">
                {fault}
            </div>

        </div>
        """), unsafe_allow_html=True)

    with v2:

        st.markdown(textwrap.dedent(f"""
        <div class="info-box">

            <div class="info-title">
                Dataset Ground Truth
            </div>

            <div class="info-value">
                {ground_truth}
            </div>

        </div>
        """), unsafe_allow_html=True)

    with v3:

        prediction_matches = (
            str(fault).upper()
            == str(ground_truth).upper()
        )

        result = "MATCH" if prediction_matches else "MISMATCH"

        st.markdown(textwrap.dedent(f"""
        <div class="info-box">

            <div class="info-title">
                Prediction Validation
            </div>

            <div class="info-value">
                {result}
            </div>

        </div>
        """), unsafe_allow_html=True)


# =========================================================
# SYSTEM INFORMATION
# =========================================================

st.markdown(
    '<div class="section-title">System Information</div>',
    unsafe_allow_html=True
)

s1, s2, s3 = st.columns(3)

with s1:

    st.markdown(textwrap.dedent(f"""
    <div class="info-box">

        <div class="info-title">
            Device ID
        </div>

        <div class="info-value">
            {value("device_id", "Unknown")}
        </div>

    </div>
    """), unsafe_allow_html=True)


with s2:

    st.markdown(textwrap.dedent(f"""
    <div class="info-box">

        <div class="info-title">
            Last Sensor Update
        </div>

        <div class="info-value">
            {value("timestamp", "Unknown")}
        </div>

    </div>
    """), unsafe_allow_html=True)


with s3:

    st.markdown(textwrap.dedent(f"""
    <div class="info-box">

        <div class="info-title">
            Data Source
        </div>

        <div class="info-value">
            SKAB / Valve 1
        </div>

    </div>
    """), unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown(textwrap.dedent("""
<div class="footer">
    FaultGuard AI · Industrial Predictive Maintenance
    · MQTT · Machine Learning · PostgreSQL
</div>
"""), unsafe_allow_html=True)