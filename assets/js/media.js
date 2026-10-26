/* 사진 확대 보기 · 코치 사진 넘기기 · 수업 영상 슬라이더. 기존 index.html에서 옮김 */
// ── LIGHTBOX ──────────────────────────────────────────
function openLb(src){document.getElementById('lbImg').src=src;document.getElementById('lightbox').classList.add('open');document.body.style.overflow='hidden';}
function closeLb(){var lb=document.getElementById('lightbox');if(!lb)return;lb.classList.remove('open');document.body.style.overflow='';}
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeLb();});

if(document.getElementById("ccarTrack")){
// ── COACH CAROUSEL ────────────────────────────────────
(function(){
  const track=document.getElementById('ccarTrack');
  const dotEls=document.querySelectorAll('.ccar-dot');
  if(!track)return;
  let cur=0,total=dotEls.length,startX=0,isDrag=false,moved=false;
  function goTo(i){
    cur=(i+total)%total;
    track.style.transform=`translateX(-${cur*100}%)`;
    dotEls.forEach((d,j)=>d.classList.toggle('active',j===cur));
  }
  dotEls.forEach((d,i)=>d.addEventListener('click',()=>{stopAuto();goTo(i);setTimeout(startAuto,3000);}));
  const car=track.parentElement;
  car.addEventListener('pointerdown',e=>{startX=e.clientX;isDrag=true;moved=false;track.classList.add('dragging');stopAuto();});
  car.addEventListener('pointermove',e=>{if(isDrag&&Math.abs(e.clientX-startX)>8)moved=true;});
  car.addEventListener('pointerup',e=>{
    track.classList.remove('dragging');
    if(!isDrag)return;isDrag=false;
    if(moved&&Math.abs(e.clientX-startX)>40)goTo(cur+(startX-e.clientX>0?1:-1));
    setTimeout(startAuto,3000);
  });
  car.addEventListener('pointercancel',()=>{isDrag=false;track.classList.remove('dragging');setTimeout(startAuto,3000);});
  // Auto-advance every 4 seconds
  let autoTimer;
  function startAuto(){autoTimer=setInterval(()=>goTo(cur+1),4000);}
  function stopAuto(){clearInterval(autoTimer);}
  startAuto();
})();

}
if(document.getElementById("reelsTrack")){
// ── REELS SLIDER ─────────────────────────────────────
(function(){
  const viewport=document.getElementById('reelsViewport');
  const track=document.getElementById('reelsTrack');
  const dots=document.querySelectorAll('.s-dot');
  if(!track||!viewport)return;
  const slides=track.querySelectorAll('.reel-slide');
  const videos=track.querySelectorAll('video');
  let cur=0,total=slides.length,startX=0,isDrag=false,moved=false;
  let sectionVisible=false;

  // Ensure all videos loop
  videos.forEach(v=>{v.loop=true;});

  function setOverlay(idx,playing){
    const el=document.getElementById('rpl'+idx);
    if(el)el.classList.toggle('hidden',playing);
  }

  function playVideo(idx){
    const v=videos[idx];
    if(!v)return;
    v.play().then(()=>setOverlay(idx,true)).catch(()=>setOverlay(idx,false));
  }

  function pauseVideo(idx){
    const v=videos[idx];
    if(v&&!v.paused){v.pause();setOverlay(idx,false);}
  }

  function goTo(i){
    const prev=cur;
    cur=Math.max(0,Math.min(total-1,i));
    track.style.transform=`translateX(-${cur*100}%)`;
    dots.forEach((d,j)=>d.classList.toggle('active',j===cur));
    if(prev!==cur)pauseVideo(prev);
    if(sectionVisible)playVideo(cur);
  }

  // Click to toggle play/pause
  slides.forEach((slide,i)=>{
    if(slide.classList.contains('reel-slide-cta'))return;
    const vid=videos[i];
    if(!vid)return;
    slide.addEventListener('click',e=>{
      if(moved)return;
      if(vid.paused){playVideo(i);}
      else{vid.pause();setOverlay(i,false);}
    });
  });

  dots.forEach((d,i)=>d.addEventListener('click',()=>goTo(i)));
  const prevBtn=document.getElementById('reelsPrev');
  const nextBtn=document.getElementById('reelsNext');
  if(prevBtn)prevBtn.addEventListener('click',()=>goTo(cur-1));
  if(nextBtn)nextBtn.addEventListener('click',()=>goTo(cur+1));

  viewport.addEventListener('pointerdown',e=>{startX=e.clientX;isDrag=true;moved=false;viewport.classList.add('dragging');});
  viewport.addEventListener('pointermove',e=>{if(isDrag&&Math.abs(e.clientX-startX)>8)moved=true;});
  viewport.addEventListener('pointerup',e=>{
    viewport.classList.remove('dragging');
    if(!isDrag)return;isDrag=false;
    if(moved&&Math.abs(e.clientX-startX)>50)goTo(cur+(startX-e.clientX>0?1:-1));
  });
  viewport.addEventListener('pointercancel',()=>{isDrag=false;viewport.classList.remove('dragging');});

  // IntersectionObserver: autoplay when section scrolls into view, pause when out
  const section=track.closest('section')||track.closest('.reels-section')||viewport.parentElement;
  const obs=new IntersectionObserver((entries)=>{
    entries.forEach(entry=>{
      sectionVisible=entry.isIntersecting;
      if(sectionVisible){
        playVideo(cur);
      } else {
        videos.forEach((v,i)=>pauseVideo(i));
      }
    });
  },{threshold:0.3});
  obs.observe(section);
})();

}
