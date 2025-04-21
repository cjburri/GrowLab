from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO

app = Flask(__name__)

# GPIO Setup
WATER_PIN = 17  # Change this to the GPIO pin you want to use for water control
LIGHT_PIN = 18  # Change this to the GPIO pin for light
HUMIDIFIER_PIN = 27  # Change this to the GPIO pin for humidifier

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(WATER_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LIGHT_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(HUMIDIFIER_PIN, GPIO.OUT, initial=GPIO.LOW)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/control', methods=['POST'])
def control():
    data = request.json
    device = data.get('device')
    state = data.get('state')
    
    if device == 'water':
        pin = WATER_PIN
    elif device == 'light':
        pin = LIGHT_PIN
    elif device == 'humidifier':
        pin = HUMIDIFIER_PIN
    else:
        return jsonify({'status': 'error', 'message': 'Invalid device'}), 400
    
    # Set the GPIO pin high or low based on the state
    if state:
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)
    
    return jsonify({'status': 'success', 'device': device, 'state': state})

@app.route('/api/status', methods=['GET'])
def status():
    # Return the current status of all devices
    return jsonify({
        'water': GPIO.input(WATER_PIN) == GPIO.HIGH,
        'light': GPIO.input(LIGHT_PIN) == GPIO.HIGH,
        'humidifier': GPIO.input(HUMIDIFIER_PIN) == GPIO.HIGH
    })

# Clean up GPIO on server shutdown
def cleanup():
    GPIO.cleanup()

# Register cleanup function
import atexit
atexit.register(cleanup)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
