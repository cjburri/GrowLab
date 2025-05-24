from app.hardware.input.LightSensor import LightSensor
import time

pump = WaterPump(23, debug_mode=True)

pump.pulse_water(1, 1, 1)

print(pump.get_usage_stats())

def test_light_sensor():
    # Initialize the light sensor on channel 0
    sensor = LightSensor(adc_channel=0, debug_mode=False)
    
    print("\nTesting Light Sensor...")
    print("Please cover and uncover the sensor to test readings")
    
    # Take 5 readings with 2-second intervals
    for i in range(5):
        light_level = sensor.read()
        if light_level is not None:
            print(f"Reading {i+1}: {light_level}%")
        else:
            print(f"Reading {i+1}: Failed to read sensor")
        time.sleep(2)

if __name__ == "__main__":
    test_light_sensor()
