from flask import Blueprint, render_template, request, jsonify

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    return render_template('index.html', active_page='home')

@bp.route('/config')
def config():
    # Get current configuration
    # This is a placeholder - you'll need to implement actual config retrieval
    current_config = {
        'light_pin_out': 24,
        'water_pin_out': 23,
        'atomizer_pin_out': 25,
        'heater_pin_out': 1,
        'light_pin_in': 1,
        'humidity_pin_in': 1,
        'temperature_pin_in': 4,
        'ultrasonic_pin_in': 1,
        'soil_moisture_pin_in': 1,
    }
    return render_template('config.html', active_page='config', config=current_config)


@bp.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    if request.method == 'GET':
        # Return current configuration
        # This is a placeholder - implement actual config retrieval
        return jsonify({
            'light_pin': 17,
            'water_pin': 18,
            'humidifier_pin': 27,
            'watering_duration': 5,
            'light_schedule': '18/6',
            'custom_light_on': 16,
            'humidity_target': 65,
            'humidity_tolerance': 5
        })
    else:  # POST
        # Save new configuration
        config_data = request.json
        
        # Validate and save configuration
        # This is a placeholder - implement actual config saving
        
        return jsonify({'success': True}) 


@bp.route('/api/control', methods=['POST'])
def control():
    data = request.json
    device = data.get('device')
    state = data.get('state')
    
    if device == 'water':
        pin = WATER_RELAY_PIN
    # elif device == 'light':
    #     pin = LIGHT_RELAY_PIN
    # elif device == 'humidifier':
    #     pin = HUMIDIFIER_PIN
    else:
        return jsonify({'status': 'error', 'message': 'Invalid device'}), 400
    
    # Set the GPIO pin high or low based on the state
    if state:
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)
    
    return jsonify({'status': 'success', 'device': device, 'state': state})

# @bp.route('/api/status', methods=['GET'])
# def status():
#     # Return the current status of all devices
#     return jsonify({
#         'water': GPIO.input(WATER_RELAY_PIN) == GPIO.HIGH,
#         # 'light': GPIO.input(LIGHT_RELAY_PIN) == GPIO.HIGH,
#         # 'humidifier': GPIO.input(HUMIDIFIER_RELAY_PIN) == GPIO.HIGH
#     })

