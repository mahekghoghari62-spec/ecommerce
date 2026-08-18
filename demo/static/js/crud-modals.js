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
      .then(data => { modalBody.innerHTML = data.html; bindForm(url); bindFormsetAddButtons(); })
      .catch(err => {
        console.error('Failed to load modal:', err);
        modalBody.innerHTML = '<p class="text-danger">Failed to load.</p>';
      });
  }

  function addFormsetRow(prefix, rowClass) {
    const totalForms = document.querySelector('#id_' + prefix + '-TOTAL_FORMS');
    const container = document.getElementById(prefix === 'images' ? 'image-formset-rows' : 'variant-formset-rows');
    if (!totalForms || !container) return;

    const rows = container.querySelectorAll('.' + rowClass);
    const lastRow = rows[rows.length - 1];
    const newRow = lastRow.cloneNode(true);

    const formNum = parseInt(totalForms.value, 10);
    newRow.innerHTML = newRow.innerHTML.replace(
      new RegExp(prefix + '-(\\d+)-', 'g'),
      prefix + '-' + formNum + '-'
    );

    newRow.querySelectorAll('input').forEach(function (input) {
      if (input.type === 'checkbox') {
        input.checked = false;
      } else if (input.name && input.name.endsWith('-id')) {
        input.value = '';
      } else if (input.type !== 'hidden') {
        input.value = '';
      }
    });

    container.appendChild(newRow);
    totalForms.value = formNum + 1;
  }

  function bindFormsetAddButtons() {
    const addImageBtn = document.getElementById('add-image-row');
    if (addImageBtn) {
      addImageBtn.addEventListener('click', function () {
        addFormsetRow('images', 'image-form-row');
      });
    }
    const addVariantBtn = document.getElementById('add-variant-row');
    if (addVariantBtn) {
      addVariantBtn.addEventListener('click', function () {
        addFormsetRow('variants', 'variant-form-row');
      });
    }
  }

  function bindForm(url) {
    const form = modalBody.querySelector('form');
    if (!form) return;
    form.setAttribute('novalidate', 'novalidate');

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
      form.querySelectorAll('.custom-invalid-feedback').forEach(el => el.remove());
      const existingAlert = modalBody.querySelector('.modal-error-alert');
      if (existingAlert) existingAlert.remove();

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
          } else if (data.html) {
            modalBody.innerHTML = data.html;
            bindForm(url);
            bindFormsetAddButtons();
          } else if (data.error) {
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-danger modal-error-alert';
            alertDiv.textContent = data.error;
            modalBody.prepend(alertDiv);
          }
        })
        .catch(err => {
          console.error('Submit failed:', err);
          const alertDiv = document.createElement('div');
          alertDiv.className = 'alert alert-danger modal-error-alert';
          alertDiv.textContent = 'Something went wrong. Please try again.';
          modalBody.prepend(alertDiv);
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

document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.alert.alert-dismissible, .alert.alert-success, .alert.alert-info');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = 'opacity 0.5s ease';
      alert.style.opacity = '0';
      setTimeout(function () {
        alert.remove();
      }, 500);
    }, 3000);
  });
});