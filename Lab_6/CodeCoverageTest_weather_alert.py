"""Line coverage tests for the weather alert classifier."""

import pytest

from weather_alert import heat_alert, overall_alert, rain_alert, wind_alert


@pytest.mark.parametrize(
    "speed, expected",
    [(10, "none"), (39, "advisory"), (62, "watch"), (89, "warning")],
)
def test_wind_levels(speed, expected):
    assert wind_alert(speed) == expected


@pytest.mark.parametrize(
    "rainfall, saturated, expected",
    [
        (0, False, "none"),
        (10, False, "advisory"),
        (10, True, "watch"),
        (50, False, "watch"),
        (50, True, "warning"),
    ],
)
def test_rain_levels(rainfall, saturated, expected):
    assert rain_alert(rainfall, saturated) == expected


@pytest.mark.parametrize(
    "temperature, expected",
    [(32, "none"), (33, "advisory"), (38, "watch"), (43, "warning")],
)
def test_heat_levels(temperature, expected):
    # Humidity 60 adds two degrees to the temperature index.
    assert heat_alert(temperature, 60) == expected


def test_empty_alert_list():
    assert overall_alert([]) == "none"


def test_increasing_alert_severity():
    assert overall_alert(["advisory", "watch", "warning"]) == "warning"


def test_unknown_alert():
    with pytest.raises(ValueError, match="^unknown alert$"):
        overall_alert(["storm"])
