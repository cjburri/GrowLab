from app.hardware.output.Atomizer import Atomizer
from app.hardware.output.Light import Light
from app.hardware.output.WaterPump import WaterPump
from app.hardware.output.Heater import Heater
from app.hardware.input.TemperatureSensor import TemperatureSensor
from app.hardware.input.HumitureSensor import HumiditySensor
from app.hardware.input.UltrasonicSensor import UltrasonicSensor
from app.hardware.input.LightSensor import LightSensor
from app.hardware.input.SoilMoistureSensor import SoilMoistureSensor
import time

class DeviceManager:
    def __init__(
            self, 
            atomizer_pin=None, 
            light_pin=None, 
            water_pin=None, 
            heater_pin=None, 
            light_pin_in=None,
            humidity_pin_in=None,
            temperature_pin_in=None, 
            ultrasonic_trigger_pin_in=None, 
            ultrasonic_echo_pin_in=None, 
            soil_moisture_pin_in=None, 
            debug_mode: bool = False
        ):
        # Only initialize components that have a pin specified
        self.atomizer = Atomizer(atomizer_pin, debug_mode) if atomizer_pin is not None else None
        self.light = Light(light_pin, debug_mode) if light_pin is not None else None
        self.water_pump = WaterPump(water_pin, debug_mode) if water_pin is not None else None
        self.heater = Heater(heater_pin, debug_mode) if heater_pin is not None else None
        self.light_sensor = LightSensor(light_pin_in, debug_mode) if light_pin_in is not None else None
        self.temperature_sensor = TemperatureSensor(temperature_pin_in, debug_mode) if temperature_pin_in is not None else None
        self.humidity_sensor = HumiditySensor(humidity_pin_in, debug_mode) if humidity_pin_in is not None else None
        self.ultrasonic_sensor = UltrasonicSensor(ultrasonic_trigger_pin_in, ultrasonic_echo_pin_in, debug_mode) if (ultrasonic_trigger_pin_in is not None and ultrasonic_echo_pin_in is not None) else None
        self.soil_moisture_sensor = SoilMoistureSensor(soil_moisture_pin_in, debug_mode) if soil_moisture_pin_in is not None else None
        

    def test_device(self, device, io=None):
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (DeviceManager) Starting test sequence for {device}")
        if io=="output":
            for _ in range(3):
                self.turn_on(device)
                time.sleep(1)
                self.turn_off(device)
                time.sleep(1)
        elif io=="input":
            return self.sense(device)
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (DeviceManager) {device} test complete")

    def turn_on(self, device):
        if device == 'atomizer' and self.atomizer is not None:
            self.atomizer.turn_on()
        elif device == 'light' and self.light is not None:
            self.light.turn_on()
        elif device == 'water' and self.water_pump is not None:
            self.water_pump.turn_on()
        elif device == 'heater' and self.heater is not None:
            self.heater.turn_on()

    def turn_off(self, device):
        if device == 'atomizer' and self.atomizer is not None:
            self.atomizer.turn_off()
        elif device == 'light' and self.light is not None:
            self.light.turn_off()
        elif device == 'water' and self.water_pump is not None:
            self.water_pump.turn_off()
        elif device == 'heater' and self.heater is not None:
            self.heater.turn_off()
        
    def sense(self, device):
        if device == 'light_sensor' and self.light_sensor is not None:
            return self.light_sensor.read()
        elif device == 'temperature_sensor' and self.temperature_sensor is not None:
            return self.temperature_sensor.read()
        elif device == 'ultrasonic_sensor' and self.ultrasonic_sensor is not None:
            return self.ultrasonic_sensor.read()
        elif device == 'humidity_sensor' and self.humidity_sensor is not None:
            return self.humidity_sensor.read()
        elif device == 'soil_moisture_sensor' and self.soil_moisture_sensor is not None:
            return self.soil_moisture_sensor.read()
        
    def __del__(self):
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (DeviceManager) Turning off devices")
        if self.atomizer is not None:
            del self.atomizer
        if self.light is not None:
            del self.light
        if self.water_pump is not None:
            del self.water_pump
        if self.heater is not None:
            del self.heater
