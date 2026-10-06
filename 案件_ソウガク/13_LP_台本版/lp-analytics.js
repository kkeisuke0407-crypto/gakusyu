(() => {
  "use strict";
  const cfg = window.LP_ANALYTICS_CONFIG || {};
  const endpoint = String(cfg.endpoint || "");
  if (!endpoint || endpoint.includes("REPLACE_ME")) return;

  const site = cfg.site || location.hostname;
  const lp = cfg.lp || location.pathname;
  const sidKey = "__lpana_sid";
  const uuid = () => crypto.randomUUID ? crypto.randomUUID() :
    "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, c => {
      const r=Math.random()*16|0, v=c==="x"?r:(r&3|8); return v.toString(16);
    });
  let sessionId=sessionStorage.getItem(sidKey);
  if(!sessionId){ sessionId=uuid(); sessionStorage.setItem(sidKey,sessionId); }
  const pageId=uuid(), start=Date.now();
  let activeMs=0,lastTick=Date.now(),visible=!document.hidden;
  const sentScroll=new Set(), sentSections=new Set(), trail=[];
  const params=new URLSearchParams(location.search);
  const adKeys=["utm_source","utm_medium","utm_campaign","utm_term","utm_content","gclid","gbraid","wbraid","campaign_id","adgroup_id","keyword","matchtype","device","network","creative"];
  const acq={}; for(const k of adKeys){const v=params.get(k);if(v)acq[k]=v.slice(0,300);}

  const selectorFor=(el)=>{
    if(!el||el===document||el===window)return "";
    if(el.dataset?.trackCta)return '[data-track-cta="'+CSS.escape(el.dataset.trackCta)+'"]';
    if(el.id)return "#"+CSS.escape(el.id);
    const parts=[]; let cur=el;
    for(let d=0;cur&&cur.nodeType===1&&d<4;d++,cur=cur.parentElement){
      let p=cur.tagName.toLowerCase();
      if(cur.classList?.length)p+="."+[...cur.classList].slice(0,2).map(CSS.escape).join(".");
      parts.unshift(p);
    }
    return parts.join(" > ").slice(0,500);
  };
  const labelFor=(el)=>String(el?.dataset?.trackCta||el?.getAttribute?.("aria-label")||el?.getAttribute?.("title")||"").slice(0,120);
  const referrer=(()=>{try{if(!document.referrer)return "";const u=new URL(document.referrer);return u.origin+u.pathname}catch{return ""}})();

  function tick(){const now=Date.now();if(visible)activeMs+=Math.max(0,now-lastTick);lastTick=now;}
  function send(type,extra={}){
    const body=JSON.stringify({
      event_id:uuid(),event_type:type,ts:new Date().toISOString(),site,lp,
      session_id:sessionId,page_id:pageId,path:location.pathname,title:document.title.slice(0,200),
      referrer,viewport_w:innerWidth,viewport_h:innerHeight,doc_h:document.documentElement.scrollHeight,
      acquisition:acq,...extra
    });
    try{
      if(document.visibilityState==="hidden"&&navigator.sendBeacon){
        if(navigator.sendBeacon(endpoint,new Blob([body],{type:"application/json"})))return;
      }
    }catch{}
    fetch(endpoint,{method:"POST",mode:"cors",credentials:"omit",keepalive:true,headers:{"content-type":"application/json"},body}).catch(()=>{});
  }

  send("page_view",{screen_w:screen.width,screen_h:screen.height,language:navigator.language||""});

  addEventListener("scroll",()=>{
    requestAnimationFrame(()=>{
      const max=Math.max(1,document.documentElement.scrollHeight-innerHeight);
      const pct=Math.min(100,Math.round(scrollY/max*100));
      for(const mark of [25,50,75,90,100])if(pct>=mark&&!sentScroll.has(mark)){sentScroll.add(mark);send("scroll_depth",{depth:mark});}
    });
  },{passive:true});

  if("IntersectionObserver" in window){
    const io=new IntersectionObserver(entries=>{
      for(const e of entries){
        if(!e.isIntersecting||e.intersectionRatio<0.4)continue;
        const key=e.target.dataset.lpSection||e.target.id||selectorFor(e.target);
        if(!key||sentSections.has(key))continue;
        sentSections.add(key);send("section_view",{section:key.slice(0,160),selector:selectorFor(e.target)});
      }
    },{threshold:[0.4]});
    document.querySelectorAll("[data-lp-section],section[id]").forEach(el=>io.observe(el));
  }

  document.addEventListener("click",e=>{
    const el=e.target?.closest?.("a,button,[role='button'],[data-track-cta]")||e.target;
    const selector=selectorFor(el),label=labelFor(el);
    const xNorm=innerWidth?e.clientX/innerWidth:0;
    const yNorm=document.documentElement.scrollHeight?(scrollY+e.clientY)/document.documentElement.scrollHeight:0;
    let hrefHost="",hrefPath="";
    const a=el?.closest?.("a[href]");
    if(a){try{const u=new URL(a.href,location.href);hrefHost=u.hostname;hrefPath=u.pathname}catch{}}
    send("click",{selector,label,x_norm:+xNorm.toFixed(4),y_norm:+yNorm.toFixed(4),href_host:hrefHost,href_path:hrefPath});
    if(el?.closest?.("[data-track-cta]"))send("cta_click",{selector,label,href_host:hrefHost,href_path:hrefPath});

    const now=Date.now();trail.push({t:now,x:e.clientX,y:e.clientY,selector,label});
    while(trail.length&&now-trail[0].t>2000)trail.shift();
    const nearby=trail.filter(c=>Math.hypot(c.x-e.clientX,c.y-e.clientY)<=50);
    if(nearby.length>=3){send("rage_click",{selector,label});trail.length=0;}
    if(!el?.closest?.("a,button,input,select,textarea,[role='button'],[onclick],[data-track-cta]"))send("dead_click",{selector,label});
  },true);

  document.addEventListener("visibilitychange",()=>{tick();visible=!document.hidden;if(!visible)send("heartbeat",{active_ms:activeMs});});
  setInterval(()=>{tick();if(visible)send("heartbeat",{active_ms:activeMs});},15000);
  addEventListener("error",e=>send("js_error",{error_message:String(e.message||"error").slice(0,300),error_file:String(e.filename||"").split("?")[0].slice(0,300),error_line:e.lineno||0}));
  addEventListener("pagehide",()=>{tick();send("session_end",{active_ms:activeMs,elapsed_ms:Date.now()-start});});
})();