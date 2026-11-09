const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(require('node:path').join(__dirname, '../meshview/static/i18n.js'), 'utf8');

function boot({catalog, language = 'es', fetch, elements = []} = {}) {
    const events = [];
    const document = {
        readyState: 'complete', documentElement: {},
        querySelectorAll(selector) {
            return elements.filter(el => selector === '[data-i18n]' ? el.dataset?.i18n :
                el.attributes?.[selector.slice(1,-1)]);
        },
        dispatchEvent(event) { events.push(event.type); }
    };
    const window = {meshLanguage: language};
    if (catalog !== undefined) window.meshTranslations = catalog;
    const context = {window, document, fetch, console, Intl, CustomEvent: class {constructor(type) {this.type = type;}}};
    vm.runInNewContext(source, context);
    return {api: window.MeshI18n, window, document, events};
}

test('bootstrap is synchronous; placeholders reorder, repeat, and preserve missing values', async () => {
    const {api, events} = boot({catalog: {'{a} then {b}': '{b}, {a}, {a}'}});
    assert.equal(api.t('{a} then {b}', {a: 'uno', b: 'dos'}), 'dos, uno, uno');
    assert.equal(api.t('{a} then {b}', {a: 'uno'}), '{b}, uno, uno');
    assert.equal(api.t('Untranslated'), 'Untranslated');
    assert.equal(api.t('constructor'), 'constructor');
    await api.ready;
    assert.deepEqual(events, ['meshview:languagechange']);
});

test('HTML interpolation escapes both translated text and network values', () => {
    const {api} = boot({catalog: {'Node {id}': '<b>Nodo {id}</b>'}});
    assert.equal(api.h('Node {id}', {id: '<img onerror="bad">&'}),
        '&lt;b&gt;Nodo &lt;img onerror=&quot;bad&quot;&gt;&amp;&lt;/b&gt;');
});

test('only explicitly marked static text and attributes are translated', async () => {
    const marked = {dataset: {i18n:'Search'}, textContent:'Search'};
    const payload = {dataset: {}, textContent:'Search'};
    const input = {attributes: {'data-i18n-placeholder':'Search'},
        getAttribute(key) {return this.attributes[key];},
        setAttribute(key,value) {this.attributes[key]=value;}};
    const {document,api} = boot({catalog: {Search:'Buscar'}, elements: [marked,payload,input]});
    await api.ready;
    assert.equal(marked.textContent,'Buscar');
    assert.equal(payload.textContent,'Search');
    assert.equal(input.attributes.placeholder,'Buscar');
    assert.equal(document.documentElement.lang,'es');
});

test('label translation preserves sort icons and child controls', () => {
    const {api} = boot({catalog:{}});
    const text = {nodeType:3,textContent:'Name '};
    const icon = {nodeType:1,textContent:'▲'};
    const el = {childNodes:[text,icon],children:[icon]};
    api.label(el,'Nombre');
    assert.equal(text.textContent,'Nombre ');
    assert.equal(icon.textContent,'▲');
    assert.equal(el.children[0],icon);
});

test('standalone pages load configured catalog, normalizing only the display locale', async () => {
    const urls = [];
    const {api} = boot({fetch:async url => {
        urls.push(url);
        return {ok:true,json:async () => url === '/api/config' ? {site:{language:'es_ES'}} : {Search:'Buscar'}};
    }});
    await api.ready;
    assert.deepEqual(urls,['/api/config','/api/lang?lang=es_ES&section=ui']);
    assert.equal(api.language,'es-ES');
    assert.equal(api.t('Search'),'Buscar');
});

test('failed static catalog request leaves English copy available', async () => {
    const {api} = boot({fetch:async url => ({ok:url==='/api/config',json:async () => ({})})});
    await api.ready;
    assert.equal(api.t('Search'),'Search');
});

test('map layer registration translates labels while preserving providers and overlay objects', () => {
    const path = require('node:path');
    const template = fs.readFileSync(path.join(__dirname, '../meshview/templates/map-view.html'), 'utf8');
    const registration = template.slice(template.indexOf('var overlayLayers ='), template.indexOf('// Data structures'));
    for (const language of ['en', 'es', 'ru']) {
        const catalog = JSON.parse(fs.readFileSync(path.join(__dirname, `../meshview/lang/${language}.json`))).ui;
        const {api} = boot({catalog, language});
        const nodeLayer = {}, packetSeenLayer = {}, trafficHeatLayer = {};
        const baseLayers = {OpenStreetMap: {}, OpenTopoMap: {}};
        const toggle = {setAttribute(key, value) {this[key] = value;}};
        let registered;
        vm.runInNewContext(registration, {
            MeshI18n: api, nodeLayer, packetSeenLayer, trafficHeatLayer, baseLayers, map: {},
            window: {matchMedia: () => ({matches: false})},
            L: {control: {layers(bases, overlays, options) {
                registered = {bases, overlays, options};
                return {addTo: () => ({getContainer: () => ({querySelector: () => toggle})})};
            }}}
        });
        assert.equal(registered.bases, baseLayers);
        assert.deepEqual(Object.keys(registered.overlays), [catalog.Nodes, catalog['Packets Reach'], catalog['Traffic HeatMap']]);
        assert.equal(registered.overlays[catalog.Nodes], nodeLayer);
        assert.equal(registered.overlays[catalog['Packets Reach']], packetSeenLayer);
        assert.equal(registered.overlays[catalog['Traffic HeatMap']], trafficHeatLayer);
        assert.equal(toggle.title, catalog['Map layers']);
        assert.equal(toggle['aria-label'], catalog['Map layers']);
    }
});

test('fresh map catalog replaces layer labels missing from the startup catalog', async () => {
    const path = require('node:path');
    const template = fs.readFileSync(path.join(__dirname, '../meshview/templates/map-view.html'), 'utf8');
    const loader = template.slice(template.indexOf('let mapTranslations = {};'), template.indexOf('var map = L.map'));
    const registration = template.slice(template.indexOf('var overlayLayers ='), template.indexOf('// Data structures'));
    for (const language of ['en', 'es', 'ru']) {
        const catalog = JSON.parse(fs.readFileSync(path.join(__dirname, `../meshview/lang/${language}.json`)));
        const {api} = boot({catalog: {Nodes: catalog.ui.Nodes}, language});
        const nodeLayer = {}, packetSeenLayer = {}, trafficHeatLayer = {};
        const overlays = new Map();
        const toggle = {setAttribute(key, value) {this[key] = value;}};
        const control = {
            addTo() {return this;},
            getContainer: () => ({querySelector: () => toggle}),
            removeLayer(layer) {overlays.delete(layer);},
            addOverlay(layer, label) {overlays.set(layer, label);}
        };
        const window = {matchMedia: () => ({matches: false}), _siteConfigPromise: Promise.resolve({site:{language}})};
        const context = vm.createContext({
            MeshI18n: api, nodeLayer, packetSeenLayer, trafficHeatLayer, baseLayers: {}, map: {}, window,
            document: {querySelectorAll: () => []},
            fetch: async () => ({json: async () => catalog.map}),
            console,
            L: {control: {layers(bases, labels) {
                for (const [label, layer] of Object.entries(labels)) overlays.set(layer, label);
                return control;
            }}}
        });
        vm.runInContext(fs.readFileSync(path.join(__dirname, '../meshview/static/html-escape.js'), 'utf8'), context);
        context.escapeHtml = window.escapeHtml;
        vm.runInContext(loader + registration, context);
        assert.equal(overlays.get(packetSeenLayer), 'Packets Reach');
        assert.equal(overlays.get(trafficHeatLayer), 'Traffic HeatMap');
        await vm.runInContext('loadTranslationsMap()', context);
        assert.equal(overlays.size, 3);
        assert.equal(overlays.get(nodeLayer), catalog.ui.Nodes);
        assert.equal(overlays.get(packetSeenLayer), catalog.ui['Packets Reach']);
        assert.equal(overlays.get(trafficHeatLayer), catalog.ui['Traffic HeatMap']);
        assert.equal(toggle.title, catalog.ui['Map layers']);
    }
});
