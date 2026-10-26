/* 하이앤드 공통 동작: 휴대폰 메뉴, 나타나기 효과, 떠 있는 버튼, 예전 주소(#) 안내 */
(function(){
  var btn=document.getElementById('menuBtn'), panel=document.getElementById('mnav');
  if(btn&&panel){
    var openIcon=btn.innerHTML, closeIcon=btn.getAttribute('data-close');
    btn.addEventListener('click',function(){
      var open=panel.classList.toggle('open');
      btn.innerHTML=open?closeIcon:openIcon;
      btn.setAttribute('aria-expanded',open?'true':'false');
      document.body.style.overflow=open?'hidden':'';
    });
    panel.addEventListener('click',function(e){
      if(e.target.tagName==='A'){panel.classList.remove('open');btn.innerHTML=openIcon;btn.setAttribute('aria-expanded','false');document.body.style.overflow='';}
    });
  }
  // 나타나기 효과
  var els=document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target);}});},{threshold:0.08,rootMargin:'0px 0px -20px 0px'});
    els.forEach(function(el){io.observe(el);});
  }else{els.forEach(function(el){el.classList.add('visible');});}
  // 떠 있는 버튼: 지도·푸터가 보이면 숨김
  var bar=document.querySelector('.float-bar');
  var targets=[document.getElementById('map'),document.querySelector('.ft')].filter(Boolean);
  if(bar&&targets.length&&'IntersectionObserver' in window){
    var seen=new Set();
    var io2=new IntersectionObserver(function(es){
      es.forEach(function(e){e.isIntersecting?seen.add(e.target):seen.delete(e.target);});
      bar.classList.toggle('away',seen.size>0);
    },{threshold:0.15});
    targets.forEach(function(t){io2.observe(t);});
  }
  // 첫 화면 배경 영상: 페이지가 다 열린 뒤 재생 (움직임 줄이기·데이터 절약 설정이면 사진만)
  var hv=document.getElementById('heroVideo');
  if(hv){
    var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
    var save=navigator.connection&&navigator.connection.saveData;
    if(!reduce&&!save){
      var start=function(){hv.src=hv.getAttribute('data-src');var p=hv.play();if(p&&p.catch)p.catch(function(){});};
      if(document.readyState==='complete')start();else window.addEventListener('load',start);
    }
  }
  // 예전 한 페이지 주소(#schedule 등)로 들어오면 새 페이지로 안내
  var old={'#schedule':'class/#schedule','#coach':'about/#career','#curriculum':'method/#level','#gallery':'story/#gallery','#cta':'contact/#ask'};
  if(document.body.getAttribute('data-page')==='home'&&old[location.hash]){location.replace(old[location.hash]);}
})();
