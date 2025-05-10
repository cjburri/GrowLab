from app.hardware.output.RelayControlledComponent import RelayControlledComponent, GPIO
import time

class Heater(RelayControlledComponent):
    """
    Represents a heater controlled by a GPIO pin on a Raspberry Pi.
    
    This class provides an interface to control a heater by setting the state
    of a specified GPIO pin to either HIGH (on) or LOW (off).
    """

    def __init__(self, signal_pin: int, debug_mode: bool = False):
        """
        Initialize the heater with the specified GPIO pin.
        
        Args:
            signal_pin (int): The GPIO pin number to use for controlling the heater.
            debug_mode (bool): Whether to run in debug mode (simulated GPIO).
        """
        super().__init__(signal_pin, "Heater", debug_mode)
        
    def heat_for_duration(self, duration: int):
        """
        Run the heater for a specified duration.
        
        Args:
            duration (int): The duration to run the heater in seconds.
        """
        self.activate_for_duration(duration)

    def __del__(self):
        """
        Destructor to clean up GPIO resources.
        """
        super().__del__() 