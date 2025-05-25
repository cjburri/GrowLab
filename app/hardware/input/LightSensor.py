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
            voltages = []
            # Convert to voltage (MCP3008 has 10-bit resolution)
            for _ in range(10):
                voltage = self.chan.voltage
                voltages.append(voltage)

            voltage = sum(voltages) / len(voltages)
            
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (LightSensor) Voltage: {voltage:.2f}V")
            return round(voltage, 2)
                
        except Exception as e:
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (LightSensor) Error: {str(e)}")
            return None 