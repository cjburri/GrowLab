from app.hardware.input.Sensor import Sensor
import time
import random
import board
import adafruit_dht

pin_map = {
    4: board.D4,
    17: board.D17,
    18: board.D18,
    27: board.D27,
    22: board.D22,
    23: board.D23,
    24: board.D24,
    25: board.D25,
    5: board.D5,
    6: board.D6,
    13: board.D13,
    19: board.D19,
    26: board.D26,
    12: board.D12,
    16: board.D16,
    20: board.D20,
    21: board.D21
}

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
            # Convert GPIO pin number to board pin
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (HumiditySensor) Converting GPIO pin {signal_pin} to board pin")
            self.board_pin = pin_map.get(signal_pin)  # Default to D4 if pin not found
            self.dht = adafruit_dht.DHT11(self.board_pin, use_pulseio=False)
            self.dht.measure()
            if self.board_pin is None:
                raise ValueError(f"Invalid GPIO pin number: {signal_pin}")
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
            humidity = self.dht.humidity
            self.dht.measure()
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (HumiditySensor) Humidity: {humidity:.1f}%")
            return round(humidity, 1)
        except Exception as e:
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (HumiditySensor) trying again: {str(e)}")
            time.sleep(2)  # Wait 2 second before retrying
            return self.read()
        
        # print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (HumiditySensor) All attempts failed")
        # return None
