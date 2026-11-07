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
