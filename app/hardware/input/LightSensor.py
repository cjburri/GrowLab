from app.hardware.input.Sensor import Sensor
import time
import random
try:
    import board
    import busio
    import digitalio
    import adafruit_mcp3xxx.mcp3008 as MCP
    from adafruit_mcp3xxx.analog_in import AnalogIn
except ImportError:
    from unittest.mock import MagicMock
    board = MagicMock()
    busio = MagicMock()
    digitalio = MagicMock()
    MCP = MagicMock()
    AnalogIn = MagicMock()

class LightSensor(Sensor):
    """
    Represents a TS0197 Photocell Light Sensor Module.
    Uses MCP3008 ADC to read analog values from the sensor.
    """
    def __init__(self, adc_channel: int = 0, debug_mode: bool = False):
        """
        Initialize the light sensor.
        
        Args:
            adc_channel (int): The ADC channel number (0-7) where the sensor is connected.
            debug_mode (bool): Whether to run in debug mode (simulated readings).
        """
        super().__init__(signal_pin=None, sensor_name="LightSensor", debug_mode=debug_mode)
        self.adc_channel = adc_channel
        if not self.debug_mode:
            # Initialize SPI bus
            spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
            # Initialize CS pin
            cs = digitalio.DigitalInOut(board.D5)  # Using GPIO5 as CS
            # Initialize the MCP3008
            self.mcp = MCP.MCP3008(spi, cs)
            # Create an analog input channel
            self.chan = AnalogIn(self.mcp, self.adc_channel)
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (LightSensor) Initialized on ADC channel {self.adc_channel}")

    def read(self):
        """
        Read the light level from the sensor.
        Returns a simulated value in debug mode.
        """
        if self.debug_mode:
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (LightSensor) Debug mode: returning simulated light value.")
            return round(500 + random.random() * 1000, 1)  # Simulated light level between 500-1500
            
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (LightSensor) Reading light level from ADC channel {self.adc_channel}")
        try:
            # Read the raw ADC value
            raw_value = self.chan.value
            
            # Convert to voltage (MCP3008 has 10-bit resolution)
            voltage = (raw_value * 3.3) / 65535.0
            
            # Convert voltage to light level (0-100%)
            # The photocell typically outputs:
            # Dark = ~0V
            # Bright = ~3.3V
            light_level = (voltage / 3.3) * 100.0
            
            # Clamp the value between 0 and 100
            light_level = max(0.0, min(100.0, light_level))
            
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (LightSensor) Raw value: {raw_value}, Voltage: {voltage:.2f}V, Light level: {light_level:.1f}%")
            return round(light_level, 1)
                
        except Exception as e:
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (LightSensor) Error: {str(e)}")
            return None 