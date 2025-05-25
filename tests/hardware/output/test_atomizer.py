import pytest
from unittest.mock import patch, call
import time
import sys
import os

# Add the app directory to the path so we can import the Atomizer class
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.hardware.output.Atomizer import Atomizer, GPIO

class TestAtomizer:
    
    @pytest.fixture
    def setup_atomizer(self):
        """Setup fixture for atomizer tests"""
        # Reset GPIO mock before each test
        GPIO.reset_mock()
        test_pin = 17
        return test_pin
    
    def test_init(self, setup_atomizer):
        """Test the initialization of the Atomizer class"""
        test_pin = setup_atomizer
        atomizer = Atomizer(test_pin)
        
        # Check that GPIO was set up correctly
        GPIO.setup.assert_called_once_with(test_pin, GPIO.OUT)
        GPIO.output.assert_called_once_with(test_pin, GPIO.LOW)
        
        # Check that attributes were set correctly
        assert atomizer.signal_pin == test_pin
        assert atomizer.state == GPIO.LOW
        assert atomizer.runtime == 0
        assert atomizer.debug_mode is False
    
    def test_init_debug_mode(self, setup_atomizer):
        """Test initialization in debug mode"""
        test_pin = setup_atomizer
        atomizer = Atomizer(test_pin, debug_mode=True)
        
        # GPIO should not be called in debug mode
        GPIO.setup.assert_not_called()
        GPIO.output.assert_not_called()
        
        assert atomizer.signal_pin == test_pin
        assert atomizer.state is False
        assert atomizer.runtime == 0
        assert atomizer.debug_mode is True
    
    def test_turn_on(self, setup_atomizer):
        """Test turning the atomizer on"""
        test_pin = setup_atomizer
        atomizer = Atomizer(test_pin)
        GPIO.reset_mock()  # Reset mock to clear initialization calls
        
        atomizer.turn_on()
        
        GPIO.output.assert_called_once_with(test_pin, GPIO.HIGH)
        assert atomizer.state == GPIO.HIGH
    
    def test_turn_off(self, setup_atomizer):
        """Test turning the atomizer off"""
        test_pin = setup_atomizer
        atomizer = Atomizer(test_pin)
        atomizer.state = GPIO.HIGH  # Set initial state to on
        GPIO.reset_mock()  # Reset mock to clear initialization calls
        
        atomizer.turn_off()
        
        GPIO.output.assert_called_once_with(test_pin, GPIO.LOW)
        assert atomizer.state == GPIO.LOW
    
    def test_get_status(self, setup_atomizer):
        """Test getting the atomizer status"""
        test_pin = setup_atomizer
        atomizer = Atomizer(test_pin)
        assert atomizer.get_status() == GPIO.LOW
        
        atomizer.state = GPIO.HIGH
        assert atomizer.get_status() == GPIO.HIGH
    
    def test_get_runtime(self, setup_atomizer):
        """Test getting the runtime"""
        test_pin = setup_atomizer
        atomizer = Atomizer(test_pin)
        assert atomizer.get_runtime() == 0
        
        atomizer.runtime = 42
        assert atomizer.get_runtime() == 42
    
    @patch('time.sleep')
    def test_mist_for_duration(self, mock_sleep, setup_atomizer):
        """Test misting for a specific duration"""
        test_pin = setup_atomizer
        atomizer = Atomizer(test_pin)
        GPIO.reset_mock()
        
        duration = 5
        atomizer.atomize_for_duration(duration)
        
        # Check that the atomizer was turned on and off
        assert GPIO.output.call_count == 2
        GPIO.output.assert_has_calls([
            call(test_pin, GPIO.HIGH),
            call(test_pin, GPIO.LOW)
        ])
        
        # Check that sleep was called with the correct duration
        mock_sleep.assert_called_once_with(duration)
        
        # Check that runtime was updated
        assert atomizer.runtime == duration
    
    def test_get_usage_stats(self, setup_atomizer):
        """Test getting usage statistics"""
        test_pin = setup_atomizer
        atomizer = Atomizer(test_pin)
        atomizer.runtime = 42
        atomizer.state = GPIO.HIGH
        
        stats = atomizer.get_usage_stats()
        
        assert stats == {
            "runtime": 42,
            "state": GPIO.HIGH
        }
    
    def test_debug_mode_operations(self, setup_atomizer):
        """Test operations in debug mode"""
        test_pin = setup_atomizer
        atomizer = Atomizer(test_pin, debug_mode=True)
        GPIO.reset_mock()
        
        # Test turn on/off in debug mode
        atomizer.turn_on()
        atomizer.turn_off()
        
        # GPIO should not be called in debug mode
        GPIO.output.assert_not_called()
        
        # Test mist_for_duration in debug mode
        with patch('time.sleep') as mock_sleep:
            atomizer.atomize_for_duration(5)
            mock_sleep.assert_called_once_with(5)
            assert atomizer.runtime == 5 