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
class SoilMoistureSensor(Sensor):
    def __init__(self, adc_channel: int = 0, debug_mode: bool = False):
        """
        Initialize the Soil Moisture sensor.
        
        Args:
            adc_channel (int): The ADC channel number (0-7) where the sensor is connected.
            debug_mode (bool): Whether to run in debug mode (simulated readings).
        """
        super().__init__(signal_pin=None, sensor_name="SoilMoistureSensor", debug_mode=debug_mode)
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
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (SoilMoistureSensor) Initialized on ADC channel {self.adc_channel}")

    def read(self):
        """
        Read the soil moisture level from the sensor.
        Returns a simulated value in debug mode.
        """
        if self.debug_mode:
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (SoilMoistureSensor) Debug mode: returning simulated soil moisture value.")
            return round(random.random() * 100, 1)  # Simulated soil moisture level between 0-100
            
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (SoilMoistureSensor) Reading soil moisture level from ADC channel {self.adc_channel}")
        try:
            voltages = []
            # Convert to voltage (MCP3008 has 10-bit resolution)
            for _ in range(10):
                voltage = self.chan.voltage
                voltages.append(voltage)
                
            voltage = sum(voltages) / len(voltages)
            
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (SoilMoistureSensor) Voltage: {voltage:.2f}V")
            return round(voltage, 1)
                
        except Exception as e:
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (SoilMoistureSensor) Error: {str(e)}")
            return None 
