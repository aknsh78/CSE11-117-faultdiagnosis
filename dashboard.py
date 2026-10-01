import plotly.express as px
import plotly.graph_objects as go
import textwrap
import streamlit as st
import json
import os
import math
import pandas as pd

try:
    from database import get_connection
except Exception:
    get_connection = None
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

st.html("""
<style>

    :root {
        --navy-950: #07111f;
        --navy-900: #0b1b2b;
        --navy-800: #10283b;
        --panel: rgba(17, 43, 60, .88);
        --line: #24516a;
        --text: #f4fbff;
        --muted: #91b2c2;
        --teal: #35d0c2;
        --cyan: #57c7ff;
        --amber: #ffbd69;
        --coral: #ff7b78;
    }

    .stApp {
        background: radial-gradient(circle at 82% 0%, #123b4b 0%, transparent 34%),
                    linear-gradient(135deg, var(--navy-950) 0%, #091827 52%, #0d2332 100%);
        color: var(--text);
        font-family: "Trebuchet MS", "Segoe UI", sans-serif;
    }

    .block-container {
        max-width: 1500px;
        padding: 2.5rem 2.5rem 2rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #081521 0%, #0b2431 100%);
        border-right: 1px solid #1d4b60;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--text);
        letter-spacing: .02em;
    }

    [data-testid="stSidebar"] hr {
        border-color: #1d4b60;
    }

    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] p {
        color: var(--muted);
    }

    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #1a6c75, #1b9b93);
        border: 1px solid #46d5c8;
        color: #effffc;
        font-weight: 700;
        box-shadow: 0 8px 22px rgba(21, 179, 167, .18);
    }

    .main-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 27px 30px;
        margin-bottom: 24px;
        border-radius: 18px;
        background: linear-gradient(120deg, rgba(17, 61, 78, .98), rgba(13, 34, 53, .94));
        border: 1px solid #2e7186;
        box-shadow: 0 18px 45px rgba(0, 0, 0, .22);
        position: relative;
        overflow: hidden;
    }

    .main-header::after {
        content: "";
        position: absolute;
        width: 210px;
        height: 210px;
        right: -70px;
        top: -100px;
        border: 1px solid rgba(87, 199, 255, .35);
        border-radius: 50%;
        box-shadow: 0 0 0 18px rgba(87, 199, 255, .05), 0 0 0 38px rgba(87, 199, 255, .035);
    }

    .brand-title {
        color: var(--text);
        font-size: 31px;
        font-weight: 800;
        letter-spacing: .01em;
        margin: 0;
    }

    .brand-subtitle {
        color: #a9c8d5;
        font-size: 14px;
        margin-top: 7px;
    }

    .live-badge {
        z-index: 1;
        padding: 9px 16px;
        border-radius: 999px;
        background: rgba(32, 176, 157, .14);
        color: #70f5d6;
        border: 1px solid #36bda9;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: .08em;
        box-shadow: 0 0 24px rgba(53, 208, 194, .12);
    }

    .status-card,
    .metric-card,
    .sensor-card,
    .info-box,
    .ai-panel {
        border-radius: 15px;
        border: 1px solid var(--line);
        box-shadow: 0 10px 26px rgba(0, 0, 0, .14);
    }

    .status-card {
        padding: 25px 28px;
        margin-bottom: 20px;
    }

    .status-normal {
        background: linear-gradient(105deg, rgba(11, 92, 88, .9), rgba(9, 49, 57, .94));
        border-color: #2fbdae;
    }

    .status-anomaly {
        background: linear-gradient(105deg, rgba(128, 48, 55, .9), rgba(64, 28, 39, .94));
        border-color: #ff7777;
    }

    .status-unknown {
        background: linear-gradient(105deg, rgba(126, 83, 32, .9), rgba(62, 48, 26, .94));
        border-color: var(--amber);
    }

    .status-label,
    .metric-title,
    .sensor-name,
    .info-title,
    .probability-label {
        color: var(--muted);
        font-size: 12px;
        letter-spacing: .08em;
        text-transform: uppercase;
    }

    .status-value {
        color: var(--text);
        font-size: 32px;
        font-weight: 800;
        margin-top: 6px;
    }

    .status-description {
        color: #d2e5eb;
        margin-top: 8px;
        font-size: 14px;
    }

    .metric-card {
        background: linear-gradient(145deg, rgba(18, 51, 69, .94), rgba(12, 31, 47, .94));
        padding: 18px;
        height: 125px;
        border-top: 2px solid rgba(87, 199, 255, .55);
    }

    .metric-title { margin-bottom: 10px; }

    .metric-value {
        color: var(--text);
        font-size: 27px;
        font-weight: 800;
    }

    .metric-unit { color: var(--cyan); font-size: 12px; margin-left: 4px; }

    .section-title {
        color: var(--text);
        font-size: 19px;
        font-weight: 800;
        margin: 28px 0 14px;
        border-left: 3px solid var(--teal);
        padding-left: 11px;
    }

    .sensor-card {
        background: linear-gradient(145deg, rgba(17, 48, 64, .9), rgba(11, 29, 44, .92));
        padding: 16px;
        margin-bottom: 12px;
        border-left: 3px solid rgba(255, 189, 105, .8);
    }

    .sensor-value { color: #f0fbff; font-size: 21px; font-weight: 800; margin-top: 5px; }

    .ai-panel {
        background: linear-gradient(145deg, rgba(20, 62, 78, .96), rgba(12, 34, 53, .96));
        padding: 22px;
        border-color: #34788d;
    }

    .probability-number { color: var(--cyan); font-size: 42px; font-weight: 800; }

    .info-box {
        background: rgba(17, 48, 64, .82);
        padding: 17px;
        margin-bottom: 12px;
    }

    .info-title { color: #78a4b5; }
    .info-value { color: #e2f5fa; font-size: 15px; margin-top: 6px; }

    .footer {
        text-align: center;
        color: #6b96a5;
        font-size: 12px;
        padding: 25px;
        margin-top: 35px;
        border-top: 1px solid #1d4b60;
    }

    @media (max-width: 700px) {
        .block-container { padding: 1.25rem 1rem; }
        .main-header { align-items: flex-start; flex-direction: column; gap: 18px; padding: 22px; }
        .brand-title { font-size: 26px; }
        .status-value { font-size: 25px; }
    }

</style>
""")


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

st.markdown("**" + "Key Machine Indicators" + "**")

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.html(f"""
    <div class="metric-card">
        <div class="metric-title">TEMPERATURE</div>
        <div class="metric-value">
            {number("temperature")}
            <span class="metric-unit">°C</span>
        </div>
    </div>
    """)


with c2:

    st.html(f"""
    <div class="metric-card">
        <div class="metric-title">CURRENT</div>
        <div class="metric-value">
            {number("current")}
            <span class="metric-unit">A</span>
        </div>
    </div>
    """)


with c3:

    st.html(f"""
    <div class="metric-card">
        <div class="metric-title">VOLTAGE</div>
        <div class="metric-value">
            {number("voltage")}
            <span class="metric-unit">V</span>
        </div>
    </div>
    """)


with c4:

    st.html(f"""
    <div class="metric-card">
        <div class="metric-title">FLOW RATE</div>
        <div class="metric-value">
            {number("volume_flow_rate_rms")}
        </div>
    </div>
    """)


# =========================================================
# SENSOR MONITORING
# =========================================================

st.markdown("**" + "Sensor Monitoring" + "**")

left, right = st.columns(2)


with left:

    sensors_left = [
        ("Accelerometer 1 RMS", "accelerometer1_rms"),
        ("Accelerometer 2 RMS", "accelerometer2_rms"),
        ("Temperature", "temperature"),
        ("Thermocouple", "thermocouple")
    ]

    for sensor_name, key in sensors_left:

        st.html(f"""
        <div class="sensor-card">
            <div class="sensor-name">{sensor_name}</div>
            <div class="sensor-value">
                {number(key)}
            </div>
        </div>
        """)


with right:

    sensors_right = [
        ("Current", "current"),
        ("Pressure", "pressure"),
        ("Voltage", "voltage"),
        ("Volume Flow Rate RMS", "volume_flow_rate_rms")
    ]

    for sensor_name, key in sensors_right:

        st.html(f"""
        <div class="sensor-card">
            <div class="sensor-name">{sensor_name}</div>
            <div class="sensor-value">
                {number(key)}
            </div>
        </div>
        """)


# =========================================================
# LIVE SENSOR TRENDS
# =========================================================

st.markdown(
    '<div class="section-title">📈 Live Sensor Trends</div>',
    unsafe_allow_html=True
)

try:
    connection = get_connection()

    history = pd.read_sql_query(
        """
        SELECT
            timestamp,
            temperature,
            current,
            voltage,
            accelerometer1_rms,
            accelerometer2_rms,
            anomaly_probability,
            fault
        FROM public.sensor_readings
        ORDER BY timestamp DESC
        LIMIT 100
        """,
        connection
    )

    connection.close()

    history["timestamp"] = pd.to_datetime(history["timestamp"])
    history = history.sort_values("timestamp")

except Exception as e:
    st.error(f"Unable to load historical sensor data: {e}")
    history = pd.DataFrame()


if not history.empty:

    # -----------------------------------------------------
    # Temperature
    # -----------------------------------------------------

    st.markdown("### 🌡️ Temperature")

    fig_temp = px.line(
        history,
        x="timestamp",
        y="temperature",
        markers=False,
        labels={
            "timestamp": "Time",
            "temperature": "Temperature (°C)"
        }
    )

    fig_temp.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Time",
        yaxis_title="Temperature (°C)",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_temp,
        use_container_width=True
    )


    # -----------------------------------------------------
    # Current + Voltage
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### ⚡ Current")

        fig_current = px.line(
            history,
            x="timestamp",
            y="current",
            labels={
                "timestamp": "Time",
                "current": "Current (A)"
            }
        )

        fig_current.update_layout(
            height=320,
            margin=dict(l=20, r=20, t=20, b=20),
            hovermode="x unified"
        )

        st.plotly_chart(
            fig_current,
            use_container_width=True
        )


    with col2:

        st.markdown("### 🔌 Voltage")

        fig_voltage = px.line(
            history,
            x="timestamp",
            y="voltage",
            labels={
                "timestamp": "Time",
                "voltage": "Voltage (V)"
            }
        )

        fig_voltage.update_layout(
            height=320,
            margin=dict(l=20, r=20, t=20, b=20),
            hovermode="x unified"
        )

        st.plotly_chart(
            fig_voltage,
            use_container_width=True
        )


    # -----------------------------------------------------
    # Vibration
    # -----------------------------------------------------

    st.markdown("### 📳 Vibration")

    fig_vibration = go.Figure()

    fig_vibration.add_trace(
        go.Scatter(
            x=history["timestamp"],
            y=history["accelerometer1_rms"],
            mode="lines",
            name="Accelerometer 1 RMS"
        )
    )

    fig_vibration.add_trace(
        go.Scatter(
            x=history["timestamp"],
            y=history["accelerometer2_rms"],
            mode="lines",
            name="Accelerometer 2 RMS"
        )
    )

    fig_vibration.update_layout(
        height=350,
        xaxis_title="Time",
        yaxis_title="RMS",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig_vibration,
        use_container_width=True
    )


    # -----------------------------------------------------
    # Anomaly Probability
    # -----------------------------------------------------

    st.markdown("### 🤖 Anomaly Probability")

    probability = (
        history["anomaly_probability"]
        .fillna(0)
        .clip(0, 1)
        * 100
    )

    fig_probability = px.line(
        x=history["timestamp"],
        y=probability,
        labels={
            "x": "Time",
            "y": "Anomaly Probability (%)"
        }
    )

    fig_probability.update_yaxes(
        range=[0, 100]
    )

    fig_probability.update_layout(
        height=350,
        hovermode="x unified",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig_probability,
        use_container_width=True
    )


# =========================================================
# DIAGNOSIS
# =========================================================

st.markdown("**" + "Diagnosis & Recommended Action" + "**")

d1, d2 = st.columns(2)


with d1:

    st.html(f"""
    <div class="info-box">

        <div class="info-title">
            Possible Cause
        </div>

        <div class="info-value">
            {value("cause", "No information available")}
        </div>

    </div>
    """)


with d2:

    st.html(f"""
    <div class="info-box">

        <div class="info-title">
            Recommended Action
        </div>

        <div class="info-value">
            {value("recommendation", "No recommendation available")}
        </div>

    </div>
    """)


# =========================================================
# GROUND TRUTH
# =========================================================

ground_truth = data.get("ground_truth_fault", data.get("ground_truth"))

if ground_truth is not None:

    st.markdown("**" + "Model Validation" + "**")

    v1, v2, v3 = st.columns(3)

    with v1:

        st.html(f"""
        <div class="info-box">

            <div class="info-title">
                AI Prediction
            </div>

            <div class="info-value">
                {fault}
            </div>

        </div>
        """)

    with v2:

        st.html(f"""
        <div class="info-box">

            <div class="info-title">
                Dataset Ground Truth
            </div>

            <div class="info-value">
                {ground_truth}
            </div>

        </div>
        """)

    with v3:

        prediction_matches = (
            str(fault).upper()
            == str(ground_truth).upper()
        )

        result = "MATCH" if prediction_matches else "MISMATCH"

        st.html(f"""
        <div class="info-box">

            <div class="info-title">
                Prediction Validation
            </div>

            <div class="info-value">
                {result}
            </div>

        </div>
        """)

# =========================================================
# MODEL PERFORMANCE
# =========================================================

st.markdown("**" + "Model Performance" + "**")

try:
    with open("model_metrics.json", "r") as file:
        metrics = json.load(file)

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.html(f"""
        <div class="info-box">
            <div class="info-title">Accuracy</div>
            <div class="info-value">
                {metrics["accuracy"] * 100:.2f}%
            </div>
        </div>
        """)

    with m2:
        st.html(f"""
        <div class="info-box">
            <div class="info-title">Anomaly Precision</div>
            <div class="info-value">
                {metrics["anomaly"]["precision"] * 100:.2f}%
            </div>
        </div>
        """)

    with m3:
        st.html(f"""
        <div class="info-box">
            <div class="info-title">Anomaly Recall</div>
            <div class="info-value">
                {metrics["anomaly"]["recall"] * 100:.2f}%
            </div>
        </div>
        """)

    with m4:
        st.html(f"""
        <div class="info-box">
            <div class="info-title">Anomaly F1 Score</div>
            <div class="info-value">
                {metrics["anomaly"]["f1_score"] * 100:.2f}%
            </div>
        </div>
        """)
    st.markdown("### Confusion Matrix")

    cm = metrics["confusion_matrix"]

    c1, c2 = st.columns(2)

    with c1:
        st.html(f"""
        <div class="info-box">
            <div class="info-title">Actual Normal → Predicted Normal</div>
            <div class="info-value">{cm[0][0]}</div>
        </div>
        """)

    with c2:
        st.html(f"""
        <div class="info-box">
            <div class="info-title">Actual Normal → Predicted Anomaly</div>
            <div class="info-value">{cm[0][1]}</div>
        </div>
        """)

    c3, c4 = st.columns(2)

    with c3:
        st.html(f"""
        <div class="info-box">
            <div class="info-title">Actual Anomaly → Predicted Normal</div>
            <div class="info-value">{cm[1][0]}</div>
        </div>
        """)

    with c4:
        st.html(f"""
        <div class="info-box">
            <div class="info-title">Actual Anomaly → Predicted Anomaly</div>
            <div class="info-value">{cm[1][1]}</div>
        </div>
        """)

except Exception as e:
    st.warning(f"Model metrics unavailable: {e}")
# =========================================================
# HISTORICAL FAULT RECORDS
# =========================================================

st.markdown("**Historical Fault Records**")

try:

    connection = get_connection()

    # Get recent records
    fault_history = pd.read_sql_query(
        """
        SELECT
            timestamp,
            fault,
            severity,
            cause,
            recommendation,
            anomaly_probability,
            ground_truth_fault
        FROM public.sensor_readings
        ORDER BY timestamp DESC
        LIMIT 100
        """,
        connection
    )

    connection.close()

    if not fault_history.empty:

        # -----------------------------
        # Summary counts
        # -----------------------------

        total_records = len(fault_history)
        anomaly_records = (
            fault_history["fault"]
            .astype(str)
            .str.upper()
            .eq("ANOMALY")
            .sum()
        )

        normal_records = (
            fault_history["fault"]
            .astype(str)
            .str.upper()
            .eq("NORMAL")
            .sum()
        )

        s1, s2, s3 = st.columns(3)

        with s1:
            st.html(f"""
            <div class="info-box">
                <div class="info-title">Total Records</div>
                <div class="info-value">{total_records}</div>
            </div>
            """)

        with s2:
            st.html(f"""
            <div class="info-box">
                <div class="info-title">Normal Records</div>
                <div class="info-value">{normal_records}</div>
            </div>
            """)

        with s3:
            st.html(f"""
            <div class="info-box">
                <div class="info-title">Anomaly Records</div>
                <div class="info-value">{anomaly_records}</div>
            </div>
            """)

        # -----------------------------
        # Fault filter
        # -----------------------------

        filter_option = st.selectbox(
            "Filter Records",
            ["ALL", "NORMAL", "ANOMALY"]
        )

        if filter_option != "ALL":
            fault_history = fault_history[
                fault_history["fault"]
                .astype(str)
                .str.upper()
                == filter_option
            ]

        # -----------------------------
        # Convert probability to %
        # -----------------------------

        fault_history["anomaly_probability"] = (
            fault_history["anomaly_probability"] * 100
        ).round(2)

        # -----------------------------
        # Rename columns
        # -----------------------------

        fault_history = fault_history.rename(
            columns={
                "timestamp": "Time",
                "fault": "Fault",
                "severity": "Severity",
                "cause": "Possible Cause",
                "recommendation": "Recommended Action",
                "anomaly_probability": "Anomaly Probability (%)",
                "ground_truth_fault": "Ground Truth"
            }
        )

        st.dataframe(
            fault_history,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No historical sensor records available.")

except Exception as e:

    st.error(f"Unable to load historical fault records: {e}")
# =========================================================
# SYSTEM INFORMATION
# =========================================================

st.markdown("**" + "System Information" + "**")

s1, s2, s3 = st.columns(3)

with s1:

    st.html(f"""
    <div class="info-box">

        <div class="info-title">
            Device ID
        </div>

        <div class="info-value">
            {value("device_id", "Unknown")}
        </div>

    </div>
    """)


with s2:

    st.html(f"""
    <div class="info-box">

        <div class="info-title">
            Last Sensor Update
        </div>

        <div class="info-value">
            {value("timestamp", "Unknown")}
        </div>

    </div>
    """)


with s3:

    st.html(f"""
    <div class="info-box">

        <div class="info-title">
            Data Source
        </div>

        <div class="info-value">
            SKAB / Valve 1
        </div>

    </div>
    """)


# =========================================================
# FOOTER
# =========================================================

st.html("""
<div class="footer">
    FaultGuard AI · Industrial Predictive Maintenance
    · MQTT · Machine Learning · PostgreSQL
</div>
""")