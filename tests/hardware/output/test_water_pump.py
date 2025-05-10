import pytest
from unittest.mock import patch, call
import time
import sys
import os

# Add the app directory to the path so we can import the WaterPump class
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.hardware.output.WaterPump import WaterPump, GPIO

class TestWaterPump:
    
    @pytest.fixture
    def setup_pump(self):
        """Setup fixture for water pump tests"""
        # Reset GPIO mock before each test
        GPIO.reset_mock()
        test_pin = 18
        return test_pin
    
    def test_init(self, setup_pump):
        """Test the initialization of the WaterPump class"""
        test_pin = setup_pump
        pump = WaterPump(test_pin)
        
        # Check that GPIO was set up correctly
        GPIO.setup.assert_called_once_with(test_pin, GPIO.OUT)
        GPIO.output.assert_called_once_with(test_pin, GPIO.LOW)
        
        # Check that attributes were set correctly
        assert pump.signal_pin == test_pin
        assert pump.state == GPIO.LOW
        assert pump.runtime == 0
        assert pump.debug_mode is False
    
    def test_init_debug_mode(self, setup_pump):
        """Test initialization in debug mode"""
        test_pin = setup_pump
        pump = WaterPump(test_pin, debug_mode=True)
        
        # GPIO should not be called in debug mode
        GPIO.setup.assert_not_called()
        GPIO.output.assert_not_called()
        
        assert pump.signal_pin == test_pin
        assert pump.state is False
        assert pump.runtime == 0
        assert pump.debug_mode is True
    
    def test_turn_on(self, setup_pump):
        """Test turning the pump on"""
        test_pin = setup_pump
        pump = WaterPump(test_pin)
        GPIO.reset_mock()  # Reset mock to clear initialization calls
        
        pump.turn_on()
        
        GPIO.output.assert_called_once_with(test_pin, GPIO.HIGH)
        assert pump.state == GPIO.HIGH
    
    def test_turn_off(self, setup_pump):
        """Test turning the pump off"""
        test_pin = setup_pump
        pump = WaterPump(test_pin)
        pump.state = GPIO.HIGH  # Set initial state to on
        GPIO.reset_mock()  # Reset mock to clear initialization calls
        
        pump.turn_off()
        
        GPIO.output.assert_called_once_with(test_pin, GPIO.LOW)
        assert pump.state == GPIO.LOW
    
    def test_get_status(self, setup_pump):
        """Test getting the pump status"""
        test_pin = setup_pump
        pump = WaterPump(test_pin)
        assert pump.get_status() == GPIO.LOW
        
        pump.state = GPIO.HIGH
        assert pump.get_status() == GPIO.HIGH
    
    def test_get_runtime(self, setup_pump):
        """Test getting the runtime"""
        test_pin = setup_pump
        pump = WaterPump(test_pin)
        assert pump.get_runtime() == 0
        
        pump.runtime = 42
        assert pump.get_runtime() == 42
    
    @patch('time.sleep')
    def test_water_for_duration(self, mock_sleep, setup_pump):
        """Test watering for a specific duration"""
        test_pin = setup_pump
        pump = WaterPump(test_pin)
        GPIO.reset_mock()
        
        duration = 5
        pump.water_for_duration(duration)
        
        # Check that the pump was turned on and off
        assert GPIO.output.call_count == 2
        GPIO.output.assert_has_calls([
            call(test_pin, GPIO.HIGH),
            call(test_pin, GPIO.LOW)
        ])
        
        # Check that sleep was called with the correct duration
        mock_sleep.assert_called_once_with(duration)
        
        # Check that runtime was updated
        assert pump.runtime == duration
    
    @patch('time.sleep')
    def test_pulse_water(self, mock_sleep, setup_pump):
        """Test pulsing the water pump"""
        test_pin = setup_pump
        pump = WaterPump(test_pin)
        GPIO.reset_mock()
        
        on_time = 2
        off_time = 1
        cycles = 3
        
        pump.pulse_water(on_time, off_time, cycles)
        
        # Check that the pump was turned on and off the correct number of times
        # Each cycle: turn_on, turn_off = 2 calls per cycle
        assert GPIO.output.call_count == cycles * 2
        
        # Check that sleep was called with the correct durations
        # Each cycle: sleep(on_time), sleep(off_time)
        assert mock_sleep.call_count == cycles * 2
        
        expected_calls = []
        for _ in range(cycles):
            expected_calls.append(call(on_time))  # on_time for water_for_duration
            expected_calls.append(call(off_time))  # off_time between pulses
        
        mock_sleep.assert_has_calls(expected_calls)
        
        # Check that runtime was updated correctly
        assert pump.runtime == on_time * cycles
    
    def test_get_usage_stats(self, setup_pump):
        """Test getting usage statistics"""
        test_pin = setup_pump
        pump = WaterPump(test_pin)
        pump.runtime = 42
        pump.state = GPIO.HIGH
        
        stats = pump.get_usage_stats()
        
        assert stats == {
            "runtime": 42,
            "state": GPIO.HIGH
        }
    
    def test_debug_mode_operations(self, setup_pump):
        """Test operations in debug mode"""
        test_pin = setup_pump
        pump = WaterPump(test_pin, debug_mode=True)
        GPIO.reset_mock()
        
        # Test turn on/off in debug mode
        pump.turn_on()
        pump.turn_off()
        
        # GPIO should not be called in debug mode
        GPIO.output.assert_not_called()
        
        # Test water_for_duration in debug mode
        with patch('time.sleep') as mock_sleep:
            pump.water_for_duration(5)
            mock_sleep.assert_called_once_with(5)
            assert pump.runtime == 5