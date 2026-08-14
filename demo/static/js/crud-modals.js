document.addEventListener('DOMContentLoaded', function () {
  const modalEl = document.getElementById('crudModal');
  if (!modalEl) return;
  const modal = new bootstrap.Modal(modalEl);
  const modalBody = document.getElementById('crudModalBody');
  const modalTitle = document.getElementById('crudModalLabel');

  function openModal(url, title) {
    modalTitle.textContent = title || '';
    modalBody.innerHTML = '<div class="text-center py-4"><div class="spinner-border" role="status"></div></div>';
    modal.show();
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
      .then(r => {
        if (!r.ok) {
          return r.text().then(text => { throw new Error('Status ' + r.status + ': ' + text); });
        }
        return r.json();
      })
      .then(data => { modalBody.innerHTML = data.html; bindForm(url); })
      .catch(err => {
        console.error('Failed to load modal:', err);
        modalBody.innerHTML = '<p class="text-danger">Failed to load.</p>';
      });
  }

  function bindForm(url) {
    const form = modalBody.querySelector('form');
    if (!form) return;
    form.setAttribute('novalidate', 'novalidate');

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      // Clear previous custom error states
      form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
      form.querySelectorAll('.custom-invalid-feedback').forEach(el => el.remove());

      // Check required fields manually, show red text below field
      let hasError = false;
      form.querySelectorAll('[required]').forEach(function (field) {
        if (!field.value || !field.value.trim()) {
          hasError = true;
          field.classList.add('is-invalid');
          const feedback = document.createElement('div');
          feedback.className = 'custom-invalid-feedback text-danger small mt-1';
          feedback.textContent = 'This field is required.';
          field.insertAdjacentElement('afterend', feedback);
        }
      });

      if (hasError) return;

      const formData = new FormData(form);
      fetch(url, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        body: formData,
      })
        .then(r => r.json())
        .then(data => {
          if (data.success) {
            modal.hide();
            window.location.reload();
          } else {
            modalBody.innerHTML = data.html;
            bindForm(url);
          }
        });
    });
  }
  document.body.addEventListener('click', function (e) {
    const trigger = e.target.closest('[data-modal-url]');
    if (!trigger) return;
    e.preventDefault();
    openModal(trigger.dataset.modalUrl, trigger.dataset.modalTitle);
  });
});
// Auto-dismiss success/info alert messages after a few seconds
document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.alert.alert-dismissible, .alert.alert-success, .alert.alert-info');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = 'opacity 0.5s ease';
      alert.style.opacity = '0';
      setTimeout(function () {
        alert.remove();
      }, 500);
    }, 3000); // 3 seconds visible, then fade out
  });
});