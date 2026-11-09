/* Translate application copy only. Mesh payloads and names never enter this lookup. */
(() => {
    let catalog = window.meshTranslations || {};
    function locale(value) {
        try { return Intl.getCanonicalLocales(String(value).replaceAll('_', '-'))[0] || 'en'; }
        catch { return 'en'; }
    }
    let language = locale(window.meshLanguage || 'en');
    function t(source, values = {}) {
        const text = Object.hasOwn(catalog, source) && typeof catalog[source] === 'string'
            ? catalog[source] : source;
        return text.replace(/\{(\w+)\}/g, (match, key) =>
            Object.hasOwn(values, key) ? String(values[key]) : match);
    }
    function h(source, values = {}) {
        return t(source, values).replace(/[&<>"']/g, char => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
        }[char]));
    }
    // Keep sort indicators and other child controls when translating a label.
    function label(element, value) {
        const text = [...element.childNodes].find(node => node.nodeType === 3 && node.textContent.trim());
        if (text) text.textContent = value + (element.children.length ? ' ' : '');
        else if (!element.children.length) element.textContent = value;
    }
    function apply(root = document) {
        root.querySelectorAll('[data-i18n]').forEach(el => {
            el.textContent = t(el.dataset.i18n);
        });
        for (const attr of ['title', 'aria-label', 'placeholder']) {
            root.querySelectorAll(`[data-i18n-${attr}]`).forEach(el => {
                el.setAttribute(attr, t(el.getAttribute(`data-i18n-${attr}`)));
            });
        }
        document.documentElement.lang = language;
    }
    const ready = (async () => {
        if (!window.meshTranslations) {
            try {
                window._siteConfigPromise ||= fetch('/api/config').then(response => {
                    if (!response.ok) throw new Error('Configuration unavailable');
                    return response.json();
                }).catch(() => ({}));
                const config = await window._siteConfigPromise;
                const selectedLanguage = config?.site?.language || 'en';
                language = locale(selectedLanguage);
                const response = await fetch(`/api/lang?lang=${encodeURIComponent(selectedLanguage)}&section=ui`);
                if (!response.ok) throw new Error('Translations unavailable');
                catalog = await response.json();
            } catch (error) { console.error('Translations:', error); }
        }
        if (document.readyState === 'loading') {
            await new Promise(resolve => document.addEventListener('DOMContentLoaded', resolve, {once: true}));
        }
        apply();
        document.dispatchEvent(new CustomEvent('meshview:languagechange'));
    })();
    window.MeshI18n = {t, h, label, apply, ready, get language() { return language; }};
})();
