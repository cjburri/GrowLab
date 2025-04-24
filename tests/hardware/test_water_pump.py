import unittest
from unittest.mock import patch, call
import time
import sys
import os

# Add the app directory to the path so we can import the WaterPump class
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.hardware.WaterPump import WaterPump, GPIO

class TestWaterPump(unittest.TestCase):
    
    def setUp(self):
        # Reset GPIO mock before each test
        GPIO.reset_mock()
        self.test_pin = 18
        
    def test_init(self):
        """Test the initialization of the WaterPump class"""
        pump = WaterPump(self.test_pin)
        
        # Check that GPIO was set up correctly
        GPIO.setup.assert_called_once_with(self.test_pin, GPIO.OUT)
        GPIO.output.assert_called_once_with(self.test_pin, GPIO.LOW)
        
        # Check that attributes were set correctly
        self.assertEqual(pump.signal_pin, self.test_pin)
        self.assertEqual(pump.state, GPIO.LOW)
        self.assertEqual(pump.runtime, 0)
        self.assertFalse(pump.debug_mode)
    
    def test_init_debug_mode(self):
        """Test initialization in debug mode"""
        pump = WaterPump(self.test_pin, debug_mode=True)
        
        # GPIO should not be called in debug mode
        GPIO.setup.assert_not_called()
        GPIO.output.assert_not_called()
        
        self.assertEqual(pump.signal_pin, self.test_pin)
        self.assertEqual(pump.state, False)
        self.assertEqual(pump.runtime, 0)
        self.assertTrue(pump.debug_mode)
    
    def test_turn_on(self):
        """Test turning the pump on"""
        pump = WaterPump(self.test_pin)
        GPIO.reset_mock()  # Reset mock to clear initialization calls
        
        pump.turn_on()
        
        GPIO.output.assert_called_once_with(self.test_pin, GPIO.HIGH)
        self.assertEqual(pump.state, GPIO.HIGH)
    
    def test_turn_off(self):
        """Test turning the pump off"""
        pump = WaterPump(self.test_pin)
        pump.state = GPIO.HIGH  # Set initial state to on
        GPIO.reset_mock()  # Reset mock to clear initialization calls
        
        pump.turn_off()
        
        GPIO.output.assert_called_once_with(self.test_pin, GPIO.LOW)
        self.assertEqual(pump.state, GPIO.LOW)
    
    def test_get_status(self):
        """Test getting the pump status"""
        pump = WaterPump(self.test_pin)
        self.assertEqual(pump.get_status(), GPIO.LOW)
        
        pump.state = GPIO.HIGH
        self.assertEqual(pump.get_status(), GPIO.HIGH)
    
    def test_get_runtime(self):
        """Test getting the runtime"""
        pump = WaterPump(self.test_pin)
        self.assertEqual(pump.get_runtime(), 0)
        
        pump.runtime = 42
        self.assertEqual(pump.get_runtime(), 42)
    
    @patch('time.sleep')
    def test_water_for_duration(self, mock_sleep):
        """Test watering for a specific duration"""
        pump = WaterPump(self.test_pin)
        GPIO.reset_mock()
        
        duration = 5
        pump.water_for_duration(duration)
        
        # Check that the pump was turned on and off
        self.assertEqual(GPIO.output.call_count, 2)
        GPIO.output.assert_has_calls([
            call(self.test_pin, GPIO.HIGH),
            call(self.test_pin, GPIO.LOW)
        ])
        
        # Check that sleep was called with the correct duration
        mock_sleep.assert_called_once_with(duration)
        
        # Check that runtime was updated
        self.assertEqual(pump.runtime, duration)
    
    @patch('time.sleep')
    def test_pulse_water(self, mock_sleep):
        """Test pulsing the water pump"""
        pump = WaterPump(self.test_pin)
        GPIO.reset_mock()
        
        on_time = 2
        off_time = 1
        cycles = 3
        
        pump.pulse_water(on_time, off_time, cycles)
        
        # Check that the pump was turned on and off the correct number of times
        # Each cycle: turn_on, turn_off = 2 calls per cycle
        self.assertEqual(GPIO.output.call_count, cycles * 2)
        
        # Check that sleep was called with the correct durations
        # Each cycle: sleep(on_time), sleep(off_time)
        self.assertEqual(mock_sleep.call_count, cycles * 2)
        
        expected_calls = []
        for _ in range(cycles):
            expected_calls.append(call(on_time))  # on_time for water_for_duration
            expected_calls.append(call(off_time))  # off_time between pulses
        
        mock_sleep.assert_has_calls(expected_calls)
        
        # Check that runtime was updated correctly
        # In the RelayControlledComponent implementation, runtime is only incremented once per cycle
        self.assertEqual(pump.runtime, on_time * cycles)
    
    def test_get_usage_stats(self):
        """Test getting usage statistics"""
        pump = WaterPump(self.test_pin)
        pump.runtime = 42
        pump.state = GPIO.HIGH
        
        stats = pump.get_usage_stats()
        
        self.assertEqual(stats, {
            "runtime": 42,
            "state": GPIO.HIGH
        })
    
    def test_debug_mode_operations(self):
        """Test operations in debug mode"""
        pump = WaterPump(self.test_pin, debug_mode=True)
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
            self.assertEqual(pump.runtime, 5)

if __name__ == '__main__':
    unittest.main()
