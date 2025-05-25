const OUTPUT_DEVICES = ['atomizer', 'light', 'water', 'heater']
const INPUT_DEVICES = ['temperature_sensor', 'humidity_sensor', 'ultrasonic_trigger', 'ultrasonic_echo', 'soil_moisture_sensor', 'light_sensor']

document.addEventListener('DOMContentLoaded', () => {
  //
  // 2) Hook up your form-submit handler
  //
  const configForm = document.getElementById('config-form');
  if (configForm) {
    configForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const formData = new FormData(this);
      const jsonData = {};
      for (const [key, value] of formData.entries()) {
        jsonData[key] = value;
      }
      console.log(jsonData);
      fetch('/api/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(jsonData),
      })
      .then(r => r.json())
      .then(data => {
        if (data.success) alert('Configuration saved successfully!');
        else             alert('Error saving config: ' + data.message);
      })
      .catch(err => {
        console.error(err);
        alert('Error saving configuration. See console for details.');
      });
    });
  }

  //
  // 3) Load your current config
  //
  if (typeof getConfig === 'function') {
    getConfig();
  }

  //
  // 4) Wire up all of your dropdowns
  //
  document.querySelectorAll('.dropdown-container').forEach(container => {
    const label   = container.querySelector('.dropdown-label');
    const content = container.querySelector('.dropdown-content');

    // start "open"
    content.classList.add('active');
    container.classList.add('active');

    label.addEventListener('click', () => {
      content.classList.toggle('active');
      container.classList.toggle('active');
    });
  });
});

// your existing getConfig() function
function getConfig() {
  fetch('/api/config')
    .then(r => r.json())
    .then(data => {
      for (const [key, value] of Object.entries(data)) {
        const el = document.querySelector(`[name="${key}"]`);
        if (el) el.value = value;
      }
      if (data.light_schedule === 'custom') {
        const c = document.getElementById('custom-light-container');
        if (c) c.style.display = 'block';
      }
    })
    .catch(console.error);
}

function testDevice(device) {
    switch(device) {
        case 'light':
            testLight();
            break;
        case 'water':
            testWater();
            break;
        case 'atomizer':
            testAtomizer();
            break;
        case 'heater':
            testHeater();
            break;
        case 'light_sensor':
            testLightSensor();
            break;
        case 'humidity_sensor':
            testHumiditySensor();
            break;
        case 'temperature_sensor':
            testTemperatureSensor();
            break;
        case 'soil_moisture_sensor':
            testSoilMoistureSensor();
            break;
        case 'ultrasonic_sensor':
            testUltrasonicSensor();
            break;
        default:
            console.error('Unknown device:', device);
            return;
    }
}

function testLight() {
    testSinglePinDevice('light', 'light-pin');
}
function testWater() {
    testSinglePinDevice('water', 'water-pin');
}
function testAtomizer() {
    testSinglePinDevice('atomizer', 'atomizer-pin');
}
function testHeater() {
    testSinglePinDevice('heater', 'heater-pin');
}
function testLightSensor() {
    testSinglePinDevice('light_sensor', 'light-pin-in');
}
function testHumiditySensor() {
    testSinglePinDevice('humidity_sensor', 'humidity-pin-in');
}
function testTemperatureSensor() {
    testSinglePinDevice('temperature_sensor', 'temperature-pin-in');
}
function testSoilMoistureSensor() {
    testSinglePinDevice('soil_moisture_sensor', 'soil-moisture-pin-in');
}

function testUltrasonicSensor() {
    const triggerInput = document.getElementById('ultrasonic-trigger-pin-in');
    const echoInput = document.getElementById('ultrasonic-echo-pin-in');
    const triggerPin = triggerInput.value;
    const echoPin = echoInput.value;
    if (!triggerPin || isNaN(triggerPin) || triggerPin <= 0 ||
        !echoPin || isNaN(echoPin) || echoPin <= 0) {
        alert('Please enter valid GPIO pin numbers for both trigger and echo');
        return;
    }
    const body = {
        device: 'ultrasonic_sensor',
        trigger_pin: parseInt(triggerPin),
        echo_pin: parseInt(echoPin)
    };
    sendTestRequest(body, 'ultrasonic_sensor');
}

function testSinglePinDevice(device, inputId) {
    const pinInput = document.getElementById(inputId);
    const pin = pinInput.value;
    if (!pin || isNaN(pin) || pin < 0 || pin > 40) {
        alert('Please enter a valid GPIO pin number first');
        return;
    }
    const body = {
        device: device,
        pin: parseInt(pin)
    };
    sendTestRequest(body, device);
}

function sendTestRequest(body, device) {
    fetch('/api/test', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(body)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.status === 'success') {
            if (INPUT_DEVICES.includes(device)) {
                if (device === 'light_sensor' || device === 'soil_moisture_sensor') {
                    alert(`${device} is reading ${data.value}V`);
                } else {
                    alert(`${device} is reading ${data.value}`);
                }
            } else {
                alert(`fired ${device} 3 times`);
            }
        } else {
            alert(`Error testing ${device}: ${data.message || ''}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to test device');
    });
}