from flask import Blueprint, render_template, request, jsonify
from app.models import db, Config
from app.services.DeviceManager import DeviceManager

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    return render_template('index.html', active_page='home')

@bp.route('/config')
def config():
    # Get current configuration from database
    config = Config.query.first()
    return render_template('config.html', active_page='config', config=config)

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
    
    device = request.json.get('device')
    pin = request.json.get('pin')
    if device == 'atomizer':
        device_manager = DeviceManager(atomizer_pin=pin, debug_mode=True)
    elif device == 'light':
        device_manager = DeviceManager(light_pin=pin, debug_mode=True)
    elif device == 'water':
        device_manager = DeviceManager(water_pin=pin, debug_mode=True)
    # elif device == 'humidifier':
    #     device_manager = DeviceManager(humidifier_pin=pin, debug_mode=True)
    # elif device == 'heater':
    #     device_manager = DeviceManager(heater_pin=pin, debug_mode=True)
    device_manager.test_device(device)
    del device_manager
    return jsonify({'status': 'success', 'device': device})

@bp.route('/api/control', methods=['POST'])
def control_device():
    # This is a placeholder - you'll need to implement actual device control
    data = request.json
    device = data.get('device')
    state = data.get('state', False)

    device_manager = DeviceManager()
    if state:
        device_manager.turn_on(device)
    else:
        device_manager.turn_off(device)
    # Here you would actually control the GPIO pins
    # For now, just return success
    return jsonify({'status': 'success', 'device': device, 'state': state})

