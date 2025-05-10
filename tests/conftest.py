import sys
from unittest.mock import MagicMock

# Create a mock for the GPIO module
mock_gpio = MagicMock()
mock_gpio.OUT = 'OUT'
mock_gpio.IN = 'IN'
mock_gpio.HIGH = 1
mock_gpio.LOW = 0
mock_gpio.setup = MagicMock()
mock_gpio.output = MagicMock()
mock_gpio.input = MagicMock()
mock_gpio.cleanup = MagicMock()

# Mock the RPi.GPIO module
sys.modules['RPi.GPIO'] = mock_gpio 