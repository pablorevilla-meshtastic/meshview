/* A short, shared arrival cue for the two live packet tables. */
window.markNewPacketArrival = function (row, startedAt = Date.now()) {
    const elapsed = Math.max(0, Date.now() - startedAt);
    const remaining = 1000 - elapsed;
    if (remaining <= 0) return;
    row.classList.add('packet-arrival-glow');
    row.style.setProperty('--packet-glow-delay', `${-elapsed}ms`);
    setTimeout(() => {
        row.classList.remove('packet-arrival-glow');
        row.style.removeProperty('--packet-glow-delay');
    }, remaining);
};
