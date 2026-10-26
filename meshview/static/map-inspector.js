/* Map inspection uses existing APIs and the map's shared packet polling events. */
(() => {
    const byId = id => document.getElementById(id);
    const packetHistory = new Map();
    const expandedPackets = new Set();
    const displayedPackets = new Set();
    const packetArrivals = new Map();
    let trafficLoaded = false;
    let nodeRequest = null;
    let inspectedNodeId = null;
    let recentPackets = [];
    let telemetryTime = -1;
    let paused = false;
    let trafficState = 'loading';
    const nodeKey = node => node.key ?? node.node_id;
    const findNode = id => nodeMap.get(Number(id)) || nodeMap.get(id);
    const nodeName = (id, fallback) => {
        const node = findNode(id);
        return node?.long_name || node?.short_name || fallback || `Node ${id}`;
    };
    const packetTime = packet => Number(packet.import_time_us) || 0;
    const packetId = packet => packet.storage_id ?? packet.id;
    const portName = packet => window.PORT_LABEL_MAP[packet.portnum] || `Port ${packet.portnum ?? '?'}`;
    const dateText = us => us ? new Date(Number(us) / 1000).toLocaleString() : 'Unknown time';
    const timeText = us => us ? new Date(Number(us) / 1000).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit', hour12:false}) : '—';


    async function fetchJson(url, signal) {
        const response = await fetch(url, {signal});
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
    }
    function note(container, text) {
        const p = document.createElement('p');
        p.className = 'mesh-inspector-note'; p.textContent = text;
        container.replaceChildren(p);
    }
    function facts(node) {
        byId('inspector-name').textContent = node.long_name || node.short_name || `Node ${nodeKey(node)}`;
        byId('inspector-node-meta').textContent = `${node.short_name || 'Node'} · ${nodeKey(node)}`;
        const container = byId('inspector-facts'); container.replaceChildren();
        for (const [label, value] of [
            ['Role', node.role || 'Unknown'], ['Hardware', node.hw_model || 'Unknown'],
            ['Firmware', node.firmware || 'Unknown'], ['Channel', node.channel || 'Unknown'],
            ['Gateway', node.is_mqtt_gateway == null ? 'Unknown' : node.is_mqtt_gateway ? 'Yes' : 'No'],
            ['Last seen', dateText(node.last_seen_us)],
            ['Location', isInvalidCoord(node) ? 'No reported position' : `${node.lat.toFixed(5)}, ${node.long.toFixed(5)}`]
        ]) {
            const dt = document.createElement('dt'); dt.textContent = label;
            const dd = document.createElement('dd'); dd.textContent = value;
            container.append(dt, dd);
        }
    }
    function normalizeNode(node) {
        return {...node, key: node.node_id, lat: node.last_lat / 1e7 || null, long: node.last_long / 1e7 || null};
    }
    function renderTelemetry(packet) {
        const container = byId('inspector-telemetry');
        if (packet && packetTime(packet) < telemetryTime) return;
        if (packet) telemetryTime = packetTime(packet);
        if (!packet && telemetryTime >= 0) return;
        if (!packet) { note(container, 'No telemetry packets found.'); return; }
        const payload = String(packet.payload || '');
        const value = field => {
            const match = payload.match(new RegExp(`(?:^|[\\s{])${field}:\\s*(-?\\d+(?:\\.\\d+)?)`));
            return match ? Number(match[1]) : null;
        };
        const battery = value('battery_level');
        const voltage = value('voltage');
        const channelUtil = value('channel_utilization');
        const airUtil = value('air_util_tx');
        const values = [
            ['Battery', battery === null ? null : battery > 100 ? 'Powered' : `${battery}%`],
            ['Voltage', voltage === null ? null : `${voltage.toFixed(2)} V`],
            ['Channel utilization', channelUtil === null ? null : `${channelUtil.toFixed(1)}%`],
            ['Air utilization TX', airUtil === null ? null : `${airUtil.toFixed(1)}%`]
        ].filter(([, value]) => value !== null);
        if (!values.length) { note(container, 'No device metrics in the latest telemetry packet.'); return; }
        container.replaceChildren();
        const grid = document.createElement('div'); grid.className = 'mesh-inspector-telemetry';
        for (const [label, value] of values) {
            const cell = document.createElement('div');
            const strong = document.createElement('strong'); strong.textContent = value;
            const span = document.createElement('span'); span.textContent = label;
            cell.append(strong, span); grid.append(cell);
        }
        const stamp = document.createElement('p'); stamp.className = 'mesh-inspector-note';
        stamp.textContent = `Reported ${dateText(packet.import_time_us)}`;
        container.append(grid, stamp);
    }
    function renderRecent() {
        const container = byId('inspector-recent');
        if (!recentPackets.length) { note(container, 'No recent packets found.'); return; }
        container.replaceChildren();
        for (const packet of recentPackets) {
            const button = document.createElement('a');
            button.href = `/packet/${encodeURIComponent(packetId(packet))}`;
            button.className = 'mesh-inspector-packet';
            const heading = document.createElement('strong');
            heading.textContent = `${portName(packet)} · ${timeText(packet.import_time_us)}`;
            const preview = document.createElement('small');
            preview.textContent = packet.payload || `From ${nodeName(packet.from_node_id, packet.long_name)}`;
            button.append(heading, preview);
            container.append(button);
        }
    }
    window.openMapNodeInspector = async (node, force = false) => {
        const id = String(nodeKey(node));
        if (!force && inspectedNodeId === id && !byId('mesh-node-inspector').hidden) return;
        nodeRequest?.abort();
        const request = new AbortController(); nodeRequest = request;
        inspectedNodeId = id; recentPackets = []; telemetryTime = -1;
        byId('mesh-node-browser').hidden = true;
        byId('mesh-node-inspector').hidden = false;
        byId('inspector-node-link').href = `/node/${encodeURIComponent(id)}`;
        byId('inspector-reliability-link').href = `/reliability?node_id=${encodeURIComponent(id)}`;
        facts(node);
        note(byId('inspector-telemetry'), 'Loading telemetry…');
        note(byId('inspector-recent'), 'Loading recent packets…');
        if (matchMedia('(max-width: 700px)').matches) byId('mesh-node-inspector').scrollIntoView({block:'nearest'});
        // A sender/gateway may be outside the map's recent-node snapshot.
        if (force || !findNode(id)) {
            fetchJson(`/api/nodes?node_id=${encodeURIComponent(id)}`, request.signal).then(data => {
                if (request.signal.aborted) return;
                const raw = data.nodes?.[0];
                if (raw) {
                    const complete = normalizeNode(raw); nodeMap.set(Number(id), complete); facts(complete);
                } else byId('inspector-node-meta').textContent = `Node ${id} · no node information available`;
            }).catch(error => {
                if (error.name !== 'AbortError') byId('inspector-node-meta').textContent = `Node ${id} · details unavailable`;
            });
        }
        await Promise.all([
            fetchJson(`/api/packets?from_node_id=${encodeURIComponent(id)}&portnum=67&limit=1`, request.signal).then(data => {
                if (request.signal.aborted) return;
                if (!Array.isArray(data.packets)) throw new Error('Invalid telemetry response');
                renderTelemetry(data.packets[0]);
            }).catch(error => {
                if (error.name !== 'AbortError') note(byId('inspector-telemetry'), 'Telemetry unavailable. Use Refresh data to retry.');
            }),
            fetchJson(`/api/packets?node_id=${encodeURIComponent(id)}&limit=8`, request.signal).then(data => {
                if (request.signal.aborted) return;
                if (!Array.isArray(data.packets)) throw new Error('Invalid packet response');
                const merged = new Map([...data.packets, ...recentPackets].map(p => [String(packetId(p)), p]));
                recentPackets = [...merged.values()].sort((a,b) => packetTime(b)-packetTime(a)).slice(0,8);
                renderRecent();
            }).catch(error => {
                if (error.name !== 'AbortError') note(byId('inspector-recent'), 'Recent packets unavailable. Use Refresh data to retry.');
            })
        ]);
    };
    byId('inspector-refresh').addEventListener('click', () => {
        if (inspectedNodeId) openMapNodeInspector(findNode(inspectedNodeId) || {key:Number(inspectedNodeId)}, true);
    });
    byId('inspector-back').addEventListener('click', () => {
        nodeRequest?.abort(); inspectedNodeId = null;
        byId('mesh-node-inspector').hidden = true;
        byId('mesh-node-browser').hidden = false;
        byId('node-search').focus({preventScroll:true});
    });

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
            if (inspectedNodeId && [packet.from_node_id,packet.to_node_id].some(id => String(id) === inspectedNodeId)) {
                const merged = new Map([...recentPackets,packet].map(p => [String(packetId(p)),p]));
                recentPackets = [...merged.values()].sort((a,b) => packetTime(b)-packetTime(a)).slice(0,8);
                renderRecent();
                if (String(packet.from_node_id) === inspectedNodeId && Number(packet.portnum) === 67) renderTelemetry(packet);
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
