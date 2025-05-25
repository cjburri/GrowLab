import pytest
from unittest.mock import patch, call
import time
import sys
import os

# Add the app directory to the path so we can import the Heater class
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.hardware.output.Heater import Heater, GPIO

class TestHeater:
    
    @pytest.fixture 
    def setup_heater(self):
        """Setup fixture for heater tests"""
        # Reset GPIO mock before each test
        GPIO.reset_mock()
        test_pin = 23
        return test_pin
    
    def test_init(self, setup_heater):
        """Test the initialization of the Heater class"""
        test_pin = setup_heater
        heater = Heater(test_pin)
        
        # Check that GPIO was set up correctly
        GPIO.setup.assert_called_once_with(test_pin, GPIO.OUT)
        GPIO.output.assert_called_once_with(test_pin, GPIO.LOW)
        
        # Check that attributes were set correctly
        assert heater.signal_pin == test_pin
        assert heater.state == GPIO.LOW
        assert heater.runtime == 0
        assert heater.debug_mode is False
    
    def test_init_debug_mode(self, setup_heater):
        """Test initialization in debug mode"""
        test_pin = setup_heater
        heater = Heater(test_pin, debug_mode=True)
        
        # GPIO should not be called in debug mode
        GPIO.setup.assert_not_called()
        GPIO.output.assert_not_called()
        
        assert heater.signal_pin == test_pin
        assert heater.state is False
        assert heater.runtime == 0
        assert heater.debug_mode is True
    
    def test_turn_on(self, setup_heater):
        """Test turning the heater on"""
        test_pin = setup_heater
        heater = Heater(test_pin)
        GPIO.reset_mock()  # Reset mock to clear initialization calls
        
        heater.turn_on()
        
        GPIO.output.assert_called_once_with(test_pin, GPIO.HIGH)
        assert heater.state == GPIO.HIGH
    
    def test_turn_off(self, setup_heater):
        """Test turning the heater off"""
        test_pin = setup_heater
        heater = Heater(test_pin)
        heater.state = GPIO.HIGH  # Set initial state to on
        GPIO.reset_mock()  # Reset mock to clear initialization calls
        
        heater.turn_off()
        
        GPIO.output.assert_called_once_with(test_pin, GPIO.LOW)
        assert heater.state == GPIO.LOW
    
    def test_get_status(self, setup_heater):
        """Test getting the heater status"""
        test_pin = setup_heater
        heater = Heater(test_pin)
        assert heater.get_status() == GPIO.LOW
        
        heater.state = GPIO.HIGH
        assert heater.get_status() == GPIO.HIGH
    
    def test_get_runtime(self, setup_heater):
        """Test getting the runtime"""
        test_pin = setup_heater
        heater = Heater(test_pin)
        assert heater.get_runtime() == 0
        
        heater.runtime = 42
        assert heater.get_runtime() == 42
    
    @patch('time.sleep')
    def test_heat_for_duration(self, mock_sleep, setup_heater):
        """Test heating for a specific duration"""
        test_pin = setup_heater
        heater = Heater(test_pin)
        GPIO.reset_mock()
        
        duration = 5
        heater.heat_for_duration(duration)
        
        # Check that the heater was turned on and off
        assert GPIO.output.call_count == 2
        GPIO.output.assert_has_calls([
            call(test_pin, GPIO.HIGH),
            call(test_pin, GPIO.LOW)
        ])
        
        # Check that sleep was called with the correct duration
        mock_sleep.assert_called_once_with(duration)
        
        # Check that runtime was updated
        assert heater.runtime == duration
    
    def test_get_usage_stats(self, setup_heater):
        """Test getting usage statistics"""
        test_pin = setup_heater
        heater = Heater(test_pin)
        heater.runtime = 42
        heater.state = GPIO.HIGH
        
        stats = heater.get_usage_stats()
        
        assert stats == {
            "runtime": 42,
            "state": GPIO.HIGH
        }
    
    def test_debug_mode_operations(self, setup_heater):
        """Test operations in debug mode"""
        test_pin = setup_heater
        heater = Heater(test_pin, debug_mode=True)
        GPIO.reset_mock()
        
        # Test turn on/off in debug mode
        heater.turn_on()
        heater.turn_off()
        
        # GPIO should not be called in debug mode
        GPIO.output.assert_not_called()
        
        # Test heat_for_duration in debug mode
        with patch('time.sleep') as mock_sleep:
            heater.heat_for_duration(5)
            mock_sleep.assert_called_once_with(5)
            assert heater.runtime == 5
    