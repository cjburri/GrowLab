from app.hardware.Sensor import Sensor
import time
import os

class TemperatureSensor(Sensor):
    """
    Represents a temperature sensor connected to a GPIO pin.
    """
    def __init__(self, signal_pin: int, debug_mode: bool = False):
        super().__init__(signal_pin, "TemperatureSensor", debug_mode)

    def read(self):
        """
        Read the temperature value from the sensor.
        Returns a simulated value in debug mode.
        """
        if self.debug_mode:
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (TemperatureSensor) Debug mode: returning simulated temperature value.")
            return 72.0  # Simulated temperature in Fahrenheit
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (TemperatureSensor) Reading temperature from pin {self.signal_pin}")
        try:
            # Open the 1-wire device file
            device_file = f'/sys/bus/w1/devices/{os.environ["1wire_sensor_id"]}/w1_slave'
            with open(device_file, 'r') as f:
                lines = f.readlines()
            
            # Parse temperature value from the device file
            if lines[0].strip()[-3:] == 'YES':  # CRC check passed
                temp_pos = lines[1].find('t=')
                if temp_pos != -1:
                    # Convert temperature from millicelsius to Fahrenheit
                    temp_c = float(lines[1][temp_pos+2:]) / 1000.0
                    temp_f = (temp_c * 9.0 / 5.0) + 32.0
                    return temp_f
                    
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (TemperatureSensor) Error reading temperature")
            return None
                
        except Exception as e:
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (TemperatureSensor) Error: {str(e)}")
            return None
        return None
