import time

class Sensor:
    """
    Base class for all sensors.
    
    Attributes:
        signal_pin (int): The GPIO pin number that reads the sensor value.
        sensor_name (str): The name of the sensor for logging purposes.
        debug_mode (bool): Whether the sensor is in debug mode.
    """
    def __init__(self, signal_pin: int, sensor_name: str, debug_mode: bool = False):
        self.signal_pin = signal_pin
        self.sensor_name = sensor_name
        self.debug_mode = debug_mode
        if self.debug_mode:
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (Sensor) Debug mode enabled, GPIO will be simulated")
        else:
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (Sensor) Initialized on pin {self.signal_pin}")

    def read(self):
        """
        Read the sensor value. Should be implemented by subclasses.
        """
        raise NotImplementedError("read() must be implemented by subclasses")

    def get_status(self):
        """
        Get the current status or value of the sensor.
        """
        return self.read() 