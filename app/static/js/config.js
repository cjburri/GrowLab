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

    // start “open”
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