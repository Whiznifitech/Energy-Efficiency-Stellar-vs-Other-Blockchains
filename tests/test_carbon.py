"""Unit tests for carbon intensity module."""
from unittest.mock import patch

from carbon import annotate_carbon, get_carbon_intensity_g_per_kwh


def test_no_api_key_returns_none():
    with patch.dict("os.environ", {}, clear=True):
        result = get_carbon_intensity_g_per_kwh("US")
    assert result is None


def test_annotate_carbon_no_key_returns_none():
    with patch.dict("os.environ", {}, clear=True):
        result = annotate_carbon("stellar", 0.000222)
    assert result is None


def test_annotate_carbon_with_intensity():
    with patch("carbon.get_carbon_intensity_g_per_kwh", return_value=400.0):
        result = annotate_carbon("stellar", 0.000222)
    assert abs(result - 0.0888) < 0.001
