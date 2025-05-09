from app.hardware.Atomizer import Atomizer
from app.hardware.Light import Light
from app.hardware.WaterPump import WaterPump
from app.hardware.Heater import Heater
from app.hardware.TemperatureSensor import TemperatureSensor
import time

class DeviceManager:
    def __init__(
            self, 
            atomizer_pin=None, 
            light_pin=None, 
            water_pin=None, 
            heater_pin=None, 
            temperature_pin_in=None, 
            humidity_pin_in=None, 
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
        self.temperature_sensor = TemperatureSensor(temperature_pin_in, debug_mode) if temperature_pin_in is not None else None
        # self.humidity_sensor = HumiditySensor(humidity_pin_in, debug_mode) if humidity_pin_in is not None else None
        # self.ultrasonic_trigger = UltrasonicTrigger(ultrasonic_trigger_pin_in, debug_mode) if ultrasonic_trigger_pin_in is not None else None
        # self.ultrasonic_echo = UltrasonicEcho(ultrasonic_echo_pin_in, debug_mode) if ultrasonic_echo_pin_in is not None else None
        # self.soil_moisture_sensor = SoilMoistureSensor(soil_moisture_pin_in, debug_mode) if soil_moisture_pin_in is not None else None
        # self.humidifier = Humidifier(humidifier_pin) if humidifier_pin is not None else None

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
        if device == 'temperature_sensor' and self.temperature_sensor is not None:
            return self.temperature_sensor.read()

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
