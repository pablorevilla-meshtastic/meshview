const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const template = fs.readFileSync(path.join(__dirname, '../meshview/templates/map-view.html'), 'utf8');
const functions = ['isNodeVisibleForPackets','isPacketReachVisible','clearPacketSeenHighlights',
    'schedulePacketSeenNodes','showPacketSeenNodes','updateNodeVisibility'].map(name => {
    const match = template.match(new RegExp(`(?:async )?function ${name}\\([^]*?\\n}`));
    assert.ok(match, name);
    return match[0];
}).join('\n');

function setup(fetchResponse) {
    const markers = {1:{getLatLng:()=>({lat:37,lng:-122})},
        2:{getLatLng:()=>({lat:38,lng:-123})},3:{getLatLng:()=>({lat:39,lng:-124})}};
    const visible = new Set([markers[1], markers[2]]);
    const filters = {'filter-channel-A':{checked:true},'filter-channel-B':{checked:false},
        'filter-routers-only':{checked:false},'filter-mqtt-only':{checked:false}};
    const nodeLayer = {hasLayer:marker=>visible.has(marker),addLayer:marker=>visible.add(marker),removeLayer:marker=>visible.delete(marker)};
    const reach = {layers:[],clearLayers(){this.layers=[];},removeLayer(layer){this.layers=this.layers.filter(item=>item!==layer);}};
    const timers = [];
    let calls = 0;
    const nodes = [{key:1,lat:37,long:-122,channel:'A',isRouter:true},
        {key:2,lat:38,long:-123,channel:'A',isRouter:false},
        {key:3,lat:39,long:-124,channel:'B',isRouter:true}];
    function item(points, options) {return {points,options,addTo(layer){layer.layers.push(this);return this;},
        getElement:()=>({getTotalLength:()=>100,style:{setProperty(){}}})};}
    const context = vm.createContext({
        console,document:{hidden:false,getElementById:id=>filters[id]},
        nodeLayer,packetSeenLayer:reach,map:{hasLayer:()=>true},markerById:markers,
        nodes,nodeMap:new Map(nodes.map(node=>[node.key,node])),channelSet:new Set(['A','B']),
        mapActivityGeneration:0,packetSeenGeneration:0,activePacketSeenHighlights:[],
        PACKET_SEEN_DELAY_MS:5000,PACKET_SEEN_COLOR:'#1f2937',PACKET_TRACE_MAX_DURATION_MS:6500,
        PACKET_TRACE_MIN_DURATION_MS:1500,PACKET_TRACE_MS_PER_PIXEL:18,PACKET_LANDING_DURATION_MS:1400,
        isInvalidCoord:node=>!node,getNodeLatLng:node=>({lat:node.lat,lng:node.long}),clearBlinkForMarker(){},
        setTimeout(callback,delay){const timer={callback,delay};timers.push(timer);return timer;},clearTimeout(timer){timer.cancelled=true;},
        fetch:async()=>{calls++;return fetchResponse ? fetchResponse() : {ok:true,json:async()=>({seen:[{node_id:2},{node_id:3}]})};},
        L:{polyline:item,circleMarker:item}
    });
    vm.runInContext(functions, context);
    return {context,reach,visible,markers,filters,timers,get calls(){return calls;}};
}
const packet = {id:10,from_node_id:1,channel:'A'};

test('hidden senders and deselected packet channels do not schedule or fetch reach',async()=>{
    const state=setup();
    state.visible.delete(state.markers[1]);
    state.context.schedulePacketSeenNodes(packet);
    await state.context.showPacketSeenNodes(packet);
    assert.equal(state.calls,0);
    assert.equal(state.timers.length,0);
    state.visible.add(state.markers[1]);
    await state.context.showPacketSeenNodes({...packet,channel:'B'});
    assert.equal(state.calls,0);
});

test('reach only draws toward gateways whose markers pass the filters',async()=>{
    const state=setup();
    await state.context.showPacketSeenNodes(packet);
    assert.equal(state.reach.layers.length,2); // white outline and travelling dot
    for(const layer of state.reach.layers)assert.equal(layer.points[1][0],38);
    state.context.updateNodeVisibility();
    assert.equal(state.reach.layers.length,0);
    assert.ok(state.timers.every(timer=>timer.cancelled));
});

test('filter changes invalidate an in-flight response even if channels are re-enabled',async()=>{
    let resolve;
    const state=setup(()=>new Promise(done=>resolve=done));
    const pending=state.context.showPacketSeenNodes(packet);
    state.filters['filter-channel-A'].checked=false;
    state.context.updateNodeVisibility();
    state.filters['filter-channel-A'].checked=true;
    state.context.updateNodeVisibility();
    resolve({ok:true,json:async()=>({seen:[{node_id:2}]})});
    await pending;
    assert.equal(state.reach.layers.length,0);
});

test('a gateway hidden before arrival does not receive a landing wave',async()=>{
    const state=setup();
    await state.context.showPacketSeenNodes(packet);
    state.visible.delete(state.markers[2]);
    state.timers[0].callback();
    assert.equal(state.reach.layers.length,2);
});

test('router-only filtering also clears existing reach and excludes clients',async()=>{
    const state=setup();
    state.filters['filter-routers-only'].checked=true;
    state.context.updateNodeVisibility();
    await state.context.showPacketSeenNodes(packet);
    assert.equal(state.reach.layers.length,0);
});
