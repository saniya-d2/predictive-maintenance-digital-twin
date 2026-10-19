"""Connect the factory simulator to the machine health monitor."""

from simulator import MACHINES, simulate_factory
from health_monitor import assess_machine


def run_factory_cycle(cycle):
    """Simulate one cycle and assess every machine."""
    readings = simulate_factory(cycle)
    reports = []

    for reading in readings:
        report = assess_machine(reading)
        reports.append({
            "reading": reading,
            "health": report,
        })

    return reports


def display_cycle(cycle, reports):
    """Display readings and health status for every machine."""
    print(f"\n{'=' * 100}")
    print(f"FACTORY CYCLE {cycle}")
    print("=" * 100)

    for item in reports:
        reading = item["reading"]
        health = item["health"]

        print(
            f"{reading['machine']:8} | "
            f"Temp: {reading['temperature_c']:6.2f} C | "
            f"Vibration: {reading['vibration_mm_s']:5.2f} mm/s | "
            f"RPM: {reading['rpm']:7.2f} | "
            f"Load: {reading['load_percent']:5.2f}% | "
            f"Current: {reading['current_amp']:5.2f} A | "
            f"Risk: {health['risk_score']:3}/100 | "
            f"Status: {health['status']}"
        )

        for warning in health["warnings"]:
            print(f"    WARNING: {warning}")


def main():
    print("PREDICTIVE MAINTENANCE DIGITAL TWIN")
    print("Five-machine factory simulation")

    for cycle in range(1, 71):
        reports = run_factory_cycle(cycle)
        display_cycle(cycle, reports)

    print("\nFactory simulation finished successfully.")


if __name__ == "__main__":
    main()