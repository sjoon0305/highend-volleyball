/* ☰ 전체 메뉴 (로켓츠식 왼쪽 메뉴): 대메뉴를 누르면 그 페이지로 이동 */
(function(){
  var d=document.getElementById('drawer');
  if(!d)return;
  var opener=null;
  var setOpen=function(open){
    if(open){
      d.hidden=false;
      requestAnimationFrame(function(){d.classList.add('show');});
      document.body.style.overflow='hidden';
      var x=d.querySelector('.drw-x'); if(x)x.focus();
    }else{
      d.classList.remove('show');
      document.body.style.overflow='';
      setTimeout(function(){d.hidden=true;},280);
      if(opener)opener.focus();
    }
    document.querySelectorAll('[data-drawer-open]').forEach(function(b){b.setAttribute('aria-expanded',open?'true':'false');});
  };
  document.querySelectorAll('[data-drawer-open]').forEach(function(b){
    b.addEventListener('click',function(){opener=b;setOpen(d.hidden);});
  });
  d.addEventListener('click',function(e){
    if(e.target.closest('[data-drawer-close]'))setOpen(false);
  });
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!d.hidden)setOpen(false);});
})();
