"""Rule-based health monitoring for the simulated factory."""

THRESHOLDS = {
    "temperature_c": (70, 90, "high"),
    "vibration_mm_s": (4, 8, "high"),
    "rpm": (850, 700, "low"),
    "load_percent": (80, 95, "high"),
    "current_amp": (6.5, 9, "high"),
}


def sensor_risk(value, warning, critical, direction):
    """Return a 0-100 severity score for one sensor."""
    if direction == "high":
        if value <= warning:
            return 0.0
        if value >= critical:
            return 100.0
        return (value - warning) / (critical - warning) * 100

    # For RPM, unusually low values are concerning.
    if value >= warning:
        return 0.0
    if value <= critical:
        return 100.0
    return (warning - value) / (warning - critical) * 100


def assess_machine(reading):
    """Evaluate five measurements and return an explainable risk report."""
    scores = {}
    warnings = []

    for sensor, (warning, critical, direction) in THRESHOLDS.items():
        value = reading[sensor]
        score = sensor_risk(value, warning, critical, direction)
        scores[sensor] = score

        if score > 0:
            label = sensor.replace("_", " ")
            warnings.append(
                f"{label} is outside its normal simulation range"
            )

    average_risk = sum(scores.values()) / len(scores)
    highest_risk = max(scores.values())

    # Transparent composite score: combines overall and worst sensor severity.
    risk_score = round(0.6 * average_risk + 0.4 * highest_risk)

    if risk_score >= 60:
        status = "CRITICAL"
    elif risk_score >= 25:
        status = "WARNING"
    else:
        status = "NORMAL"

    return {
        "machine": reading["machine"],
        "cycle": reading["cycle"],
        "risk_score": risk_score,
        "status": status,
        "sensor_scores": {
            sensor: round(score, 1)
            for sensor, score in scores.items()
        },
        "warnings": warnings,
    }


if __name__ == "__main__":
    # Test the monitor using the simulator's generated readings.
    from simulator import simulate_factory

    print("MACHINE HEALTH MONITOR")
    print("=" * 65)

    for cycle in [1, 30, 40, 60, 70]:
        print(f"\nCycle {cycle}")

        for reading in simulate_factory(cycle):
            report = assess_machine(reading)
            print(
                f"{report['machine']:8} | "
                f"Risk: {report['risk_score']:3}/100 | "
                f"Status: {report['status']}"
            )

            for warning in report["warnings"]:
                print(f"    - {warning}")