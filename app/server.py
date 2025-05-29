from flask import Blueprint, render_template, request, jsonify
from app.models import db, Config, Reading, LightReading, TemperatureReading, HumidityReading, Water_Reading, Soil_Moisture_Reading, Log, Event
from app.services.DeviceManager import DeviceManager
from app.config import DEBUG_MODE
from app.hardware.gpio_manager import initialize_gpio, cleanup_gpio
import time
import datetime
from sqlalchemy import text

OUTPUT_DEVICES = ['atomizer', 'light', 'water', 'heater']
INPUT_DEVICES = ['temperature_sensor', 'humidity_sensor', 'ultrasonic_trigger', 'ultrasonic_echo', 'soil_moisture_sensor', 'light_sensor']

bp = Blueprint('api', __name__)

# Initialize GPIO at module level
initialize_gpio()

@bp.route('/')
def index():
    return render_template('index.html', active_page='home')

@bp.route('/config')
def config():
    # Get current configuration from database
    config = Config.query.first()
    return render_template('config.html', active_page='config', config=config)

@bp.route('/graph')
def graph():
    return render_template('graph.html', active_page='graph')

@bp.route('/api/config', methods=['GET'])
def get_config():
    # Get current configuration from database
    config = Config.query.first()
    if not config:
        # Create default config if none exists
        config = Config()
        db.session.add(config)
        db.session.commit()
    
    return jsonify(config.to_dict())

@bp.route('/api/config', methods=['POST'])
def update_config():
    # Get current configuration from database
    config = Config.query.first()
    if not config:
        config = Config()
        db.session.add(config)
    
    # Update configuration with form data
    data = request.json
    
    # Update each field if it exists in the request
    for key, value in data.items():
        if hasattr(config, key):
            # Convert string values to integers where needed
            if isinstance(getattr(config, key), int):
                try:
                    setattr(config, key, int(value))
                except ValueError:
                    return jsonify({'success': False, 'message': f'Invalid value for {key}'})
            else:
                setattr(config, key, value)
    
    # Save changes
    try:
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

# Add your existing control endpoints here
@bp.route('/api/status', methods=['GET'])
def get_status():
    # This is a placeholder - you'll need to implement actual status retrieval
    return jsonify({
        'light': False,
        'humidifier': False,
        'water': False
    })

@bp.route('/api/test', methods=['POST'])
def test_device():
    data = request.json
    print(data)
    device = data.get('device')
    if device == 'ultrasonic_sensor':
        trigger_pin = data.get('trigger_pin')
        echo_pin = data.get('echo_pin')
        device_manager = DeviceManager(ultrasonic_trigger_pin_in=trigger_pin, ultrasonic_echo_pin_in=echo_pin, debug_mode=DEBUG_MODE)
        value = device_manager.test_device(device, io="input")
        del device_manager
        return jsonify({'status': 'success', 'device': device, 'value': value})
    elif device == 'atomizer':
        device_manager = DeviceManager(atomizer_pin=data.get('pin'), debug_mode=DEBUG_MODE)
    elif device == 'light':
        device_manager = DeviceManager(light_pin=data.get('pin'), debug_mode=DEBUG_MODE)
    elif device == 'water':
        device_manager = DeviceManager(water_pin=data.get('pin'), debug_mode=DEBUG_MODE)
    elif device == 'heater':
        device_manager = DeviceManager(heater_pin=data.get('pin'), debug_mode=DEBUG_MODE)
    elif device == 'light_sensor':
        device_manager = DeviceManager(light_pin_in=data.get('pin'), debug_mode=DEBUG_MODE)
    elif device == 'temperature_sensor':
        device_manager = DeviceManager(temperature_pin_in=data.get('pin'), debug_mode=DEBUG_MODE)
    elif device == 'humidity_sensor':
        device_manager = DeviceManager(humidity_pin_in=data.get('pin'), debug_mode=DEBUG_MODE)
    elif device == 'soil_moisture_sensor':
        device_manager = DeviceManager(soil_moisture_pin_in=data.get('pin'), debug_mode=DEBUG_MODE)
    
    if device in OUTPUT_DEVICES:
        device_manager.test_device(device, io="output")
        return jsonify({'status': 'success', 'device': device})
    elif device in INPUT_DEVICES:
        value = device_manager.test_device(device, io="input")
        return jsonify({'status': 'success', 'device': device, 'value': value})

    del device_manager
    

@bp.route('/api/control', methods=['POST'])
def control_device():
    data = request.json
    device = data.get('device')
    state = data.get('state', False)

    device_manager = DeviceManager(debug_mode=DEBUG_MODE)
    if state:
        device_manager.turn_on(device)
    else:
        device_manager.turn_off(device)
    return jsonify({'status': 'success', 'device': device, 'state': state})

@bp.route('/database')
def database():
    # Define tables that can be viewed
    tables = {
        'Reading': 'Sensor readings base table',
        'LightReading': 'Light sensor readings',
        'TemperatureReading': 'Temperature sensor readings',
        'HumidityReading': 'Humidity sensor readings',
        'Water_Reading': 'Water level readings',
        'Soil_Moisture_Reading': 'Soil moisture readings',
        'Config': 'System configuration',
        'Log': 'System logs',
        'Event': 'System events'
    }
    return render_template('database.html', active_page='database', tables=tables)

@bp.route('/api/database/<table_name>', methods=['GET'])
def get_table_data(table_name):
    # Map table names to actual model classes
    models = {
        'Reading': Reading,
        'LightReading': LightReading,
        'TemperatureReading': TemperatureReading,
        'HumidityReading': HumidityReading,
        'Water_Reading': Water_Reading,
        'Soil_Moisture_Reading': Soil_Moisture_Reading,
        'Config': Config,
        'Log': Log,
        'Event': Event
    }
    
    # Check if the requested table exists
    if table_name not in models:
        return jsonify({'error': 'Table not found'}), 404
    
    # Get the model class
    model = models[table_name]
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    # For all sensor readings tables, use a joined query to include the timestamp
    if table_name in ['LightReading', 'TemperatureReading', 'HumidityReading', 'Water_Reading', 'Soil_Moisture_Reading']:
        # Build a custom query based on the sensor type
        if table_name == 'LightReading':
            # Custom query for light readings
            result = db.session.execute(text("""
                SELECT 
                    lr.id, lr.light_level, r.timestamp
                FROM light_reading lr
                JOIN reading r ON lr.id = r.id
                ORDER BY r.timestamp DESC
                LIMIT :limit OFFSET :offset
            """), {'limit': per_page, 'offset': (page - 1) * per_page})
            
            # Convert result to dict
            data = []
            for row in result:
                # Handle timestamp
                timestamp_value = row.timestamp
                if timestamp_value is not None:
                    if isinstance(timestamp_value, str):
                        formatted_timestamp = timestamp_value
                    else:
                        # It's a datetime object, so we can call isoformat()
                        formatted_timestamp = timestamp_value.isoformat()
                else:
                    formatted_timestamp = None
                    
                data.append({
                    'id': row.id,
                    'light_level': row.light_level,
                    'timestamp': formatted_timestamp
                })
            
            # Get total count for pagination
            count_result = db.session.execute(text("SELECT COUNT(*) as count FROM light_reading"))
            total = next(count_result).count
            
        elif table_name == 'TemperatureReading':
            # Custom query for temperature readings
            result = db.session.execute(text("""
                SELECT 
                    tr.id, tr.temperature, r.timestamp
                FROM temperature_reading tr
                JOIN reading r ON tr.id = r.id
                ORDER BY r.timestamp DESC
                LIMIT :limit OFFSET :offset
            """), {'limit': per_page, 'offset': (page - 1) * per_page})
            
            # Convert result to dict
            data = []
            for row in result:
                # Handle timestamp
                timestamp_value = row.timestamp
                if timestamp_value is not None:
                    if isinstance(timestamp_value, str):
                        formatted_timestamp = timestamp_value
                    else:
                        # It's a datetime object, so we can call isoformat()
                        formatted_timestamp = timestamp_value.isoformat()
                else:
                    formatted_timestamp = None
                    
                data.append({
                    'id': row.id,
                    'temperature': row.temperature,
                    'timestamp': formatted_timestamp
                })
            
            # Get total count for pagination
            count_result = db.session.execute(text("SELECT COUNT(*) as count FROM temperature_reading"))
            total = next(count_result).count
            
        elif table_name == 'HumidityReading':
            # Custom query for humidity readings
            result = db.session.execute(text("""
                SELECT 
                    hr.id, hr.humidity, r.timestamp
                FROM humidity_reading hr
                JOIN reading r ON hr.id = r.id
                ORDER BY r.timestamp DESC
                LIMIT :limit OFFSET :offset
            """), {'limit': per_page, 'offset': (page - 1) * per_page})
            
            # Convert result to dict
            data = []
            for row in result:
                # Handle timestamp
                timestamp_value = row.timestamp
                if timestamp_value is not None:
                    if isinstance(timestamp_value, str):
                        formatted_timestamp = timestamp_value
                    else:
                        # It's a datetime object, so we can call isoformat()
                        formatted_timestamp = timestamp_value.isoformat()
                else:
                    formatted_timestamp = None
                    
                data.append({
                    'id': row.id,
                    'humidity': row.humidity,
                    'timestamp': formatted_timestamp
                })
            
            # Get total count for pagination
            count_result = db.session.execute(text("SELECT COUNT(*) as count FROM humidity_reading"))
            total = next(count_result).count
            
        elif table_name == 'Water_Reading':
            # Custom query for water readings
            result = db.session.execute(text("""
                SELECT 
                    wr.id, wr.water_level, r.timestamp
                FROM water_reading wr
                JOIN reading r ON wr.id = r.id
                ORDER BY r.timestamp DESC
                LIMIT :limit OFFSET :offset
            """), {'limit': per_page, 'offset': (page - 1) * per_page})
            
            # Convert result to dict
            data = []
            for row in result:
                # Handle timestamp
                timestamp_value = row.timestamp
                if timestamp_value is not None:
                    if isinstance(timestamp_value, str):
                        formatted_timestamp = timestamp_value
                    else:
                        # It's a datetime object, so we can call isoformat()
                        formatted_timestamp = timestamp_value.isoformat()
                else:
                    formatted_timestamp = None
                    
                data.append({
                    'id': row.id,
                    'water_level': row.water_level,
                    'timestamp': formatted_timestamp
                })
            
            # Get total count for pagination
            count_result = db.session.execute(text("SELECT COUNT(*) as count FROM water_reading"))
            total = next(count_result).count
            
        elif table_name == 'Soil_Moisture_Reading':
            # Custom query for soil moisture readings
            result = db.session.execute(text("""
                SELECT 
                    smr.id, smr.soil_moisture, r.timestamp
                FROM soil_moisture_reading smr
                JOIN reading r ON smr.id = r.id
                ORDER BY r.timestamp DESC
                LIMIT :limit OFFSET :offset
            """), {'limit': per_page, 'offset': (page - 1) * per_page})
            
            # Convert result to dict
            data = []
            for row in result:
                # Handle timestamp
                timestamp_value = row.timestamp
                if timestamp_value is not None:
                    if isinstance(timestamp_value, str):
                        formatted_timestamp = timestamp_value
                    else:
                        # It's a datetime object, so we can call isoformat()
                        formatted_timestamp = timestamp_value.isoformat()
                else:
                    formatted_timestamp = None
                    
                data.append({
                    'id': row.id,
                    'soil_moisture': row.soil_moisture,
                    'timestamp': formatted_timestamp
                })
            
            # Get total count for pagination
            count_result = db.session.execute(text("SELECT COUNT(*) as count FROM soil_moisture_reading"))
            total = next(count_result).count
            
        return jsonify({
            'data': data, 
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        })
    
    # For joined tables, use a custom query
    elif table_name == 'Reading' and request.args.get('joined') == 'true':
        # Custom query for joined readings
        result = db.session.execute(text("""
            SELECT 
                r.id, r.timestamp,
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
            ORDER BY r.timestamp DESC
            LIMIT :limit OFFSET :offset
        """), {'limit': per_page, 'offset': (page - 1) * per_page})
        
        # Convert result to dict
        data = []
        for row in result:
            # Check if timestamp is already a string or a datetime object
            timestamp_value = row.timestamp
            if timestamp_value is not None:
                if isinstance(timestamp_value, str):
                    formatted_timestamp = timestamp_value
                else:
                    # It's a datetime object, so we can call isoformat()
                    formatted_timestamp = timestamp_value.isoformat()
            else:
                formatted_timestamp = None
                
            data.append({
                'id': row.id,
                'timestamp': formatted_timestamp,
                'temperature': row.temperature,
                'humidity': row.humidity,
                'light_level': row.light_level,
                'water_level': row.water_level,
                'soil_moisture': row.soil_moisture
            })
        
        # Get total count for pagination
        count_result = db.session.execute(text("SELECT COUNT(*) as count FROM reading"))
        total = next(count_result).count
        
        return jsonify({
            'data': data, 
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        })
    
    # For regular tables, use the default query
    else:
        # Get data from the table with pagination
        items = model.query.paginate(page=page, per_page=per_page)
        
        # Convert to dict
        data = []
        for item in items.items:
            item_dict = {}
            for column in item.__table__.columns:
                value = getattr(item, column.name)
                # Convert datetime to string for JSON
                if isinstance(value, datetime.datetime):
                    value = value.isoformat()
                # Handle any timestamp strings that might have been saved incorrectly
                elif column.name == 'timestamp' and isinstance(value, str):
                    value = value  # Keep as is, it's already a string
                item_dict[column.name] = value
            data.append(item_dict)
        
        return jsonify({
            'data': data, 
            'total': items.total,
            'page': page,
            'per_page': per_page,
            'pages': items.pages
        })

def cleanup():
    """Cleanup function to be called when the application is shutting down"""
    cleanup_gpio()

