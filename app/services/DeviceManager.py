from app.hardware.Atomizer import Atomizer
from app.hardware.Light import Light
from app.hardware.WaterPump import WaterPump
# from app.hardware.Humidifier import Humidifier
# from app.hardware.Heater import Heater
import time

class DeviceManager:
    def __init__(self, atomizer_pin=None, light_pin=None, water_pin=None, humidifier_pin=None, heater_pin=None, debug_mode: bool = False):
        self.atomizer = Atomizer(atomizer_pin, debug_mode)
        self.light = Light(light_pin, debug_mode)
        self.water_pump = WaterPump(water_pin, debug_mode)
        # self.humidifier = Humidifier(humidifier_pin)
        # self.heater = Heater(heater_pin)

    def test_device(self, device):
        for _ in range(3):
            self.turn_on(device)
            time.sleep(.5)
            self.turn_off(device)
            time.sleep(.5)
        print(f"{device} test complete")

    def turn_on(self, device):
        if device == 'atomizer':
            self.atomizer.turn_on()
        elif device == 'light':
            self.light.turn_on()
        elif device == 'water_pump':
            self.water_pump.turn_on()

    def turn_off(self, device):
        if device == 'atomizer':
            self.atomizer.turn_off()
        elif device == 'light':
            self.light.turn_off()
        elif device == 'water_pump':
            self.water_pump.turn_off()

    def __del__(self):
        print("[DeviceManager] Turning off devices")
        self.atomizer.turn_off()
        self.light.turn_off()
        self.water_pump.turn_off()
        # self.heater.turn_off()
        # self.humidifier.turn_off()
