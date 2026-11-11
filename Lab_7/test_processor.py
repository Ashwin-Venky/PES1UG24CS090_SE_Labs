import math

from hypothesis import example, given, settings, strategies as st

from processor import parse_reading, rainfall_spread, wind_category


NON_TEXT = st.one_of(
    st.none(), st.booleans(), st.integers(), st.floats(), st.binary(),
    st.lists(st.integers(), max_size=5), st.dictionaries(st.text(), st.integers(), max_size=5),
)
JUNK_TEXT = st.text(alphabet="abcXYZ!?_", min_size=1, max_size=20)
TEMPERATURES = st.floats(allow_nan=False, allow_infinity=False)
HUMIDITIES = st.integers(min_value=0, max_value=100)
WIND_SPEEDS = st.integers(min_value=0, max_value=10**9)
RAINFALL = st.floats(min_value=0, allow_nan=False, allow_infinity=False)
NONFINITE = st.sampled_from(["nan", "inf", "-inf", "1e309"])


@given(st.one_of(
    NON_TEXT,
    JUNK_TEXT,
    st.sampled_from(["", " ", "/", "21/", "/50", "21/50/40", "21/50.5"]),
    NONFINITE.map(lambda temperature: f"{temperature}/50"),
    st.integers(min_value=101).map(lambda humidity: f"21/{humidity}"),
    st.integers(max_value=-1).map(lambda humidity: f"21/{humidity}"),
))
@settings(max_examples=200, derandomize=True)
def test_parse_reading_rejects_invalid_input(reading):
    assert parse_reading(reading) is None


@given(TEMPERATURES, HUMIDITIES)
@example(-12.5, 0)
@example(35.5, 100)
@settings(derandomize=True)
def test_parse_reading_round_trips_valid_input(temperature, humidity):
    result = parse_reading(f" {temperature!r} / {humidity} ")
    assert result == (temperature, humidity)
    assert type(result[0]) is float
    assert type(result[1]) is int


@given(st.one_of(
    NON_TEXT,
    JUNK_TEXT,
    NONFINITE,
    st.sampled_from(["", " ", "45.0", "4e1", "39 km/h"]),
    st.integers(max_value=-1).map(str),
))
@settings(max_examples=200, derandomize=True)
def test_wind_category_rejects_invalid_input(speed_text):
    assert wind_category(speed_text) is None


@given(WIND_SPEEDS)
@example(0)
@example(38)
@example(39)
@example(88)
@example(89)
@settings(derandomize=True)
def test_wind_category_preserves_thresholds(speed):
    expected = {0: "none", 1: "advisory", 2: "warning"}
    assert wind_category(f" {speed} ") == expected[(speed >= 39) + (speed >= 89)]


@given(st.one_of(
    NON_TEXT,
    JUNK_TEXT,
    st.sampled_from(["", " ", ",", ",1", "1,", "1,,2", "1, ,2", "1,heavy"]),
    NONFINITE.map(lambda reading: f"0,{reading},3"),
    st.integers(max_value=-1).map(lambda reading: f"0,{reading},3"),
))
@settings(max_examples=200, derandomize=True)
def test_rainfall_spread_rejects_invalid_input(readings_csv):
    assert rainfall_spread(readings_csv) is None


@given(st.lists(RAINFALL, min_size=1, max_size=20))
@example([0.0])
@example([2.0, 5.5, 10.0])
@settings(derandomize=True)
def test_rainfall_spread_is_the_range_in_any_order(readings):
    fields = [f" {reading!r} " for reading in readings]
    spread = rainfall_spread(",".join(fields))
    assert math.isfinite(spread)
    assert spread == max(readings) - min(readings)
    assert rainfall_spread(",".join(reversed(fields))) == spread
