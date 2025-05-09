import RPi.GPIO as GPIO
import time
from app.config import DEBUG_MODE

def initialize_gpio():
    """
    Initialize the GPIO system. This should be called once at application startup.
    Sets up the GPIO mode and performs any necessary initialization.
    """
    if not DEBUG_MODE:
        GPIO.setmode(GPIO.BCM)
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (GPIO Manager) GPIO mode set to BCM")
    else:
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (GPIO Manager) Debug mode enabled, GPIO will be simulated")

def cleanup_gpio():
    """
    Clean up GPIO resources. This should be called when the application is shutting down.
    """
    if not DEBUG_MODE:
        GPIO.cleanup()
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (GPIO Manager) GPIO resources cleaned up")
    else:
        print(f"[{time.strftime('%m-%d-%Y %H:%M:%S')}] - (GPIO Manager) Debug mode enabled, GPIO resources not cleaned up") 