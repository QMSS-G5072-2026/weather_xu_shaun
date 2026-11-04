"""
Tests for the weather_xx2510 package for QMSS G5072 Homework 7.
"""

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from weather_xx2510 import (
    celsius_to_fahrenheit,
    clean_readings,
    summarize_temperatures,
)

# =============================================================================
# UNIT TESTS
# =============================================================================


@pytest.mark.parametrize("celsius, expected", [
    (0, 32.0),
    (100, 212.0),
    (-40, -40.0),
    (37, 98.6),
    (-273.15, -459.67),
    (25.5, 77.9),
])
def test_celsius_to_fahrenheit(celsius, expected):
    """Check known Celsius -> Fahrenheit conversions, including absolute zero."""
    assert celsius_to_fahrenheit(celsius) == pytest.approx(expected)


# The expected exception class itself is passed in as a parameter
@pytest.mark.parametrize("bad_input, expected_error", [
    ("25", TypeError),
    (None, TypeError),
    ([25], TypeError),
    (-273.16, ValueError),
    (-500, ValueError),
])
def test_celsius_to_fahrenheit_invalid(bad_input, expected_error):
    """Check that non-numbers raise TypeError and values below absolute zero raise ValueError."""
    with pytest.raises(expected_error):
        celsius_to_fahrenheit(bad_input)


def test_summarize_temperatures():
    """Check that summarize_temperatures ignores NaN and counts it as missing."""
    # Arrange
    temps = [10.0, float("nan"), 20.0, 30.0]

    # Act
    result = summarize_temperatures(temps)

    # Assert
    assert result["mean"] == pytest.approx(20.0)
    assert result["min"] == 10.0
    assert result["max"] == 30.0
    assert result["n_missing"] == 1


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def raw_readings():
    """Unsorted station readings with one missing and one implausible (999.0) temperature."""
    return pd.DataFrame({
        "station": ["JFK", "CPK", "JFK", "CPK", "LGA"],
        "date": ["2026-07-02", "2026-07-01", "2026-07-01", "2026-07-02", "2026-07-01"],
        "temp_c": [30.0, 25.0, float("nan"), 999.0, 28.0],
    })


def test_raw_readings_fixture(raw_readings):
    """Check the fixture has the expected columns, 5 rows, and 1 missing temperature."""
    assert list(raw_readings.columns) == ["station", "date", "temp_c"]
    assert len(raw_readings) == 5
    assert raw_readings["temp_c"].isna().sum() == 1


# =============================================================================
# TESTING DATAFRAMES
# =============================================================================


def test_clean_readings(raw_readings):
    """Check that clean_readings drops bad rows, adds temp_f, sorts, and resets the index."""
    # Arrange
    expected = pd.DataFrame({
        "station": ["CPK", "JFK", "LGA"],
        "date": ["2026-07-01", "2026-07-02", "2026-07-01"],
        "temp_c": [25.0, 30.0, 28.0],
        "temp_f": [77.0, 86.0, 82.4],
    })

    # Act
    result = clean_readings(raw_readings)

    # Assert
    assert_frame_equal(result, expected)