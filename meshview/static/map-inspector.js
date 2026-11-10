/* Shared node inspector for Home and Map, using existing APIs and packet events. */
(() => {
    const byId = id => document.getElementById(id);
    const panel = byId('mesh-node-panel');
    // Home stacks the node list under the map below 1000px; there it starts folded.
    const STACKED = matchMedia('(max-width: 1000px)');
    const listToggle = byId('node-panel-toggle');
    const listBody = byId('mesh-node-browser-body');
    function setNodeListOpen(open) {
        if (!listToggle || !listBody) return;
        listToggle.setAttribute('aria-expanded', String(open));
        listBody.hidden = !open;
    }
    function syncNodeListLayout() {
        if (!listToggle) return;
        listToggle.disabled = !STACKED.matches;
        setNodeListOpen(!STACKED.matches);
    }
    if (listToggle) {
        listToggle.addEventListener('click', () => {
            const open = listBody.hidden;
            setNodeListOpen(open);
            if (open) byId('node-search')?.focus({preventScroll:true});
        });
        STACKED.addEventListener('change', syncNodeListLayout);
        syncNodeListLayout();
    }
    const closeButton = byId('map-panel-close');
    if (closeButton) {
        let returnFocus = null;
        const close = () => {
            panel.hidden = true;
            window.clearMapSelection?.();
            (returnFocus?.isConnected ? returnFocus : byId('map')).focus({preventScroll:true});
        };
        closeButton.addEventListener('click', close);
        document.addEventListener('keydown', event => {
            if (event.key === 'Escape' && !panel.hidden) {
                event.preventDefault();
                close();
            }
        });
        // The live map uses its existing node snapshot, without packet-detail requests.
        window.openMapNodeInspector = node => {
            if (panel.hidden) returnFocus = document.activeElement;
            const id = node.key ?? node.node_id;
            const link = byId('inspector-node-link');
            link.textContent = node.short_name || String(id);
            link.href = `/node/${encodeURIComponent(id)}`;
            byId('inspector-name').textContent = node.long_name || node.short_name || MeshI18n.t("Node {id}", {id});
            byId('inspector-node-meta').textContent = MeshI18n.t("Node {id}", {id});
            const facts = byId('inspector-facts');
            facts.replaceChildren();
            for (const [label, value] of [
                [MeshI18n.t("Role"), node.role || MeshI18n.t("Unknown")],
                [MeshI18n.t("Channel"), node.channel || MeshI18n.t("Unknown")],
                [MeshI18n.t("Last seen"), node.last_seen_us ? new Date(Number(node.last_seen_us) / 1000).toLocaleString(MeshI18n.language) : MeshI18n.t("Unknown")]
            ]) {
                const dt = document.createElement('dt'); dt.textContent = label;
                const dd = document.createElement('dd'); dd.textContent = value;
                facts.append(dt, dd);
            }
            panel.hidden = false;
            closeButton.focus({preventScroll:true});
        };
        L.DomEvent.disableClickPropagation(panel);
        L.DomEvent.disableScrollPropagation(panel);
        return;
    }
    let nodeRequest = null;
    let inspectedNodeId = null;
    let recentPackets = [];
    let telemetryTime = -1;
    const nodeKey = node => node.key ?? node.node_id;
    const findNode = id => nodeMap.get(Number(id)) || nodeMap.get(id);
    const nodeName = (id, fallback) => {
        const node = findNode(id);
        return node?.long_name || node?.short_name || fallback || MeshI18n.t("Node {id}", {id});
    };
    const packetTime = packet => Number(packet.import_time_us) || 0;
    const packetId = packet => packet.storage_id ?? packet.id;
    const portName = packet => window.PORT_LABEL_MAP[packet.portnum] || MeshI18n.t("Port {port}", {port: packet.portnum ?? "?"});
    const dateText = us => us ? new Date(Number(us) / 1000).toLocaleString(MeshI18n.language) : MeshI18n.t("Unknown time");
    const timeText = us => us ? new Date(Number(us) / 1000).toLocaleTimeString(MeshI18n.language, {hour:'2-digit', minute:'2-digit', hour12:false}) : '—';


    async function fetchJson(url, signal) {
        const response = await fetch(url, {signal});
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
    }
    function note(container, text, loading = false) {
        const p = document.createElement('p');
        p.className = 'mesh-inspector-note'; p.textContent = text;
        p.classList.toggle('is-loading', loading);
        container.replaceChildren(p);
    }
    function facts(node) {
        byId('inspector-name').textContent = node.long_name || node.short_name || MeshI18n.t("Node {id}", {id: nodeKey(node)});
        byId('inspector-node-meta').textContent = `${node.short_name || MeshI18n.t("Node")} · ${nodeKey(node)}`;
        const container = byId('inspector-facts'); container.replaceChildren();
        for (const [label, value] of [
            [MeshI18n.t("Role"), node.role || MeshI18n.t("Unknown")], ['Hardware', node.hw_model || MeshI18n.t("Unknown")],
            [MeshI18n.t("Firmware"), node.firmware || MeshI18n.t("Unknown")], [MeshI18n.t("Channel"), node.channel || MeshI18n.t("Unknown")],
            [MeshI18n.t("Gateway"), node.is_mqtt_gateway == null ? MeshI18n.t("Unknown") : node.is_mqtt_gateway ? MeshI18n.t("Yes") : MeshI18n.t("No")],
            [MeshI18n.t("Last seen"), dateText(node.last_seen_us)],
            [MeshI18n.t("Location"), isInvalidCoord(node) ? MeshI18n.t("No reported position") : `${node.lat.toFixed(5)}, ${node.long.toFixed(5)}`]
        ]) {
            const dt = document.createElement('dt'); dt.textContent = label;
            const dd = document.createElement('dd'); dd.textContent = value;
            container.append(dt, dd);
        }
    }
    function normalizeNode(node) {
        return {...node, key: node.node_id, lat: node.last_lat / 1e7 || null, long: node.last_long / 1e7 || null};
    }
    // Device metrics (battery, voltage, channel and air utilization) found in a telemetry
    // packet; empty for the environment, power and other telemetry nodes send in between.
    function deviceMetrics(packet) {
        const payload = String(packet?.payload || '');
        const value = field => {
            const match = payload.match(new RegExp(`(?:^|[\\s{])${field}:\\s*(-?\\d+(?:\\.\\d+)?)`));
            return match ? Number(match[1]) : null;
        };
        const battery = value('battery_level');
        const voltage = value('voltage');
        const channelUtil = value('channel_utilization');
        const airUtil = value('air_util_tx');
        return [
            // Same icons as the node page charts.
            // Meshtastic reports a battery level above 100 when the node runs on external power.
            battery !== null && battery > 100
                ? [MeshI18n.t("Power"), MeshI18n.t("External"), 'plug']
                : [MeshI18n.t("Battery"), battery === null ? null : `${battery}%`, 'battery-2'],
            [MeshI18n.t("Voltage"), voltage === null ? null : `${voltage.toFixed(2)} V`, 'bolt'],
            [MeshI18n.t("Channel utilization"), channelUtil === null ? null : `${channelUtil.toFixed(1)}%`, 'antenna-bars-5'],
            [MeshI18n.t("Air utilization TX"), airUtil === null ? null : `${airUtil.toFixed(1)}%`, 'broadcast']
        ].filter(([, value]) => value !== null);
    }
    function showTelemetry(packet, values) {
        telemetryTime = packetTime(packet);
        const container = byId('inspector-telemetry');
        container.replaceChildren();
        const grid = document.createElement('div'); grid.className = 'mesh-inspector-telemetry';
        for (const [label, value, icon] of values) {
            const cell = document.createElement('div');
            const span = document.createElement('span');
            const mark = document.createElement('span'); mark.className = `ti ti-${icon}`; mark.setAttribute('aria-hidden', 'true');
            span.append(mark, label);
            const strong = document.createElement('strong'); strong.textContent = value;
            cell.append(span, strong); grid.append(cell);
        }
        const stamp = document.createElement('p'); stamp.className = 'mesh-inspector-note';
        stamp.textContent = MeshI18n.t("Reported {time}", {time: dateText(packet.import_time_us)});
        container.append(grid, stamp);
    }
    // Initial load: the newest of the recent telemetry packets that carries device metrics.
    function renderTelemetry(packets) {
        for (const packet of packets) {
            const values = deviceMetrics(packet);
            if (values.length) { showTelemetry(packet, values); return; }
        }
        if (telemetryTime >= 0) return;
        note(byId('inspector-telemetry'), packets.length
            ? MeshI18n.t("No device metrics in recent telemetry packets.")
            : MeshI18n.t("No telemetry packets found."));
    }
    // Live packets only replace the metrics shown with newer ones.
    function updateTelemetry(packet) {
        const values = deviceMetrics(packet);
        if (values.length && packetTime(packet) >= telemetryTime) showTelemetry(packet, values);
    }
    function renderRecent() {
        const container = byId('inspector-recent');
        if (!recentPackets.length) { note(container, MeshI18n.t("No recent packets found.")); return; }
        container.replaceChildren();
        for (const packet of recentPackets) {
            const hasPacketLink = Number(packet.portnum) !== 73 && Number(packetId(packet)) > 0;
            const button = document.createElement(hasPacketLink ? 'a' : 'div');
            if (hasPacketLink) button.href = `/packet/${encodeURIComponent(packetId(packet))}`;
            button.className = 'mesh-inspector-packet';
            const heading = document.createElement('strong');
            heading.textContent = `${portName(packet)} · ${timeText(packet.import_time_us)}`;
            const preview = document.createElement('small');
            preview.textContent = packet.payload || MeshI18n.t("From {name}", {name: nodeName(packet.from_node_id, packet.long_name)});
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
        note(byId('inspector-telemetry'), MeshI18n.t("Loading telemetry…"), true);
        note(byId('inspector-recent'), MeshI18n.t("Loading recent packets…"), true);
        if (STACKED.matches) byId('mesh-node-inspector').scrollIntoView({block:'nearest'});
        // A sender/gateway may be outside the map's recent-node snapshot.
        if (force || !findNode(id)) {
            fetchJson(`/api/nodes?node_id=${encodeURIComponent(id)}`, request.signal).then(data => {
                if (request.signal.aborted) return;
                const raw = data.nodes?.[0];
                if (raw) {
                    const complete = normalizeNode(raw); nodeMap.set(Number(id), complete); facts(complete);
                } else byId('inspector-node-meta').textContent = MeshI18n.t("Node {id} · no node information available", {id});
            }).catch(error => {
                if (error.name !== 'AbortError') byId('inspector-node-meta').textContent = MeshI18n.t("Node {id} · details unavailable", {id});
            });
        }
        await Promise.all([
            fetchJson(`/api/packets?from_node_id=${encodeURIComponent(id)}&portnum=67&limit=20`, request.signal).then(data => {
                if (request.signal.aborted) return;
                if (!Array.isArray(data.packets)) throw new Error('Invalid telemetry response');
                renderTelemetry(data.packets);
            }).catch(error => {
                if (error.name !== 'AbortError') note(byId('inspector-telemetry'), MeshI18n.t("Telemetry unavailable. Use Refresh data to retry."));
            }),
            fetchJson(`/api/packets?node_id=${encodeURIComponent(id)}&limit=8`, request.signal).then(data => {
                if (request.signal.aborted) return;
                if (!Array.isArray(data.packets)) throw new Error('Invalid packet response');
                const merged = new Map([...data.packets, ...recentPackets].map(p => [String(packetId(p)), p]));
                recentPackets = [...merged.values()].sort((a,b) => packetTime(b)-packetTime(a)).slice(0,8);
                renderRecent();
            }).catch(error => {
                if (error.name !== 'AbortError') note(byId('inspector-recent'), MeshI18n.t("Recent packets unavailable. Use Refresh data to retry."));
            })
        ]);
    };
    byId('inspector-refresh').addEventListener('click', () => {
        if (inspectedNodeId) openMapNodeInspector(findNode(inspectedNodeId) || {key:Number(inspectedNodeId)}, true);
    });
    byId('inspector-back').addEventListener('click', () => {
        nodeRequest?.abort(); inspectedNodeId = null;
        window.clearMapSelection?.();
        byId('mesh-node-inspector').hidden = true;
        byId('mesh-node-browser').hidden = false;
        setNodeListOpen(true);
        byId('node-search').focus({preventScroll:true});
    });

    document.addEventListener('mesh:packets', event => {
        for (const packet of event.detail) {
            if (inspectedNodeId && [packet.from_node_id,packet.to_node_id].some(id => String(id) === inspectedNodeId)) {
                const merged = new Map([...recentPackets,packet].map(p => [String(packetId(p)),p]));
                recentPackets = [...merged.values()].sort((a,b) => packetTime(b)-packetTime(a)).slice(0,8);
                renderRecent();
                if (String(packet.from_node_id) === inspectedNodeId && Number(packet.portnum) === 67) updateTelemetry(packet);
            }
        }
    });
})();
