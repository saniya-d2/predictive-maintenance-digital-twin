import random
import time

MACHINES = ["Feeder", "Cutter", "Welder", "Press", "Packer"]


def generate_reading(machine, cycle):
    """Generate simulated sensor readings for one machine."""

    # Normal operating conditions
    temperature = random.uniform(45, 65)       # Degrees Celsius
    vibration = random.uniform(1.0, 3.0)       # mm/s RMS
    rpm = random.uniform(900, 1100)            # Revolutions per minute
    load = random.uniform(40, 75)              # Percentage
    current = random.uniform(3.0, 6.0)         # Amperes

    # Gradually simulate a developing fault in the Welder
    if machine == "Welder" and cycle >= 30:
        fault_progress = min((cycle - 29) / 40, 1.0)

        temperature += 25 * fault_progress
        vibration += 5 * fault_progress
        rpm -= 180 * fault_progress
        load += 20 * fault_progress
        current += 3 * fault_progress

    # Keep the values within plausible simulation limits
    temperature = max(0, temperature)
    vibration = max(0, vibration)
    rpm = max(0, rpm)
    load = min(100, max(0, load))
    current = max(0, current)

    return {
        "cycle": cycle,
        "machine": machine,
        "temperature_c": round(temperature, 2),
        "vibration_mm_s": round(vibration, 2),
        "rpm": round(rpm, 2),
        "load_percent": round(load, 2),
        "current_amp": round(current, 2),
    }


def simulate_factory(cycle):
    """Generate readings from all five factory machines."""
    return [
        generate_reading(machine, cycle)
        for machine in MACHINES
    ]


if __name__ == "__main__":
    print("FACTORY DIGITAL TWIN - SENSOR MONITORING")
    print("=" * 95)

    for cycle in range(1, 41):
        readings = simulate_factory(cycle)

        print(f"\nCYCLE {cycle}")
        print("-" * 95)

        for r in readings:
            print(
                f"{r['machine']:8} | "
                f"Temp: {r['temperature_c']:6.2f} °C | "
                f"Vibration: {r['vibration_mm_s']:5.2f} mm/s | "
                f"RPM: {r['rpm']:7.2f} | "
                f"Load: {r['load_percent']:5.2f}% | "
                f"Current: {r['current_amp']:5.2f} A"
            )

        time.sleep(0.2)

    print("\nSimulation completed!")