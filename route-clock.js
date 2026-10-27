(() => {
  'use strict';
  document.querySelectorAll('[data-route-clock]').forEach(root => {
    const dateInput = root.querySelector('input[type="date"]');
    const output = root.querySelector('[data-clock-output]');
    const origin = root.dataset.originZone, destination = root.dataset.destinationZone;
    const offset = (zone, date) => {
      const parts = new Intl.DateTimeFormat('en-US', { timeZone: zone, timeZoneName: 'longOffset' }).formatToParts(date);
      const label = parts.find(p => p.type === 'timeZoneName').value;
      if (label === 'GMT') return 0;
      const match = label.match(/GMT([+-])(\d{2}):(\d{2})/);
      if (!match) throw new Error('Time zone offset unavailable');
      return (Number(match[2]) + Number(match[3]) / 60) * (match[1] === '+' ? 1 : -1);
    };
    const render = () => {
      try {
        const date = new Date(`${dateInput.value}T12:00:00Z`);
        if (!Number.isFinite(date.getTime())) return;
        const shift = offset(destination, date) - offset(origin, date);
        output.textContent = `On ${dateInput.value}, the destination clock is ${Math.abs(shift)} hours ${shift >= 0 ? 'ahead of' : 'behind'} the origin clock (compared at 12:00 UTC). Check both local dates on your ticket.`;
      } catch { output.textContent = 'Use the dated clock examples below; your browser could not calculate this date.'; }
    };
    dateInput.addEventListener('change', render);
    // Explicit user edits stay local. No itinerary or dates are stored or transmitted.
    render();
  });
})();
