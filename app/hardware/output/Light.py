from app.hardware.output.RelayControlledComponent import RelayControlledComponent, GPIO

class Light(RelayControlledComponent):
    """
    Represents a light controlled by a GPIO pin on a Raspberry Pi.
    
    This class provides an interface to control a light by setting the state
    of a specified GPIO pin to either HIGH (on) or LOW (off).
    """

    def __init__(self, signal_pin: int, debug_mode: bool = False):
        """
        Initialize the light with the specified GPIO pin.
        
        Args:
            signal_pin (int): The GPIO pin number to use for controlling the light.
            debug_mode (bool): Whether to run in debug mode (simulated GPIO).
        """
        super().__init__(signal_pin, "Light", debug_mode)

    def illuminate_for_duration(self, duration: int):
        """
        Turn the light on for a specified duration.
        
        Args:
            duration (int): The duration to keep the light on in seconds.
        """
        self.activate_for_duration(duration)
    
    def __del__(self):
        """
        Destructor to clean up GPIO resources.
        """
        super().__del__()

