// Build the static API reference from the canonical Markdown, without runtime dependencies.
// Supports the headings, paragraphs, lists, links, rules, and fenced code used by this reference.
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const source = new URL('../docs/API_Documentation.md', import.meta.url);
const output = new URL('../meshview/static/api.html', import.meta.url);
const markdown = readFileSync(source, 'utf8');
const escape = text => text.replace(/[&<>"']/g, char => ({
    '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'
}[char]));
const slug = text => text.toLowerCase().replace(/`/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
function inline(text) {
    const tokens = /`([^`]+)`|\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*/g;
    let html = '', cursor = 0;
    for (const match of text.matchAll(tokens)) {
        html += escape(text.slice(cursor, match.index));
        if (match[1] !== undefined) html += `<code>${escape(match[1])}</code>`;
        else if (match[2] !== undefined && /^(#|\/|https?:\/\/)/.test(match[3])) {
            html += `<a href="${escape(match[3])}">${escape(match[2])}</a>`;
        } else if (match[4] !== undefined) html += `<strong>${escape(match[4])}</strong>`;
        else html += escape(match[0]);
        cursor = match.index + match[0].length;
    }
    return html + escape(text.slice(cursor));
}

const endpoints = [];
const blocks = [];
const lines = markdown.split('\n');
let sectionOpen = false;
for (let i = 0; i < lines.length;) {
    const line = lines[i];
    if (!line.trim()) { i++; continue; }
    if (line.startsWith('```')) {
        const language = line.slice(3).trim(); const code = []; i++;
        while (i < lines.length && !lines[i].startsWith('```')) code.push(lines[i++]);
        if (i === lines.length) throw new Error('Unclosed code fence');
        if (language === 'json') JSON.parse(code.join('\n'));
        blocks.push(`<pre><code class="language-${escape(language)}">${escape(code.join('\n'))}</code></pre>`);
        i++; continue;
    }
    const heading = line.match(/^(#{1,3})\s+(.+)$/);
    if (heading) {
        if (sectionOpen) { blocks.push('</section>'); sectionOpen = false; }
        const level = heading[1].length; const text = heading[2];
        if (level === 3 && text.startsWith('GET ')) {
            const id = slug(text); endpoints.push({text:text.replace(/`/g, ''),id});
            blocks.push(`<section class="endpoint" id="${id}"><h3><span class="method">GET</span> ${inline(text.slice(4))}</h3>`);
            sectionOpen = true;
        } else blocks.push(`<h${level} id="${slug(text)}">${inline(text)}</h${level}>`);
        i++; continue;
    }
    if (/^---+$/.test(line)) { blocks.push('<hr>'); i++; continue; }
    if (/^- /.test(line)) {
        const items = [];
        while (i < lines.length && /^- /.test(lines[i])) {
            let item = lines[i++].slice(2);
            while (i < lines.length && /^\s+\S/.test(lines[i])) item += ` ${lines[i++].trim()}`;
            items.push(`<li>${inline(item)}</li>`);
        }
        blocks.push(`<ul>${items.join('')}</ul>`); continue;
    }
    const paragraph = [line]; i++;
    while (i < lines.length && lines[i].trim() && !/^(#{1,3} |```|- |---+$)/.test(lines[i])) paragraph.push(lines[i++]);
    blocks.push(`<p>${inline(paragraph.join(' '))}</p>`);
}
if (sectionOpen) blocks.push('</section>');
const index = endpoints.map(({text,id}) => `<li><a href="#${id}">${escape(text)}</a></li>`).join('');
writeFileSync(output, `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Meshview API Reference</title>
<link rel="icon" type="image/svg+xml" href="/static/meshview-icon.svg">
<style>
:root { color-scheme:light; --primary:#187346; --border:#dce7df; }
* { box-sizing:border-box; }
html { scroll-padding-top:80px; }
body { margin:0; background:#f5f9f6; color:#243247; font:14px/1.7 system-ui,-apple-system,"Segoe UI",sans-serif; }
a { color:var(--primary); }
a:hover { color:#0f5132; }
header { background:var(--primary); color:white; position:sticky; top:0; z-index:2; box-shadow:0 2px 8px #174b2d18; }
.header-inner { max-width:1180px; margin:auto; min-height:56px; display:flex; align-items:center; gap:12px; padding:8px 24px; }
header img { width:32px; height:32px; }
header a { color:white; text-decoration:none; }
header a:hover { color:white; text-decoration:underline; }
.brand { font-size:18px; font-weight:700; display:flex; align-items:center; gap:10px; }
.home-link { margin-left:auto; font-size:13px; }
main { max-width:1180px; margin:auto; padding:28px 24px 60px; min-width:0; }
h1 { font-size:28px; margin:0 0 16px; } h2 { font-size:21px; margin:32px 0 14px; } h3 { font-size:17px; margin:0 0 16px; }
p,li { overflow-wrap:anywhere; }
code { font:12px/1.7 ui-monospace,Consolas,monospace; color:#155c39; background:#eaf5ee; border-radius:4px; padding:2px 5px; overflow-wrap:anywhere; }
pre { background:#f7faf8; border:1px solid var(--border); border-radius:7px; padding:16px; overflow:auto; }
pre code { background:none; padding:0; white-space:pre; color:#334155; }
h3 code { font-size:15px; }
.endpoint { background:white; border:1px solid var(--border); border-radius:9px; padding:24px; margin-bottom:22px; scroll-margin-top:12px; min-width:0; }
.method { display:inline-block; background:var(--primary); color:white; font-size:11px; padding:3px 8px; border-radius:5px; margin-right:5px; }
hr { border:0; border-top:1px solid var(--border); margin:24px 0; }
.api-index { background:white; border:1px solid var(--border); border-radius:9px; padding:16px 20px; margin-bottom:24px; }
.api-index summary { color:var(--primary); font-weight:600; cursor:pointer; }
.api-index ul { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px 24px; padding-left:20px; }
.api-index a { font:12px ui-monospace,monospace; }
:focus-visible { outline:2px solid var(--primary); outline-offset:3px; }
footer { border-top:1px solid var(--border); padding:20px 24px; text-align:center; color:#64748b; font-size:12px; }
@media(max-width:700px) { main { padding:20px 14px 40px; } .header-inner { padding:8px 14px; } h1 { font-size:24px; } h2 { font-size:19px; } h3 code { font-size:12px; } .endpoint { padding:16px; } .api-index ul { grid-template-columns:minmax(0,1fr); } }
</style>
</head>
<body>
<header><div class="header-inner"><a class="brand" href="/"><img src="/static/meshview-icon.svg" alt="" width="32" height="32">Meshview</a><span>API reference</span><a class="home-link" href="/">Home ↗</a></div></header>
<main>
<details class="api-index"><summary>Browse all ${endpoints.length} endpoints</summary><nav aria-label="API endpoints"><ul>${index}</ul></nav></details>
${blocks.join('\n')}
</main>
<footer>Source: docs/API_Documentation.md · Generated with node scripts/build-api-docs.mjs</footer>
</body>
</html>
`);
console.log(`Built ${endpoints.length} endpoint sections: ${fileURLToPath(output)}`);
