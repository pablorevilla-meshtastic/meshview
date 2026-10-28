/* Read-only chat presentation using Meshview's existing packet API. */
document.addEventListener('DOMContentLoaded', async () => {
    const log = document.getElementById('chat-log');
    const channel = document.getElementById('channel-filter');
    const search = document.getElementById('chat-search');
    const status = document.getElementById('chat-status');
    const pause = document.getElementById('chat-pause');
    const latest = document.getElementById('chat-latest');
    const packets = new Map();
    let lastTime = null;
    let paused = false;
    let busy = false;
    let loaded = false;
    let unread = 0;
    let chatLang = {};
    const colors = ['#b54136', '#2563b4', '#23824d', '#8553af', '#a65d19', '#15817b', '#b63b79'];
    const timeOf = p => Number(p.import_time_us) || Date.parse(p.import_time) * 1000 || 0;
    const atBottom = () => log.scrollHeight - log.scrollTop - log.clientHeight < 60;
    const nodeName = p => (p.long_name || '').trim() || `Node ${p.from_node_id}`;
    const packetUrl = id => `/packet/${encodeURIComponent(id)}`;
    function setStatus(text, state) { status.textContent = text; status.dataset.state = state; }
    function goLatest() { log.scrollTop = log.scrollHeight; unread = 0; latest.textContent = '↓ Latest'; }

    function render(scrollToBottom = false, highlights = new Set()) {
        const query = search.value.trim().toLowerCase();
        const sorted = [...packets.values()].sort((a, b) => timeOf(a) - timeOf(b));
        const visible = sorted.filter(p => (!channel.value || (p.channel || '') === channel.value) &&
            `${nodeName(p)} ${p.payload || ''} ${p.from_node_id} ${p.channel || ''}`.toLowerCase().includes(query));
        const fragment = document.createDocumentFragment();
        let lastDay = '';
        const parents = new Map(sorted.map(p => [String(p.packet_id ?? p.id), p]));
        for (const packet of visible) {
            const date = new Date(timeOf(packet) / 1000);
            const day = date.toLocaleDateString([], { weekday:'long', month:'long', day:'numeric', year:'numeric' });
            if (day !== lastDay) {
                const separator = document.createElement('div');
                separator.className = 'chat-date-sep'; separator.textContent = day;
                fragment.append(separator); lastDay = day;
            }
            const row = document.createElement('article');
            row.className = `chat-line${highlights.has(String(packet.id)) ? ' flash' : ''}`;
            row.dataset.packetId = packet.id;
            let hash = 0;
            for (const char of String(packet.from_node_id)) hash = (hash * 31 + char.charCodeAt(0)) >>> 0;
            const time = document.createElement('time');
            time.className = 'chat-time'; time.dateTime = date.toISOString(); time.title = date.toLocaleString();
            time.textContent = date.toLocaleTimeString([], {hour:'2-digit', minute:'2-digit', hour12:false});
            const nick = document.createElement('a');
            nick.className = 'chat-nick'; nick.href = `/node/${encodeURIComponent(packet.from_node_id)}`;
            nick.textContent = nodeName(packet); nick.title = nodeName(packet); nick.style.color = colors[hash % colors.length];
            const message = document.createElement('div'); message.className = 'chat-message';
            // Mesh payloads and node names are untrusted text, never markup.
            message.textContent = packet.payload ?? '';
            if (packet.reply_id) {
                const reply = document.createElement('span'); reply.className = 'replying-to';
                const parent = parents.get(String(packet.reply_id)) || packets.get(String(packet.reply_id));
                reply.append(`${chatLang.replying_to || 'Replying to:'} `);
                if (parent) reply.append(`${nodeName(parent)}: ${parent.payload || ''}`);
                else {
                    const link = document.createElement('a'); link.href = packetUrl(packet.reply_id);
                    link.textContent = String(packet.reply_id); reply.append(link);
                }
                message.append(reply);
            }
            const meta = document.createElement('span'); meta.className = 'chat-meta';
            const tag = document.createElement('span'); tag.className = 'chat-channel';
            tag.textContent = packet.channel ? `# ${packet.channel}` : 'Unknown channel'; tag.title = packet.channel || 'Unknown channel';
            const details = document.createElement('a'); details.className = 'chat-details'; details.href = packetUrl(packet.id);
            details.textContent = 'Details ↗'; details.title = chatLang.view_packet_details || 'View packet details';
            details.setAttribute('aria-label', details.title);
            meta.append(tag, details); row.append(time, nick, message, meta); fragment.append(row);
        }
        if (!visible.length) {
            const empty = document.createElement('p'); empty.className = 'chat-empty';
            empty.textContent = packets.size ? 'No messages match your filters.' : 'No text messages received yet.';
            fragment.append(empty);
        }
        const previousTop = log.scrollTop;
        log.replaceChildren(fragment);
        document.getElementById('chat-count').textContent = `${visible.length} message${visible.length === 1 ? '' : 's'}`;
        if (scrollToBottom) goLatest(); else log.scrollTop = previousTop;
    }

    async function fetchMessages() {
        if (paused || busy || document.hidden) return;
        busy = true;
        try {
            const url = new URL('/api/packets', location.origin);
            url.searchParams.set('portnum', '1'); url.searchParams.set('limit', '100');
            if (lastTime) url.searchParams.set('since', lastTime);
            const response = await fetch(url);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            if (!Array.isArray(data.packets)) throw new Error('Invalid packet response');
            const follow = !loaded || atBottom();
            const added = new Set();
            for (const packet of data.packets) {
                const id = String(packet.id);
                if (!packets.has(id)) { packets.set(id, packet); added.add(id); }
                if (packet.channel && ![...channel.options].some(o => o.value === packet.channel)) {
                    channel.add(new Option(packet.channel, packet.channel));
                }
            }
            // Keep the browser's session history bounded without changing the API.
            if (packets.size > 1000) {
                const oldest = [...packets.values()].sort((a, b) => timeOf(a) - timeOf(b));
                for (const p of oldest.slice(0, packets.size - 1000)) packets.delete(String(p.id));
            }
            if (!loaded || added.size) render(follow, loaded ? added : new Set());
            if (loaded && !follow && added.size) {
                unread += [...added].filter(id => {
                    const p = packets.get(id);
                    return p && (!channel.value || p.channel === channel.value) &&
                        `${nodeName(p)} ${p.payload || ''} ${p.from_node_id} ${p.channel || ''}`.toLowerCase().includes(search.value.trim().toLowerCase());
                }).length;
                latest.textContent = unread ? `↓ Latest (${unread})` : '↓ Latest';
            }
            lastTime = data.latest_import_time || lastTime;
            loaded = true;
            setStatus(paused ? 'Paused' : 'Live', paused ? 'paused' : 'live');
            document.getElementById('chat-updated').textContent = `Updated ${new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})}`;
        } catch (error) {
            console.error('Chat fetch:', error);
            if (!paused) setStatus('Retrying…', 'error');
            if (!loaded) log.innerHTML = '<p class="chat-empty">Unable to load messages. Retrying automatically…</p>';
        } finally { busy = false; }
    }

    channel.addEventListener('change', () => render(true));
    search.addEventListener('input', () => render(true));
    latest.addEventListener('click', goLatest);
    log.addEventListener('scroll', () => { if (atBottom()) { unread = 0; latest.textContent = '↓ Latest'; } });
    pause.addEventListener('click', () => {
        paused = !paused; pause.setAttribute('aria-pressed', String(paused));
        pause.textContent = paused ? 'Resume' : 'Pause';
        setStatus(paused ? 'Paused' : 'Connecting…', paused ? 'paused' : 'loading');
        if (!paused) fetchMessages();
    });
    document.addEventListener('visibilitychange', () => { if (!document.hidden) fetchMessages(); });

    // Load optional translations and channel metadata without delaying messages.
    (async () => {
        try {
            const cfg = await window._siteConfigPromise;
            const response = await fetch(`/api/lang?lang=${encodeURIComponent(cfg?.site?.language || 'en')}&section=chat`);
            if (!response.ok) return;
            chatLang = await response.json();
            document.querySelectorAll('[data-chat-translate]').forEach(el => {
                if (chatLang[el.dataset.chatTranslate]) el.textContent = chatLang[el.dataset.chatTranslate];
            });
            if (loaded) render(atBottom());
        } catch (error) { console.error('Chat translations:', error); }
    })();
    (async () => {
        try {
            const response = await fetch('/api/channels');
            if (!response.ok) return;
            const data = await response.json();
            for (const name of data.channels || []) {
                if (![...channel.options].some(o => o.value === name)) channel.add(new Option(name, name));
            }
        } catch (error) { console.error('Chat channels:', error); }
    })();
    await fetchMessages();
    setInterval(fetchMessages, 5000);
});
