// Function to send control commands to the server
function updateControl(device, state) {
    fetch('/api/control', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            device: device,
            state: state
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(`${device} is now ${state ? 'ON' : 'OFF'}`);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Get initial status
function getStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            document.getElementById('light-control').checked = data.light;
            document.getElementById('humidifier-control').checked = data.humidifier;
            document.getElementById('water-control').checked = data.water;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

// Load initial status when page loads
window.onload = getStatus;

document.getElementById('light-control').addEventListener('change', function() {
    updateControl('light', this.checked);
});

document.getElementById('atomizer-control').addEventListener('change', function() {
    updateControl('atomizer', this.checked);
});

document.getElementById('water-control').addEventListener('change', function() {
    updateControl('water', this.checked);
});