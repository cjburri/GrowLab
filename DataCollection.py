from app.services.DeviceManager import DeviceManager
from datetime import datetime
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv

# Load environment variables including database connection info
load_dotenv()

class DataCollection:
    def __init__(self):
        # Set up direct database connection
        db_uri = os.getenv('DATABASE_URL', 'sqlite:///app/growlab.db')
        self.engine = create_engine(db_uri)
        session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(session_factory)
        self.session = self.Session()
        
        # Import models - make sure they are defined properly with Base
        from app.models import Config, Reading, LightReading, TemperatureReading, HumidityReading, Water_Reading, Soil_Moisture_Reading
        
        self.models = {
            'Config': Config,
            'Reading': Reading,
            'LightReading': LightReading,
            'TemperatureReading': TemperatureReading,
            'HumidityReading': HumidityReading,
            'Water_Reading': Water_Reading,
            'Soil_Moisture_Reading': Soil_Moisture_Reading
        }
        
        # Initialize device manager
        self.config = self.session.query(Config).first()
        print(self.config)
        self.device_manager = DeviceManager(
            light_pin_in=self.config.light_pin_in,
            humidity_pin_in=self.config.humidity_pin_in,
            temperature_pin_in=self.config.temperature_pin_in,
            ultrasonic_trigger_pin_in=self.config.ultrasonic_trigger_pin_in,
            ultrasonic_echo_pin_in=self.config.ultrasonic_echo_pin_in,
            soil_moisture_pin_in=self.config.soil_moisture_pin_in,
            debug_mode=True if os.getenv('debug_mode') == 'true' else False
        )
        
        print(self.config)

    def collect_data(self):
        timestamp = datetime.now()
        reading = self.models['Reading']()
        reading.timestamp = timestamp
        self.session.add(reading)
        self.session.commit()
        try:
            # Process each sensor in a separate transaction
            self._collect_light_data(reading.id)
            self._collect_temperature_data(reading.id)
            self._collect_humidity_data(reading.id)
            self._collect_water_level_data(reading.id)
            self._collect_soil_moisture_data(reading.id)
            
        except Exception as e:
            print(f"Error in data collection: {e}")
    
    def _collect_light_data(self, reading_id):
        if self.device_manager.light_sensor is not None:
            light_level = self.device_manager.sense('light_sensor')
            if light_level is not None:
                try:
                    # Create a new reading with the specific type
                    light_reading = self.models['LightReading'](id=reading_id, light_level=light_level)
                    self.session.add(light_reading)
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                    print(f"Error saving light reading to database: {e}")
    
    def _collect_temperature_data(self, reading_id):
        if self.device_manager.temperature_sensor is not None:
            temperature = self.device_manager.sense('temperature_sensor')
            if temperature is not None:
                try:
                    # Create a new reading with the specific type
                    temperature_reading = self.models['TemperatureReading'](id=reading_id, temperature=temperature)
                    self.session.add(temperature_reading)
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                    print(f"Error saving temperature reading to database: {e}")
    
    def _collect_humidity_data(self, reading_id):
        if self.device_manager.humidity_sensor is not None:
            humidity = self.device_manager.sense('humidity_sensor')
            if humidity is not None:
                try:
                    # Create a new reading with the specific type
                    humidity_reading = self.models['HumidityReading'](id=reading_id, humidity=humidity)
                    self.session.add(humidity_reading)
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                    print(f"Error saving humidity reading to database: {e}")
    
    def _collect_water_level_data(self, reading_id):
        if self.device_manager.ultrasonic_sensor is not None:
            water_level = self.device_manager.sense('ultrasonic_sensor')
            if water_level is not None:
                try:
                    # Create a new reading with the specific type
                    water_reading = self.models['Water_Reading'](id=reading_id, water_level=water_level)
                    self.session.add(water_reading)
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                    print(f"Error saving water level reading to database: {e}")
    
    def _collect_soil_moisture_data(self, reading_id):
        if self.device_manager.soil_moisture_sensor is not None:
            soil_moisture = self.device_manager.sense('soil_moisture_sensor')
            if soil_moisture is not None:
                try:
                    # Create a new reading with the specific type
                    soil_moisture_reading = self.models['Soil_Moisture_Reading'](id=reading_id, soil_moisture=soil_moisture)
                    self.session.add(soil_moisture_reading)
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                    print(f"Error saving soil moisture reading to database: {e}")

    def __del__(self):
        # Clean up database session
        if hasattr(self, 'session'):
            self.session.close()
        if hasattr(self, 'Session'):
            self.Session.remove()

if __name__ == "__main__":
    data_collection = DataCollection()
    try:
        while True:
            data_collection.collect_data()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Data collection stopped")
    finally:
        
        # Execute the query and print results
        try:
            result = data_collection.session.execute(text("""
                SELECT 
                    r.timestamp,
                    tr.temperature,
                    hr.humidity,
                    lr.light_level,
                    wr.water_level,
                    smr.soil_moisture
                FROM reading r
                LEFT JOIN temperature_reading tr ON r.id = tr.id
                LEFT JOIN humidity_reading hr ON r.id = hr.id
                LEFT JOIN light_reading lr ON r.id = lr.id
                LEFT JOIN water_reading wr ON r.id = wr.id
                LEFT JOIN soil_moisture_reading smr ON r.id = smr.id
                ORDER BY r.timestamp ASC;
            """))
            
            print("\nQuery Results:")
            print("-" * 80)
            print(f"{'Timestamp':<26} {'Temp':<8} {'Humidity':<10} {'Light':<8} {'Water':<8} {'Soil':<8}")
            print("-" * 80)
            
            for row in result:
                print(f"{str(row.timestamp):<20} {row.temperature or 'N/A':<8} {row.humidity or 'N/A':<10} {row.light_level or 'N/A':<8} {row.water_level or 'N/A':<8} {row.soil_moisture or 'N/A':<8}")
                
            # Clean up
            if hasattr(data_collection, 'session'):
                data_collection.session.close()
            if hasattr(data_collection, 'Session'):
                data_collection.Session.remove()
            
        except Exception as e:
            print(f"Error executing query: {e}")
