from app.hardware.output.RelayControlledComponent import RelayControlledComponent, GPIO

class WaterPump(RelayControlledComponent):
    """
    Represents a water pump controlled by a GPIO pin on a Raspberry Pi.
    
    This class provides an interface to control a water pump by setting the state
    of a specified GPIO pin to either HIGH (on) or LOW (off).
    """

    def __init__(self, signal_pin: int, debug_mode: bool = False):
        """
        Initialize the water pump with the specified GPIO pin.
        
        Args:
            signal_pin (int): The GPIO pin number to use for controlling the pump.
            debug_mode (bool): Whether to run in debug mode (simulated GPIO).
        """
        super().__init__(signal_pin, "WaterPump", debug_mode)

    def water_for_duration(self, duration: int):
        """
        Water the plant for a specified duration.
        
        Args:
            duration (int): The duration to water the plant in seconds.
        """
        self.activate_for_duration(duration)

    def pulse_water(self, on_time: int, off_time: int, cycles: int):
        """
        Pulse the water pump on and off for a specified number of cycles.
        
        Args:
            on_time (int): The duration to keep the pump on in seconds.
            off_time (int): The duration to keep the pump off in seconds.
            cycles (int): The number of cycles to repeat.
        """
        self.pulse_activate(on_time, off_time, cycles)
    
    def __del__(self):
        """
        Destructor to clean up GPIO resources.
        """
        try:
            RelayControlledComponent.__del__(self)
        except AttributeError:
            pass 
