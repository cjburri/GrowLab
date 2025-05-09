from app.hardware.Sensor import Sensor
import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    from unittest.mock import MagicMock
    GPIO = MagicMock()

class UltrasonicSensor(Sensor):
    """
    Represents an HC-SR04 Ultrasonic Distance Sensor.
    Uses two GPIO pins: trigger and echo.
    """
    def __init__(self, trigger_pin: int, echo_pin: int, debug_mode: bool = False):
        super().__init__(signal_pin=None, sensor_name="UltrasonicSensor", debug_mode=debug_mode)
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        if not self.debug_mode:
            GPIO.setup(self.trigger_pin, GPIO.OUT)
            GPIO.setup(self.echo_pin, GPIO.IN)
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (UltrasonicSensor) Initialized with trigger pin {self.trigger_pin} and echo pin {self.echo_pin}")

    def read(self):
        """
        Measure distance using the ultrasonic sensor.
        Returns distance in centimeters.
        """
        if self.debug_mode:
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (UltrasonicSensor) Debug mode: returning simulated distance value.")
            return 42.0  # Simulated distance in cm
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (UltrasonicSensor) Measuring distance...")
        # Send 10us pulse to trigger
        GPIO.output(self.trigger_pin, False)
        time.sleep(0.0002)
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)

        # Wait for echo to go high
        pulse_start = time.time()
        timeout = pulse_start + 0.04  # 40ms timeout
        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()
            if pulse_start > timeout:
                print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (UltrasonicSensor) Timeout waiting for echo to go high")
                return None

        # Wait for echo to go low
        pulse_end = time.time()
        timeout = pulse_end + 0.04
        while GPIO.input(self.echo_pin) == 1:
            pulse_end = time.time()
            if pulse_end > timeout:
                print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (UltrasonicSensor) Timeout waiting for echo to go low")
                return None

        pulse_duration = pulse_end - pulse_start
        # Speed of sound at sea level = 34300 cm/s
        distance = pulse_duration * 17150  # (34300/2)
        distance = round(distance, 2)
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (UltrasonicSensor) Measured distance: {distance} cm")
        return distance 