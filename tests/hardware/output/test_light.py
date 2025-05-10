import pytest
from unittest.mock import patch, call
import time
import sys
import os

# Add the app directory to the path so we can import the Light class
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.hardware.output.Light import Light, GPIO

class TestLight:
    
    @pytest.fixture
    def setup_light(self):
        """Setup fixture for light tests"""
        # Reset GPIO mock before each test
        GPIO.reset_mock()
        test_pin = 27
        return test_pin
    
    def test_init(self, setup_light):
        """Test the initialization of the Light class"""
        test_pin = setup_light
        light = Light(test_pin)
        
        # Check that GPIO was set up correctly
        GPIO.setup.assert_called_once_with(test_pin, GPIO.OUT)
        GPIO.output.assert_called_once_with(test_pin, GPIO.LOW)
        
        # Check that attributes were set correctly
        assert light.signal_pin == test_pin
        assert light.state == GPIO.LOW
        assert light.runtime == 0
        assert light.debug_mode is False
    
    def test_init_debug_mode(self, setup_light):
        """Test initialization in debug mode"""
        test_pin = setup_light
        light = Light(test_pin, debug_mode=True)
        
        # GPIO should not be called in debug mode
        GPIO.setup.assert_not_called()
        GPIO.output.assert_not_called()
        
        assert light.signal_pin == test_pin
        assert light.state is False
        assert light.runtime == 0
        assert light.debug_mode is True
    
    def test_turn_on(self, setup_light):
        """Test turning the light on"""
        test_pin = setup_light
        light = Light(test_pin)
        GPIO.reset_mock()  # Reset mock to clear initialization calls
        
        light.turn_on()
        
        GPIO.output.assert_called_once_with(test_pin, GPIO.HIGH)
        assert light.state == GPIO.HIGH
    
    def test_turn_off(self, setup_light):
        """Test turning the light off"""
        test_pin = setup_light
        light = Light(test_pin)
        light.state = GPIO.HIGH  # Set initial state to on
        GPIO.reset_mock()  # Reset mock to clear initialization calls
        
        light.turn_off()
        
        GPIO.output.assert_called_once_with(test_pin, GPIO.LOW)
        assert light.state == GPIO.LOW
    
    def test_get_status(self, setup_light):
        """Test getting the light status"""
        test_pin = setup_light
        light = Light(test_pin)
        assert light.get_status() == GPIO.LOW
        
        light.state = GPIO.HIGH
        assert light.get_status() == GPIO.HIGH
    
    def test_get_runtime(self, setup_light):
        """Test getting the runtime"""
        test_pin = setup_light
        light = Light(test_pin)
        assert light.get_runtime() == 0
        
        light.runtime = 42
        assert light.get_runtime() == 42
    
    @patch('time.sleep')
    def test_light_for_duration(self, mock_sleep, setup_light):
        """Test lighting for a specific duration"""
        test_pin = setup_light
        light = Light(test_pin)
        GPIO.reset_mock()
        
        duration = 5
        light.illuminate_for_duration(duration)
        
        # Check that the light was turned on and off
        assert GPIO.output.call_count == 2
        GPIO.output.assert_has_calls([
            call(test_pin, GPIO.HIGH),
            call(test_pin, GPIO.LOW)
        ])
        
        # Check that sleep was called with the correct duration
        mock_sleep.assert_called_once_with(duration)
        
        # Check that runtime was updated
        assert light.runtime == duration
    
    def test_get_usage_stats(self, setup_light):
        """Test getting usage statistics"""
        test_pin = setup_light
        light = Light(test_pin)
        light.runtime = 42
        light.state = GPIO.HIGH
        
        stats = light.get_usage_stats()
        
        assert stats == {
            "runtime": 42,
            "state": GPIO.HIGH
        }
    
    def test_debug_mode_operations(self, setup_light):
        """Test operations in debug mode"""
        test_pin = setup_light
        light = Light(test_pin, debug_mode=True)
        GPIO.reset_mock()
        
        # Test turn on/off in debug mode
        light.turn_on()
        light.turn_off()
        
        # GPIO should not be called in debug mode
        GPIO.output.assert_not_called()
        
        # Test light_for_duration in debug mode
        with patch('time.sleep') as mock_sleep:
            light.illuminate_for_duration(5)
            mock_sleep.assert_called_once_with(5)
            assert light.runtime == 5 