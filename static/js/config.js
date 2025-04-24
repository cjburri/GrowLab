// Show/hide custom light schedule options
document.getElementById('light-schedule')
  .addEventListener('change', function() {
    const custom = document.getElementById('custom-light-container');
    custom.style.display = (this.value === 'custom') ? 'block' : 'none';
  });

// Fetch current config on load
window.onload = function getConfig() {
  fetch('/api/config')
    .then(r => r.json())
    .then(data => {
      Object.entries(data).forEach(([key, val]) => {
        const el = document.querySelector(`[name="${key}"]`);
        if (el) el.value = val;
      });
      if (data.light_schedule === 'custom') {
        document.getElementById('custom-light-container').style.display = 'block';
      }
    })
    .catch(console.error);
};

// Submit form via fetch
document.getElementById('config-form')
  .addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const json = {};
    for (let [k, v] of formData.entries()) json[k] = v;

    fetch('/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(json)
    })
    .then(r => r.json())
    .then(data => {
      alert(data.success
        ? 'Configuration saved successfully!'
        : 'Error: ' + data.message);
    })
    .catch(err => {
      console.error(err);
      alert('Error saving configuration. See console for details.');
    });
});

// Dropdown toggle
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.dropdown-container').forEach(c => {
    const lbl = c.querySelector('.dropdown-label'),
          cnt = c.querySelector('.dropdown-content');
    // expand both by default
    c.classList.add('active');
    cnt.classList.add('active');
    lbl.addEventListener('click', () => {
      c.classList.toggle('active');
      cnt.classList.toggle('active');
    });
  });
}); 