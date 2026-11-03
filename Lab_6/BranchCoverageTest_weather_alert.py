"""Branch and boundary tests for the weather alert classifier."""

import pytest

from weather_alert import heat_alert, overall_alert, rain_alert, wind_alert


@pytest.mark.parametrize(
    "speed, expected",
    [
        (0, "none"),
        (38, "none"),
        (39, "advisory"),
        (40, "advisory"),
        (61, "advisory"),
        (62, "watch"),
        (63, "watch"),
        (88, "watch"),
        (89, "warning"),
        (90, "warning"),
    ],
)
def test_wind_thresholds(speed, expected):
    assert wind_alert(speed) == expected


@pytest.mark.parametrize(
    "rainfall, saturated, expected",
    [
        (0, False, "none"),
        (0, True, "none"),
        (9, False, "none"),
        (9, True, "none"),
        (10, False, "advisory"),
        (10, True, "watch"),
        (11, False, "advisory"),
        (11, True, "watch"),
        (49, False, "advisory"),
        (49, True, "watch"),
        (50, False, "watch"),
        (50, True, "warning"),
        (51, False, "watch"),
        (51, True, "warning"),
    ],
)
def test_rain_thresholds_and_soil(rainfall, saturated, expected):
    assert rain_alert(rainfall, saturated) == expected


@pytest.mark.parametrize("humidity", [30, 40])
@pytest.mark.parametrize(
    "temperature, expected",
    [
        (34, "none"),
        (35, "advisory"),
        (36, "advisory"),
        (39, "advisory"),
        (40, "watch"),
        (41, "watch"),
        (44, "watch"),
        (45, "warning"),
        (46, "warning"),
    ],
)
def test_heat_without_humidity_adjustment(temperature, humidity, expected):
    # Humidity at or below 40 must not change the temperature index.
    assert heat_alert(temperature, humidity) == expected


@pytest.mark.parametrize(
    "temperature, humidity, expected",
    [
        (32, 60, "none"),       # Adjusted index 34: below advisory.
        (33, 60, "advisory"),   # Adjusted index 35: advisory boundary.
        (34, 60, "advisory"),   # Adjusted index 36: above advisory.
        (37, 60, "advisory"),   # Adjusted index 39: below watch.
        (38, 60, "watch"),      # Adjusted index 40: watch boundary.
        (39, 60, "watch"),      # Adjusted index 41: above watch.
        (42, 60, "watch"),      # Adjusted index 44: below warning.
        (43, 60, "warning"),    # Adjusted index 45: warning boundary.
        (44, 60, "warning"),    # Adjusted index 46: above warning.
        (35, 41, "advisory"),   # Humidity immediately above 40.
    ],
)
def test_heat_with_humidity_adjustment(temperature, humidity, expected):
    assert heat_alert(temperature, humidity) == expected


@pytest.mark.parametrize(
    "alerts, expected",
    [
        ([], "none"),
        (["none"], "none"),
        (["advisory"], "advisory"),
        (["watch"], "watch"),
        (["warning"], "warning"),
        (["none", "advisory", "watch", "warning"], "warning"),
        (["warning", "watch", "advisory", "none"], "warning"),
        (["watch", "watch"], "watch"),
        (["none", "none"], "none"),
        (["advisory", "none", "watch", "advisory"], "watch"),
    ],
)
def test_overall_alert_order_and_repetition(alerts, expected):
    assert overall_alert(alerts) == expected


@pytest.mark.parametrize(
    "alerts",
    [["storm"], [""], ["watch", "storm"], ["warning", "unknown"]],
)
def test_unknown_alerts_raise_value_error(alerts):
    # Even an earlier warning must not hide a later invalid entry.
    with pytest.raises(ValueError, match="^unknown alert$"):
        overall_alert(alerts)
