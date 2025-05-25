try:
    import RPi.GPIO as GPIO
except ImportError:
    # Mock GPIO for development environments
    from unittest.mock import MagicMock
    GPIO = MagicMock()
    GPIO.HIGH = True
    GPIO.LOW = False
    GPIO.OUT = 'out'
import time
from app.models import db, Log
from datetime import datetime
from typing import Literal, Union

class RelayControlledComponent:
    """
    Base class for components controlled by a GPIO pin on a Raspberry Pi.
    
    This class provides an interface to control components by setting the state
    of a specified GPIO pin to either HIGH (on) or LOW (off).
    
    Attributes:
        signal_pin (int): The GPIO pin number that controls the component.
        state (bool): The current state of the component (GPIO.HIGH or GPIO.LOW).
        runtime (int): The total runtime of the component in seconds.
        debug_mode (bool): Whether the component is in debug mode.
        component_name (str): The name of the component for logging purposes.
    """

    def __init__(self, signal_pin: int, component_name: str, debug_mode: bool = False):
        """
        Initialize the component with the specified GPIO pin.
        
        Args:
            signal_pin (int): The GPIO pin number to use for controlling the component.
            component_name (str): The name of the component for logging purposes.
            debug_mode (bool): Whether to run in debug mode (simulated GPIO).
        """
        self.debug_mode = debug_mode
        self.component_name = component_name
        if self.debug_mode:
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - ({self.component_name}) Debug mode enabled, GPIO will be simulated")
        self.signal_pin = signal_pin                               # The GPIO pin number to use for controlling the component
        self.state = GPIO.LOW if not self.debug_mode else False    # Initialize component in OFF state
        self.runtime = 0                                           # The total runtime of the component in seconds
        self.__setup()

    def __setup(self):
        """
        Configure the GPIO pin for output and set initial state.
        
        This private method is called during initialization to set up the GPIO pin
        as an output and set its initial state to LOW (off).
        """
        if not self.debug_mode:
            GPIO.setup(self.signal_pin, GPIO.OUT)
            GPIO.output(self.signal_pin, self.state)
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - ({self.component_name}) Initialized on pin {self.signal_pin} with state {self.state}")

    def __set_state(self, state: Union[Literal[GPIO.HIGH, GPIO.LOW], bool]):
        """
        Set the state of the component.
        
        This private method updates the component's state and sets the GPIO pin accordingly.
        
        Args:
            state (Union[Literal[1, 0], bool]): The state to set (1/True for on, 0/False for off).
        """
        self.state = state
        if not self.debug_mode:
            GPIO.output(self.signal_pin, state)
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - ({self.component_name}) Set state to {state}")

    def get_status(self) -> Union[bool, Literal[GPIO.HIGH, GPIO.LOW]]:
        """
        Get the current state of the component.
        
        Returns:
            Union[bool, Literal[GPIO.HIGH, GPIO.LOW]]: The current state of the component.
        """
        return self.state
    
    def get_runtime(self) -> int:
        """
        Get the current runtime of the component.
        
        Returns:
            int: The total runtime of the component in seconds.
        """
        return self.runtime

    def turn_on(self):
        """
        Turn the component on by setting the GPIO pin to HIGH.
        """
        if not self.debug_mode:
            self.__set_state(GPIO.HIGH)
        else:
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - ({self.component_name}) Debug mode enabled, {self.component_name} set to HIGH")
        if self.component_name == "Light":
            code = 101
        elif self.component_name == "Atomizer":
            code = 201
        elif self.component_name == "Fan":
            code = 301
        elif self.component_name == "Pump":
            code = 401
        elif self.component_name == "Heater":
            code = 501
        log = Log(timestamp=datetime.now(), event_code=code)
        db.session.add(log)
        db.session.commit()
        

    def turn_off(self):
        """
        Turn the component off by setting the GPIO pin to LOW.
        """
        if not self.debug_mode:
            self.__set_state(GPIO.LOW)
        else:
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - ({self.component_name}) Debug mode enabled, {self.component_name} set to LOW")
        if self.component_name == "Light":
            code = 100
        elif self.component_name == "Atomizer":
            code = 200
        elif self.component_name == "Fan":
            code = 300
        elif self.component_name == "Pump":
            code = 400
        elif self.component_name == "Heater":
            code = 500
        log = Log(timestamp=datetime.now(), event_code=code)
        db.session.add(log)
        db.session.commit()
        

    def activate_for_duration(self, duration: int):
        """
        Activate the component for a specified duration.
        
        Args:
            duration (int): The duration to keep the component on in seconds.
        """
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - ({self.component_name}) Activating for {duration} seconds")
        self.turn_on()
        time.sleep(duration)
        self.turn_off()
        self.runtime += duration
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - ({self.component_name}) Activation complete for {duration} seconds")

    def pulse_activate(self, on_time: int, off_time: int, cycles: int):
        """
        Pulse the component on and off for a specified number of cycles.
        
        Args:
            on_time (int): The duration to keep the component on in seconds.
            off_time (int): The duration to keep the component off in seconds.
            cycles (int): The number of cycles to repeat.
        """
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - ({self.component_name}) Pulsing for {cycles} cycles")
        for _ in range(cycles):
            self.activate_for_duration(on_time)
            time.sleep(off_time)
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - ({self.component_name}) {cycles}x{on_time} pulse(s) complete")

    def get_usage_stats(self) -> dict:
        """
        Get the usage statistics of the component.
        
        Returns:
            dict: A dictionary containing runtime and state information.
        """
        return {
            "runtime": self.runtime,
            "state": self.state,
        }
    
    def __del__(self):
        """
        Destructor to clean up GPIO resources.
        """
        if not self.debug_mode:
            # Don't clean up GPIO here as it might be needed by other components
            # Just set the pin to LOW
            try:
                GPIO.output(self.signal_pin, GPIO.LOW)
                print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - ({self.component_name}) Set pin {self.signal_pin} to LOW")
            except RuntimeError:
                # GPIO might be cleaned up already
                pass
        else:
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - ({self.component_name}) Debug mode enabled, GPIO resources not cleaned up")
