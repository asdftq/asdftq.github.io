(() => {
  'use strict';
  document.querySelectorAll('[data-timer]').forEach(root => {
    const digits = root.querySelector('[data-digits]');
    const progress = root.querySelector('progress');
    const status = root.querySelector('[data-timer-status]');
    const start = root.querySelector('[data-start]');
    const reset = root.querySelector('[data-reset]');
    const input = root.querySelector('[data-minutes]');
    let total = Number(root.dataset.seconds) * 1000;
    let remaining = total, deadline = 0, running = false, frame = 0, announced = '';
    const announce = text => { if (announced !== text) { status.textContent = text; announced = text; } };
    const render = () => {
      if (running) remaining = Math.max(0, deadline - Date.now());
      const seconds = Math.ceil(remaining / 1000);
      digits.textContent = `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;
      progress.value = Math.max(0, Math.min(1, (total - remaining) / total));
      progress.setAttribute('aria-valuetext', `${seconds} seconds remaining`);
      if (running && remaining === 0) {
        running = false; root.dataset.state = 'finish'; start.textContent = 'Start again';
        announce('Time is up. Your timer is complete.');
      } else if (running) {
        announce(seconds <= 30 ? 'Closing cue — finish your main point.' : 'Running — keep your pace.');
      }
      if (running) frame = requestAnimationFrame(render);
    };
    start.addEventListener('click', () => {
      if (running) {
        remaining = Math.max(0, deadline - Date.now()); running = false;
        cancelAnimationFrame(frame); start.textContent = 'Resume'; announce('Paused'); render();
      } else {
        if (remaining <= 0) remaining = total;
        deadline = Date.now() + remaining; running = true; root.dataset.state = 'running';
        start.textContent = 'Pause'; render();
      }
    });
    const resetTimer = () => {
      running = false; cancelAnimationFrame(frame); remaining = total;
      root.dataset.state = 'ready'; start.textContent = 'Start timer'; announce('Ready when you are.'); render();
    };
    reset.addEventListener('click', resetTimer);
    input.addEventListener('change', () => {
      const minutes = Number(input.value);
      if (!Number.isFinite(minutes) || minutes < 1 / 60 || minutes > 360) {
        input.value = String(total / 60000); announce('Choose between one second and 360 minutes.'); return;
      }
      total = Math.round(minutes * 60000); resetTimer();
    });
    // One loop only: returning to a tab cancels the pending frame before rescheduling.
    document.addEventListener('visibilitychange', () => {
      if (!document.hidden && running) { cancelAnimationFrame(frame); render(); }
    });
    window.addEventListener('pagehide', () => { cancelAnimationFrame(frame); running = false; });
    render();
  });
})();
