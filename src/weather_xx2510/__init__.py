# read version from installed package
from importlib.metadata import version
__version__ = version("weather_xx2510")

from .weather_xx2510 import celsius_to_fahrenheit, clean_readings, summarize_temperatures