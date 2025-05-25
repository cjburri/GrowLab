from app.hardware.output.RelayControlledComponent import RelayControlledComponent, GPIO
import time

class Atomizer(RelayControlledComponent):
    """
    Represents a atomizer controlled by a GPIO pin on a Raspberry Pi.
    
    This class provides an interface to control a atomizer by setting the state
    of a specified GPIO pin to either HIGH (on) or LOW (off).
    """

    def __init__(self, signal_pin: int, debug_mode: bool = False):
        """
        Initialize the atomizer with the specified GPIO pin.
        
        Args:
            signal_pin (int): The GPIO pin number to use for controlling the atomizer.
            debug_mode (bool): Whether to run in debug mode (simulated GPIO).
            max_continuous_runtime (int): Maximum time in seconds the atomizer can run continuously.
        """
        super().__init__(signal_pin, "Atomizer", debug_mode)
        
    def atomize_for_duration(self, duration: int):
        """
        Run the atomizer for a specified duration.
        
        Args:
            duration (int): The duration to run the atomizer in seconds.
        """
        self.activate_for_duration(duration)

    def __del__(self):
        """
        Destructor to clean up GPIO resources.
        """
        try:
            RelayControlledComponent.__del__(self)
        except AttributeError:
            pass 
