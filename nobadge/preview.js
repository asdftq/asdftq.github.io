// Cosmetic, local-only preview. This never changes the visitor's Mac settings.
const controls = document.querySelector('.surface-controls');
const comparison = document.querySelector('.surface-comparison');
if (controls && comparison) {
  controls.hidden = false;
  controls.addEventListener('click', event => {
    const button = event.target.closest('button[data-surface]');
    if (!button) return;
    const surface = button.dataset.surface;
    comparison.dataset.activeSurface = surface;
    for (const control of controls.querySelectorAll('button')) {
      control.setAttribute('aria-pressed', String(control === button));
    }
    for (const scene of comparison.querySelectorAll('.mac-scene')) {
      scene.classList.toggle('dock-scene', surface === 'dock');
      scene.classList.toggle('switcher-scene', surface === 'switcher');
    }
    const before = comparison.querySelector('.scene-detail');
    before.textContent = surface === 'dock'
      ? 'The red dots keep calling.'
      : 'Badges follow you into ⌘Tab.';
    comparison.querySelector('.mac-scene').setAttribute('aria-label', `Before: ${before.textContent}`);
  });
}
