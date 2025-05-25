import time
from app.config import DEBUG_MODE
if not DEBUG_MODE:
    import RPi.GPIO as GPIO

def initialize_gpio():
    """
    Initialize the GPIO system. This should be called once at application startup.
    Sets up the GPIO mode and performs any necessary initialization.
    """
    if not DEBUG_MODE:
        try:
            GPIO.setmode(GPIO.BCM)
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (GPIO Manager) GPIO mode set to BCM")
        except RuntimeError:
            # If GPIO is already initialized, just set the mode
            GPIO.setmode(GPIO.BCM)
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (GPIO Manager) GPIO mode reset to BCM")
    else:
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (GPIO Manager) Debug mode enabled, GPIO will be simulated")

def cleanup_gpio():
    """
    Clean up GPIO resources. This should be called when the application is shutting down.
    """
    if not DEBUG_MODE:
        try:
            GPIO.cleanup()
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (GPIO Manager) GPIO resources cleaned up")
            # Reinitialize GPIO mode after cleanup
            GPIO.setmode(GPIO.BCM)
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (GPIO Manager) GPIO mode reset to BCM")
        except RuntimeError:
            # If GPIO is already cleaned up, just reinitialize
            GPIO.setmode(GPIO.BCM)
            print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (GPIO Manager) GPIO mode reset to BCM")
    else:
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (GPIO Manager) Debug mode enabled, GPIO resources not cleaned up") 