/* 하이앤드 공통 동작: 나타나기 효과, "문의" 버튼 (☰ 메뉴는 drawer.js) */
(function(){
  // 나타나기 효과: 화면에 조금이라도 들어오면 바로 표시, 3초 뒤엔 남은 것도 모두 표시
  var els=document.querySelectorAll('.reveal');
  var showAll=function(){els.forEach(function(el){el.classList.add('visible');});};
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target);}});},{threshold:0});
    els.forEach(function(el){io.observe(el);});
    setTimeout(showAll,3000);
  }else{showAll();}
  // "문의" 버튼: 누르면 카카오톡·전화·인스타·네이버가 펼쳐짐, 지도·푸터가 보이면 숨김
  var fab=document.getElementById('fab'), fb=document.getElementById('fabBtn');
  if(fab&&fb){
    fb.addEventListener('click',function(){var o=fab.classList.toggle('open');fb.setAttribute('aria-expanded',o?'true':'false');});
    var targets=[document.getElementById('map'),document.querySelector('.ft')].filter(Boolean);
    if(targets.length&&'IntersectionObserver' in window){
      var seen=new Set();
      var io2=new IntersectionObserver(function(es){
        es.forEach(function(e){e.isIntersecting?seen.add(e.target):seen.delete(e.target);});
        fab.classList.toggle('away',seen.size>0);
      },{threshold:0.15});
      targets.forEach(function(t){io2.observe(t);});
    }
  }
})();
