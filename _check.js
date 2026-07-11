
/* ====== EDIT THIS LIST: 5-10 creators for this niche. Priority: portfolio > ig > youtube ====== */
const CREATORS = [{"name": "Andrea B", "portfolio": "https://andreabarrigadiezugc.my.canva.site/ugcbyandreab", "ig": "ugcbyandreab", "youtube": ""}, {"name": "Stacy Parks", "portfolio": "https://stacyparksugc.my.canva.site", "ig": "stacyparks.ugc", "youtube": ""}];
/* ============================================================================================= */
function ytId(u){const m=(u||'').match(/(?:v=|youtu\.be\/|embed\/)([\w-]{11})/);return m?m[1]:null}
function card(c){
  const yt=ytId(c.youtube); const has=(c.portfolio||c.ig||c.youtube);
  const thumb = yt ? `<img src="https://i.ytimg.com/vi/${yt}/hqdefault.jpg">` : `<span class="ph">${has?'&#9654; view their work':'+ add creator'}</span>`;
  const badge = c.portfolio ? `<span class="badge">portfolio</span>` : '';
  const el=document.createElement('div'); el.className='card';
  // priority-ordered links
  let lks='';
  if(c.portfolio) lks+=`<a class="lk p" href="${c.portfolio}" target="_blank">Portfolio</a>`;
  if(c.ig) lks+=`<a class="lk" href="https://instagram.com/${c.ig}" target="_blank">@${c.ig}</a>`;
  if(c.youtube) lks+=`<a class="lk" href="#" onclick="openLb('${c.youtube}');return false">Podcast</a>`;
  const hint=(!c.portfolio && c.ig)?`<div class="hint">portfolio in bio</div>`:'';
  el.innerHTML=`<div class="tile">${thumb}${badge}</div><div class="meta"><div class="cname">${c.name||''}</div>${hint}<div class="links">${lks}</div></div>`;
  // tile click = highest-priority link
  const tile=el.querySelector('.tile');
  if(c.portfolio) tile.onclick=()=>window.open(c.portfolio,'_blank');
  else if(c.youtube) tile.onclick=()=>openLb(c.youtube);
  else if(c.ig) tile.onclick=()=>window.open('https://instagram.com/'+c.ig,'_blank');
  return el;
}
function openLb(url){const yt=ytId(url); if(!yt){window.open(url,'_blank');return}
  document.getElementById('lbbox').innerHTML=`<iframe src="https://www.youtube.com/embed/${yt}?autoplay=1&playsinline=1" allow="autoplay" allowfullscreen></iframe>`;
  document.getElementById('lb').classList.add('open');}
function closeLb(){document.getElementById('lb').classList.remove('open');document.getElementById('lbbox').innerHTML=''}
document.getElementById('lb').onclick=e=>{if(e.target.id==='lb')closeLb()};
const g=document.getElementById('grid');
const real=CREATORS.filter(c=>c.name && c.name.indexOf('[')<0 && (c.ig||c.portfolio||c.youtube));
if(real.length){ real.forEach(c=>g.appendChild(card(c))); }
else { g.style.display='block'; g.innerHTML='<div style="text-align:center;color:#6b7280;padding:30px 10px">New creators in this niche are added every week. Watch the free class to meet them live.</div>'; }
