"""Parse weather readings and return None for invalid inputs."""

import math


def parse_reading(text):
    """Parse a finite Celsius temperature and a whole humidity percentage."""
    if not isinstance(text, str):
        return None
    try:
        temperature_text, humidity_text = text.split("/")
        temperature = float(temperature_text)
        humidity = int(humidity_text)
    except ValueError:
        return None
    if not math.isfinite(temperature) or not 0 <= humidity <= 100:
        return None
    return temperature, humidity


def wind_category(speed_text):
    """Classify a nonnegative whole-number wind speed in km/h."""
    if not isinstance(speed_text, str):
        return None
    try:
        speed = int(speed_text)
    except ValueError:
        return None
    if speed < 0:
        return None
    if speed >= 89:
        return "warning"
    if speed >= 39:
        return "advisory"
    return "none"


def rainfall_spread(readings_csv):
    """Return the range of one or more finite, nonnegative rainfall readings."""
    if not isinstance(readings_csv, str):
        return None
    try:
        readings = [float(field) for field in readings_csv.split(",")]
    except ValueError:
        return None
    if any(not math.isfinite(reading) or reading < 0 for reading in readings):
        return None
    return max(readings) - min(readings)


def main():
    print("==== Running parse_reading ====")
    text = input("Enter temperature/humidity (e.g. 35.5/80): ")
    reading = parse_reading(text)
    if reading is None:
        print("Invalid reading. Enter a finite temperature and a whole humidity from 0 to 100.")
    else:
        print("Temperature and Humidity:", reading)

    print("\n==== Running wind_category ====")
    text = input("Enter a wind speed in km/h (e.g. 45): ")
    category = wind_category(text)
    if category is None:
        print("Invalid wind speed. Enter a nonnegative whole number.")
    else:
        print("Wind Category:", category)

    print("\n==== Running rainfall_spread ====")
    text = input("Enter hourly rainfall in mm as CSV (e.g. 2,5.5,10): ")
    spread = rainfall_spread(text)
    if spread is None:
        print("Invalid rainfall. Enter comma-separated, finite, nonnegative amounts.")
    else:
        print("Rainfall Spread:", spread)


if __name__ == "__main__":
    try:
        main()
    except EOFError:
        print("\nInput ended before all weather readings were entered.")
