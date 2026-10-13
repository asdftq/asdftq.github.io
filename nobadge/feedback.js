(() => {
  const form = document.querySelector('#feedback-form');
  const message = document.querySelector('#feedback-message');
  const draft = document.querySelector('#email-draft');
  function updateDraft() {
    const rating = form.querySelector('input[name="rating"]:checked')?.value;
    const lines = ['NoBadge feedback', '', rating ? `Rating: ${rating} / 5` : 'Rating: not provided', '', message.value.slice(0, 3000)];
    draft.href = 'mailto:asdftqtq+nobadge@gmail.com?subject=' + encodeURIComponent('NoBadge feedback') + '&body=' + encodeURIComponent(lines.join('\n'));
  }
  form.addEventListener('input', updateDraft);
  form.addEventListener('submit', event => event.preventDefault());
  updateDraft();
})();
