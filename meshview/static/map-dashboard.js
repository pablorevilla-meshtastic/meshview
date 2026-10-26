/* UI only: reuse the map's nodes, markers, and existing API. */
function initializeNodeExplorer() {
    const activeSince = Date.now() - 24 * 60 * 60 * 1000;
    document.getElementById('metric-nodes').textContent = nodes.length.toLocaleString();
    document.getElementById('metric-active').textContent = nodes.filter(n => n.last_seen_us / 1000 >= activeSince).length.toLocaleString();
    document.getElementById('metric-gateways').textContent = nodes.filter(n => n.is_mqtt_gateway).length.toLocaleString();
    renderNodeExplorer();
}

function renderNodeExplorer() {
    const query = document.getElementById('node-search').value.trim().toLowerCase();
    const matches = nodes.filter(n => `${n.long_name} ${n.short_name} ${n.key} ${Number(n.key).toString(16)}`.toLowerCase().includes(query));
    matches.sort((a, b) => (b.last_seen_us || 0) - (a.last_seen_us || 0));
    const list = document.getElementById('mesh-node-list');
    list.replaceChildren();
    document.getElementById('node-result-count').textContent = matches.length;
    if (!matches.length) {
        const empty = document.createElement('p');
        empty.className = 'mesh-empty';
        empty.textContent = query ? 'No nodes match your search.' : 'No nodes seen in the last 3 days.';
        list.append(empty);
    }
    for (const node of matches) {
        const row = document.createElement('button');
        row.type = 'button';
        row.className = 'mesh-node-row';
        const active = node.last_seen_us / 1000 >= Date.now() - 86400000;
        row.innerHTML = `<span class="mesh-node-dot${active ? '' : ' offline'}" aria-hidden="true"></span><span class="mesh-node-copy"><strong>${escapeHtml(node.long_name || node.short_name || String(node.key))}</strong><small>${escapeHtml(node.short_name || 'Node')} · ${active ? 'Seen within 24h' : 'Seen within 3 days'}</small></span><span class="mesh-node-role">${markerById[node.key] ? '↗' : 'No GPS'}</span>`;
        row.addEventListener('click', () => {
            const marker = markerById[node.key];
            if (!marker) {
                openMapNodeInspector(node);
                return;
            }
            // Selecting a search result also reveals it if a saved filter hid it.
            nodeLayer.addTo(map);
            nodeLayer.addLayer(marker);
            map.setView(marker.getLatLng(), Math.max(map.getZoom(), 12));
            marker.fire('click');
        });
        list.append(row);
    }
}

document.getElementById('node-search').addEventListener('input', renderNodeExplorer);
document.getElementById('fit-network').addEventListener('click', () => {
    const points = Object.values(markerById).filter(marker => nodeLayer.hasLayer(marker)).map(marker => marker.getLatLng());
    if (points.length) map.fitBounds(L.latLngBounds(points), { padding: [35, 35], maxZoom: 13 });
});

(async () => {
    try {
        const response = await fetch('/api/stats/count');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const counts = await response.json();
        document.getElementById('metric-packets').textContent = Number(counts.total_packets || 0).toLocaleString();
        document.getElementById('metric-status').textContent = 'All packets in database';
    } catch (error) {
        document.getElementById('metric-status').textContent = 'Packet totals unavailable';
        console.error('Dashboard totals:', error);
    }
})();
