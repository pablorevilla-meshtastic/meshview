/* Home-only traffic table; shares packet polling with the map. */
(() => {
    const byId = id => document.getElementById(id);
    const packetHistory = new Map();
    const expandedPackets = new Set();
    const displayedPackets = new Set();
    const packetArrivals = new Map();
    let trafficLoaded = false;
    let paused = false;
    let trafficState = 'loading';
    const findNode = id => nodeMap.get(Number(id)) || nodeMap.get(id);
    const nodeName = (id, fallback) => {
        const node = findNode(id);
        return node?.long_name || node?.short_name || fallback || `Node ${id}`;
    };
    const packetTime = packet => Number(packet.import_time_us) || 0;
    const packetId = packet => packet.storage_id ?? packet.id;
    const portName = packet => window.PORT_LABEL_MAP[packet.portnum] || `Port ${packet.portnum ?? '?'}`;
    const dateText = us => us ? new Date(Number(us) / 1000).toLocaleString() : 'Unknown time';


    function renderTraffic() {
        const list = byId('map-traffic-list');
        const body = byId('map-traffic-body');
        const scrollTop = list.scrollTop;
        const focusedRow = document.activeElement?.closest('.mesh-traffic-row');
        const focusedId = focusedRow?.dataset.packetId;
        const focusedControl = document.activeElement?.dataset.trafficFocus;
        body.replaceChildren();
        const channel = byId('map-traffic-channel').value;
        const packets = [...packetHistory.values()].sort((a,b) => packetTime(b)-packetTime(a))
            .slice(0,30).filter(packet => !channel || packet.channel === channel);
        if (!packets.length) {
            const row = document.createElement('tr'); const cell = document.createElement('td');
            cell.colSpan = 6; cell.className = 'mesh-empty';
            cell.textContent = trafficState === 'error' ? 'Unable to load traffic. Use Refresh to try again.' :
                channel ? 'No packets for this channel in the latest sample.' : 'No packets received yet.';
            row.append(cell); body.append(row);
        }
        function nodeCell(id, label, isDestination = false) {
            const cell = document.createElement('td');
            if (Number(id) === 4294967295 || (isDestination && Number(id) === 1)) {
                const muted = document.createElement('span'); muted.className = 'mesh-inspector-note';
                muted.textContent = Number(id) === 4294967295 ? 'All' : 'Direct to MQTT'; cell.append(muted);
            } else {
                const link = document.createElement('a'); link.href = `/node/${encodeURIComponent(id)}`;
                link.textContent = nodeName(id,label); cell.append(link);
            }
            return cell;
        }
        for (const packet of packets) {
            const id = String(packetId(packet));
            const row = document.createElement('tr'); row.className = 'mesh-traffic-row'; row.dataset.packetId = id;
            const time = document.createElement('td'); time.className = 'mesh-traffic-time';
            time.textContent = packet.import_time_us ? new Date(Number(packet.import_time_us)/1000).toLocaleTimeString([], {hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false}) : '—';
            time.title = dateText(packet.import_time_us);
            const packetCell = document.createElement('td');
            const toggle = document.createElement('button'); toggle.type = 'button'; toggle.className = 'mesh-traffic-toggle';
            toggle.dataset.trafficFocus = 'toggle';
            toggle.setAttribute('aria-label', `Toggle payload for packet ${id}`);
            toggle.setAttribute('aria-expanded',String(expandedPackets.has(id)));
            toggle.textContent = expandedPackets.has(id) ? '▼' : '▶';
            const details = document.createElement('a'); details.href = `/packet/${encodeURIComponent(id)}`;
            details.dataset.trafficFocus = 'details'; details.title = 'View packet details';
            details.textContent = packet.packet_id == null ? 'Details' : String(packet.packet_id);
            packetCell.append(toggle,details);
            const channelCell = document.createElement('td'); channelCell.textContent = packet.channel || '—';
            const port = document.createElement('td');
            const tag = document.createElement('span'); tag.className = 'mesh-traffic-type'; tag.textContent = portName(packet);
            tag.style.backgroundColor = window.PORT_COLOR_MAP[packet.portnum] || '#6c757d';
            tag.title = packet.payload || '';
            const number = document.createElement('span'); number.className = 'mesh-traffic-port-number'; number.textContent = `(${packet.portnum ?? '?'})`;
            port.append(tag,number);
            row.append(time,packetCell,nodeCell(packet.from_node_id,packet.long_name),nodeCell(packet.to_node_id,packet.to_long_name,true),channelCell,port);
            const payloadRow = document.createElement('tr'); payloadRow.className = 'mesh-traffic-payload';
            payloadRow.hidden = !expandedPackets.has(id);
            const payloadCell = document.createElement('td'); payloadCell.colSpan = 6;
            const payload = document.createElement('pre'); payload.textContent = packet.payload || '(No decoded payload)';
            payloadCell.append(payload); payloadRow.append(payloadCell);
            toggle.addEventListener('click', () => {
                if (expandedPackets.has(id)) expandedPackets.delete(id); else expandedPackets.add(id);
                payloadRow.hidden = !expandedPackets.has(id);
                toggle.setAttribute('aria-expanded',String(!payloadRow.hidden)); toggle.textContent = payloadRow.hidden ? '▶' : '▼';
            });
            body.append(row,payloadRow);
            if (!displayedPackets.has(id)) {
                displayedPackets.add(id);
                packetArrivals.set(id,Date.now());
            }
            if (packetArrivals.has(id)) markNewPacketArrival(row,packetArrivals.get(id));
        }
        list.scrollTop = scrollTop;
        if (focusedId && focusedControl) {
            const row = [...body.children].find(row => row.dataset.packetId === focusedId);
            [...(row?.querySelectorAll('[data-traffic-focus]') || [])]
                .find(el => el.dataset.trafficFocus === focusedControl)?.focus({preventScroll:true});
        }
    }
    function renderTrafficStatus() {
        const el = byId('map-traffic-status');
        el.dataset.state = trafficState;
        el.textContent = paused ? 'Feed paused' : trafficState === 'error' ? 'Traffic unavailable' :
            trafficState === 'loading' ? 'Loading packets…' : mapInterval > 0 ? `Live · every ${mapInterval}s` : 'Snapshot · auto-refresh off';
    }
    document.addEventListener('mesh:traffic-status', event => {
        trafficState = event.detail; renderTrafficStatus();
        if (!paused && !packetHistory.size) renderTraffic();
    });
    document.addEventListener('mesh:packets', event => {
        let added = false;
        for (const packet of event.detail) {
            if (!packetHistory.has(String(packetId(packet)))) added = true;
            packetHistory.set(String(packetId(packet)),packet);
            if (!trafficLoaded) displayedPackets.add(String(packetId(packet)));
            if (packet.channel && ![...byId('map-traffic-channel').options].some(o => o.value === packet.channel)) {
                byId('map-traffic-channel').add(new Option(packet.channel,packet.channel));
            }
        }
        trafficLoaded = true;
        if (packetHistory.size > 30) {
            const sorted = [...packetHistory.values()].sort((a,b) => packetTime(b)-packetTime(a));
            for (const packet of sorted.slice(30)) {
                packetHistory.delete(String(packetId(packet))); expandedPackets.delete(String(packetId(packet)));
                displayedPackets.delete(String(packetId(packet))); packetArrivals.delete(String(packetId(packet)));
            }
        }
        if (!paused && added) renderTraffic();
    });
    byId('map-traffic-channel').addEventListener('change', () => renderTraffic());
    byId('map-traffic-pause').addEventListener('click', () => {
        paused = !paused;
        byId('map-traffic-pause').textContent = paused ? 'Resume feed' : 'Pause feed';
        byId('map-traffic-pause').setAttribute('aria-pressed',String(paused));
        if (!paused) renderTraffic();
        renderTrafficStatus();
    });
    byId('map-traffic-refresh').addEventListener('click', () => fetchLatestPacket());
})();
