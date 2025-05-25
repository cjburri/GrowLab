import pytest
from unittest.mock import patch, call, MagicMock
import time
import sys
import os

# Add the app directory to the path so we can import the RelayControlledComponent class
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.hardware.output.RelayControlledComponent import RelayControlledComponent, GPIO

class TestRelayControlledComponent:
    
    @pytest.fixture
    def setup_component(self):
        """Setup fixture for component tests"""
        # Reset GPIO mock before each test
        GPIO.reset_mock()
        test_pin = 22
        component_name = "TestComponent"
        return test_pin, component_name
    
    def test_init(self, setup_component):
        """Test the initialization of the RelayControlledComponent class"""
        test_pin, component_name = setup_component
        component = RelayControlledComponent(signal_pin=test_pin, component_name=component_name)
        
        # Check that GPIO was set up correctly
        GPIO.setup.assert_called_once_with(test_pin, GPIO.OUT)
        GPIO.output.assert_called_once_with(test_pin, GPIO.LOW)
        
        # Check that attributes were set correctly
        assert component.signal_pin == test_pin
        assert component.component_name == component_name
        assert component.state == GPIO.LOW
        assert component.runtime == 0
        assert component.debug_mode is False
    
    def test_init_debug_mode(self, setup_component):
        """Test initialization in debug mode"""
        test_pin, component_name = setup_component
        component = RelayControlledComponent(signal_pin=test_pin, component_name=component_name, debug_mode=True)
        
        # GPIO should not be called in debug mode
        GPIO.setup.assert_not_called()
        GPIO.output.assert_not_called()
        
        assert component.signal_pin == test_pin
        assert component.component_name == component_name
        assert component.state is False
        assert component.runtime == 0
        assert component.debug_mode is True
    
    def test_turn_on(self, setup_component):
        """Test turning the component on"""
        test_pin, component_name = setup_component
        component = RelayControlledComponent(signal_pin=test_pin, component_name=component_name)
        GPIO.reset_mock()  # Reset mock to clear initialization calls
        
        component.turn_on()
        
        GPIO.output.assert_called_once_with(test_pin, GPIO.HIGH)
        assert component.state == GPIO.HIGH
    
    def test_turn_off(self, setup_component):
        """Test turning the component off"""
        test_pin, component_name = setup_component
        component = RelayControlledComponent(signal_pin=test_pin, component_name=component_name)
        component.state = GPIO.HIGH  # Set initial state to on
        GPIO.reset_mock()  # Reset mock to clear initialization calls
        
        component.turn_off()
        
        GPIO.output.assert_called_once_with(test_pin, GPIO.LOW)
        assert component.state == GPIO.LOW
    
    def test_get_status(self, setup_component):
        """Test getting the component status"""
        test_pin, component_name = setup_component
        component = RelayControlledComponent(signal_pin=test_pin, component_name=component_name)
        assert component.get_status() == GPIO.LOW
        
        component.state = GPIO.HIGH
        assert component.get_status() == GPIO.HIGH
    
    def test_get_runtime(self, setup_component):
        """Test getting the runtime"""
        test_pin, component_name = setup_component
        component = RelayControlledComponent(signal_pin=test_pin, component_name=component_name)
        assert component.get_runtime() == 0
        
        component.runtime = 42
        assert component.get_runtime() == 42
    
    def test_get_usage_stats(self, setup_component):
        """Test getting usage statistics"""
        test_pin, component_name = setup_component
        component = RelayControlledComponent(signal_pin=test_pin, component_name=component_name)
        component.runtime = 42
        component.state = GPIO.HIGH
        
        stats = component.get_usage_stats()
        
        assert stats == {
            "runtime": 42,
            "state": GPIO.HIGH
        }
    
    def test_debug_mode_operations(self, setup_component):
        """Test operations in debug mode"""
        test_pin, component_name = setup_component
        component = RelayControlledComponent(signal_pin=test_pin, component_name=component_name, debug_mode=True)
        GPIO.reset_mock()
        
        # Test turn on/off in debug mode
        component.turn_on()
        component.turn_off()
        
        # GPIO should not be called in debug mode
        GPIO.output.assert_not_called() 