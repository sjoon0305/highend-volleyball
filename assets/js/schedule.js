/* 하이앤드 공개 수업 일정 달력 (Firebase 읽기 전용). 기존 index.html에서 그대로 옮김 */
(function(){
if(!document.getElementById("calDays"))return;
// ── FIREBASE (READ ONLY) ──────────────────────────────
const firebaseConfig={apiKey:"AIzaSyBLP7b8C94e1g6eMlsEwntOAmGcVTm7gHg",authDomain:"highend-volleyball-60f04.firebaseapp.com",databaseURL:"https://highend-volleyball-60f04-default-rtdb.firebaseio.com",projectId:"highend-volleyball-60f04",storageBucket:"highend-volleyball-60f04.firebasestorage.app",messagingSenderId:"815322795093",appId:"1:815322795093:web:4339fb5d71f1a4406b98dc"};
firebase.initializeApp(firebaseConfig);
const db=firebase.database();

let pubSessions={}, pubReservations={};
let calY=new Date().getFullYear(), calM=new Date().getMonth();
let selDate=null, _nearestDone=false;

function todayStr(){const t=new Date();return`${t.getFullYear()}-${String(t.getMonth()+1).padStart(2,'0')}-${String(t.getDate()).padStart(2,'0')}`;}
function calcEnd(t){if(!t)return'';const[h,m]=t.split(':').map(Number);const e=new Date(2000,0,1,h,m+80);return`${String(e.getHours()).padStart(2,'0')}:${String(e.getMinutes()).padStart(2,'0')}`;}

function autoSelectNearest(){
  if(_nearestDone||!Object.keys(pubSessions).length)return;
  const td=todayStr();
  const future=Object.values(pubSessions)
    .filter(s=>s.date>=td&&s.status!=='cancelled')
    .sort((a,b)=>a.date.localeCompare(b.date)||a.time.localeCompare(b.time));
  if(!future.length)return;
  _nearestDone=true;
  const d=future[0].date;
  const[y,m]=d.split('-').map(Number);
  calY=y;calM=m-1;selDate=d;
  renderCal();renderPanel(d);
}

db.ref('sessions').on('value',s=>{pubSessions=s.val()||{};renderCal();autoSelectNearest();});
db.ref('reservations').on('value',s=>{pubReservations=s.val()||{};renderCal();if(selDate)renderPanel(selDate);});

function renderCal(){
  const y=calY,m=calM;
  const firstDay=new Date(y,m,1).getDay();
  const daysInMonth=new Date(y,m+1,0).getDate();
  const today=todayStr();
  const ms=`${y}-${String(m+1).padStart(2,'0')}`;

  const $title=document.getElementById('calTitle');
  const $days=document.getElementById('calDays');
  if(!$title||!$days) return;
  $title.textContent=`${y}년 ${m+1}월`;

  // sessions in this month, keyed by date
  const daySessions={};
  Object.values(pubSessions).forEach(s=>{
    if(s.date&&s.date.startsWith(ms)){
      if(!daySessions[s.date]) daySessions[s.date]=[];
      daySessions[s.date].push(s);
    }
  });

  let html='';
  for(let i=0;i<firstDay;i++) html+=`<div class="cal-day empty"></div>`;
  for(let d=1;d<=daysInMonth;d++){
    const ds=`${ms}-${String(d).padStart(2,'0')}`;
    const dow=new Date(ds+'T12:00:00').getDay();
    const isSat=dow===6, isSun=dow===0;
    const isToday=ds===today;
    const isPast=ds<today;
    const sessions=daySessions[ds]||[];
    const activeSess=sessions.filter(s=>s.status!=='cancelled');
    const cancelledSess=sessions.filter(s=>s.status==='cancelled');
    const hasSess=activeSess.length>0;
    const hasCancelled=cancelledSess.length>0 && !hasSess;
    const isSelected=selDate===ds;

    // check if any sessions almost full
    let dotClass='';
    if(hasSess){
      const anyAlmostFull=activeSess.some(s=>{
        const rc=Object.values(pubReservations).filter(r=>r.sessionId===s.id&&r.status!=='cancelled').length;
        const cap=s.maxCapacity||16;
        return rc/cap>=0.7;
      });
      dotClass=anyAlmostFull?'full-dot':'';
    } else if(hasCancelled) dotClass='cancelled-dot';

    html+=`<div class="cal-day${isSat?' saturday':''}${isSun?' sunday':''}${isToday?' today':''}${isPast?' past':''}${hasSess||hasCancelled?' has-sess':''}${isSelected?' selected':''} ${dotClass}" data-date="${ds}">
      <span class="day-num">${d}</span>
      ${(hasSess||hasCancelled)?'<div class="cal-sess-dot"></div>':''}
    </div>`;
  }
  $days.innerHTML=html;

  // attach events
  $days.querySelectorAll('.cal-day[data-date]').forEach(el=>{
    el.addEventListener('click',()=>{
      selDate=el.dataset.date;
      renderCal();
      renderPanel(el.dataset.date);
    });
  });

  if(selDate) renderPanel(selDate);
}

function renderPanel(date){
  const $panel=document.getElementById('schedPanel');
  if(!$panel) return;
  const sessions=Object.values(pubSessions)
    .filter(s=>s.date===date)
    .sort((a,b)=>a.time.localeCompare(b.time));

  if(!sessions.length){
    $panel.innerHTML=`<div class="no-sess-msg"><div class="icon"><svg class="ln" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17"/><path d="M8 3v4M16 3v4"/><circle cx="8.5" cy="14.5" r="1.2" fill="currentColor"/><circle cx="12" cy="14.5" r="1.2" fill="currentColor"/><circle cx="15.5" cy="14.5" r="1.2" fill="currentColor"/></svg></div><div>${new Date(date+'T12:00:00').toLocaleDateString('ko-KR',{month:'long',day:'numeric',weekday:'long'})}<br>등록된 수업이 없습니다</div></div>`;
    return;
  }

  const dt=new Date(date+'T12:00:00');
  const dtStr=dt.toLocaleDateString('ko-KR',{year:'numeric',month:'long',day:'numeric',weekday:'long'});
  const today=todayStr();
  const isPast=date<today;

  let html=`<div class="panel-date-title">${dtStr}</div>`;
  sessions.forEach(s=>{
    const isCancelled=s.status==='cancelled';
    const rc=Object.values(pubReservations).filter(r=>r.sessionId===s.id&&r.status!=='cancelled').length;
    const cap=s.maxCapacity||16;
    const isFull=rc>=cap;
    const isAlmost=!isFull&&rc>5;

    html+=`<div class="sess-slot${isCancelled?' cancelled-slot':''}">
      <div>
        <div class="slot-time-big">${s.time}</div>
        <div style="font-size:11px;color:var(--muted);">~${calcEnd(s.time)}</div>
      </div>
      <div class="slot-info">
        <div class="slot-title">${s.title||'정규반'} ${isCancelled?'<span style="color:var(--red);font-size:12px;">(취소됨)</span>':''}</div>
        <div class="slot-meta">${s.sessionType||'정규반'} · 최대 ${cap}명</div>
      </div>
      ${!isCancelled?`
      <div class="slot-avail" style="text-align:right;flex-shrink:0;">
        ${isFull
          ?'<span style="background:var(--redL);color:var(--red);font-size:12px;font-weight:700;padding:5px 12px;border-radius:20px;">마감</span>'
          :isAlmost
          ?'<span style="background:var(--orangeL);color:var(--orange);font-size:12px;font-weight:700;padding:5px 12px;border-radius:20px;">거의 마감</span>'
          :'<span style="background:var(--blue);color:#fff;font-size:12px;font-weight:700;padding:5px 12px;border-radius:20px;">여유</span>'}
      </div>`:`<div style="font-size:12px;color:var(--muted);">취소</div>`}
    </div>`;
  });

  if(!isPast){
    html+=`<div class="sched-login-note"><svg class="ln lock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="10.5" width="14" height="10.5" rx="2.5"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/><circle cx="12" cy="15" r="1.4" fill="currentColor"/><path d="M12 16.2v2"/></svg> 예약을 하려면 <a href="${window.HE_ROOT||''}dashboard.html" style="font-weight:700;color:var(--blue);text-decoration:underline;">회원 로그인</a>이 필요합니다</div>`;
  }
  $panel.innerHTML=html;
}

function changeMonth(d){calM+=d;if(calM<0){calM=11;calY--;}if(calM>11){calM=0;calY++;}selDate=null;renderCal();}
document.getElementById('calPrev').onclick=()=>changeMonth(-1);
document.getElementById('calNext').onclick=()=>changeMonth(1);

})();
