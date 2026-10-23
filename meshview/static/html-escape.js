/* Shared HTML escaping for strings that come from the mesh (node names, channel ids,
   firmware strings, message text). Anything a radio can send must go through this
   before it is placed in innerHTML, insertAdjacentHTML or a Leaflet popup/tooltip. */
(function () {
    const MAP = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
    window.escapeHtml = function escapeHtml(value) {
        if (value === null || value === undefined) return "";
        return String(value).replace(/[&<>"']/g, ch => MAP[ch]);
    };
})();
