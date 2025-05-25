from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Reading(db.Model):
    """Reading data from the grow system."""
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class LightReading(Reading):
    """Light reading data from the grow system."""
    id = db.Column(db.Integer, db.ForeignKey('reading.id'), primary_key=True)
    light_level = db.Column(db.Float, nullable=False)

class TemperatureReading(Reading):
    """Temperature reading data from the grow system."""
    id = db.Column(db.Integer, db.ForeignKey('reading.id'), primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    

class HumidityReading(Reading):
    """Humidity reading data from the grow system."""
    id = db.Column(db.Integer, db.ForeignKey('reading.id'), primary_key=True)
    humidity = db.Column(db.Float, nullable=False)

class Water_Reading(Reading):
    """Water reading data from the grow system."""
    id = db.Column(db.Integer, db.ForeignKey('reading.id'), primary_key=True)
    water_level = db.Column(db.Float, nullable=False)

class Soil_Moisture_Reading(Reading):
    """Soil moisture reading data from the grow system."""
    id = db.Column(db.Integer, db.ForeignKey('reading.id'), primary_key=True)
    soil_moisture = db.Column(db.Float, nullable=False)

class Config(db.Model):
    """Configuration settings for the grow system."""
    id = db.Column(db.Integer, primary_key=True)
    
    # Input pins
    light_pin_in = db.Column(db.Integer, default=1)
    humidity_pin_in = db.Column(db.Integer, default=1)
    temperature_pin_in = db.Column(db.Integer, default=1)
    ultrasonic_trigger_pin_in = db.Column(db.Integer, default=1)
    ultrasonic_echo_pin_in = db.Column(db.Integer, default=1)
    soil_moisture_pin_in = db.Column(db.Integer, default=1)
    
    # Output pins
    light_pin = db.Column(db.Integer, default=1)
    water_pin = db.Column(db.Integer, default=1)
    atomizer_pin = db.Column(db.Integer, default=1)
    heater_pin = db.Column(db.Integer, default=1)
    
    # Thresholds
    light_threshold = db.Column(db.Integer, default=40)
    humidity_threshold_low = db.Column(db.Integer, default=40)
    humidity_threshold_high = db.Column(db.Integer, default=40)
    temperature_threshold_low = db.Column(db.Integer, default=40)
    temperature_threshold_high = db.Column(db.Integer, default=40)
    water_level_threshold_low = db.Column(db.Integer, default=40)
    dry_soil_threshold = db.Column(db.Integer, default=40)
    watered_soil_threshold = db.Column(db.Integer, default=40)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization."""
        return {
            'light_pin_in': self.light_pin_in,
            'humidity_pin_in': self.humidity_pin_in,
            'temperature_pin_in': self.temperature_pin_in,
            'ultrasonic_trigger_pin_in': self.ultrasonic_trigger_pin_in,
            'ultrasonic_echo_pin_in': self.ultrasonic_echo_pin_in,
            'soil_moisture_pin_in': self.soil_moisture_pin_in,
            'light_pin': self.light_pin,
            'water_pin': self.water_pin,
            'atomizer_pin': self.atomizer_pin,
            'heater_pin': self.heater_pin,
            'light_threshold': self.light_threshold,
            'humidity_threshold_low': self.humidity_threshold_low,
            'humidity_threshold_high': self.humidity_threshold_high,
            'temperature_threshold_low': self.temperature_threshold_low,
            'temperature_threshold_high': self.temperature_threshold_high,
            'water_level_threshold_low': self.water_level_threshold_low,
            'dry_soil_threshold': self.dry_soil_threshold,
            'watered_soil_threshold': self.watered_soil_threshold
        }

class Log(db.Model):
    """Log data from the grow system."""
    id = db.Column(db.Integer, primary_key=True)
    event_code = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Event(db.Model):
    """Event data from the grow system."""
    id = db.Column(db.Integer, primary_key=True)
    event_string = db.Column(db.String(255), nullable=False)
    

