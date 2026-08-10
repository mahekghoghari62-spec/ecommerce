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
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const formData = new FormData(form);
      fetch(url, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        body: formData,
      })
        .then(r => {
          if (!r.ok) {
            return r.text().then(text => { throw new Error('Status ' + r.status + ': ' + text); });
          }
          return r.json();
        })
        .then(data => {
          if (data.success) {
            modal.hide();
            window.location.reload();
          } else {
            modalBody.innerHTML = data.html;
            bindForm(url);
          }
        })
        .catch(err => {
          console.error('Form submit failed:', err);
          alert('Something went wrong — check console for details.');
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