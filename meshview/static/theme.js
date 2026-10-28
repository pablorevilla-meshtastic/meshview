/* Apply before paint; one preference shared by every Meshview page. */
(() => {
    const root = document.documentElement;
    const key = 'meshview-theme';
    const system = matchMedia('(prefers-color-scheme: dark)');
    let preference = null;
    try { preference = localStorage.getItem(key); } catch {}
    if (!['light','dark'].includes(preference)) preference = null;
    root.dataset.bsTheme = preference || (system.matches ? 'dark' : 'light');

    const colors = () => {
        const style = getComputedStyle(root);
        return {
            surface:style.getPropertyValue('--mesh-surface').trim(),
            text:style.getPropertyValue('--mesh-text').trim(),
            muted:style.getPropertyValue('--mesh-muted').trim(),
            border:style.getPropertyValue('--mesh-border').trim()
        };
    };
    // Neutral chart colors follow the theme; packet/route/series colors stay intact.
    function chartOption(option) {
        const palette = colors();
        const text = new Set(['#333','#334155','#243247','#26364a','#e7eef7','#e2ece5']);
        const muted = new Set(['#ccc','#64748b','#888','#9faea6','#8190a5']);
        const border = new Set(['#aaa','#c3cfdf','#34483c','#dce7df']);
        function visit(value, key) {
            if (Array.isArray(value)) return value.map(item => visit(item,key));
            if (value && Object.getPrototypeOf(value) === Object.prototype) {
                return Object.fromEntries(Object.entries(value).map(([k,v]) => [k,visit(v,k)]));
            }
            if (typeof value !== 'string') return value;
            const hex = value.toLowerCase();
            if (key === 'backgroundColor' && ['#fff','#ffffff','#18231e'].includes(hex)) return palette.surface;
            if (['borderColor','textBorderColor'].includes(key) && ['#fff','#ffffff','#000','#18231e'].includes(hex)) return palette.surface;
            if (key === 'color' && text.has(hex)) return palette.text;
            if (key === 'color' && muted.has(hex)) return palette.muted;
            if (key === 'color' && border.has(hex)) return palette.border;
            return value;
        }
        const themed = visit(option,'');
        themed.textStyle = {...themed.textStyle,color:palette.text};
        const tooltip = value => ({...value,backgroundColor:palette.surface,borderColor:palette.border,textStyle:{...value?.textStyle,color:palette.text}});
        if (Array.isArray(themed.tooltip)) themed.tooltip = themed.tooltip.map(tooltip);
        else themed.tooltip = tooltip(themed.tooltip);
        return themed;
    }
    const wrapped = new WeakSet();
    window.initMeshChart = (...args) => {
        const chart = window.echarts.init(...args);
        if (!wrapped.has(chart)) {
            const setOption = chart.setOption.bind(chart);
            chart.setOption = (option,...rest) => setOption(chartOption(option),...rest);
            wrapped.add(chart);
        }
        return chart;
    };
    function updateButton() {
        document.querySelectorAll('[data-theme-toggle]').forEach(button => {
            const dark = root.dataset.bsTheme === 'dark';
            button.setAttribute('aria-label',dark ? 'Switch to day mode' : 'Switch to night mode');
            button.setAttribute('aria-pressed',String(dark));
            button.title = dark ? 'Day mode' : 'Night mode';
        });
    }
    function apply(theme) {
        root.dataset.bsTheme = theme;
        updateButton();
        if (window.echarts) {
            document.querySelectorAll('[_echarts_instance_]').forEach(el => {
                const chart = window.echarts.getInstanceByDom(el);
                if (chart) chart.setOption(chartOption(chart.getOption()));
            });
        }
        document.dispatchEvent(new CustomEvent('meshview:themechange',{detail:theme}));
    }
    document.addEventListener('DOMContentLoaded',() => {
        updateButton();
        document.querySelectorAll('[data-theme-toggle]').forEach(button => {
            button.addEventListener('click',() => {
                preference = root.dataset.bsTheme === 'dark' ? 'light' : 'dark';
                try { localStorage.setItem(key,preference); } catch {}
                apply(preference);
            });
        });
    });
    system.addEventListener('change',event => {
        if (!preference) apply(event.matches ? 'dark' : 'light');
    });
    window.addEventListener('storage',event => {
        if (event.key !== key && event.key !== null) return;
        preference = ['light','dark'].includes(event.newValue) ? event.newValue : null;
        apply(preference || (system.matches ? 'dark' : 'light'));
    });
})();
