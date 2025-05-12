from app.hardware.input.Sensor import Sensor
import time
import random

try:
    import adafruit_dht
except ImportError:
    # Mock DHT for development environments
    from unittest.mock import MagicMock
    adafruit_dht = MagicMock()
    adafruit_dht.DHT11 = MagicMock

class HumiditySensor(Sensor):
    """
    Represents a SunFounder Humiture (DHT11) sensor.
    This sensor provides both temperature and humidity readings.
    """
    def __init__(self, signal_pin: int, debug_mode: bool = False):
        """
        Initialize the humidity sensor.
        
        Args:
            signal_pin (int): The GPIO pin number where the sensor is connected.
            debug_mode (bool): Whether to run in debug mode (simulated readings).
        """
        super().__init__(signal_pin, "HumiditySensor", debug_mode)
        if not self.debug_mode:
            self.dht = adafruit_dht.DHT11(self.signal_pin)
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (HumiditySensor) Initialized on pin {self.signal_pin}")

    def read(self):
        """
        Read the humidity value from the sensor.
        Returns a simulated value in debug mode.
        """
        if self.debug_mode:
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (HumiditySensor) Debug mode: returning simulated humidity value.")
            return round(45.0 + random.random() * 20.0, 1)  # Simulated humidity between 45-65%
            
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (HumiditySensor) Reading humidity from pin {self.signal_pin}")
        try:
            # Read humidity from DHT11
            humidity = self.dht.humidity
            
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (HumiditySensor) Humidity: {humidity:.1f}%")
            return round(humidity, 1)
                
        except Exception as e:
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (HumiditySensor) Error: {str(e)}")
            return None
