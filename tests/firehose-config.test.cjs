const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const template=fs.readFileSync(path.join(__dirname,'../meshview/templates/firehose.html'),'utf8');
const configure=template.match(/async function configureFirehose\(\)[^]*?\n}/)[0];
const startup=template.slice(template.lastIndexOf('    await loadTranslationsFirehose();'),template.lastIndexOf('});\n</script>'));

for(const [value,expected] of [[3,3000],[5,5000],[0,null],[-1,null],[undefined,3000],['invalid',3000]]) {
    test(`Firehose interval ${String(value)} preserves initial fetch and schedules correctly`,async()=>{
        const timers=[];
        let initialFetches=0;
        const context=vm.createContext({updateInterval:3000,
            window:{_siteConfigPromise:Promise.resolve({site:{firehose_interval:value}})},
            loadTranslationsFirehose:async()=>{},loadNodes:async()=>{},loadChannels:async()=>{},
            fetchUpdates:()=>initialFetches++,setInterval:(callback,delay)=>timers.push(delay)});
        await vm.runInContext(configure+'\n(async()=>{'+startup+'})()',context);
        assert.equal(initialFetches,1);
        assert.deepEqual(timers,expected===null?[]:[expected]);
    });
}
