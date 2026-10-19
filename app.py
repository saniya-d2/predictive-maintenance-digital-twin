import streamlit as st
import pandas as pd
import plotly.express as px

from simulator import MACHINES, simulate_factory
from health_monitor import assess_machine

st.set_page_config(
    page_title="Factory Digital Twin",
    page_icon="🏭",
    layout="wide",
)

st.title("🏭 Predictive Maintenance Digital Twin")
st.caption(
    "Simulated five-machine factory | "
    "Temperature • Vibration • RPM • Load • Current"
)

# Keep the simulation cycle and history between dashboard reruns.
if "cycle" not in st.session_state:
    st.session_state.cycle = 1

if "history" not in st.session_state:
    st.session_state.history = []

if "current_readings" not in st.session_state:
    st.session_state.current_readings = simulate_factory(1)
    st.session_state.history.extend(st.session_state.current_readings)

if st.button("▶ Run Next Factory Cycle"):
    st.session_state.cycle += 1
    new_readings = simulate_factory(st.session_state.cycle)
    st.session_state.current_readings = new_readings
    st.session_state.history.extend(new_readings)

readings = st.session_state.current_readings
reports = [assess_machine(r) for r in readings]

df = pd.DataFrame(readings)
health_df = pd.DataFrame(reports)

st.subheader(f"Factory Cycle {st.session_state.cycle}")

# Summary metrics
total_machines = len(MACHINES)
critical_count = sum(r["status"] == "CRITICAL" for r in reports)
warning_count = sum(r["status"] == "WARNING" for r in reports)
normal_count = sum(r["status"] == "NORMAL" for r in reports)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Machines", total_machines)
c2.metric("Normal", normal_count)
c3.metric("Warning", warning_count)
c4.metric("Critical", critical_count)

st.divider()
st.subheader("Machine Status")

for reading, report in zip(readings, reports):
    with st.container(border=True):
        left, right = st.columns([3, 1])

        with left:
            st.markdown(f"### {reading['machine']}")

            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("Temperature", f"{reading['temperature_c']:.1f} °C")
            m2.metric("Vibration", f"{reading['vibration_mm_s']:.2f} mm/s")
            m3.metric("RPM", f"{reading['rpm']:.0f}")
            m4.metric("Load", f"{reading['load_percent']:.1f}%")
            m5.metric("Current", f"{reading['current_amp']:.2f} A")

        with right:
            st.metric("Risk Score", f"{report['risk_score']}/100")

            if report["status"] == "CRITICAL":
                st.error("🔴 CRITICAL")
            elif report["status"] == "WARNING":
                st.warning("🟠 WARNING")
            else:
                st.success("🟢 NORMAL")

            for warning in report["warnings"]:
                st.caption(f"• {warning}")

st.divider()
st.subheader("Sensor Comparison")

sensor = st.selectbox(
    "Choose a measurement",
    [
        "temperature_c",
        "vibration_mm_s",
        "rpm",
        "load_percent",
        "current_amp",
    ],
    format_func=lambda value: {
        "temperature_c": "Temperature (°C)",
        "vibration_mm_s": "Vibration (mm/s)",
        "rpm": "RPM",
        "load_percent": "Load (%)",
        "current_amp": "Current (A)",
    }[value],
)

fig = px.bar(
    df,
    x="machine",
    y=sensor,
    color="machine",
    title="Current sensor readings by machine",
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Machine Risk Scores")

risk_chart = px.bar(
    health_df,
    x="machine",
    y="risk_score",
    color="status",
    range_y=[0, 100],
    title="Simulated health risk (0–100)",
)
st.plotly_chart(risk_chart, use_container_width=True)

st.caption(
    "Simulation only: values and thresholds are illustrative, "
    "not real machine measurements or calibrated failure probabilities."
)