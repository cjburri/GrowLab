from flask import Blueprint, render_template, request, jsonify

bp = Blueprint('api', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

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

