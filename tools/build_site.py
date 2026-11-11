#!/usr/bin/env python3
"""하이앤드 홈페이지 생성기 (v3: 로켓츠 방식 3단계 메뉴 + 하위 메뉴마다 서브페이지).

설계서: 구글 드라이브 2026-10-26_홈페이지시안/홈페이지_메뉴구조_A안_로켓츠벤치마킹.md
문구 원본: 같은 폴더 v2_여러페이지 + 지금 사이트 문구 (검수 반영)
사실·표기 규칙: highend-ai-office/CLAUDE.md
실행: 저장소 맨 위에서 `python3 tools/build_site.py`
결과: index.html(기존 홈 그대로 + 메뉴만 3단계), 서브페이지들, 404.html, robots.txt, sitemap.xml, llms.txt
"""
import hashlib
import json
import os
import re
from html import escape

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── 사이트 기본 정보 (도메인을 바꾸면 BASE 한 줄만 바꾸고 다시 실행) ──
BASE = 'https://sjoon0305.github.io/highend-volleyball/'
UPDATED = '2026-10-26'
NAME = '하이앤드 발리볼 아카데미'
NAME_EN = 'HIGH END Volleyball Academy'
ADDR = '상암 인근 · 현천동 180-1'
PHONE = '010-4463-1177'
PHONE_INTL = '+82-10-4463-1177'
EMAIL = 'highendv0lly@gmail.com'
KAKAO = 'http://pf.kakao.com/_pCEzX'
KAKAO_CHAT = 'https://pf.kakao.com/_pCEzX/chat'
INSTA = 'https://www.instagram.com/highend_volleyball'
YOUTUBE = 'https://www.youtube.com/@Highendvolleyball'
BLOG = 'https://m.blog.naver.com/highendv0lly'
NAVER_PLACE = 'https://naver.me/G8fjuvBh'
NAVER_REVIEW = 'https://m.place.naver.com/place/2022442484/review/visitor'
NAVER_MAP = 'https://map.naver.com/p/entry/place/2022442484'
NAVER_BOOK = 'https://m.place.naver.com/place/2022442484/ticket?entry=pll&bk_query=%ED%95%98%EC%9D%B4%EC%95%A4%EB%93%9C%20%EB%B0%9C%EB%A6%AC%EB%B3%BC'
GOOGLE_MAP = 'https://www.google.com/maps?cid=1837675666172275385'
GOOGLE_EMBED = 'https://maps.google.com/maps?cid=1837675666172275385&amp;z=16&amp;hl=ko&amp;output=embed'
# 네이버 지도 (2026-11-11 대표: 구글 지도 대신 네이버 지도 하나만). 이미지는 네이버 정적 지도에서 받아 assets/img/map-naver.webp로 보관, 누르면 네이버 지도 열림
# 지도 아래 버튼: 구글 지도 · 카카오맵 (2026-11-11 대표: 네이버 지도 열기 버튼 삭제, 지도 자체가 네이버)
KAKAO_MAP = 'https://map.kakao.com/link/map/하이앤드 발리볼 아카데미 상암점,37.5958553,126.8672514'
KAKAO_PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#191919" d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>'
def naver_map_img(root=''):
    return ('<a class="loc-map naver-map" href="https://map.naver.com/p/entry/place/2022442484" target="_blank" rel="noopener" '
                 'aria-label="네이버 지도에서 하이앤드 발리볼 아카데미 상암점 열기">'
                 '<img src="' + root + 'assets/img/map-naver.webp" alt="하이앤드 발리볼 아카데미 상암점 위치 (네이버 지도)" width="1400" height="630" loading="lazy">'
                 '<span class="nm-chip">하이앤드 발리볼 아카데미 상암점</span><span class="nm-open">네이버 지도에서 크게 보기 ↗</span></a>')
CAREER = '국가대표 7년 · 프로(V리그) 10년, 선수 17년'

SN = json.load(open(os.path.join(ROOT_DIR, 'tools', 'snippets.json'), encoding='utf-8'))
MAP_BTNS = (f'<div class="loc-btns"><a class="loc-btn google" href="{GOOGLE_MAP}" target="_blank" rel="noopener">{SN["google"]}Google 지도</a>'
            f'<a class="loc-btn kakao" href="{KAKAO_MAP}" target="_blank" rel="noopener">{KAKAO_PIN}카카오맵</a></div>')
USER_ICON = ('<svg class="ln" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
             'stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>')
CHAT_ICON = ('<svg class="ln" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
             'stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg>')

# ════════════════════════ 페이지 목록 ════════════════════════
# path: 주소, title/desc: 검색 제목·설명문, crumb: 경로 표시 이름, banner: (영문 작은 제목, H1, 한 줄 설명),
# bg: 배너 사진(없으면 남색), hidden: 메뉴·sitemap에서 숨김(검색 제외), cta: 하단 띠 제목
P = lambda **k: k  # noqa: E731
PAGES = {
    'home': P(path='', crumb='HOME', title='상암·고양 프리미엄 배구 아카데미 하이앤드 | 국가대표·프로 출신 코치진의 배구 학원·배구교실',
              desc='국가대표·프로 선수의 훈련 방식을 시스템으로 만든 프리미엄 배구 아카데미 하이앤드. 상암 인근 · 현천동 180-1, 국가대표·프로 출신 코치진이 초등학생부터 성인까지 가르칩니다. 원데이 클래스는 네이버 예약, 문의 010-4463-1177'),
    # ABOUT US
    'about': P(path='about/', crumb='ABOUT US', title='하이앤드 소개 | 국가대표·프로 출신 코치진의 프리미엄 배구아카데미 · 상암배구학원',
               desc='국가대표·프로 선수의 훈련 방식을 시스템으로 만든 프리미엄 배구아카데미. 상암 인근에서 초등배구·성인배구·국제학교배구·배구개인레슨을 지도합니다.',
               banner=('ABOUT US', '하이앤드 소개', '가장 완벽한 기본, 그것이 우리가 말하는 하이앤드입니다'),
               cta='국가대표·프로 출신 코치진에게 배워 보세요'),
    'coaches': P(path='about/coaches/', crumb='코칭 스태프',
                 title='코칭 스태프 | 국가대표·프로 출신 하이앤드 코치진 · 김재휘 헤드코치 · 황준태 코치',
                 desc='프리미엄 배구 아카데미 하이앤드 코칭 스태프. 김재휘 헤드코치: 국가대표 2016~2022, 2018 아시안게임 은메달, V리그 우승 4회, FIVB 코치 레벨1. 황준태 코치: 리베로, 서울 우리카드 배구단, 대통령배 배구대회 리베로상.',
                 banner=('COACHING STAFF', '코칭 스태프', '국가대표·프로 출신 하이앤드 코치진이 가르칩니다'), cta='국가대표·프로 출신 코치진에게 배워 보세요'),
    'facility': P(path='about/facility/', crumb='시설', title='200평 풀코트 배구 체육관 | 하이앤드 시설 안내',
                  desc='프리미엄 배구 아카데미 하이앤드는 200평 풀코트에서 수업합니다. 상암 인근 · 현천동 180-1, 건물 앞 주차 가능. 프리미엄 배구 학원 · 배구교실 시설 안내',
                  banner=('FACILITY', '시설', '200평 풀코트에서 배웁니다'), bg='class-1'),
    # METHOD
    'method': P(path='method/', crumb='METHOD', title='알고 하면 쉬운 배구 | 하이앤드 코칭 시스템 · 프리미엄 배구 아카데미',
                desc='이유를 알고 하는 반복이 몸을 바꿉니다. 국가대표·프로 선수의 훈련 방식을 시스템으로 만든 하이앤드 코칭 시스템: 몸 방향, 플랫폼, Why ? → How ? → Play !, Ask → Point → Watch, 운동일지 Today & Next Ball.',
                banner=('HIGH END COACHING SYSTEM', '알고 하면 쉬운 배구', '이유를 알고 하는 반복이 몸을 바꿉니다. 국가대표·프로 선수의 훈련 방식을 시스템으로 만든 하이앤드 코칭 시스템입니다.'),
                cta='이유를 알면, 배구가 쉬워집니다'),
    'maps': P(path='method/maps/', crumb='MAPS 워밍업', title='MAPS 워밍업 | 안전하게 오래 하는 배구 준비 운동 · 하이앤드',
              desc='하이앤드 MAPS 워밍업: 가동성(Mobility) · 활성화(Activation) · 순발력(Plyometrics) · 안정성(Stability). 발목 · 무릎 · 어깨를 준비하는 순서와 나이별 실제 동작.',
              banner=('WARM-UP', 'MAPS 워밍업', '안전하게, 오래 배구하는 몸을 만드는 하이앤드의 준비 운동'), cta='이유를 알면, 배구가 쉬워집니다'),
    'correction': P(path='method/correction/', crumb='정밀 교정', title='배구 자세 교정 · 리시브 · 치킨윙 교정 | 하이앤드 정밀 교정',
                    desc='하이앤드 정밀 교정: 리시브는 팔보다 먼저 엉덩이와 몸 방향, 스파이크는 치킨윙을 바로잡아 힘을 효율적으로 싣는 스윙. 한 사람씩 묻고, 짚고, 영상으로 확인합니다.',
                    banner=('PRECISION', '생체역학 기반 정밀 교정', '"왜 공이 저쪽으로 갔을까?"의 답은 몸에 있습니다.'), cta='이유를 알면, 배구가 쉬워집니다'),
    'flow': P(path='method/flow/', crumb='수업 80분 흐름', title='80분 정규수업 흐름 | 하이앤드 배구 수업',
              desc='하이앤드 80분 정규수업은 매번 MAPS 워밍업 → 왜: 원리 이해 → 어떻게: 교정 반복 → 해보기: 게임 순서로 진행합니다. 기다리는 시간은 줄이고, 공을 만지는 시간은 늘립니다.',
              banner=('80 MINUTES', '80분 정규수업, 이렇게 진행됩니다', '기다리는 시간은 줄이고, 공을 만지는 시간은 늘립니다.'), cta='이유를 알면, 배구가 쉬워집니다'),
    'level': P(path='method/level/', crumb='성장 레벨', title='하이앤드 성장 레벨 LV.1~4 | 배구 실력 단계 · 프리미엄 배구 아카데미',
               desc='하이앤드 성장 레벨 LV.1 입문 · LV.2 기본 · LV.3 심화 · LV.4 시합. 나이보다 지금 할 수 있는 동작을 기준으로 단계를 나누고, 단계마다 맞는 반을 안내합니다.',
               banner=('LEVEL', '4단계 성장 레벨', '지금 어디에 있는지, 다음에 무엇을 배우면 되는지 알 수 있습니다.'), cta='이유를 알면, 배구가 쉬워집니다'),
    # CLASS
    'class': P(path='class/', crumb='CLASS', title='클래스 안내 | 배구교실·배구레슨·배구개인레슨 · 하이앤드',
               desc='상암배구학원 하이앤드 클래스 안내. 배구교실·배구레슨 원데이 클래스(정규 수업 그대로 체험), 유소년반(초등학생)·초급반·중급반 80분 정규수업, 배구개인레슨, 국제학교배구. 상암 인근 · 현천동 180-1',
               banner=('CLASS', '클래스 전체 안내', '나에게 맞는 수업을 골라 보세요'), bg='class-4', cta='어떤 반이 맞을지 모르겠다면',
               cta_sub='나이와 배구 경력, 가능한 시간을 남겨 주시면 맞는 반을 추천해 드립니다.'),
    'oneday': P(path='class/oneday/', crumb='원데이 클래스', tab=False, title='배구 원데이 클래스 | 상암배구학원 하이앤드',
                desc='배구 배우는 곳을 찾는다면 배구원데이클래스로 시작하세요. 토요일 12:00 · 13:30 · 16:30 정규 수업에 그대로 함께하는 배구입문 체험 수업. 네이버 예약으로 신청, 정규 등록 시 원데이 비용 차감.',
                banner=('ONE DAY CLASS', '원데이 클래스', '처음이라면, 실제 수업 그대로 경험해 보세요'), bg='class-5'),
    'oneday-apply': P(path='class/oneday/apply/', crumb='원데이 신청', tab=False, title='원데이 클래스 신청 | 네이버 예약 · 하이앤드',
                      desc='하이앤드 배구 원데이 클래스 신청은 네이버 예약으로 받습니다. 토요일 12:00 · 13:30 · 16:30 정규 수업에 그대로 함께합니다. 준비물: 실내 운동화, 물, 편한 운동복. 수업 10분 전 도착.',
                      banner=('APPLY', '원데이 클래스 신청', '네이버 예약으로 간편하게 신청하세요')),
    'oneday-reviews': P(path='class/oneday/reviews/', crumb='원데이 후기', hidden=True, title='원데이 클래스 후기 | 하이앤드',
                        desc='하이앤드 원데이 클래스 후기', banner=('REVIEW', '원데이 클래스 후기', '네이버 방문자 리뷰에서 확인하세요')),
    'youth': P(path='class/regular/youth/', crumb='유소년반', title='유소년반 | 초등배구 · 어린이배구 · 유소년배구 (초등학생 대상)',
               desc='초등배구·어린이배구를 찾는 학부모님께. 하이앤드 유소년반은 초등학생 대상 80분 정규수업(토요일 12:00)으로, 국가대표·프로 출신 코치진이 바른 자세와 기본기를 처음부터 가르치는 유소년배구 교실입니다.',
               banner=('YOUTH', '유소년반', '초등학생, 처음부터 제대로'), bg='class-5'),
    'beginner': P(path='class/regular/beginner/', crumb='초급반', title='초급반 | 중학생·성인 배구입문 레슨',
                  desc='배구입문 레슨: 배구를 처음 배우는 중학생배구·성인배구 초급반. 패스·서브·리시브 기본기와 배구의 재미, 토요일 13:30 80분 정규수업. 국가대표·프로 출신 하이앤드 코치진이 가르칩니다.',
                  banner=('BEGINNER', '초급반', '중학생 이상, 배구를 처음 배우는 분'), bg='class-3'),
    'intermediate': P(path='class/regular/intermediate/', crumb='중급반', title='중급반 | 배구동호회 준비 · 성인배구레슨',
                      desc='배구 경력 6개월 이상 중학생·고등학생배구·성인배구 중급반. 배구동호회 활동을 준비하는 분께 볼 컨트롤 정밀화와 신체 정렬 코칭, 토요일 16:30 80분 정규수업.',
                      banner=('INTERMEDIATE', '중급반', '중학생 이상, 배구 경력 6개월 이상'), bg='class-4'),
    'regular-reviews': P(path='class/regular/reviews/', crumb='정규 후기', hidden=True, title='정규 클래스 후기 | 하이앤드',
                         desc='하이앤드 정규 클래스 후기', banner=('REVIEW', '정규 클래스 후기', '네이버 방문자 리뷰에서 확인하세요')),
    'competition': P(path='class/team/competition/', crumb='시합반', title='시합반 | U15·U18 유소년 배구클럽 · 엘리트배구',
                     desc='배구선수반을 찾는다면 하이앤드 시합반. U15(13세 이상·중학생)·U18(16세 이상·고등학생) 연령별 대표팀 선발과 대회를 목표로 한 집중 코칭. 엘리트유소년배구 준비, 초등 고학년·성인은 상담으로 맞춤 진행.',
                     banner=('COMPETITION CLASS', '시합반', 'U15 · U18 연령별 대표팀 선발과 대회를 목표로 한 집중 코칭')),
    'team': P(path='class/team-class/', crumb='팀클래스', title='팀클래스 | 동호회·학교·기업 단체 배구 레슨 · 하이앤드',
              desc='하이앤드 팀클래스: 배구동호회(6인제·9인제)·학교 배구부·방과후·기업 단체 배구레슨과 해외 학교 배구부 단기 캠프. 레벨 진단부터 팀 플레이까지 주 1회 정기 수업, 수강료는 카카오톡 상담. 국가대표·프로 출신 하이앤드 코치진.',
              banner=('TEAM CLASS', '팀클래스', '동호회 · 학교 · 기업 단체, 함께 배우는 배구')),
    'private': P(path='class/private/', crumb='개인레슨', title='배구개인레슨 | 1:1 포지션별 원포인트 레슨',
                 desc='배구개인레슨 60분 1회 25만 원(10회 등록 시 회당 20만 원). 포지션별 원포인트레슨으로 서브·리시브·스파이크타점교정·점프서브까지 내 몸에 맞게 교정합니다. 국가대표·프로 출신 하이앤드 코치진.',
                 banner=('PRIVATE LESSON', '1:1 개인레슨', '60분 동안 한 사람만 봅니다'), bg='class-6'),
    'elite': P(path='class/elite/', crumb='엘리트 선수 준비반', title='엘리트 선수 준비반 | 배구선수 되는법 · 배구부 입단 테스트 준비',
               desc='배구선수를 꿈꾸는 초등 4학년~고등학생을 위한 하이앤드 엘리트 선수 준비반. 레벨 진단부터 포지션별 기술, 배구부 입단 테스트 준비까지 국가대표·프로 출신 하이앤드 코치진이 함께합니다. 수업 시간과 수강료는 카카오톡 상담.',
               banner=('ELITE PLAYER PREP', '엘리트 선수 준비반', '국가대표·프로 출신 코치진이 함께 준비합니다'), bg='class-6'),
    'intl': P(path='class/international/', crumb='INTERNATIONAL', title='국제학교배구 · 외국인학교배구 | 바시티 트라이아웃 준비',
              desc='국제학교배구·외국인학교배구 레슨. 바시티(Varsity)·JV 대표팀 트라이아웃 준비, 방학 단기 집중 레슨, 익숙한 영어 배구 용어. Volleyball lesson Seoul for international school students. 국가대표·프로 출신 하이앤드 코치진.',
              banner=('INTERNATIONAL SCHOOL', 'INTERNATIONAL', '국제학교 · 외국인학교 · 해외 학생'), en=None),
    'guide': P(path='class/guide/', crumb='수강 · 결제 안내', title='배구 수업 시간표 · 수강 · 결제 안내 | 하이앤드',
               desc='하이앤드 토요일 정규수업 시간표(유소년반 12:00 · 초급반 13:30 · 중급반 16:30, 80분)와 수업 일정 달력, 정규 수강권 · 결제 안내. 회원 로그인 후 수업 예약',
               banner=('SCHEDULE & PAYMENT', '수강 · 결제 안내', '시간표와 수업 일정, 수강권 · 결제 방법')),
    'photos': P(path='class/photos/', crumb='클래스 사진', title='클래스 사진 HIGHEND PHOTOS | 배구 수업 사진 · 프리미엄 배구 아카데미 하이앤드',
                desc='하이앤드는 원데이 클래스부터 정규 수업까지 수업 사진을 촬영해 회원 가족과 나누고 있습니다. 유소년반 · 초급반 · 중급반 배구 수업 현장 사진과 영상, 지점별 클래스 사진 보기.',
                banner=('HIGHEND PHOTOS', '클래스 사진', '원데이 클래스부터 정규 수업까지, 하이앤드 수업 현장')),
    # STORY
    'story': P(path='story/', crumb='STORY', title='하이앤드 수업 이야기 | 배구 수업 기록',
               desc='하이앤드 발리볼 아카데미 토요일 수업 이야기. 네이버 블로그 수업기록, 방문자 리뷰, 인스타그램 · 유튜브. 상암 인근 프리미엄 배구 아카데미 하이앤드',
               banner=('CLASS STORY', '수업 이야기', '매주 토요일 수업에서 있었던 일을 기록합니다'), cta='다음 이야기의 주인공이 되어 보세요'),
    'hiand': P(path='story/hiandday/', crumb='Hi : And Day', title='Hi : And Day | 프로배구 선수와 함께하는 배구 클래스 · 하이앤드 배구아카데미',
               desc='국가대표·프로배구 선수에게 직접 배우는 하이앤드 발리볼 아카데미의 특별 배구 클래스. 유소년·초등학생 배구교실부터 중·고등 배구까지, 아이의 배구선수 꿈이 시작되는 하루.',
               banner=('HI : AND DAY', 'Hi : And Day', '〔 프로 선수들과 함께하는 특별한 배구 경험 〕')),
    'school': P(path='story/school-class/', crumb='국가대표가 찾아가는 배구교실',
                title='국가대표가 찾아가는 배구교실 | 유소년 배구 저변 확대 배구교실 · 하이앤드',
                desc='국가대표가 찾아가는 배구교실: 국가대표 출신 하이앤드 코치진이 학교 체육관을 찾아가 여는 유소년 배구 저변 확대 배구교실. 2026년 가재울중·등촌고·은평중에서 수업했습니다.',
                banner=('SCHOOL VOLLEYBALL CLASS', '국가대표가 찾아가는 배구교실', '국가대표 출신 코치진이 학교로 찾아가는 배구교실'),
                cta='우리 학교에도 찾아가는 배구교실을 신청해 보세요'),
    'note': P(path='story/note/', crumb='배구 노트', hidden=True, title='배구 노트 | 하이앤드',
              desc='하이앤드 배구 노트', banner=('VOLLEYBALL NOTE', '배구 노트', '하이앤드 코치진의 배구 이야기를 준비하고 있습니다')),
    # CONTACT
    'contact': P(path='contact/', crumb='CONTACT', title='오시는 길 | 하이앤드 발리볼 아카데미 상암점',
                 desc='하이앤드 발리볼 아카데미 오시는 길: 상암 인근 · 현천동 180-1, 건물 앞 주차 가능. 네이버 지도 · 구글 지도, 토요일 정규수업. 문의 010-4463-1177',
                 banner=('LOCATION', '오시는 길', ADDR), cta='가까운 곳에서, 처음부터 제대로'),
    'local': P(path='sangam-volleyball-academy/', crumb='상암·은평·고양 배구학원', title='상암·은평·고양 배구학원 | 하이앤드 발리볼 아카데미',
               desc='상암·은평·고양 프리미엄 배구 아카데미 하이앤드(배구 학원·배구교실). 상암 인근 · 현천동 180-1, 국가대표·프로 출신 코치진이 초등학생부터 성인까지 가르칩니다. 원데이 클래스 네이버 예약, 토요일 수업 · 010-4463-1177',
               banner=('LOCAL VOLLEYBALL ACADEMY', '상암·은평·고양 배구학원', '가까운 곳에서 만나는 프리미엄 배구 아카데미'), bg='class-2-1200',
               cta='가까운 곳에서, 처음부터 제대로'),
    'faq': P(path='contact/faq/', crumb='자주 묻는 질문', title='자주 묻는 질문 | 배구학원 수강료 · 준비물 · 주차 · 하이앤드',
             desc='하이앤드 자주 묻는 질문: 초등학생도 배울 수 있나요, 누가 가르치나요, 수업 시간, 수강료, 준비물, 주차, 원데이비 차감, 형제 수강권, 결제 방법.',
             banner=('FAQ', '자주 묻는 질문', '궁금한 점을 먼저 확인해 보세요')),
    'ask': P(path='contact/ask/', crumb='상담하기', title='수업 상담 · 문의 | 카카오톡 · 전화 · 하이앤드',
             desc='하이앤드 수업 상담: 카카오톡 채널 1:1 채팅, 전화 010-4463-1177, 인스타그램 DM, 이메일. 나이(학년) · 배구 경력 · 가능한 요일을 남겨 주세요.',
             banner=('CONTACT US', '상담하기', '나이(학년) · 배구 경력 · 가능한 요일을 남겨 주세요')),
    'notfound': P(path='404.html', crumb='404', hidden=True, title='페이지를 찾을 수 없습니다 | 하이앤드 발리볼 아카데미',
                  desc='주소가 바뀌었을 수 있습니다.', banner=('404', '페이지를 찾을 수 없습니다', '주소가 바뀌었을 수 있습니다. 아래에서 원하시는 페이지로 이동해 주세요.')),
}

# ── 메뉴: 대메뉴 → 2단계 → 3단계 (설계서 2장). (페이지키, 이름) 또는 (None, 묶음 이름, [3단계]) ──
NAV = [
    ('about', 'ABOUT US', [('about', '하이앤드 소개'), ('coaches', '코칭 스태프'), ('facility', '시설')]),
    ('method', 'METHOD', [('method', '알고 하면 쉬운 배구'), ('maps', 'MAPS 워밍업'), ('correction', '정밀 교정'),
                          ('flow', '수업 80분 흐름'), ('level', '성장 레벨')]),
    ('class', 'CLASS', [(None, '원데이 클래스', [('oneday', '원데이클래스'), ('oneday-apply', '원데이클래스 신청'), ('oneday-reviews', '원데이클래스 후기')]),
                        (None, '정규 클래스', [('youth', '유소년반'), ('beginner', '초급반'), ('intermediate', '중급반'), ('competition', '시합반'), ('team', '팀클래스'), ('regular-reviews', '정규 클래스 후기')]),
                        ('elite', '엘리트 선수 준비반'),
                        ('intl', 'INTERNATIONAL'),
                        ('private', '개인레슨'), ('guide', '수강 · 결제 안내'), ('photos', '클래스 사진')]),
    ('story', 'STORY', [('school', '국가대표가 찾아가는 배구교실'), ('hiand', 'Hi : And Day'), ('story', '수업 이야기'), ('note', '배구 노트')]),
    ('contact', 'CONTACT', [('contact', '오시는 길'), ('local', '상암·은평·고양 배구학원'), ('faq', '자주 묻는 질문'), ('ask', '상담하기')]),
]


def shown(k):
    return not PAGES[k].get('hidden')


def nav_items(subs):
    """숨긴 페이지를 뺀 2단계 목록"""
    out = []
    for it in subs:
        if it[0] is None:
            kids = [(k, t) for k, t in it[2] if shown(k) and PAGES[k].get('tab', True)]
            if kids:
                out.append((None, it[1], kids))
        elif shown(it[0]) and PAGES[it[0]].get('tab', True):
            out.append(it)
    return out


def place_of(key):
    """페이지가 속한 (대메뉴키, 대메뉴 이름, 묶음 이름 또는 None)"""
    for top, label, subs in NAV:
        if key == top:
            return top, label, None
        for it in subs:
            if it[0] == key:
                return top, label, None
            if it[0] is None and any(k == key for k, _ in it[2]):
                return top, label, it[1]
    return None, None, None


def leaves(top):
    for t, label, subs in NAV:
        if t == top:
            out = []
            for it in nav_items(subs):
                out += it[2] if it[0] is None else [it]
            return out
    return []


# ════════════════════════ 작은 도우미 ════════════════════════
def ver(path):
    return hashlib.md5(open(os.path.join(ROOT_DIR, path), 'rb').read()).hexdigest()[:8]


def url(key, frag=''):
    return BASE + PAGES[key]['path'] + frag


def rootof(key):
    p = PAGES[key]['path']
    return '../' * p.count('/')


def rel(root, key, frag=''):
    p = PAGES[key]['path']
    return (root + p + frag) if p else ((root or './') + frag)


def img(root, name, alt, w, h, lazy=True, cls=''):
    ext = 'jpg' if name.startswith('0820') or name.startswith('coach-hwang') or name.startswith('hero-') else 'webp'
    attrs = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ''
    # 사진을 바꿔도 브라우저가 예전 사진을 보여 주지 않도록 파일 내용 기준 버전을 붙임 (2026-11-09)
    v = ver(f'assets/img/{name}.{ext}')
    return f'<img{c} src="{root}assets/img/{name}.{ext}?v={v}" alt="{escape(alt)}" width="{w}" height="{h}"{attrs}>'


# ════════════════════════ 구조화 데이터 ════════════════════════
SAME_AS = [INSTA, YOUTUBE, NAVER_PLACE, BLOG, KAKAO]


def org_graph():
    return [
        {'@type': 'Organization', '@id': BASE + '#org', 'name': NAME, 'alternateName': NAME_EN, 'url': BASE,
         'logo': BASE + 'assets/img/logo-square.png', 'email': EMAIL, 'telephone': PHONE_INTL, 'sameAs': SAME_AS,
         'founder': {'@id': url('coaches') + '#kim'}},
        {'@type': 'SportsActivityLocation', '@id': BASE + '#place', 'name': NAME + ' 상암점', 'url': BASE,
         'image': BASE + 'assets/img/og-image.jpg', 'telephone': PHONE_INTL, 'email': EMAIL,
         'description': '국가대표·프로 선수의 훈련 방식을 시스템으로 만든 상암 인근 프리미엄 배구 아카데미. 국가대표·프로 출신 하이앤드 코치진이 초등학생부터 성인까지 가르칩니다.',
         'address': {'@type': 'PostalAddress', 'streetAddress': '현천동 180-1', 'addressLocality': '고양시 덕양구',
                     'addressRegion': '경기도', 'addressCountry': 'KR'},
         'geo': {'@type': 'GeoCoordinates', 'latitude': 37.595877, 'longitude': 126.8672995},
         'hasMap': GOOGLE_MAP,
         'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': 'https://schema.org/Saturday',
                                        'opens': '12:00', 'closes': '17:50'}],
         'sameAs': SAME_AS, 'parentOrganization': {'@id': BASE + '#org'}},
    ]


def ld(objs):
    return '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@graph': objs},
                                                              ensure_ascii=False, separators=(',', ':')) + '</script>'


def trail(key):
    """경로: [(이름, 페이지키)] — HOME › 대메뉴 › 묶음 › 페이지"""
    if key in ('home', 'notfound'):
        return [('HOME', 'home')]
    top, label, group = place_of(key)
    out = [('HOME', 'home'), (label, top)]
    if group:
        subs = [g for g in NAV if g[0] == top][0][2]
        kids = [k for it in subs if it[0] is None and it[1] == group for k, _ in it[2] if shown(k)]
        out.append((group, kids[0] if kids else key))
    if key != top and not (group and out[-1][1] == key and not PAGES[key].get('tab', True)):
        out.append((PAGES[key]['crumb'], key))   # 탭에 안 보이는 묶음(원데이)의 첫 페이지는 묶음 이름과 겹치지 않게
    return out


def breadcrumb_ld(key):
    t = trail(key)
    if len(t) < 2:
        return None
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': url(k)} for i, (n, k) in enumerate(t)]}


def faq_ld(faqs):
    return {'@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]}


def faq_html(faqs, first_open=True):
    out = []
    for i, (q, a) in enumerate(faqs):
        op = ' open' if (i == 0 and first_open) else ''
        out.append(f'<details{op}><summary>{escape(q)}</summary><p>{escape(a)}</p></details>')
    return '<div class="faq">' + ''.join(out) + '</div>'


# ════════════════════════ 공통 틀 ════════════════════════

def icons(root):
    """브라우저 탭 아이콘 · 휴대폰 홈 화면 아이콘 (하이앤드 엠블럼)"""
    return (f'<link rel="icon" type="image/png" sizes="64x64" href="{root}assets/img/favicon-64.png">'
            f'<link rel="apple-touch-icon" href="{root}assets/img/apple-touch-icon.png">')

def head(key, root, extra_ld):
    p = PAGES[key]
    graph = org_graph() + [x for x in [breadcrumb_ld(key)] + list(extra_ld) if x]
    if key == 'home':
        graph.append({'@type': 'WebSite', '@id': BASE + '#site', 'url': BASE, 'name': NAME, 'inLanguage': 'ko-KR',
                      'publisher': {'@id': BASE + '#org'}})
    robots = 'noindex,follow' if p.get('hidden') else 'index,follow,max-image-preview:large'
    canon = '' if key == 'notfound' else f'<link rel="canonical" href="{url(key)}">\n'
    # 영어 페이지가 생기면 PAGES의 en='en/international/' 처럼 적어 두면 서로 연결됨 (hreflang)
    if PAGES[key].get('en'):
        canon += (f'<link rel="alternate" hreflang="ko" href="{url(key)}">\n'
                  f'<link rel="alternate" hreflang="en" href="{BASE}{PAGES[key]["en"]}">\n')
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(p['title'])}</title>
<meta name="description" content="{escape(p['desc'])}">
{canon}<meta name="robots" content="{robots}">
<meta name="theme-color" content="#003960">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{escape(p['title'])}">
<meta property="og:description" content="{escape(p['desc'])}">
<meta property="og:url" content="{url(key) if key != 'notfound' else BASE}">
<meta property="og:image" content="{BASE}assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="하이앤드 발리볼 아카데미 수강생 단체 사진">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(p['title'])}">
<meta name="twitter:description" content="{escape(p['desc'])}">
<meta name="twitter:image" content="{BASE}assets/img/og-image.jpg">
{icons(root)}
<script>document.documentElement.classList.add('js')</script>
<link rel="preload" href="{root}fonts/Paperlogy-9Black.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}fonts/Paperlogy-4Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/css/base.css?v={ver('assets/css/base.css')}">
<link rel="stylesheet" href="{root}assets/css/site.css?v={ver('assets/css/site.css')}">
{ld(graph)}
</head>'''


def header(key, root):
    cur_top = place_of(key)[0]
    g1 = []
    for top, label, subs in NAV:
        lis = []
        for it in nav_items(subs):
            if it[0] is None:
                kids = ''.join(f'<li><a href="{rel(root, k)}"{" aria-current=page" if k == key else ""}>{escape(t)}</a></li>' for k, t in it[2])
                lis.append(f'<li class="has3"><a href="{rel(root, it[2][0][0])}">{escape(it[1])}<span class="arr" aria-hidden="true">›</span></a><ul class="g3">{kids}</ul></li>')
            else:
                lis.append(f'<li><a href="{rel(root, it[0])}"{" aria-current=page" if it[0] == key else ""}>{escape(it[1])}</a></li>')
        on = ' on' if top == cur_top else ''
        g1.append(f'<div class="g1{on}"><a class="g1a" href="{rel(root, top)}">{label}</a><ul class="g2">{"".join(lis)}</ul></div>')
    return f'''<body data-page="{key}">
<a class="skip" href="#main">본문 바로가기</a>
<header class="hd3">
  <div class="hd3-in">
    <button class="hd3-all" id="menuBtn" type="button" aria-label="전체 메뉴 열기" aria-expanded="false" aria-controls="drawer" data-drawer-open>{SN['menu']}</button>
    <a class="hd3-logo" href="{rel(root, 'home')}"><img class="lg-emb" src="{root}assets/img/logo-emblem.webp" alt="" width="36" height="40"><img class="lg-word" src="{root}assets/img/logo-text-white.webp" alt="HIGH END VOLLEYBALL ACADEMY 하이앤드 발리볼 아카데미" width="88" height="26"></a>
    <nav class="gnb3" aria-label="주요 메뉴">{"".join(g1)}</nav>
    <div class="hd3-act">
      <a class="hd3-login" href="{root}dashboard.html" aria-label="회원 로그인">{USER_ICON}<span>로그인</span></a>
    </div>
  </div>
</header>
{drawer_html(root, key)}'''



def drawer_html(root, key=''):
    """☰ 를 누르면 왼쪽에서 나오는 전체 메뉴 (로켓츠식): 대메뉴만 보이고, 누르면 그 페이지로 이동"""
    cur_top = place_of(key)[0] if key and key != 'home' else ''
    cols = [f'<a class="drw-top" href="{rel(root, top)}"{" aria-current=page" if top == cur_top else ""}>{label}</a>'
            for top, label, subs in NAV]
    home_on = ' aria-current="page"' if key == 'home' else ''
    return f'''<div class="drw" id="drawer" hidden>
  <div class="drw-bg" data-drawer-close></div>
  <nav class="drw-in" aria-label="전체 메뉴">
    <button class="drw-x" type="button" aria-label="메뉴 닫기" data-drawer-close><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19"/></svg></button>
    <a class="drw-brand" href="{rel(root, 'home')}"><img src="{root}assets/img/logo-emblem.webp" alt="" width="64" height="70"><span>하이앤드</span></a>
    <a class="drw-top" href="{rel(root, 'home')}"{home_on}>HOME</a>
    {"".join(cols)}
    <div class="drw-cta"><a href="{root}dashboard.html">회원 로그인</a></div>
  </nav>
</div>'''

def sechead(key, root):
    """로켓츠 방식: 가운데 대메뉴 이름(양옆 선) + 2단계 탭 줄 + (묶음 안이면) 3단계 줄"""
    top, label, group = place_of(key)
    if not top:
        return ''
    subs = [g for g in NAV if g[0] == top][0][2]
    tabs, third = [], ''
    for it in nav_items(subs):
        if it[0] is None:
            on = it[1] == group
            tabs.append(f'<a href="{rel(root, it[2][0][0])}"{" class=on" if on else ""}>{escape(it[1])}</a>')
            if on:
                third = '<div class="sh-3">' + ''.join(
                    f'<a href="{rel(root, k)}"{" class=on aria-current=page" if k == key else ""}>{escape(t)}</a>' for k, t in it[2]) + '</div>'
        else:
            on = it[0] == key
            tabs.append(f'<a href="{rel(root, it[0])}"{" class=on aria-current=page" if on else ""}>{escape(it[1])}</a>')
    return (f'<section class="sh"><div class="sh-title"><a href="{rel(root, top)}">{label}</a></div>'
            f'<nav class="sh-tabs" aria-label="{label} 하위 메뉴"><div class="wrap">{"".join(tabs)}</div></nav>{third}</section>')


def pagehead(key, root):
    k, h1, sub = PAGES[key]['banner']
    return f'<section class="ph3"><div class="wrap"><p class="ph3-k">{escape(k)}</p><h1>{escape(h1)}</h1><p class="ph3-s">{escape(sub)}</p></div></section>'


def crumbs(key, root):
    t = trail(key)
    lis = []
    for i, (n, k) in enumerate(t):
        if i == len(t) - 1:
            lis.append(f'<li aria-current="page">{escape(n)}</li>')
        else:
            lis.append(f'<li><a href="{rel(root, k)}">{escape(n)}</a></li>')
    return f'<nav class="crumb wrap" aria-label="현재 위치"><ol>{"".join(lis)}</ol></nav>'


def cta_band(root, title, sub=''):
    s = f'<p class="cta2-sub">{sub}</p>' if sub else ''
    return f'''<section class="sec cta2"><div class="wrap"><div class="cta2-in reveal"><h2>{title}</h2>{s}
<div class="cta2-boxes">
<a class="cta2-box p" href="{NAVER_BOOK}" target="_blank" rel="noopener"><b>원데이 클래스 신청하기</b><span class="go">네이버 예약 →</span></a>
<a class="cta2-box s" href="{KAKAO_CHAT}" target="_blank" rel="noopener"><b>수업 문의하기</b><span class="go">카카오톡 상담 →</span></a>
</div></div></div></section>'''


def footer(root):
    links = ''.join(f'<a href="{rel(root, t)}">{l}</a>' for t, l, _ in NAV)
    return f'''<footer class="ft">
  <div class="wrap">
    <div class="ft-top">
      <div>
        <div class="ft-name">{NAME}</div>
        <div class="ft-info"><span>대표 김재휘</span><span>{ADDR}</span><span><a href="tel:01044631177">{PHONE}</a></span><span><a href="mailto:{EMAIL}">{EMAIL}</a></span></div>
        <nav class="ft-nav" aria-label="하단 메뉴"><a href="{rel(root, 'home')}">HOME</a>{links}<a href="{rel(root, 'local')}">상암·은평·고양 배구학원</a><a href="{root}dashboard.html">회원 로그인</a></nav>
      </div>
      <div class="ft-sns">
        <a href="{KAKAO}" target="_blank" rel="noopener" aria-label="카카오톡 채널">{SN['kakao']}</a>
        <a href="{INSTA}" target="_blank" rel="noopener" aria-label="인스타그램">{SN['insta']}</a>
        <a href="{YOUTUBE}" target="_blank" rel="noopener" aria-label="유튜브">{SN['youtube']}</a>
        <a href="{BLOG}" target="_blank" rel="noopener" aria-label="네이버 블로그">{SN['blog']}</a>
        <a href="{NAVER_PLACE}" target="_blank" rel="noopener" aria-label="네이버 플레이스">{SN['naver']}</a>
      </div>
    </div>
    <div class="ft-copy">© 2026 HIGH END VOLLEYBALL ACADEMY</div>
  </div>
</footer>
{fab_html()}'''



def fab_html():
    """떠 있는 \"문의\" 버튼 하나 → 누르면 카카오톡·전화·인스타·네이버 (홈·하위 페이지 공통)"""
    return f'''<div class="fab" id="fab">
  <div class="fab-list" id="fabList">
    <a href="{KAKAO_CHAT}" target="_blank" rel="noopener" class="fab-i kakao" aria-label="카카오톡 상담">{SN['kakao']}<span>카카오톡</span></a>
    <a href="tel:01044631177" class="fab-i phone" aria-label="전화 문의">{SN['phone']}<span>전화</span></a>
    <a href="{INSTA}" target="_blank" rel="noopener" class="fab-i insta" aria-label="인스타그램">{SN['insta']}<span>인스타</span></a>
    <a href="{NAVER_PLACE}" target="_blank" rel="noopener" class="fab-i naver" aria-label="네이버 플레이스">{SN['naver']}<span>네이버</span></a>
  </div>
  <button class="fab-btn" id="fabBtn" type="button" aria-expanded="false" aria-controls="fabList">{CHAT_ICON}<span>문의</span></button>
</div>'''

def page(key, body, extra_ld=(), scripts=(), root=None):
    root = rootof(key) if root is None else root
    sc = ''.join(f'<script src="{s if s.startswith("http") else root + s + "?v=" + ver(s)}" defer></script>' for s in scripts)
    p = PAGES[key]
    cta = cta_band(root, p.get('cta', '처음부터 제대로.'), p.get('cta_sub', '')) if key not in ('notfound', 'hiand') else ''  # Hi : And Day는 맨 아래가 카카오 채널 소식받기
    return (head(key, root, extra_ld) + '\n' + header(key, root) + '\n<main id="main">\n'
            + sechead(key, root) + '\n' + crumbs(key, root) + '\n' + pagehead(key, root) + '\n'
            + body(root) + '\n' + cta + '\n</main>\n' + footer(root) + '\n'
            + f'<script src="{root}assets/js/site.js?v={ver("assets/js/site.js")}" defer></script>'
            + f'<script src="{root}assets/js/drawer.js?v={ver("assets/js/drawer.js")}" defer></script>{sc}\n</body>\n</html>\n')


def go(r, key, text, cls='s'):
    return f'<a class="btn {cls}" href="{rel(r, key)}">{escape(text)}</a>'


def tl(r, key, text):
    """본문 중간의 다른 페이지 안내: 큰 버튼 대신 작은 글자 링크 (2026-11-09 대표 결정)"""
    return f'<a class="tlink" href="{rel(r, key)}">{escape(text)} →</a>'


def linkcards(r, items):
    """다른 서브페이지로 가는 카드 (예전 #위치 id를 붙여 길을 잃지 않게)"""
    out = []
    for key, title, desc, anchor in items:
        aid = f' id="{anchor}"' if anchor else ''
        out.append(f'<a class="lcard reveal"{aid} href="{rel(r, key)}"><div class="t">{escape(title)}</div><p>{escape(desc)}</p><span class="go">자세히 보기 →</span></a>')
    return '<div class="lcards">' + ''.join(out) + '</div>'


# ════════════════════════ 본문: ABOUT US ════════════════════════
def about_body(r):
    return f'''<section class="sec about-intro">
  <div class="wrap center">
    <img class="ai-logo reveal" src="{r}assets/img/logo-emblem.webp" alt="하이앤드 발리볼 아카데미 엠블럼" width="160" height="176" loading="lazy">
    <h2 class="ai-title">가장 완벽한 기본</h2>
    <p class="ai-tag">프리미엄 배구 아카데미, 하이앤드</p>
    <p class="ai-p">하이앤드 발리볼 아카데미는 국가대표·프로 선수의 훈련 방식을 시스템으로 만든 프리미엄 배구 아카데미입니다.<br>처음 배구를 시작하는 <strong>초등학생부터</strong> 학교 배구부·엘리트를 준비하는 학생, <strong>취미로 배우는 성인까지</strong> 지금 실력에 맞는 단계에서 배웁니다.</p>
    <p class="ai-p ai-why">서울배구학원과 배구아카데미를 알아보는 분들이 하이앤드를 찾는 이유는 하나입니다.<br><strong>국가대표·프로 출신 코치진이 처음부터 원리를 알려 주기 때문입니다.</strong></p>
    <p class="ai-p">200평 풀코트에서 <strong>MAPS 워밍업</strong>으로 몸을 준비하고, 줄 서서 기다리지 않고 모두가 동시에 움직이며, <strong>이유를 알고 하는 반복</strong>으로 기본기를 만듭니다.<br>원데이 클래스, 정규 클래스, 시합반, 1:1 개인레슨, 국제학교 학생 레슨까지 다양한 프로그램으로 배구의 즐거움을 전하고 있습니다.</p>
    <div class="pillars">
      <div class="pillar reveal"><b>01</b><span>안전하게 오래 하는 배구</span></div>
      <div class="pillar reveal"><b>02</b><span>즐겁게 지속하는 배구</span></div>
      <div class="pillar reveal"><b>03</b><span>기본이 무너지지 않는 배구</span></div>
    </div>
    <p class="ai-goal">하이앤드의 목표는 하나입니다.<br>수강생이 <strong>"하이앤드에서 배구를 배우고, 내 배구가 완전히 바뀌었다"</strong>고 말하는 것.</p>
  </div>
</section>
<section class="sec founder">
  <div class="wrap center reveal">
    <p class="eyebrow">OUR STORY</p>
    <h2>"만약 내가 16살 때 올바른 방법으로 배구를 배웠더라면…"</h2>
    <p class="lead">하이앤드는 이 질문에서 시작했습니다. 16살, 그때 알았더라면 좋았을 배구를 가르칩니다.</p>
    <p class="note">헤드코치 김재휘 (국가대표 7년 · 프로(V리그) 10년, 선수 17년) · <a href="{rel(r, 'coaches')}">코칭 스태프 보기</a></p>
    <p class="ai-give">수업 밖에서도 배구를 나눕니다.<br>2026년에는 가재울중·등촌고·은평중을 찾아가 배구교실을 열었습니다.<br><a href="{rel(r, 'school')}">국가대표가 찾아가는 배구교실 보기 →</a></p>
  </div>
</section>
<section class="sec alt">
  <div class="wrap center reveal">
    <h2>선수 경험을 "가르치는 말"로 바꿉니다</h2>
    <p class="lead">하이앤드 코치진은 국가대표와 V리그에서 뛴 선수 경험을 수업으로 옮깁니다. 하이앤드 수업은 "잘하는 사람의 감"이 아니라, 쉽게 이해할 수 있는 원리로 설명합니다. 국제학교와 해외 체류 학생을 지도한 경험도 있습니다.</p>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <h2>더 알아보기</h2>
    {linkcards(r, [('coaches', '코칭 스태프', '국가대표·프로 출신 하이앤드 코치진.', 'career'),
                   ('facility', '시설', '200평 풀코트, 건물 앞 주차 가능.', 'place'),
                   ('method', '하이앤드 코칭 시스템', '알고 하면 쉬운 배구, Why ? → How ? → Play !', ''),
                   ('class', '클래스 안내', '원데이 · 정규 · 시합반 · 개인레슨.', '')])}
  </div>
</section>'''


def coaches_body(r):
    return f'''<section class="sec" id="kim">
  <div class="wrap">
    <p class="eyebrow">HEAD COACH</p>
    <h2>김재휘 헤드코치</h2>
    <div class="career mt">
      <div class="reveal"><img class="coach-photo" src="{r}assets/img/coach-kim-profile.webp" alt="메인코치 김재휘 프로필: 대한민국 국가대표 2016~2022, 현대캐피탈·KB손해보험·우리카드·삼성화재" width="721" height="960" fetchpriority="high"></div>
      <div>
        <p class="role">대표 · 헤드코치 · 포지션 센터</p>
        <div class="stats4"><div><b>7년</b><span>국가대표</span></div><div><b>10년</b><span>프로(V리그)</span></div><div><b>4회</b><span>V리그 우승</span></div><div><b>17년</b><span>선수 경력</span></div></div>
        <h3>대한민국 국가대표 (2016~2022)</h3>
        <ul class="plain">
          <li>2016 AVC컵</li><li>2017 AVC컵 · 세계선수권</li>
          <li>2018 자카르타·팔렘방 아시안게임 <strong>은메달</strong> · VNL</li>
          <li>2019 도쿄올림픽 세계예선 · AVC컵</li><li>2020 도쿄올림픽 아시아 예선</li><li>2022 발리볼 챌린저컵</li>
        </ul>
        <h3>프로배구 V리그 (2015~2025)</h3>
        <ul class="plain"><li>천안 현대캐피탈 (2015~2020)</li><li>의정부 KB손해보험 스타즈 (2020~2021)</li><li>서울 우리카드 (2021~2024)</li><li>대전 삼성화재 (2024~2025)</li></ul>
        <h3>V리그 우승 4회</h3>
        <ul class="plain"><li>2015~2016 정규리그 우승</li><li>2016~2017 챔피언결정전 우승</li><li>2017~2018 정규리그 우승</li><li>2018~2019 챔피언결정전 우승</li></ul>
        <h3>지도자 자격</h3>
        <ul class="plain"><li>FIVB(국제배구연맹) 코치 레벨1</li><li>전문스포츠지도사 2급 (배구)</li></ul>
      </div>
    </div>
    <div id="hwang" class="coach2">
      <p class="eyebrow">COACH</p>
      <h2>황준태 코치</h2>
      <div class="career mt">
        <div class="reveal"><img class="coach-photo" src="{r}assets/img/coach-hwang-profile.jpg" alt="황준태 코치 프로필: 리베로, 서울 우리카드 배구단 2022~2024, 대통령배 배구대회 리베로상" width="720" height="960" loading="lazy" decoding="async"></div>
        <div>
          <p class="role">코치 · 포지션 리베로</p>
          <h3>프로배구 V리그</h3>
          <ul class="plain"><li>서울 우리카드 배구단 (2022~2024)</li></ul>
          <h3>수상</h3>
          <ul class="plain"><li>제50회 대통령배 배구대회 리베로상</li><li>제52회 대통령배 배구대회 리베로상</li></ul>
          <h3>학력</h3>
          <ul class="plain"><li>경북사대부고 졸업</li><li>한양대학교 졸업</li></ul>
        </div>
      </div>
    </div>
    <p class="tlinks">{tl(r, 'method', '수업 방식 보기')}</p>
  </div>
</section>'''


def facility_body(r):
    return f'''<section class="sec">
  <div class="wrap">
    <h2>200평 풀코트에서 배웁니다</h2>
    <div class="photos mt">
      <figure class="reveal">{img(r, 'class-1', '하이앤드 200평 풀코트 체육관에서 진행되는 배구 수업 전경', 720, 960)}</figure>
      <figure class="reveal">{img(r, 'class-3', '네트 앞에서 수강생들이 리시브 자세를 연습하는 수업 장면', 1200, 1600)}</figure>
    </div>
    <p class="note">{ADDR} · 건물 앞 주차 가능 · <a href="{rel(r, 'contact')}">오시는 길 보기</a></p>
  </div>
</section>'''


# ════════════════════════ 본문: METHOD ════════════════════════
def method_body(r):
    return f'''<section class="sec">
  <div class="wrap">
    <p class="lead">같은 동작을 백 번 반복해도, 왜 하는지 모르면 몸은 쉽게 바뀌지 않습니다. 하이앤드는 <strong>이유를 알고 하는 반복</strong>으로 가르칩니다. 동작마다 이유를 말로 설명하고, 코치가 몸으로 직접 보여 줍니다.</p>
    <div class="grid3 mt">
      <div class="card reveal"><div class="big-letter lbl2">Why ?<small>왜 필요한지</small></div><p style="margin-top:12px">오늘 배울 동작이 왜 필요한지, 몸이 어떻게 움직여야 하는지 먼저 이해합니다.</p></div>
      <div class="card reveal"><div class="big-letter lbl2">How ?<small>어떻게 움직이는지</small></div><p style="margin-top:12px">한 사람씩 자세를 보고, 몸에 맞게 정밀하게 교정합니다.</p></div>
      <div class="card reveal"><div class="big-letter lbl2">Play !<small>직접 해 보기</small></div><p style="margin-top:12px">배운 원리를 게임과 실전 상황에서 직접 써 봅니다.</p></div>
    </div>
    <div class="principle reveal"><div class="t">하이앤드가 가장 먼저 가르치는 원리</div><p>몸 방향이 공에서 멀어지면, 플랫폼(두 팔로 만든 판)과 공을 보낼 곳이 몸에서 멀어집니다. 그러면 몸통의 힘이 공에 전달되기 어렵습니다. 리시브, 토스, 스파이크 모두 <strong>몸 방향</strong>에서 시작합니다.</p></div>
  </div>
</section>
<section class="sec alt">
  <div class="wrap">
    <h2>스스로 고칠 수 있는 선수</h2>
    <p class="lead">코치가 없을 때도 "방금 공이 왜 저쪽으로 갔는지" 스스로 알아차리는 것이 목표입니다. 그래서 교정할 때 세 가지를 함께 씁니다.</p>
    <div class="grid3 mt">
      <div class="card reveal"><div class="big-letter lbl2">Ask<small>먼저 묻기</small></div><p style="margin-top:12px">"방금 어땠어요?" 수강생이 먼저 느낀 점을 말합니다.</p></div>
      <div class="card reveal"><div class="big-letter lbl2">Point<small>코치가 짚기</small></div><p style="margin-top:12px">코치가 원인과 고칠 점 하나를 짚어 줍니다.</p></div>
      <div class="card reveal"><div class="big-letter lbl2">Watch<small>영상으로 확인</small></div><p style="margin-top:12px">찍은 영상을 함께 보며 내 몸이 실제로 어떻게 움직였는지 확인합니다.</p></div>
    </div>
    <div class="principle reveal"><div class="t">하이앤드 운동일지 "Today &amp; Next Ball"</div><p>국가대표·프로 선수들이 피드백을 기록하던 습관을 하이앤드 운동일지로 만들었습니다. 개인레슨과 시합반은 매 수업이 끝나면 오늘의 좋았던 순간, 배운 점, 고칠 점을 적고 <strong>다음 공(Next Ball)</strong>을 준비합니다.</p></div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <h2>하이앤드 코칭 시스템을 이루는 것</h2>
    {linkcards(r, [('maps', 'MAPS 워밍업', '가동성 · 활성화 · 순발력 · 안정성. 안전하게 오래 하는 몸 만들기.', 'maps'),
                   ('correction', '정밀 교정', 'Ask → Point → Watch. 리시브와 스파이크를 한 사람씩.', 'fix'),
                   ('flow', '수업 80분 흐름', 'MAPS 워밍업 → 왜? → 어떻게? → 해보기!', 'flow'),
                   ('level', '성장 레벨', 'LV.1~4. 지금 할 수 있는 동작을 기준으로.', 'level')])}
  </div>
</section>'''


def maps_body(r):
    return f'''<section class="sec">
  <div class="wrap">
    <p class="lead">배구는 점프와 착지, 팔 스윙, 짧은 방향 전환이 반복되는 운동입니다. MAPS는 <strong>발목 · 무릎 · 어깨</strong>가 편하게 움직이도록 몸을 준비하는 하이앤드의 준비 운동입니다.</p>
    <div class="grid4 mt">
      <div class="card reveal"><div class="big-letter">M</div><h2 class="t" style="margin-top:10px">Mobility · 가동성</h2><p>발목 · 고관절 · 흉추 · 어깨가 잘 움직이게 풉니다.</p><p class="note">유소년은 기린 · 고릴라 · 개구리 · 게 걸음 같은 "애니멀 모빌리티"로 합니다.</p></div>
      <div class="card reveal"><div class="big-letter">A</div><h2 class="t" style="margin-top:10px">Activation · 활성화</h2><p>스윙과 착지 때 몸을 잡아 주는 엉덩이 · 몸통 · 어깨 뒤쪽 근육을 깨웁니다.</p><p class="note">배구공 · 풍선 · 콘으로 몸과 머리를 함께 깨우는 웜업 게임.</p></div>
      <div class="card reveal"><div class="big-letter">P</div><h2 class="t" style="margin-top:10px">Plyometrics · 순발력</h2><p>가벼운 점프와 스텝으로 부드럽게 내려앉는 착지를 익힙니다.</p><p class="note">사다리 · 허들 스텝, 점프 후 바로 언더 · 토스 · 어택으로 연결.</p></div>
      <div class="card reveal"><div class="big-letter">S</div><h2 class="t" style="margin-top:10px">Stability · 안정성</h2><p>한 발 서기, 착지 후 버티기로 방향 전환 때 흔들리지 않게 합니다.</p><p class="note">2인 1조 상체 안정성 운동.</p></div>
    </div>
    <div class="principle reveal"><div class="t">하이앤드가 MAPS를 만든 이유</div><p>국가대표·프로 선수 경험을 바탕으로 하이앤드가 만든 준비 운동입니다. 오래, 안전하게 배구를 즐길 수 있는 몸을 어릴 때부터 만들어 주고 싶다는 마음에서 시작했습니다. 나이에 맞게 바꿔서, 초등 저학년은 놀이와 게임으로, 중·고등과 시합반은 더 높은 강도로 합니다.</p></div>
    <p class="tlinks">{tl(r, 'flow', '수업 80분 흐름 보기')}</p>
  </div>
</section>'''


def correction_body(r):
    return f'''<section class="sec">
  <div class="wrap">
    <div class="grid3">
      <div class="card reveal"><h2 class="t">리시브: 팔보다 먼저 몸 방향</h2><p>팔만 고치지 않습니다. 준비 자세에서 엉덩이를 얼마나 접는지, 몸이 공과 목표 쪽을 향하는지부터 봅니다. 어디부터 고칠지는 사람마다 다릅니다.</p></div>
      <div class="card reveal"><h2 class="t">스파이크: 치킨윙 바로잡기</h2><p>가장 빠르고 간결한 동작이 가장 큰 힘을 만듭니다. 스텝에서 불필요한 동작을 덜어 내고, 팔을 펴서 힘을 효율적으로 싣는 스윙을 함께 만들어 갑니다.</p></div>
      <div class="card reveal"><h2 class="t">기다리지 않는 수업</h2><p>줄 서서 차례를 기다리지 않고, 모두가 동시에 움직여 공을 만지는 시간이 많습니다.</p></div>
    </div>
    <div class="principle reveal"><div class="t">한 사람씩 봅니다</div><p>같은 실수라도 원인은 사람마다 다릅니다. 하이앤드 코치진은 <strong>먼저 묻고 → 원인을 짚어 주고 → 영상으로 함께 확인</strong>합니다.</p></div>
    <p class="note">유튜브와 인스타에서는 방법을 보여 드립니다. 내 몸에 맞는 세부 교정은 하이앤드 수업에서 직접 경험해 보세요.</p>
    <p class="tlinks">{tl(r, 'private', '1:1 개인레슨 보기')}</p>
  </div>
</section>'''


def flow_body(r):
    return f'''<section class="sec">
  <div class="wrap">
    <ol class="steps">
      <li class="reveal"><div class="k">STEP 1</div><h2 class="t">MAPS 워밍업</h2><p>가동성 → 활성화 → 순발력 → 안정성. 안전하게 움직이는 몸 준비</p></li>
      <li class="reveal"><div class="k">STEP 2</div><h2 class="t">Why ? · 원리 이해</h2><p>오늘 배울 동작과 그 이유를 짧게. 목표를 알고 연습해야 오래 남습니다</p></li>
      <li class="reveal"><div class="k">STEP 3</div><h2 class="t">How ? · 교정 반복</h2><p>처음엔 같은 동작을 반복하고, 익숙해지면 공의 방향 · 높이 · 순서를 바꿔 가며</p></li>
      <li class="reveal"><div class="k">STEP 4</div><h2 class="t">Play ! · 게임</h2><p>작은 게임에서 실전 게임으로. 배운 동작을 판단과 함께 써 봅니다</p></li>
    </ol>
    <div class="grid3 mt">
      <div class="card reveal"><h2 class="t">매 수업 같은 순서</h2><p>토요일 정규수업은 매번 이 순서로 진행합니다.</p></div>
      <div class="card reveal"><h2 class="t">기다리지 않는 연습</h2><p>한 사람이 공을 만지는 횟수가 중요합니다. 모두가 동시에 움직이도록 수업을 짭니다.</p></div>
      <div class="card reveal"><h2 class="t">게임으로 마무리</h2><p>게임은 수업마다 다르게 준비합니다. 유소년 수업에서는 아이들이 즐겁게 몰입하는 놀이형 게임을 많이 합니다.</p></div>
    </div>
    <p class="tlinks">{tl(r, 'level', '성장 레벨 보기')}</p>
  </div>
</section>'''


def level_body(r):
    return f'''<section class="sec">
  <div class="wrap">
    <p class="lead">배구는 나이보다 <strong>"지금 할 수 있는 동작"</strong>이 중요합니다. 하이앤드 성장 레벨은 국가대표·프로 선수의 훈련 방식을 바탕으로 만들었습니다. 처음 배우는 분부터 배구부·엘리트 진학과 대회를 준비하는 학생까지, 지금 실력에 맞는 단계에서 시작해 한 단계씩 올라갑니다. 프리미엄 배구 학원 · 배구교실 · 배구 아카데미를 찾는 초등학생부터 성인까지, 누구나 이유를 알고 배우는 배구를 경험할 수 있습니다.</p>
    <div class="lvx-grid mt">
      <article class="lvx reveal">
        <div class="lvx-hd"><b>LV.1</b><div><h2>입문 · 초급반</h2><p>기초 기술 습득 · 배구에 재미 붙이기</p></div></div>
        <p class="lvx-who"><strong>이런 분께</strong> 배구를 처음 시작하는 분. 중학생 이상은 초급반, 처음 배우는 초등학생은 유소년반에서 시작합니다.</p>
        <ul class="plain"><li>기본 메커니즘 습득: 패스, 서브, 리시브</li><li>배구 놀이를 바탕으로 한 신체 감각 강화</li><li>팀워크 경험으로 배구의 재미 발견</li></ul>
        <p class="lvx-coach"><strong>이 단계를 마치면</strong> 기본 자세로 공을 받아 위로 띄우고, 언더핸드 서브로 네트를 넘길 수 있습니다.</p>
      </article>
      <article class="lvx reveal">
        <div class="lvx-hd"><b>LV.2</b><div><h2>기본 · 중급반</h2><p>기술의 정교화 · 신체 밸런스 강화</p></div></div>
        <p class="lvx-who"><strong>이런 분께</strong> 중학생 이상, 배구 경력 6개월 이상. 초등학생은 유소년반에서 이어 갑니다.</p>
        <ul class="plain"><li>볼 컨트롤 정밀화와 몸 방향 · 플랫폼 코칭</li><li>몸에 무리를 줄이는 효율적인 폼 만들기</li><li>기본 포지션 이해</li><li>상황별 협력 수비 시스템</li></ul>
        <p class="lvx-coach"><strong>이 단계를 마치면</strong> 리시브를 목표 방향으로 보내고, 오버핸드 토스를 하고, 서브를 꾸준히 넘길 수 있습니다.</p>
      </article>
      <article class="lvx reveal">
        <div class="lvx-hd"><b>LV.3</b><div><h2>심화 · 엘리트</h2><p>실전 퍼포먼스 극대화 · 전술 이해도와 배구 IQ 향상</p></div></div>
        <p class="lvx-who"><strong>이런 분께</strong> 학교 배구부·엘리트 진학을 준비하는 학생, 경기 경험을 갖춘 분. 중급반 · 개인레슨에서 진행합니다.</p>
        <ul class="plain"><li>공격과 수비 전반의 고난도 기술</li><li>팀 포메이션 시스템 구축</li><li>실전 전술 지능(VQ) 향상</li><li>경기력을 높이는 피지컬 고도화</li></ul>
        <p class="lvx-coach"><strong>이 단계를 마치면</strong> 스파이크 스텝과 스윙을 하고, 랠리 중 리시브-토스-공격 3번 터치를 만들 수 있습니다.</p>
      </article>
      <article class="lvx reveal">
        <div class="lvx-hd"><b>LV.4</b><div><h2>시합 · 시합반</h2><p>연령별 대표팀 선발과 대회를 목표로 한 집중 코칭</p></div></div>
        <p class="lvx-who"><strong>이런 분께</strong> 초등 고학년, 중·고등학생, 성인. 별도 상담으로 맞춤 진행합니다.</p>
        <ul class="plain"><li>실전 경기 리딩 능력 훈련</li><li>실제 경기 수준의 기술과 전략 적용</li><li>경기 운영 능력과 상황 판단력 강화</li><li>팀워크 · 팀 전술 완성</li></ul>
        <p class="lvx-coach"><strong>이 단계를 마치면</strong> 포지션 역할을 이해하고 6대6 경기를 하며 대회를 준비합니다.</p>
      </article>
    </div>
    <div class="lvx-common reveal">
      <div><strong>모든 단계 공통</strong> MAPS 워밍업 → 왜: 원리 이해 → 어떻게: 정밀 교정 → 해보기: 게임. 안전하게 오래 하는 배구, 즐겁게 지속하는 배구, 기본이 무너지지 않는 배구를 지향합니다.</div>
    </div>
    <div class="lvx-private reveal">
      <div><b>1:1 개인레슨</b><p>영상 분석을 바탕으로 한 개인 맞춤 훈련. 국가대표·프로 출신 코치진이 신체 조건에 맞는 폼으로 정밀하게 교정하고, 운동일지 "Today &amp; Next Ball"로 다음 수업을 준비합니다.</p></div>
      <a class="btn s" href="{rel(r, 'private')}">개인레슨 안내</a>
    </div>
  </div>
</section>'''


# ════════════════════════ 본문: CLASS ════════════════════════
CAL_PANEL = '''<div class="sched-grid" id="schedGrid">
  <div class="cal-wrap">
    <div class="cal-nav-row"><button class="cal-nav-btn" id="calPrev" aria-label="이전 달">‹</button><div class="month-title" id="calTitle">수업 일정 불러오는 중</div><button class="cal-nav-btn" id="calNext" aria-label="다음 달">›</button></div>
    <div class="cal-head"><div class="cal-hd sun">일</div><div class="cal-hd">월</div><div class="cal-hd">화</div><div class="cal-hd">수</div><div class="cal-hd">목</div><div class="cal-hd">금</div><div class="cal-hd sat">토</div></div>
    <div class="cal-days" id="calDays"></div>
    <div class="legend"><div class="legend-item"><div class="legend-dot" style="background:var(--blue)"></div>수업있음</div><div class="legend-item"><div class="legend-dot" style="background:var(--orange)"></div>거의 마감</div><div class="legend-item"><div class="legend-dot" style="background:var(--muted);opacity:.5"></div>취소됨</div></div>
  </div>
  <div class="sched-panel" id="schedPanel"><div class="no-sess-msg"><div class="icon">CALICON</div><div>날짜를 선택하면<br>수업 일정이 표시됩니다</div></div></div>
</div>'''


def hk_tiles(r, rich=False):
    """수업 고르기 사진 칸 6개 (메인·CLASS 공통). rich=True면 CLASS 페이지용 자세한 설명 + 앵커 id"""
    # 2026-11-09 대표: 메인은 대상만 짧게, CLASS 페이지는 시간 없이 꼭 필요한 안내 한 줄
    # 2026-11-10 대표: 국제학교 시합반을 3번째, 팀클래스를 5번째로
    cards = [('youth', 'class-5.webp', '초등학생', '초등학생 · 정규 수업', '유소년반', 'youth', None),
             ('beginner', 'class-3.webp', '중학생 이상', '중학생 이상 · 입문 / 경력 6개월 이상', '초급 · 중급반', 'group',
              [('beginner', '초급반 보기'), ('intermediate', '중급반 보기')]),
             ('intl', 'class-6.webp', '국제학교 · U15 · U18', '국제학교 트라이아웃 · U15 · U18 대회', '국제학교<br>시합반', 'intl',
              [('intl', 'INTERNATIONAL 보기'), ('competition', '시합반 보기')]),
             ('elite', 'elite-tokyo-qual.webp', '초등 4학년~고등학생', '초등 4학년~고등학생 · 배구선수를 꿈꾸는 학생', '엘리트<br>선수 준비반', 'elite', None),
             ('team', 'class-2.webp', '동호회 · 학교 · 기업', '동호회 · 학교 · 기업', '팀 클래스', 'team', None),
             ('private', '0820-04.jpg', '1:1 맞춤 수업', '1:1 맞춤 수업', '개인레슨', 'private', None)]
    out = []
    for key, f, sm, d, t, aid, links in cards:
        a = f' id="{aid}"' if rich else ''
        name = t.replace('<br>', ' ')
        go = ''.join(f'<a href="{rel(r, k)}">{escape(x)} →</a>' for k, x in (links or [(key, '자세히 보기')]))
        out.append(f'<div class="hk reveal"{a}><img src="{r}assets/img/{f}?v={ver("assets/img/" + f)}" alt="" loading="lazy">'
                   f'<a class="hk-cover" href="{rel(r, key)}" aria-label="{escape(name)}"></a>'
                   f'<span class="hk-t"><small>{escape(d)}</small><b>{t}</b><span class="hk-go">{go}</span></span></div>')
    return out


def class_body(r):
    # 2026-11-09 대표 확정: 메인과 같은 '사진 위 큰 자막' 칸 6개(3×2). 원데이는 카드에서 빼고 한 줄 링크
    out = hk_tiles(r, rich=True)
    return f'''<section class="sec">
  <div class="wrap">
    <p class="lead">국가대표·프로 출신 하이앤드 코치진이 가르칩니다. 처음이라면 원데이 클래스로, 실력과 나이에 맞춰 정규 클래스로 이어집니다.</p>
    <h2 class="cgrp">정규 클래스</h2>
    <p class="cgrp-sub">토요일 정규 수업과 대회 준비</p>
    <div class="hk-grid">{"".join(out[:3])}</div>
    <h2 class="cgrp cgrp-gap">목표별 · 맞춤 클래스</h2>
    <p class="cgrp-sub">선수 준비, 단체 수업, 1:1 맞춤 수업</p>
    <div class="hk-grid">{"".join(out[3:])}</div>
    <p class="ccard-oneday" id="oneday"><a href="{rel(r, 'oneday')}">처음이라면 원데이 클래스로 먼저 경험해 보세요 →</a></p>
    <div class="ccard-more"><a id="schedule" href="{rel(r, 'guide')}">수강 · 결제 안내 · 시간표 →</a><a href="{rel(r, 'photos')}">클래스 사진 →</a></div>
  </div>
</section>'''.replace('<section class="sec">', '<section class="sec sec-tight">', 1)


def oneday_body(r):
    return f'''<section class="sec">
  <div class="wrap">
    <div class="oneday">
      <div class="price-card reveal">
        <span class="tag">원데이 클래스</span>
        <div class="pr pr-txt">토요일 정규 수업에 그대로 함께하는 체험 수업</div>
        <ul class="ticks">
          <li>토요일 12:00 · 13:30 · 16:30</li>
          <li>처음 배구를 하는 초등학생부터 성인까지</li>
          <li>네이버 예약으로 신청 · 정규 등록 시 원데이 비용 차감</li>
          <li>수업 시작 10분 전 도착 · 실내 운동화, 물, 편한 운동복</li>
        </ul>
        <a class="btn w" href="{rel(r, 'oneday-apply')}">원데이 클래스 신청</a>
      </div>
      <div class="card reveal">
        <div class="cta-card-icon" style="margin-bottom:10px">{SN['ticket']}</div>
        <h2 class="t">원데이 클래스에서 하는 것</h2>
        <p>원데이 클래스는 정규 수업에 그대로 함께합니다. 실제 수업을 그대로 경험해 보세요.</p>
        <ol class="plain" style="margin-top:10px"><li>MAPS 워밍업</li><li>Why ? 오늘 배울 동작의 원리</li><li>How ? 한 사람씩 정밀 교정</li><li>Play ! 게임</li></ol>
      </div>
    </div>
  </div>
</section>'''


def apply_body(r):
    return f'''<section class="sec">
  <div class="wrap">
    <div class="apply reveal">
      <div class="apply-main">
        <span class="tag">원데이 클래스</span>
        <div class="pr pr-txt">토요일 정규 수업에 그대로 함께하는 체험 수업</div>
        <p>네이버 예약으로 신청해 주세요. 토요일 12:00 · 13:30 · 16:30 중 원하시는 시간을 네이버 예약에서 골라 주세요.</p>
        <a class="btn naverbook" href="{NAVER_BOOK}" target="_blank" rel="noopener">{SN['naverN']}네이버 예약으로 신청하기</a>
      </div>
      <ul class="apply-list">
        <li><b>준비물</b>실내 운동화, 물, 편한 운동복</li>
        <li><b>도착</b>수업 시작 10분 전까지 와 주세요</li>
        <li><b>주차</b>건물 앞 주차 가능</li>
        <li><b>정규 등록</b>원데이 후 정규 수업을 등록하시면 원데이 비용을 차감해 드립니다</li>
        <li><b>문의</b><a href="{KAKAO_CHAT}" target="_blank" rel="noopener">카카오톡 상담</a> · <a href="tel:01044631177">{PHONE}</a></li>
      </ul>
    </div>
  </div>
</section>'''


def reviews_body(r):
    return f'''<section class="sec"><div class="wrap center"><p class="lead">수강생과 학부모님의 후기는 네이버 방문자 리뷰에서 확인하실 수 있습니다.</p><div class="btns"><a class="btn p" href="{NAVER_REVIEW}" target="_blank" rel="noopener">네이버 방문자 리뷰 보기</a></div></div></section>'''


def youth_body(r):
    return f'''<section class="sec">
  <div class="wrap split">
    <figure class="reveal">{img(r, 'class-5', '어린이 수강생들이 코치의 설명을 듣고 있는 유소년반 수업 장면', 1200, 1600)}</figure>
    <div class="reveal">
      <h2>초등학생 배구교실부터 엘리트 진학 준비까지</h2>
      <p>바른 자세와 기본기를 처음부터 제대로 익힙니다. 학부모님께 "우리 아이가 제대로 배우고 있다"는 안심을 드리고 싶습니다.</p>
      <ul class="ticks"><li>토요일 12:00 · 80분 정규수업</li><li>대상: 초등학생</li><li>형제는 수강권을 함께 쓸 수 있습니다</li></ul>
      <p class="tlinks">{tl(r, 'level', '성장 레벨 보기')}</p>
    </div>
  </div>
</section>'''


def beginner_body(r):
    return f'''<section class="sec">
  <div class="wrap split rev">
    <figure class="reveal">{img(r, 'class-3', '수강생들이 콘을 두고 리시브 자세를 연습하는 초급반 수업 장면', 1200, 1600)}</figure>
    <div class="reveal">
      <h2>기초 기술 습득 · 배구에 재미 붙이기</h2>
      <p>배구를 처음 시작하는 중학생 이상을 위한 반입니다. 패스, 서브, 리시브의 기본 메커니즘을 익히고, 팀워크 경험으로 배구의 재미를 발견합니다.</p>
      <ul class="ticks"><li>토요일 13:30 · 80분 정규수업</li><li>대상: 중학생 이상, 처음 배우는 분</li><li>처음 배우는 초등학생은 유소년반에서 시작합니다</li></ul>
      <p class="tlinks">{tl(r, 'intermediate', '중급반 보기')}</p>
    </div>
  </div>
</section>'''


def intermediate_body(r):
    return f'''<section class="sec">
  <div class="wrap split">
    <figure class="reveal">{img(r, 'class-4', '공 카트 옆에서 패스를 연습하는 중급반 수강생', 1200, 1600)}</figure>
    <div class="reveal">
      <h2>기술의 정교화 · 신체 밸런스 강화</h2>
      <p>기본기를 갖추고 실전 실력을 높이고 싶은 분을 위한 반입니다. 볼 컨트롤을 정밀하게 다듬고, 신체 정렬 코칭으로 몸에 무리를 줄이는 효율적인 폼을 만듭니다.</p>
      <ul class="ticks"><li>토요일 16:30 · 80분 정규수업</li><li>대상: 중학생 이상, 배구 경력 6개월 이상</li><li>기본 포지션 이해, 상황별 협력 수비</li></ul>
      <p class="tlinks">{tl(r, 'level', '성장 레벨 보기')}</p>
    </div>
  </div>
</section>'''


def competition_body(r):
    return f'''<section class="sec">
  <div class="wrap split">
    <figure class="reveal">{img(r, 'class-6', '점프해서 스파이크를 하는 시합반 수강생', 1200, 1600)}</figure>
    <div class="reveal">
      <h2>실전에서 흔들리지 않는 판단</h2>
      <p>연령별 대표팀 선발과 대회를 목표로 하는 학생과 성인을 위한 반입니다. 하이앤드 코치진이 국가대표와 V리그에서 경험한 팀 시스템을 쉬운 말로 풀어, 왜 그 자리에 서야 하는지부터 이해하게 합니다.</p>
      <ul class="ticks"><li>실전 경기 리딩 능력 훈련</li><li>실제 경기 수준의 기술과 전략 적용</li><li>경기 운영 능력과 상황 판단력 강화</li><li>팀워크 · 팀 전술 완성</li></ul>
      <dl class="hd-info cm-age">
        <div><dt>U15</dt><dd>13세 이상 · 중학생</dd></div>
        <div><dt>U18</dt><dd>16세 이상 · 고등학생</dd></div>
        <div><dt>그 밖에</dt><dd>초등 고학년 · 성인은 상담으로 맞춰 드립니다</dd></div>
      </dl>
      <p class="note">수업 시간과 구성은 별도 상담으로 맞춰 드립니다.</p>
      <p class="tlinks">{tl(r, 'level', '4단계 성장 레벨 보기')}</p>
    </div>
  </div>
</section>'''


def team_body(r):
    return f'''<section class="sec">
  <div class="wrap split rev">
    <figure class="reveal">{img(r, 'class-2', '함께 수업을 마친 하이앤드 수강생 단체 사진', 1600, 1200)}</figure>
    <div class="reveal">
      <h2>함께 배우는 팀클래스</h2>
      <p>같은 동호회, 같은 학교, 같은 회사 사람들이 한 팀으로 배우는 수업입니다. 인원과 목표에 맞춰 주 1회 정기 수업으로 진행합니다. 국가대표·프로 출신 하이앤드 코치진이 기본기부터 팀 전술까지 가르칩니다.</p>
      <ul class="ticks"><li>주 1회 정기 수업 · 1시간 30분</li><li>일정 · 인원 · 수업 장소는 상담으로 맞춰 드립니다</li><li>수강료는 카카오톡 상담으로 안내드립니다</li></ul>
    </div>
  </div>
</section>
<section class="sec alt">
  <div class="wrap">
    <h2>이런 팀에 맞습니다</h2>
    <div class="grid4 mt">
      <div class="card reveal"><h3 class="t">배구 동호회</h3><p>6인제 · 9인제 모두 가능합니다. 처음 모인 팀부터, 기본기와 포지션 역할을 다시 다지고 싶은 팀까지.</p></div>
      <div class="card reveal"><h3 class="t">학교 배구부 · 방과후</h3><p>학교 배구부, 방과후, 학교스포츠클럽 수업과 선생님 연수. 2026년에는 <a href="{rel(r, 'school')}">국가대표가 찾아가는 배구교실</a>(가재울중 · 등촌고 · 은평중)도 열었습니다.</p></div>
      <div class="card reveal"><h3 class="t">회사 · 단체</h3><p>사내 동호회, 팀워크 활동. 처음 배구를 하는 사람도 함께할 수 있게 수준에 맞춰 나눠서 지도합니다.</p></div>
      <div class="card reveal"><h3 class="t">해외 학교 배구부</h3><p>국제학교 · 해외 학교 배구부의 단기 캠프. 기간과 인원, 진행 언어는 상담으로 맞춰 드립니다.</p></div>
    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <h2>팀 수업은 이렇게 진행됩니다</h2>
    <p class="lead">한 번 수업은 1시간 30분. 줄 서서 기다리지 않고, 모두가 동시에 움직입니다.</p>
    <ol class="steps mt">
      <li class="reveal"><span class="k">STEP 1</span><p class="t">MAPS 워밍업</p><p>부상을 줄이고 몸을 깨우는 하이앤드 워밍업</p></li>
      <li class="reveal"><span class="k">STEP 2</span><p class="t">Why ? · 원리 이해</p><p>오늘 배울 동작을 왜 그렇게 하는지 먼저 이해합니다</p></li>
      <li class="reveal"><span class="k">STEP 3</span><p class="t">How ? · 스테이션 훈련</p><p>팀을 나눠 동시에 연습하고, 코치가 한 사람씩 짚어 줍니다</p></li>
      <li class="reveal"><span class="k">STEP 4</span><p class="t">Play ! · 실전 게임</p><p>포지션과 로테이션을 실제 경기처럼 맞춰 봅니다</p></li>
    </ol>
  </div>
</section>
<section class="sec alt">
  <div class="wrap">
    <h2>팀 단계별 과정</h2>
    <p class="lead">팀의 지금 수준을 먼저 보고, 우리 팀에 맞는 단계부터 시작합니다.</p>
    <ol class="steps mt">
      <li class="reveal"><span class="k">01</span><p class="t">레벨 진단</p><p>팀원 한 명 한 명의 지금 실력과 포지션을 확인합니다</p></li>
      <li class="reveal"><span class="k">02</span><p class="t">기본기</p><p>패스 · 리시브의 몸 방향과 플랫폼을 다집니다</p></li>
      <li class="reveal"><span class="k">03</span><p class="t">연결</p><p>서브 → 리시브 → 토스로 이어지는 흐름을 만듭니다</p></li>
      <li class="reveal"><span class="k">04</span><p class="t">공격 · 팀 플레이</p><p>공격, 로테이션, 연습경기와 대회 준비까지 이어 갑니다</p></li>
    </ol>
    <p class="tlinks">{tl(r, 'intl', 'INTERNATIONAL 국제학교 레슨')}{tl(r, 'competition', '시합반 보기')}</p>
  </div>
</section>'''


def private_body(r):
    return f'''<section class="sec">
  <div class="wrap split">
    <figure class="reveal">{img(r, 'class-6', '수강생이 점프해서 스파이크를 하는 장면', 1200, 1600)}</figure>
    <div class="reveal">
      <h2>내 약점을, 내 몸에 맞게</h2>
      <p>국가대표·프로 출신 하이앤드 코치진이 60분 동안 한 사람만 봅니다. 서브, 리시브, 스파이크 등 내 약점을 내 몸에 맞게 교정합니다. 영상 분석을 바탕으로 신체 조건에 맞는 폼을 함께 찾습니다.</p>
      <div class="prices"><div><span>1회 (60분)</span><strong>25만 원</strong></div><div><span>10회 등록</span><strong>회당 20만 원</strong></div></div>
    </div>
  </div>
</section>'''


def elite_body(r):
    return f'''<section class="sec">
  <div class="wrap split">
    <figure class="reveal">{img(r, 'elite-tokyo-qual', '도쿄올림픽 아시아 대륙예선에 출전한 대한민국 남자 배구 대표팀', 2400, 1572)}</figure>
    <div class="reveal">
      <h2>선수의 길을 걸어 본 코치진이 함께 준비합니다</h2>
      <p>배구선수를 꿈꾸는 초등 4학년부터 고등학생까지를 위한 반입니다.<br>국가대표·프로 선수의 훈련 방식을 바탕으로,<br>지금 실력을 먼저 진단하고 목표에 맞춰 준비합니다.</p>
      <ul class="ticks"><li>대상: 초등 4학년 ~ 고등학생</li><li>수업: 주 1회 그룹 수업 + 소그룹 집중 클래스</li><li>1:1 개인레슨은 필요할 때 함께 선택할 수 있습니다</li><li>입반: 상담과 레벨 진단 후 시작합니다</li></ul>
      <p class="note">취미로 배우는 초등학생은 유소년반, 선수를 목표로 하는 학생은 엘리트 선수 준비반에서 시작합니다.<br>초등 고학년 학부모님은 상담에서 아이의 단계를 함께 확인해 드립니다.</p>
      <p class="tlinks">{tl(r, 'level', '4단계 성장 레벨 보기')}</p>
    </div>
  </div>
</section>
<section class="sec alt">
  <div class="wrap split">
    <figure class="reveal r916">{img(r, 'coach-kim-national', 'VNL 국가대표 경기에서 득점 후 웃으며 손가락을 든 하이앤드 헤드코치', 900, 1600, cls='obj-top')}</figure>
    <div>
    <p class="k">HEAD COACH STORY</p>
    <h2>먼저 걸어 본 길</h2>
    <p class="lead reveal">하이앤드 헤드코치는 16살에 배구를 시작했습니다.<br>쉽지 않은 시간도 이겨 내며,<br>국가대표 7년 · 프로(V리그) 10년의 선수가 되었습니다.</p>
    <p class="reveal">그래서 늦은 시작도, 다시 일어서는 과정도 가까이에서 압니다.<br>하이앤드는 가능성을 약속하지 않고,<br>지금 단계를 정직하게 진단하는 것부터 시작합니다.</p>
    <blockquote class="reveal">"만약 내가 16살 때 올바른 방법으로 배구를 배웠더라면…"</blockquote>
    <p class="reveal">하이앤드는 그 아쉬움을 학생들의 준비 과정에 담았습니다.</p>
    <p class="tlinks">{tl(r, 'coaches', '코칭 스태프 보기')}</p>
    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <h2>이런 학생에게 맞습니다</h2>
    <div class="grid2 mt">
      <div class="card reveal"><h3 class="t">배구부 입단 테스트를 앞둔 학생</h3><p>리시브 · 토스 · 서브 같은 기본기를 먼저 점검합니다.</p></div>
      <div class="card reveal"><h3 class="t">엘리트 중·고 진학을 고민하는 학생</h3><p>지금 단계와 준비할 순서를 함께 정합니다.</p></div>
      <div class="card reveal"><h3 class="t">늦게 시작해 기본기를 다지고 싶은 학생</h3><p>이유를 알고 하는 반복으로 기본기를 쌓습니다.</p></div>
      <div class="card reveal"><h3 class="t">포지션을 고민하는 학생</h3><p>포지션에 필요한 기술과 움직임을 익힙니다.</p></div>
    </div>
  </div>
</section>
<section class="sec alt">
  <div class="wrap">
    <h2>이렇게 준비합니다</h2>
    <ol class="steps mt">
      <li class="reveal"><div class="k">STEP 1</div><h3 class="t">상담 · 레벨 진단</h3><p>지금 실력과 목표를 확인하고,<br>점프력 · 체력을 측정해 시작점을 확인합니다</p></li>
      <li class="reveal"><div class="k">STEP 2</div><h3 class="t">맞춤 계획</h3><p>진단 결과로 준비할 순서를 정합니다</p></li>
      <li class="reveal"><div class="k">STEP 3</div><h3 class="t">포지션별 기술</h3><p>세터 · 레프트 · 센터 · 리베로,<br>포지션마다 필요한 기술을 익힙니다</p></li>
      <li class="reveal"><div class="k">STEP 4</div><h3 class="t">몸 준비</h3><p>국가대표·프로 선수 경험을 바탕으로<br>하이앤드가 만든 MAPS 워밍업으로,<br>점프와 착지를 안전하게 배웁니다</p></li>
      <li class="reveal"><div class="k">STEP 5</div><h3 class="t">영상 · 운동일지</h3><p>국가대표·프로 선수 시절,<br>경기 전 상대 분석을 A4 한 장에 적어 외우던 습관을<br>운동일지 Today &amp; Next Ball로 만들었습니다</p></li>
    </ol>
    <div class="grid3 mt">
      <div class="card reveal"><h3 class="t">그룹 수업 · 주 1회</h3><p>같은 목표를 가진 학생들과 기본기와 포지션 기술을 함께 훈련합니다.</p></div>
      <div class="card reveal"><h3 class="t">소그룹 집중 클래스</h3><p>적은 인원으로 기술 하나하나를 깊게 다룹니다.</p></div>
      <div class="card reveal"><h3 class="t">1:1 개인레슨 · 선택</h3><p>약점과 포지션 기술을 코치가 한 사람만 보며 교정합니다.</p></div>
    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <h2>선수로 성장하는 방향</h2>
    <div class="grid3 mt">
      <div class="card reveal"><h3 class="t">어느 길이 맞을까</h3><p>즐기는 배구(스포츠클럽)와 선수를 목표로 하는 배구는 준비가 다릅니다.<br>상담에서 함께 정합니다.</p></div>
      <div class="card reveal"><h3 class="t">공부와 함께</h3><p>수업과 운동을 함께 하며 성장하는 방향을 지향합니다.<br>성장 속도보다 방향을 봅니다.</p></div>
      <div class="card reveal"><h3 class="t en">Next Ball</h3><p>실수는 지나가고, 다음 공은 늘 옵니다.<br>실수한 다음 공을 다시 준비하는 법까지 연습합니다.</p></div>
    </div>
    <p class="note">국가대표·프로 출신 하이앤드 코치진이 가르칩니다. 수업 시간과 수강료는 카카오톡 상담으로 안내드립니다.</p>
    <p class="tlinks">{tl(r, 'private', '1:1 개인레슨 보기')}</p>
  </div>
</section>'''


def elite_dream(r):
    """엘리트 선수 준비반 맺음 칸: 미래의 국가대표에게 (2026-11-09 대표 선택 1안·4안)"""
    return f'''
<section class="sec dream" style="--dream-bg:url('{r}assets/img/elite-dream-bg.webp')">
  <div class="wrap hd-narrow">
    <p class="k">FUTURE NATIONAL TEAM</p>
    <h2>미래의 국가대표를 꿈꾸는 학생에게</h2>
    <div class="dream-cards">
      <div class="dream-card reveal"><p>국가대표의 길은 하루아침에 만들어지지 않습니다.<br>오늘의 기본기 하나, 다음 공 하나가 쌓여 꿈에 가까워집니다.<br>그 길을 먼저 걸어 본 코치진이,<br>첫걸음부터 함께 준비합니다.</p></div>
      <div class="dream-card reveal"><span class="dream-tag">학부모님께</span><p>아이가 국가대표를 꿈꾼다고 말할 때,<br>그 길을 직접 걸어 본 코치진이<br>정직하게 함께 준비합니다.</p></div>
    </div>
  </div>
</section>'''

def intl_body(r):
    return f'''<section class="sec intl">
  <div class="wrap">
    <h2>국제학교 · 해외 거주 학생 배구 레슨</h2>
    <p class="lead">국제학교 · 외국인학교 학생과, 방학마다 한국을 찾는 해외 거주 학생도 함께 배웁니다. 국가대표·프로 출신 하이앤드 코치진이 지도합니다.</p>
    <p class="intl-en" lang="en">HIGH END Volleyball Academy offers volleyball lessons in Seoul for international and foreign school students (students from YISS, SFS, Dwight School Seoul, SIS, KIS, SPPS and Cheongna Dalton School have trained with us) — private lessons, school-break intensive training, and Varsity / JV tryout preparation, coached by former Korean national team and professional players. Located near Sangam (Hyeoncheon-dong 180-1).</p>
    <div class="intl-grid mt">
      <div class="intl-card reveal"><span class="n">01</span><h3>익숙한 배구 용어로</h3><p>Forearm pass(bump) · Set · Spike · Serve. 해외 학교와 클럽에서 쓰던 용어를 함께 써서, 영어가 편한 아이들도 자연스럽게 적응합니다. 영어 수업이 아니라 익숙한 용어로 몸의 움직임을 이해하는 데 초점을 둡니다.</p></div>
      <div class="intl-card reveal"><span class="n">02</span><h3>한 명 한 명, 기본기 교정</h3><p>팀 훈련과는 별개로 리시브할 때 발의 위치, 공을 맞히는 팔의 각도, 스파이크를 위한 몸의 움직임을 세밀하게 교정합니다. 작아 보이는 차이가 쌓여 실력의 차이가 됩니다.</p></div>
      <div class="intl-card reveal"><span class="n">03</span><h3>방학마다 이어지는 성장</h3><p>첫 방학에는 기본기, 다음 방학에는 기술 향상, 그다음에는 실전. 매번 처음부터 다시 시작하지 않고 지난 훈련을 다음 방학으로 이어갑니다.</p></div>
    </div>
    <div class="intl-more mt">
      <div class="intl-box reveal">
        <h2>바시티(Varsity) · JV 팀 트라이아웃 준비</h2>
        <p>국제학교·외국인학교 배구팀 트라이아웃은 짧은 시간 안에 기본기와 포지션 역할을 보여 줘야 합니다.</p>
        <p>하이앤드는 트라이아웃 전에 리시브·토스·서브를 다시 점검하고, 포지션에 맞는 움직임을 개인레슨으로 준비합니다.</p>
        <p>국제학교·외국인학교 배구팀은 시즌마다 트라이아웃으로 선수를 뽑습니다.<br>바시티 팀에 들어가면 학교 대표로 경기에 나설 수 있어,<br>트라이아웃 전에 미리 준비하는 것이 중요합니다.</p>
        <p>트라이아웃까지 남은 시간은 길지 않은 경우가 많습니다.<br>하이앤드는 국가대표·프로 선수의 훈련 방식을 바탕으로,<br>포지션에 꼭 필요한 기술부터 우선순위를 정해 집중해서 준비합니다.</p>
        <ul class="ticks intl-ticks"><li>지금 실력을 먼저 확인하고, 트라이아웃에서 보는 리시브·토스·서브부터 점검</li><li>동작마다 이유를 설명하고 영상으로 함께 확인해 스스로 고칠 수 있게</li><li>1:1 개인레슨으로 포지션에 맞는 움직임을 반복</li></ul>
      </div>
      <div class="intl-box reveal">
        <h2>하이앤드에서 배운 학생들의 학교</h2>
        <ul class="intl-schools">
          <li>서울용산국제학교 (YISS)</li><li>서울외국인학교 (SFS)</li><li>드와이트 외국인학교 (Dwight School Seoul)</li><li>서울국제학교 (SIS)</li>
          <li>한국외국인학교 (KIS)</li><li>세인트폴 서울 (SPPS)</li><li>청라달튼외국인학교 (CDS)</li>
        </ul>
        <p>학교마다 시즌과 팀 구성이 달라, 다니는 학교에 맞춰 준비합니다.</p>
      </div>
    </div>
    <p class="note">방학 단기 집중 레슨 · 캠프 일정과 학교 배구팀 트라이아웃 준비는 상담으로 맞춰 드립니다. 국제학교 학생과 한국 학생이 함께하는 유소년반 수업도 있습니다.</p>
  </div>
</section>'''


def guide_body(r):
    return f'''<section class="sec">
  <div class="wrap">
    <h2>토요일 정규수업 시간표</h2>
    <div class="tbl-wrap"><table class="tbl">
      <caption class="skip">하이앤드 토요일 정규 수업 시간표</caption>
      <thead><tr><th scope="col">토요일</th><th scope="col">수업</th><th scope="col">대상</th><th scope="col">원데이</th></tr></thead>
      <tbody>
        <tr><td>12:00</td><td><a href="{rel(r, 'youth')}">유소년반</a> (80분)</td><td>초등학생</td><td>가능</td></tr>
        <tr><td>13:30</td><td><a href="{rel(r, 'beginner')}">초급반</a> (80분)</td><td>중학생 이상 · 입문</td><td>가능</td></tr>
        <tr><td>16:30</td><td><a href="{rel(r, 'intermediate')}">중급반</a> (80분)</td><td>중학생 이상 · 경력 6개월 이상</td><td>가능</td></tr>
      </tbody>
    </table></div>
    <div class="info">
      <div class="card"><h3 class="t">정규 수강권</h3><p>반과 일정에 맞춰 <a href="{KAKAO_CHAT}" target="_blank" rel="noopener" style="color:var(--blue);font-weight:700">카카오톡 상담</a>으로 안내드립니다.</p></div>
      <div class="card"><h3 class="t">결제</h3><p>원데이는 네이버 예약, 그 밖에는 계좌이체 · 현금 · 카드 모두 가능합니다.</p></div>
    </div>
    <h2 class="mt" id="calendar">수업 일정 달력 · 회원 예약</h2>
    <p>로그인 없이 수업 일정을 확인할 수 있습니다. 예약 · 취소와 수강권 관리는 회원 로그인 후 이용하세요.</p>
    <div class="mt">{CAL_PANEL.replace('CALICON', SN['cal'])}</div>
    <div class="btns"><a class="btn s" href="{r}dashboard.html">회원 로그인 · 수업 예약</a></div>
  </div>
</section>'''


PHOTOS_0820 = ['워밍업 중인 수강생들', '네트 앞에서 수업을 준비하는 수강생들', '리시브 자세를 연습하는 수강생',
               '공을 받으며 리시브 연습', '패스 연습', '토스 연습', '코트 전체를 쓰는 수업', '하이앤드 배너 앞 패스 연습',
               '네트 앞에서 함께 점프하는 수강생들', '혼자 공을 다루는 연습']


PHOTO_DRIVE = 'https://drive.google.com/drive/folders/1XPur9pc9yPQ7SnZm183PMINXb00BF4Ch'


def photos_body(r):
    grid = ''.join(
        f'<a class="ig-item" href="{INSTA}" target="_blank" rel="noopener" aria-label="인스타그램에서 보기: {escape(a)}">{img(r, f"0820-{i + 1:02d}", "하이앤드 토요일 수업: " + a, 1200, 900)}</a>'
        for i, a in enumerate(PHOTOS_0820))
    more = [('class-1', '체육관에서 수강생들이 리시브를 연습하는 토요일 수업 장면', 720, 960),
            ('class-2', '수업을 마친 하이앤드 수강생 단체 사진', 1600, 1200),
            ('class-3', '콘을 두고 리시브 자세를 연습하는 수강생들', 1200, 1600),
            ('class-4', '공 카트 옆에서 패스를 연습하는 청소년 수강생', 1200, 1600),
            ('class-5', '코치 설명을 듣는 어린이 수강생들', 1200, 1600),
            ('class-6', '점프해서 스파이크를 하는 수강생', 1200, 1600)]
    grid += ''.join(
        f'<a class="ig-item" href="{INSTA}" target="_blank" rel="noopener" aria-label="인스타그램에서 보기: {escape(a)}">{img(r, n, a, w, h)}</a>'
        for n, a, w, h in more)
    vids = ''.join(
        f'<div class="reel-slide" data-idx="{i}"><video src="{r}4.%20%EC%88%98%EC%97%85%20%EC%82%AC%EC%A7%84/%EB%8F%99%EC%98%81%EC%83%81/{i + 1}.mp4" loop muted playsinline preload="none" aria-label="하이앤드 수업 영상 {i + 1}"></video><div class="reel-play-layer" id="rpl{i}"><div class="reel-play-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></div></div></div>'
        for i in range(4))
    dots = ''.join(f'<div class="s-dot{" active" if i == 0 else ""}"></div>' for i in range(5))
    # HIGHEND PHOTOS 사진 3장 (드라이브 2026-10-29_홈페이지_클래스사진 → WebP 800px). 파일이 없으면 빈 자리
    alts = ['하이앤드 배구 수업에서 배구공을 잡고 언더핸드 서브를 준비하는 학생',
            '하이앤드 배구 수업에서 웃으며 배구공을 튀기며 이동하는 수강생',
            '하이앤드 유소년 배구 수업에서 코트 위 위치를 손으로 가리키며 확인하는 아이들']
    slots = ''
    for n in range(1, 4):
        f = f'photos-{n}.webp'
        if os.path.exists(os.path.join(ROOT_DIR, 'assets', 'img', f)):
            inner = f'<img src="{r}assets/img/{f}" alt="{alts[n - 1]}" width="800" height="1067" loading="lazy" decoding="async">'
        else:
            inner = f'<div class="hp-empty" aria-hidden="true"><span>사진 {n}</span></div>'
        slots += f'<figure class="hp-card reveal"><a href="{PHOTO_DRIVE}" target="_blank" rel="noopener" aria-label="클래스 사진 {n}: 구글 드라이브에서 지점별 클래스 사진 보기 (새 탭)">{inner}</a></figure>'
    return f'''<section class="sec hp">
  <div class="wrap center">
    <h2 class="hp-title">HIGHEND PHOTOS</h2>
    <p class="hp-desc">하이앤드는 원데이 클래스부터 정규 수업까지 수업 사진을 촬영해 회원 가족과 나누고 있습니다.</p>
    <a class="hp-btn" href="{PHOTO_DRIVE}" target="_blank" rel="noopener">📷 지점별 클래스 사진 보러가기 &gt;</a>
    <div class="hp-grid">{slots}</div>
  </div>
</section>
<section class="sec ig">
  <div class="wrap">
    <div class="ig-head">
      <p class="eyebrow">수업 현장</p>
      <h2 class="ig-title">INSTAGRAM</h2>
      <a class="ig-id" href="{INSTA}" target="_blank" rel="noopener">@highend_volleyball</a>
    </div>
    <div class="ig-grid">{grid}</div>
    <h2 class="mt">수업 영상</h2>
    <div class="reels-section">
      <div class="reels-outer">
        <div class="reels-viewport" id="reelsViewport"><div class="reels-track" id="reelsTrack">{vids}
          <div class="reel-slide reel-slide-cta"><div class="reel-cta-text">더 많은 영상<br>인스타그램에서</div><div class="reel-cta-sub">팔로우하고 최신 수업<br>현장을 확인하세요</div><a href="{INSTA}" target="_blank" rel="noopener" class="reel-cta-btn">@highend_volleyball</a></div>
        </div></div>
        <div class="reels-nav"><button class="reels-arr" id="reelsPrev" aria-label="이전 영상">&#8249;</button><div class="slider-dots" id="reelsDots">{dots}</div><button class="reels-arr" id="reelsNext" aria-label="다음 영상">&#8250;</button></div>
      </div>
    </div>
    <div class="links mt"><a class="chip-link" href="{INSTA}" target="_blank" rel="noopener">{SN['insta']}인스타그램에서 더 보기</a><a class="chip-link" href="{BLOG}" target="_blank" rel="noopener">{SN['blog']}블로그 수업기록</a></div>
  </div>
</section>'''


# ════════════════════════ 본문: Hi : And Day ════════════════════════
HIAND_FAQ = [
    ('배구를 처음 하는 아이도 참여할 수 있나요?', '네. 유소년·초보 클래스가 따로 있어 배구를 처음 배우는 초등학생도 함께할 수 있습니다.'),
    ('누가 참여할 수 있나요?', '정규 수강권을 가진 하이앤드 수강생이 대상입니다. 하이앤드가 처음이라면 원데이 클래스로 수업을 먼저 경험해 보세요.'),
    ('정원은 몇 명인가요?', '클래스당 20명이며, 행사 공지 후 선착순으로 신청받습니다.'),
    ('다음 Hi : And Day는 언제인가요?', '일정이 정해지면 카카오 채널과 인스타그램으로 가장 먼저 알려 드립니다.'),
]
HIAND_PHOTOS = [
    ('hiand-1', 'Hi : And Day 2026.07.25 참가 수강생들과 초청 프로배구 선수·하이앤드 코치진 단체 사진'),
    ('hiand-2', 'Hi : And Day 2026.07.25 초청 프로배구 선수들과 하이앤드 코치진 기념 사진'),
    ('hiand-3', 'Hi : And Day 2026.07.25 유소년·초보 클래스 어린이 수강생들과 선수들의 단체 사진'),
    ('hiand-4', 'Hi : And Day 2026.07.25 초청 선수와 브이 포즈로 기념 촬영하는 어린이 수강생'),
]
HIAND_EVENT = {
    '@type': 'Event', 'name': 'Hi : And Day', 'startDate': '2026-07-25',
    'eventStatus': 'https://schema.org/EventScheduled',
    'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode',
    'description': '국가대표 출신 및 현역 프로배구 선수와 함께하는 하이앤드 발리볼 아카데미의 특별 배구 클래스.',
    'image': [BASE + 'assets/img/hiand-banner.webp'] + [BASE + f'assets/img/{n}.webp' for n, _ in HIAND_PHOTOS],
    'location': {'@type': 'Place', 'name': '하이앤드 발리볼 아카데미',
                 'address': {'@type': 'PostalAddress', 'streetAddress': '상암 인근 · 현천동 180-1', 'addressCountry': 'KR'}},
    'organizer': {'@type': 'Organization', '@id': BASE + '#org', 'name': '하이앤드 발리볼 아카데미', 'url': BASE},
}
HIAND_STEPS = ['수비 · 리시브', '토스', '공격', '서브', '선수와 미니 랠리']


def hiand_body(r):
    steps = ''.join(f'<li class="reveal"><span class="hd-ico" aria-hidden="true">{i + 1}</span><b>{t}</b></li>'
                    for i, t in enumerate(HIAND_STEPS))
    gal = ''.join(f'<figure class="hd-ph reveal"><a href="{INSTA}" target="_blank" rel="noopener" aria-label="인스타그램에서 Hi : And Day 사진 더 보기 (새 탭)">{img(r, n, a, 1200, 801)}</a></figure>' for n, a in HIAND_PHOTOS)
    return f'''<section class="hd-sec sec hd-top">
  <div class="wrap">
    <figure class="hd-banner"><a href="{INSTA}" target="_blank" rel="noopener" aria-label="인스타그램에서 Hi : And Day 소식 보기 (새 탭)">{img(r, 'hiand-banner', 'Hi : And Day 초청 프로배구 선수들과 하이앤드 코치진이 하이앤드 발리볼 아카데미 코트에서 함께한 단체 사진', 1200, 600, lazy=False)}</a></figure>
    <p class="lead center hd-lead">국가대표 출신 및 현역 프로 선수들과 함께하며<br>배구 실전 기술은 물론, 선수들의 훈련 방법과 노하우를<br>가까이에서 배우고 한 단계 더 성장하는 시간을 가져보세요!</p>
    <div class="hd-intro">
      <p>화면 속에서만 보던 선수들의 리시브, 토스, 스파이크를 같은 코트에서 직접 보고 따라 해 봅니다.</p>
      <p>선수들이 어떤 순서로 연습하고, 공 하나를 받을 때 무엇을 생각하며 움직이는지 가까이에서 느낄 수 있습니다.</p>
      <p>평소 하이앤드 수업에서 다져 온 기본기가 실전에서 어떻게 쓰이는지 확인하는 하루입니다.</p>
    </div>
  </div>
</section>
<section class="hd-sec sec alt">
  <div class="wrap hd-narrow">
    <h2>우리 아이의 꿈이 시작되는 하루</h2>
    <p>TV와 경기장에서 응원하던 선수가 바로 내 앞에서 공을 띄워 줍니다.</p>
    <p>좋아하는 선수에게 직접 리시브를 배우고, 함께 랠리를 하고, 사인을 받는 순간.</p>
    <p>배구를 막 시작한 초등학생에게도, 학교 배구부를 준비하는 중학생에게도<br>"나도 배구선수가 되고 싶다"는 꿈이 또렷해지는 경험이 됩니다.</p>
    <p class="hd-callout">Hi : And Day는 하이앤드 수강생이 좋아하는 선수에게 직접 배울 수 있는,<br>하이앤드만의 특별 프로그램입니다.</p>
  </div>
</section>
<section class="hd-sec sec">
  <div class="wrap">
    <h2>왜 프로 선수와 함께 배우나요</h2>
    <div class="grid3 mt">
      <div class="card reveal"><h3 class="t">눈으로 보는 기준</h3><p>프로 선수의 리시브 자세, 스텝, 스윙을 가까이에서 보면<br>내가 연습하는 동작의 완성형이 보입니다.</p></div>
      <div class="card reveal"><h3 class="t">이유를 알고 하는 연습</h3><p>하이앤드 코치진이 선수의 동작을 쉬운 말로 풀어 설명해, 보는 데서 끝나지 않고 내 몸에 적용합니다. 알고 하면 쉬운 배구입니다.</p></div>
      <div class="card reveal"><h3 class="t">꾸준함의 동기</h3><p>다음 Hi : And Day까지 무엇을 연습할지, 아이 스스로 목표가 생깁니다.</p></div>
    </div>
  </div>
</section>
<section class="hd-sec sec alt">
  <div class="wrap">
    <h2>이렇게 진행됩니다</h2>
    <ol class="hd-steps mt">{steps}</ol>
    <p class="center">초청 선수와 하이앤드 코치진이 함께 진행합니다.<br>수업이 끝나면 단체 사진, 사인회, 기념 촬영이 이어집니다.</p>
  </div>
</section>
<section class="hd-sec sec">
  <div class="wrap hd-narrow">
    <h2>매년 이어 갈 하이앤드의 대표 행사</h2>
    <p>하이앤드 배구아카데미는 전·현직 국가대표와 프로배구 선수를 초청하는 Hi : And Day를 매년 이어 갈 대표 행사로 만들어 가고 있습니다.</p>
    <p>배구교실에서 배운 기본기를, 1년에 한 번 꿈꾸던 선수 앞에서 보여 주는 날. 그 하루가 다음 1년의 연습을 이끌어 줍니다.</p>
  </div>
</section>
<section class="hd-sec sec alt">
  <div class="wrap hd-narrow">
    <h2>참여 안내</h2>
    <dl class="hd-info">
      <div><dt>대상</dt><dd>정규 수강권을 가진 하이앤드 수강생</dd></div>
      <div><dt>정원</dt><dd>클래스당 20명</dd></div>
      <div><dt>신청</dt><dd>행사 공지 후 선착순</dd></div>
    </dl>
  </div>
</section>
<section class="hd-sec sec">
  <div class="wrap">
    <h2>지난 Hi : And Day · 2026.07.25 (토)</h2>
    <dl class="hd-info">
      <div><dt>초청 선수</dt><dd>허수봉 · 이시우 · 김지한 · 이승원 · 박주형 · 박준혁</dd></div>
      <div><dt>1부</dt><dd>중학생 이상 (배구 경력 6개월 이상)</dd></div>
      <div><dt>2부</dt><dd>유소년 · 초보 (전 연령)</dd></div>
    </dl>
    <div class="hd-gallery mt">{gal}</div>
  </div>
</section>
<section class="hd-sec sec alt">
  <div class="wrap hd-narrow">
    <h2>자주 묻는 질문</h2>
    {faq_html(HIAND_FAQ, first_open=False)}
  </div>
</section>
<section class="hd-sec sec">
  <div class="wrap hd-narrow">
    <h2>상암·은평·고양에서 배구학원을 찾고 계신다면</h2>
    <p>하이앤드 발리볼 아카데미는 상암 인근 · 현천동 180-1에 있는 프리미엄 배구 아카데미입니다.</p>
    <p>유소년 배구교실, 초·중·고 배구 레슨, 성인 배구, 배구 개인레슨을 운영하며, 국가대표·프로 출신 하이앤드 코치진이 가르칩니다.</p>
    <div class="hd-news reveal">
      <p><strong>다음 Hi : And Day는 추후 공지합니다.</strong><br>카카오 채널을 추가하시면 가장 먼저 소식을 받아보실 수 있습니다.</p>
      <a class="hp-btn" href="{KAKAO}" target="_blank" rel="noopener">카카오 채널 소식받기</a>
    </div>
  </div>
</section>'''



# ════════════════════════ 본문: 국가대표가 찾아가는 배구교실 ════════════════════════
SCHOOL_VISITS = [
    ('2026.07.21', '등촌고등학교', '서울 강서구', 'deungchon'),
    ('2026.07.21', '은평중학교', '서울 은평구', 'eunpyeong'),
    ('2026.08.28', '가재울중학교', '서울 서대문구', 'gajaeul'),
]
SCHOOL_ALTS = {
    'deungchon': ['등촌고등학교 국가대표가 찾아가는 배구교실: 체육관 코트에서 공을 주고받으며 연습하는 학생들',
                  '등촌고등학교 국가대표가 찾아가는 배구교실: 넓은 체육관에서 짝을 지어 패스를 연습하는 학생들'],
    'eunpyeong': ['은평중학교 국가대표가 찾아가는 배구교실: 배구공을 앞에 두고 자세를 배우는 학생들',
                  '은평중학교 국가대표가 찾아가는 배구교실: 체육관에서 서브와 패스를 연습하는 학생들'],
    'gajaeul': ['가재울중학교 국가대표가 찾아가는 배구교실: 배구부 학생들과 함께한 체육관 수업',
                '가재울중학교 국가대표가 찾아가는 배구교실: 네트 앞에서 랠리를 연습하는 학생들'],
}


def school_body(r):
    rows = ''.join(f'<tr><td>{d}</td><td>{n}</td><td>{a}</td></tr>' for d, n, a, _ in SCHOOL_VISITS)
    gal = ''
    for d, n, a, k in SCHOOL_VISITS:
        figs = ''.join(f'<figure class="sc-ph reveal">{img(r, f"school-{k}-{i + 1}", SCHOOL_ALTS[k][i], 1600, 1200)}</figure>' for i in range(2))
        gal += f'<div class="sc-school"><h3>{n} <span>{d} · {a}</span></h3><div class="sc-grid">{figs}</div></div>'
    return f'''<section class="hd-sec sec hd-top">
  <div class="wrap">
    <figure class="hd-banner">{img(r, 'school-main-banner', '국가대표가 찾아가는 배구교실 가재울중학교 단체 사진', 1200, 600, lazy=False)}</figure>
  </div>
  <div class="wrap hd-narrow">
    <p class="lead center hd-lead">배구를 좋아하는 아이들이 더 많아지면 좋겠다는 마음으로,<br>하이앤드 코치진이 학교 체육관을 직접 찾아갑니다.</p>
  </div>
</section>
<section class="hd-sec sec alt">
  <div class="wrap hd-narrow">
    <h2>왜 학교로 찾아가나요</h2>
    <p>배구는 축구나 농구보다 처음 접할 기회가 적은 운동입니다.<br>학교에 공과 네트는 있어도,<br>기본기를 처음부터 제대로 알려 줄 사람을 만나기는 쉽지 않습니다.</p>
    <p>처음 배우는 순간이 가장 중요합니다.<br>그때 생긴 습관이 몇 년이 지나도 몸에 남기 때문입니다.<br>하이앤드가 "만약 내가 16살 때 올바른 방법으로 배구를 배웠더라면"이라는 질문에서 시작한 것도 같은 이유입니다.</p>
    <p>유소년 배구의 저변을 넓히는 일은<br>배구를 먼저 해 본 사람이 해야 할 일이라고 생각합니다.<br>국가대표와 프로 코트에서 배운 것을<br>이제 막 배구를 시작하는 아이들에게 돌려주고 싶습니다.</p>
  </div>
</section>
<section class="hd-sec sec">
  <div class="wrap hd-narrow">
    <h2>배구를 좋아하는 아이가 많아지면</h2>
    <p>배구를 한 번 제대로 경험한 아이는<br>학교스포츠클럽에서, 동네 체육관에서, 다시 공을 찾습니다.<br>그렇게 배구를 즐기는 아이가 많아질수록<br>학교 배구부와 지역 클럽이 살아나고,<br>그 안에서 다음 세대 선수도 자랍니다.</p>
    <p>하이앤드의 꿈은<br>상암과 고양의 아이들이 처음부터 원리를 알고 배구를 배우는 동네를 만드는 것입니다.<br>찾아가는 배구교실은 그 꿈을 학교 체육관에서부터 시작하는 일입니다.</p>
  </div>
</section>
<section class="hd-sec sec alt">
  <div class="wrap">
    <h2>2026년 찾아간 학교</h2>
    <div class="tbl-wrap sc-tbl"><table class="tbl">
      <caption class="skip">2026년 국가대표가 찾아가는 배구교실 학교 목록</caption>
      <thead><tr><th scope="col">날짜</th><th scope="col">학교</th><th scope="col">지역</th></tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
    {gal}
  </div>
</section>
<section class="hd-sec sec">
  <div class="wrap hd-narrow">
    <h2>이렇게 수업합니다</h2>
    <p>하이앤드 정규 수업과 같은 순서로 진행합니다.</p>
    <p>워밍업으로 몸을 준비하고,<br>왜 그렇게 움직이는지 먼저 이야기한 뒤,<br>어떻게 하는지 코치가 몸으로 보여 주고,<br>마지막에는 다 같이 해 봅니다.</p>
    <p>처음 배구공을 만져 보는 학생도<br>학교 배구부·스포츠클럽 학생도 함께할 수 있도록<br>수준에 맞춰 나눠서 지도합니다.</p>
  </div>
</section>
<section class="hd-sec sec alt">
  <div class="wrap hd-narrow">
    <h2>우리 학교에도 와 주실 수 있나요?</h2>
    <p>학교 체육 시간, 방과후, 학교스포츠클럽 수업으로<br>찾아가는 배구교실을 신청하실 수 있습니다.</p>
    <p>일정과 인원을 카카오톡 채널로 남겨 주시면<br>확인 후 안내드리겠습니다.</p>
    <div class="hd-news"><a class="btn k" href="{KAKAO_CHAT}" target="_blank" rel="noopener">{SN['kakao']}카카오톡 상담</a></div>
  </div>
</section>
<section class="hd-sec sec">
  <div class="wrap hd-narrow">
    <h2>서울 서북권 · 고양에서 배구를 찾고 계신다면</h2>
    <p>하이앤드 발리볼 아카데미 상암점은 상암배구, 상암배구학원을 찾는 분들뿐 아니라<br>수색배구, DMC배구, 은평배구, 서대문배구, 마포배구, 강서배구,<br>고양배구, 행신배구, 향동배구, 덕은배구, 창릉배구, 도래울배구, 삼송배구를<br>알아보시는 분들도 찾아오고 있습니다.</p>
    <p>유소년 배구교실부터 배구개인레슨, 성인 배구, 국제학교배구까지<br>수준과 목적에 맞춰 수업합니다.</p>
  </div>
</section>'''



# ════════════════════════ 본문: STORY ════════════════════════
def story_body(r):
    return f'''<section class="sec">
  <div class="wrap">
    <p class="lead">매주 토요일 수업에서 있었던 일을 기록합니다. 네이버 블로그 수업기록과 연결됩니다.</p>
    <div class="links">
      <a class="chip-link" href="{BLOG}" target="_blank" rel="noopener">{SN['blog']}블로그 전체 보기</a>
      <a class="chip-link" href="{NAVER_REVIEW}" target="_blank" rel="noopener">{SN['naver']}네이버 방문자 리뷰</a>
      <a class="chip-link" href="{INSTA}" target="_blank" rel="noopener">{SN['insta']}인스타그램</a>
      <a class="chip-link" href="{YOUTUBE}" target="_blank" rel="noopener">{SN['youtube']}유튜브</a>
    </div>
    <div class="mt" id="gallery">{linkcards(r, [('photos', '수업 사진', '토요일 수업 현장 사진을 모았습니다.', ''), ('class', '클래스 안내', '원데이 · 유소년반 · 초급반 · 중급반 · 개인레슨.', '')])}</div>
  </div>
</section>
<section class="hd-sec sec">
  <div class="wrap hd-narrow">
    <h2>서울 서북권 · 고양에서 배구를 찾고 계신다면</h2>
    <p>하이앤드 발리볼 아카데미 상암점은 상암배구, 상암배구학원을 찾는 분들뿐 아니라<br>수색배구, DMC배구, 은평배구, 서대문배구, 마포배구, 강서배구,<br>고양배구, 행신배구, 향동배구, 덕은배구, 창릉배구, 도래울배구, 삼송배구를<br>알아보시는 분들도 찾아오고 있습니다.</p>
    <p>유소년 배구교실부터 배구개인레슨, 성인 배구, 국제학교배구까지<br>수준과 목적에 맞춰 수업합니다.</p>
  </div>
</section>'''


def soon_body(r):
    return f'''<section class="sec"><div class="wrap center"><p class="lead">준비 중입니다. 소식은 인스타그램과 블로그에서 먼저 전해 드립니다.</p><div class="btns"><a class="btn s" href="{INSTA}" target="_blank" rel="noopener">인스타그램</a><a class="btn s" href="{BLOG}" target="_blank" rel="noopener">블로그</a></div></div></section>'''


# ════════════════════════ 본문: CONTACT ════════════════════════
CONTACT_FAQ = [
    ('서울에서 배구학원을 찾고 있는데, 하이앤드는 어떤 곳인가요?', '하이앤드 발리볼 아카데미는 국가대표·프로 선수의 훈련 방식을 시스템으로 만든 프리미엄 배구아카데미입니다. 국가대표·프로 출신 하이앤드 코치진이 초등학생부터 성인까지 가르치고, 상암 인근 · 현천동 180-1에 있습니다.'),
    ('배구아카데미 수업은 어떤 순서로 진행되나요?', '정규 수업은 매번 MAPS 워밍업 → 왜 → 어떻게 → 해보기(게임) 순서로 진행합니다. 줄 서서 기다리지 않고 모두 동시에 움직이는 훈련이라 공을 만지는 시간이 많습니다.'),
    ('배구레슨 반과 시간은 어떻게 되나요?', '토요일 정규 수업은 80분이며 유소년반(초등학생) 12:00, 초급반(중학생 이상 입문) 13:30, 중급반(중학생 이상, 경력 6개월 이상) 16:30입니다. 평일 반은 4명 이상 모이면 개설하고, 1:1 개인레슨은 따로 시간을 맞춰 드립니다.'),
    ('배구학원 수강료와 결제는 어떻게 하나요?', '원데이 클래스 금액과 일정은 네이버 예약에서 확인하실 수 있고, 개인레슨은 60분 1회 25만 원(10회 등록 시 회당 20만 원)입니다. 정규 수강권은 카카오톡 상담으로 안내드리며, 결제는 계좌이체 · 현금 · 카드 모두 가능합니다.'),
    ('처음 배구레슨을 받을 때 무엇을 준비하나요?', '실내 운동화, 물, 편한 운동복을 준비하시고 수업 시작 10분 전까지 와 주세요. 처음이라면 원데이 클래스(네이버 예약)로 시작하시고, 정규 수업을 등록하시면 원데이 비용을 차감해 드립니다.'),
    ('서울배구학원을 찾는데 어느 지역에서 다니기 좋나요?', '상암 인근 · 현천동 180-1에 있어 상암·수색·DMC·은평·서대문·마포와 고양(덕양구·일산·향동·덕은·행신·도래울·창릉)에서 오기 좋습니다. 건물 앞 주차가 가능합니다.'),
    ('하이앤드 코치는 누구인가요?', '국가대표·프로 출신 하이앤드 코치진이 가르칩니다. 헤드코치 김재휘는 국가대표 7년(2016~2022) · 프로(V리그) 10년, 선수 17년 경력에 2018 아시안게임 은메달, V리그 우승 4회, FIVB 코치 레벨1, 전문스포츠지도사 2급(배구) 자격이 있습니다.'),
    ('형제가 함께 다녀도 되나요?', '네. 형제는 모든 수강권을 함께 나눠 쓸 수 있습니다.'),
    ('키가 작아도 배구를 할 수 있나요?', '네. 배구에는 리시브와 수비를 맡는 리베로 같은 포지션이 있습니다. 하이앤드 황준태 코치도 리베로로, 대통령배 배구대회 리베로상을 두 번 받았습니다. 키가 작아도 시작할 수 있고, 몸 방향과 발 쓰는 법을 익히면 도움이 됩니다.'),
    ('배구 전에 스트레칭은 어떻게 하나요?', '하이앤드 수업은 매번 MAPS 워밍업으로 시작합니다. 국가대표·프로 선수 경험을 바탕으로 하이앤드가 만든 워밍업으로, Mobility · Activation · Plyometrics · Stability 순서로 몸을 깨웁니다. 안전하게 오래 하는 배구를 위해 몸 준비부터 가르칩니다.'),
]
# 클래스 페이지별 자주 묻는 질문 (답이 None이면 대표 확인 전이라 싣지 않음)
CLASS_FAQ = {
    'youth': [
        ('초등학생 운동으로 배구를 시작해도 괜찮을까요?', '네. 하이앤드 유소년반은 초등학생 대상 토요일 12:00, 80분 정규수업입니다. MAPS 워밍업으로 몸을 준비한 뒤 왜 → 어떻게 → 해보기(게임) 순서로, 줄 서서 기다리지 않고 모두 함께 움직이며 배웁니다. 처음이라면 원데이 클래스(네이버 예약)로 먼저 경험해 보세요. 초등학생운동으로 배구를 고민하신다면 원데이 클래스로 먼저 경험해 보세요.'),
        ('배구가 키 크는 운동에 도움이 되나요?', '배구는 점프와 전신을 함께 쓰는 운동이라 성장기 아이들이 즐겁게 몸을 쓰기 좋습니다. 다만 키 성장은 사람마다 다릅니다. 하이앤드는 MAPS 워밍업으로 몸을 먼저 준비해 안전하게 오래 하는 배구를 가르칩니다. 키크는운동을 찾으신다면, 아이가 즐겁고 꾸준하게 할 수 있는 운동인지가 가장 중요합니다.'),
        ('유소년 배구는 몇 살부터 배울 수 있나요?', '5세 이상 유아부터 배울 수 있습니다. 유아와 초등 저학년도 유소년반에서 눈높이에 맞춰 수업합니다. 처음이라면 원데이 클래스(네이버 예약)로 먼저 경험해 보세요.'),
        ('아이가 배구 규칙을 몰라도 되나요?', '괜찮습니다. 수업 마지막은 매번 게임으로 마무리해서, 배운 동작을 게임에서 써 보며 규칙을 접합니다.'),
        ('무릎보호대가 꼭 필요한가요?', '성장기 아이들에게는 무릎보호대를 필수로 권합니다. 바닥에서 공을 받는 동작이 많아 무릎을 보호하는 것이 좋습니다.'),
    ],
    'beginner': [
        ('중학생이 처음 배구를 배워도 되나요?', '네. 초급반은 배구를 처음 배우는 중학생 이상을 위한 토요일 13:30, 80분 정규수업입니다. 패스 · 서브 · 리시브 기본기를 왜 그렇게 움직이는지부터 이해하며 익힙니다. 중학생운동, 중등배구를 처음 시작하는 학생도 기본기부터 차근차근 배웁니다.'),
        ('공이 무서운 완전 초보도 괜찮을까요?', '네. 처음 배우는 분은 초급반(중학생 이상), 초등학생은 유소년반에서 시작합니다. 왜 이렇게 움직이는지 이유부터 쉽게 설명하고, 코치가 몸으로 먼저 보여 드립니다. 처음이라면 원데이 클래스로 수업 분위기를 먼저 경험해 보세요.'),
        ('취미로 배구를 처음 시작해도 괜찮을까요?', '네. 성인도 초급반에서 처음부터 배울 수 있고, 혼자 오셔도 괜찮습니다. 동호회에 들어가기 전에 기본기를 다지고 싶은 분도 이 반에서 시작합니다. 국가대표·프로 출신 하이앤드 코치진이 동작마다 이유를 설명하고 몸으로 보여 줍니다. 처음이라면 원데이 클래스(네이버 예약)로 실제 수업을 먼저 경험해 보세요. 취미배구를 처음 시작하는 성인에게도 맞는 수업입니다.'),
    ],
    'intermediate': [
        ('배구를 조금 해 봤는데 어느 반이 맞나요?', '중학생 이상이고 배구 경력이 6개월 이상이면 중급반(토요일 16:30, 80분)이 맞습니다. 경력이 그보다 짧거나 기본기를 처음부터 다지고 싶다면 초급반(토요일 13:30)을 권합니다. 어느 반이 맞을지 모르겠다면 카카오톡으로 상담해 주세요.'),
        ('배구교실과 배구학원 수업은 무엇이 다른가요?', '이름보다 수업 방식이 중요합니다. 하이앤드는 정규 수업마다 MAPS 워밍업 → 왜 → 어떻게 → 해보기(게임) 순서로 진행하고, 줄 서서 기다리지 않고 모두 동시에 움직이는 훈련을 합니다. 국가대표·프로 출신 하이앤드 코치진이 이유를 알고 하는 반복으로 기본기를 만듭니다. 학원을 고를 때는 코치 경력, 기다리는 시간 없이 모두 움직이는지, 동작마다 이유를 설명해 주는지 보시고, 원데이 클래스로 직접 경험해 보세요.'),
    ],
    'competition': [
        ('대회에 나가고 싶은 중·고등학생도 배울 수 있나요?', '네. 시합반은 U15(13세 이상) · U18(16세 이상) 연령별 대표팀 선발과 대회를 목표로 한 반입니다. 수업 시간과 구성은 카카오톡 상담으로 맞춰 드립니다.'),
        ('시합반은 어떤 훈련을 하나요?', '6인제 실전 훈련을 중심으로 경기 리딩, 상황 판단, 팀 전술을 익힙니다. 하이앤드 코치진이 국가대표와 V리그에서 경험한 팀 시스템을 쉬운 말로 풀어, 왜 그 자리에 서야 하는지부터 이해하게 합니다.'),
    ],
    'team': [
        ('배구동호회 팀 단위로 배구레슨을 받을 수 있나요?', '네. 하이앤드 팀클래스는 배구동호회처럼 한 팀이 함께 배우는 주 1회 정기 수업입니다. 6인제와 9인제 모두 가능하고, 팀의 인원과 목표에 맞춰 수업합니다. 수강료와 일정은 카카오톡 상담으로 안내드립니다.'),
        ('초보만 있는 동호회도 배울 수 있나요?', '네. 첫 수업에서 팀원 한 명 한 명의 레벨을 진단하고, 패스와 리시브 같은 기본기부터 시작합니다. 동작마다 이유를 먼저 설명하기 때문에 처음 배구를 하는 사람도 따라올 수 있습니다.'),
        ('몇 명부터 팀클래스를 신청할 수 있나요?', '팀의 인원과 목표에 따라 수업 구성이 달라져, 카카오톡 상담으로 맞춰 안내드립니다.'),
        ('6인제와 9인제 중 어떤 방식으로 수업하나요?', '팀이 실제로 하는 경기 방식에 맞춥니다. 동호회 대회가 9인제라면 9인제 포지션과 로테이션으로, 6인제라면 6인제로 연습합니다.'),
        ('학교 배구부나 방과후 수업도 가능한가요?', '네. 학교 배구부, 방과후, 학교스포츠클럽 수업과 선생님 연수를 진행할 수 있습니다. 2026년에는 국가대표가 찾아가는 배구교실로 가재울중 · 등촌고 · 은평중에서 수업했습니다.'),
        ('회사 사내 동호회나 팀워크 활동으로도 할 수 있나요?', '네. 회사 동호회와 단체 수업도 팀클래스로 진행합니다. 처음 배구를 하는 사람도 함께할 수 있게 수준에 맞춰 나눠서 지도하고, 마지막은 함께하는 게임으로 마무리합니다.'),
        ('해외 학교 배구부의 단기 캠프도 가능한가요?', '네. 국제학교와 해외 학교 배구부의 단기 캠프를 상담할 수 있습니다. 레벨 진단부터 팀 플레이까지 기간에 맞춰 구성하고, 진행 언어와 일정은 미리 협의합니다.'),
        ('팀클래스는 어디에서 수업하나요?', '하이앤드 상암점(상암 인근 · 현천동 180-1)의 200평 풀코트 체육관에서 진행합니다. 건물 앞 주차가 가능합니다. 수업 장소는 팀 상황에 따라 상담으로 정합니다.'),
        ('함께 배구할 사람들을 만날 수 있나요?', '팀클래스에서는 같은 팀이 한 주에 한 번 함께 배웁니다. 또 하이앤드 수강생이 함께하는 행사 Hi : And Day에서 국가대표 출신 · 현역 프로 선수들과 함께 배구를 경험할 수 있습니다.'),
    ],
    'private': [
        ('배구 개인레슨은 어떻게 진행되나요?', '1:1 개인레슨은 60분 동안 코치가 한 사람만 봅니다. 서브 · 리시브 · 토스 · 스파이크 · 블로킹까지, 배우고 싶은 기술을 골라 배울 수 있습니다. 지금 실력을 확인하고, 약점을 영상으로 함께 보며 교정합니다. 1회 25만 원, 10회 등록 시 회당 20만 원입니다.'),
        ('짧은 기간에 집중해서 배구레슨을 받을 수 있나요?', '네. 1:1 개인레슨은 코치가 한 사람에게만 집중하는 수업입니다. 수업 중 동작을 영상으로 촬영해 함께 보며 교정하고, 원하시는 기간과 횟수에 맞춰 일정을 잡아 드립니다.'),
        ('학교 배구 수행평가도 준비할 수 있나요?', '네. 언더토스 · 오버토스 · 서브처럼 수행평가에 나오는 동작을, 이유부터 이해하고 반복으로 몸에 익힙니다. 동작마다 이유를 알고 하니까, 수행평가 기술도 쉽게 익힙니다. 학교마다 종목이 다를 수 있어, 상담으로 먼저 확인해 드립니다. 1:1 개인레슨에서는 시험에 나오는 기술만 골라 연습할 수 있습니다.'),
        ('혼자 영상 보고 연습하다가 와도 되나요?', '네. 먼저 지금 실력을 확인하고 맞는 반을 안내해 드립니다. 고치고 싶은 동작이 분명하다면, 1:1 개인레슨에서 영상으로 함께 보며 교정할 수 있습니다.'),
    ],
    'elite': [
        ('몇 학년부터 들을 수 있나요?', '초등 4학년부터 고등학생까지 들을 수 있습니다. 상담과 레벨 진단 후 시작합니다.'),
        ('배구를 늦게 시작했는데 괜찮을까요?', '하이앤드 헤드코치도 16살에 배구를 시작했습니다. 지금 실력을 먼저 진단하고, 기본기부터 준비할 순서를 정합니다. 가능성을 약속하지 않고, 이유를 알고 하는 반복으로 차근차근 쌓아 갑니다.'),
        ('키가 작아도 선수를 준비할 수 있나요?', '포지션마다 필요한 기술이 다릅니다. 리시브와 수비를 맡는 리베로처럼, 몸에 맞는 포지션 기술을 익힙니다. 하이앤드 황준태 코치도 리베로로 대통령배 배구대회 리베로상을 두 번 받았습니다. 가능 여부는 약속하지 않고, 지금 단계를 진단한 뒤 방향을 정합니다.'),
        ('스포츠클럽에서 하다가 엘리트를 준비해도 되나요?', '즐기는 배구와 선수를 목표로 하는 배구는 준비가 다릅니다. 지금 단계를 진단하고, 어느 길이 맞을지 상담에서 함께 정합니다.'),
        ('배구부 입단 테스트를 준비할 수 있나요?', '네. 테스트는 학교마다 다를 수 있어, 상담 후 리시브 · 토스 · 서브 같은 기본기와 포지션 움직임을 먼저 점검합니다. 필요하면 1:1 개인레슨으로 반복합니다.'),
        ('수업 시간과 수강료는 어떻게 되나요?', '수업 시간과 수강료는 카카오톡 상담으로 안내드립니다.'),
        ('성장기 아이도 괜찮을까요?', '수업은 매번 MAPS 워밍업으로 시작해 점프와 착지부터 가르칩니다. 성장기 아이들에게는 무릎보호대 착용을 꼭 권합니다.'),
    ],
    'intl': [
        ('국제학교 학생도 서울에서 배구학원을 다닐 수 있나요?', '네. 국제학교 · 외국인학교 학생과 방학마다 한국을 찾는 해외 거주 학생도 상암 인근 · 현천동 180-1의 하이앤드에서 배웁니다. 해외 학교에서 쓰는 영어 배구 용어를 함께 쓰고, 1:1 개인레슨과 방학 단기 집중 레슨을 상담으로 맞춰 드립니다.'),
        ('학교 배구팀 트라이아웃을 준비할 수 있나요?', '트라이아웃은 학교 배구팀이 선수를 뽑는 선발 테스트입니다. 네. 바시티(Varsity) · JV 팀 트라이아웃 전에 리시브 · 토스 · 서브를 먼저 점검하고, 포지션에 맞는 움직임을 1:1 개인레슨으로 반복합니다. 동작마다 이유를 설명하고 영상으로 함께 확인해 스스로 고칠 수 있게 돕습니다.'),
    ],
}


def class_faq(key):
    return [(q, a) for q, a in CLASS_FAQ.get(key, []) if a]


def with_faq(key, body):
    """클래스 페이지 본문 아래에 '자주 묻는 질문' 칸 붙이기"""
    def wrapped(r):
        faqs = class_faq(key)
        if not faqs:
            return body(r)
        return body(r) + f'''
<section class="sec sec-tight" id="faq">
  <div class="wrap hd-narrow">
    <h2>자주 묻는 질문</h2>
    {faq_html(faqs, first_open=False)}
    <p class="faq-more"><a href="{rel(r, 'faq')}">전체 자주 묻는 질문 보기 →</a></p>
  </div>
</section>'''
    return wrapped

LOCAL_FAQ = [
    ('상암·은평·고양 근처에 배구학원이 있나요?', '상암 인근 · 현천동 180-1에 프리미엄 배구 아카데미 하이앤드가 있습니다. 매주 토요일 유소년반(12:00), 초급반(13:30), 중급반(16:30) 수업을 하고, 개인레슨은 따로 예약합니다.'),
    ('국가대표 출신 코치에게 배울 수 있나요?', '네. 하이앤드는 국가대표·프로 출신 코치진이 가르칩니다. 헤드코치 김재휘(국가대표 7년 · 프로(V리그) 10년)는 2018 아시안게임 은메달, V리그 우승 4회 경력과 FIVB 코치 레벨1 자격이 있습니다.'),
    ('초등학생 배구교실도 있나요?', '네. 유소년반(초등학생)은 토요일 12:00, 80분 수업입니다. 처음 배우는 초등학생도 원데이 클래스로 시작할 수 있습니다.'),
    ('배구학원 비용은 얼마인가요?', '원데이 클래스 금액과 일정은 네이버 예약에서 확인하실 수 있습니다. 개인레슨은 1회 25만 원(10회 등록 시 회당 20만 원)입니다. 정규 수강권은 카카오톡 상담으로 안내드립니다.'),
    ('주차할 수 있나요?', '건물 앞에 주차할 수 있습니다.'),
]


def map_block(root=''):
    return f'''{naver_map_img(root)}
      {MAP_BTNS}'''


def contact_body(r):
    return f'''<section class="sec" id="map">
  <div class="wrap">
    <div class="contact-grid">
      <div class="reveal">{map_block(r)}</div>
      <div class="card reveal">
        <h2 class="t">{NAME}</h2>
        <dl class="facts">
          <dt>주소</dt><dd>{ADDR}</dd>
          <dt>주차</dt><dd>건물 앞 주차 가능</dd>
          <dt>운영</dt><dd>정규수업 매주 토요일 12:00 · 13:30 · 16:30<br>(개인레슨은 별도 예약)</dd>
          <dt>전화</dt><dd><a href="tel:01044631177">{PHONE}</a></dd>
        </dl>
      </div>
    </div>
  </div>
</section>
<section class="sec alt">
  <div class="wrap">
    {linkcards(r, [('faq', '자주 묻는 질문', '수업 시간, 수강료, 준비물, 주차, 결제.', 'faq'),
                   ('ask', '상담하기', '카카오톡 · 전화 · 인스타그램 · 이메일.', 'ask'),
                   ('local', '상암·은평·고양 배구학원', '가까운 곳에서 만나는 프리미엄 배구 아카데미.', '')])}
  </div>
</section>'''


def faq_body(r):
    links = ''.join(f'<a href="{rel(r, k)}#faq">{escape(PAGES[k]["crumb"])}</a>' for k in CLASS_FAQ if class_faq(k))
    return f'''<section class="sec"><div class="wrap">{faq_html(CONTACT_FAQ)}
  <h2 class="cgrp">반별 자주 묻는 질문</h2>
  <div class="faq-links">{links}</div>
  <div class="btns">{go(r, 'ask', '더 궁금한 점 문의하기')}</div></div></section>'''


def ask_body(r):
    return f'''<section class="sec">
  <div class="wrap">
    <div class="ask">
      <a href="{KAKAO}" target="_blank" rel="noopener"><div class="ic kakao">{SN['kakao']}</div><h2 class="t">카카오톡 채널</h2><p>나이(학년) · 배구 경력 · 가능한 요일을 남겨 주세요</p></a>
      <a href="tel:01044631177"><div class="ic phone">{SN['phone']}</div><h2 class="t">전화</h2><p>{PHONE}</p></a>
      <a href="{INSTA}" target="_blank" rel="noopener"><div class="ic insta">{SN['insta']}</div><h2 class="t">인스타그램 DM</h2><p>@highend_volleyball</p></a>
      <a href="mailto:{EMAIL}"><div class="ic mail">{SN['mail']}</div><h2 class="t">이메일</h2><p>{EMAIL}</p></a>
    </div>
    <div class="kakao-banner reveal"><div><div class="kb-title">궁금한 점이 있으신가요?</div><div class="kb-sub">카카오톡으로 메시지 남겨 주시면 확인 후 답변드립니다</div></div><a href="{KAKAO_CHAT}" target="_blank" rel="noopener" class="kb-btn">{SN['kakao']}1:1 채팅하기</a></div>
  </div>
</section>'''


def local_body(r):
    return f'''<section class="sec">
  <div class="wrap">
    <p class="lead">상암 인근 · 현천동 180-1의 프리미엄 배구 아카데미 하이앤드입니다. 국가대표·프로 선수의 훈련 방식을 시스템으로 만들었고, 국가대표·프로 출신 코치진이 초등학생부터 성인까지 배구를 가르칩니다.</p>
    {linkcards(r, [('coaches', '국가대표·프로 출신 코치진', '헤드코치 국가대표 7년 · 프로(V리그) 10년. 아시안게임 은메달, V리그 우승 4회.', ''),
                   ('method', '알고 하면 쉬운 배구', 'Why ? → How ? → Play ! 이유를 알고 하는 반복으로 기본기를 만듭니다.', ''),
                   ('oneday', '원데이 클래스', '처음이라면 · 정규 수업 그대로 체험. 토요일 12:00 · 13:30 · 16:30, 네이버 예약.', '')])}
  </div>
</section>
<section class="sec alt">
  <div class="wrap">
    <h2>서울 서북권 · 고양에서 배구를 찾고 계신다면</h2>
    <p>하이앤드 발리볼 아카데미 상암점은 상암배구, 상암배구학원을 찾는 분들뿐 아니라<br>수색배구, DMC배구, 은평배구, 서대문배구, 마포배구, 강서배구,<br>고양배구, 행신배구, 향동배구, 덕은배구, 창릉배구, 도래울배구, 삼송배구를<br>알아보시는 분들도 찾아오고 있습니다.</p>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <h2>상암·고양 배구학원, 자주 묻는 질문</h2>
    {faq_html(LOCAL_FAQ)}
  </div>
</section>'''


def notfound_body(r):
    return f'''<section class="sec"><div class="wrap center"><div class="btns"><a class="btn p" href="{BASE}">홈으로</a><a class="btn s" href="{url('class')}">클래스 안내</a><a class="btn s" href="{url('contact')}">오시는 길</a></div></div></section>'''


# ════════════════════════ 페이지별 구조화 데이터 ════════════════════════
KIM = {'@type': 'Person', '@id': url('coaches') + '#kim', 'name': '김재휘', 'jobTitle': '헤드코치', 'url': url('coaches') + '#kim',
       'description': '하이앤드 발리볼 아카데미 대표 · 헤드코치(포지션 센터). ' + CAREER + '.',
       'image': BASE + 'assets/img/coach-kim-profile.webp', 'worksFor': {'@id': BASE + '#org'}, 'nationality': 'KR',
       'award': ['2018 자카르타·팔렘방 아시안게임 은메달', 'V리그 우승 4회 (2015~2016 정규리그, 2016~2017 챔피언결정전, 2017~2018 정규리그, 2018~2019 챔피언결정전)'],
       'hasCredential': [{'@type': 'EducationalOccupationalCredential', 'name': 'FIVB(국제배구연맹) 코치 레벨1'},
                         {'@type': 'EducationalOccupationalCredential', 'name': '전문스포츠지도사 2급 (배구)'}],
       'knowsAbout': ['배구', '배구 기본기', '배구 자세 교정']}
HWANG = {'@type': 'Person', '@id': url('coaches') + '#hwang', 'name': '황준태', 'jobTitle': '코치', 'url': url('coaches') + '#hwang',
         'description': '하이앤드 발리볼 아카데미 코치(포지션 리베로). 서울 우리카드 배구단(2022~2024).',
         'image': BASE + 'assets/img/coach-hwang-profile.jpg', 'worksFor': {'@id': BASE + '#org'},
         'award': ['제50회 대통령배 배구대회 리베로상', '제52회 대통령배 배구대회 리베로상'],
         'alumniOf': [{'@type': 'EducationalOrganization', 'name': '경북사대부고'},
                      {'@type': 'CollegeOrUniversity', 'name': '한양대학교'}]}


def course(key, name, desc, times, offer=None):
    c = {'@type': 'Course', '@id': url(key) + '#course', 'name': name, 'description': desc, 'url': url(key),
         'provider': {'@id': BASE + '#org'}, 'inLanguage': 'ko',
         'hasCourseInstance': [{'@type': 'CourseInstance', 'courseMode': 'Onsite', 'location': {'@id': BASE + '#place'},
                                'courseSchedule': {'@type': 'Schedule', 'byDay': 'https://schema.org/Saturday',
                                                   'startTime': t, 'duration': 'PT80M', 'repeatFrequency': 'P1W'}} for t in times]}
    if offer:
        c['offers'] = offer
    return c


ONEDAY = course('oneday', '배구 원데이 클래스',
                '처음 배구를 하는 초등학생부터 성인까지 정규 수업에 그대로 함께하는 하루 수업. MAPS 워밍업, 원리 이해, 정밀 교정, 게임 순서로 진행합니다.',
                ('12:00', '13:30', '16:30'),
                {'@type': 'Offer', 'url': NAVER_BOOK, 'availability': 'https://schema.org/InStock'})
YOUTH = course('youth', '유소년 배구교실 (유소년반)', '초등학생 대상 80분 정규수업. 바른 자세와 기본기를 처음부터 제대로 익힙니다.', ('12:00',))
BEGINNER = course('beginner', '배구 초급반', '중학생 이상, 배구를 처음 배우는 분을 위한 80분 정규수업.', ('13:30',))
INTER = course('intermediate', '배구 중급반', '중학생 이상, 배구 경력 6개월 이상을 위한 80분 정규수업.', ('16:30',))
PRIVATE = {'@type': 'Service', '@id': url('private') + '#service', 'name': '배구 1:1 개인레슨 (60분)', 'url': url('private'),
           'provider': {'@id': BASE + '#org'}, 'areaServed': '상암 인근',
           'offers': [{'@type': 'Offer', 'name': '1회 (60분)', 'price': '250000', 'priceCurrency': 'KRW'},
                      {'@type': 'Offer', 'name': '10회 등록 (회당)', 'price': '200000', 'priceCurrency': 'KRW'}]}

FIREBASE = ['https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js',
            'https://www.gstatic.com/firebasejs/10.7.1/firebase-database-compat.js']

# 페이지키: (본문, 구조화 데이터, 스크립트)
BUILD = {
    'about': (about_body, [], []), 'coaches': (coaches_body, [KIM, HWANG], []),
    'facility': (facility_body, [], []),
    'method': (method_body, [], []), 'maps': (maps_body, [], []), 'correction': (correction_body, [], []),
    'flow': (flow_body, [], []), 'level': (level_body, [], []),
    'class': (class_body, [ONEDAY, YOUTH, BEGINNER, INTER, PRIVATE], []), 'oneday': (oneday_body, [ONEDAY], []),
    'oneday-apply': (apply_body, [], []), 'oneday-reviews': (reviews_body, [], []),
    'youth': (with_faq('youth', youth_body), [YOUTH] + ([faq_ld(class_faq('youth'))] if class_faq('youth') else []), []), 'beginner': (with_faq('beginner', beginner_body), [BEGINNER] + ([faq_ld(class_faq('beginner'))] if class_faq('beginner') else []), []), 'intermediate': (with_faq('intermediate', intermediate_body), [INTER] + ([faq_ld(class_faq('intermediate'))] if class_faq('intermediate') else []), []),
    'regular-reviews': (reviews_body, [], []), 'competition': (with_faq('competition', competition_body), [] + ([faq_ld(class_faq('competition'))] if class_faq('competition') else []), []), 'team': (with_faq('team', team_body), [] + ([faq_ld(class_faq('team'))] if class_faq('team') else []), []), 'private': (with_faq('private', private_body), [PRIVATE] + ([faq_ld(class_faq('private'))] if class_faq('private') else []), []), 'elite': (lambda r: with_faq('elite', elite_body)(r) + elite_dream(r), [] + ([faq_ld(class_faq('elite'))] if class_faq('elite') else []), []), 'intl': (with_faq('intl', intl_body), [] + ([faq_ld(class_faq('intl'))] if class_faq('intl') else []), []),
    'guide': (guide_body, [], FIREBASE + ['assets/js/schedule.js']), 'photos': (photos_body, [], ['assets/js/media.js']),
    'story': (story_body, [], []), 'hiand': (hiand_body, [faq_ld(HIAND_FAQ), HIAND_EVENT], []), 'school': (school_body, [], []), 'note': (soon_body, [], []),
    'contact': (contact_body, [], []), 'local': (local_body, [faq_ld(LOCAL_FAQ)], []), 'faq': (faq_body, [faq_ld(CONTACT_FAQ)], []),
    'ask': (ask_body, [], []),
}


# ── 읽기 쉬운 줄바꿈 (대표 지시 2026-10-29, 직원지식/공통_홈페이지글_줄바꿈규칙.md) ──
SENT_END = re.compile(r'([가-힣)]\.|(?<=\S)[!?])[ \t]+(?=[^\s→])')  # "왜? → 어떻게?"처럼 화살표가 이어지면 문장 끝이 아님
CLAUSE = re.compile(r'([가-힣]{1,6}(?:지|고|해|면|며|서|데|도|만|게|니),)[ \t]+')


def _brk_sentences(inner):
    return SENT_END.sub(lambda m: m.group(1) + ' <br>', inner)


CONNECT = set('고며서면지해데니게도만요다')


def _brk_long(part):
    """긴 한 문장(34자 넘음)은 쉼표에서 끊는다.
    1순위: '~하고, ~하며, ~해서,' 같은 이어지는 말 뒤 / 2순위(45자 넘는데 1순위가 없을 때): 가운데에 가까운 쉼표"""
    toks = re.split(r'(<[^>]+>)', part)
    text = ''.join(t for t in toks if not t.startswith('<'))
    if len(text) <= 34 or ', ' not in text:
        return part
    depth, commas = 0, []
    for i, ch in enumerate(text):       # 괄호 안 쉼표에서는 끊지 않음
        depth += (ch == '(') - (ch == ')')
        if ch == ',' and depth == 0 and text[i + 1:i + 2] == ' ':
            commas.append(i)
    picks, last = [], 0
    for c in commas:
        if text[c - 1] in CONNECT and c + 1 - last >= 14 and len(text) - (c + 2) >= 12:
            picks.append(c); last = c + 2
    if not picks and len(text) > 44:
        ok = [c for c in commas if c >= 14 and len(text) - c >= 14]
        if ok:
            picks = [min(ok, key=lambda c: abs(c - len(text) / 2))]
    if not picks:
        return part
    cut = {c + 1 for c in picks}    # 쉼표 다음 공백 자리를 줄바꿈으로
    out, k = [], 0
    for t in toks:
        if t.startswith('<'):
            out.append(t)
            continue
        seg = []
        for ch in t:
            seg.append(' <br>' if k in cut else ch)
            k += 1
        out.append(''.join(seg))
    return ''.join(out)


# 쉼표 없는 긴 문장: 뜻이 나뉘는 자리에서 줄바꿈 ("앞|뒤" → "앞<br>뒤")
MANUAL_BREAKS = [
    '훈련 방식을|시스템으로 만든', 'Hi : And Day를|매년 이어 갈', '움직이도록|몸을 준비하는', '몸을|어릴 때부터',
    '정규 수업까지|수업 사진을', '아카데미는|상암 인근 · 현천동 180-1에 있는', '기본기가|실전에서 어떻게',
    '16:30 중|원하시는 시간을', '캠프 일정과|학교 배구팀', 'Serve.|해외 학교와', '갔는지"|스스로 알아차리는',
    '의존하지 않고|국제 기준의', '따로 있어|배구를 처음', '단체 레슨은|인원과 목표에', '하이앤드 코치진은|먼저 묻고',
    '기록하던 습관을|하이앤드 운동일지로', '학생과|방학마다 한국을', '6대6 경기를 하며|대회를 준비합니다',
]


def _soft(html_part):
    """문장 중간 줄바꿈은 <br class="bk"> (휴대폰처럼 좁은 화면에서는 숨겨 자연스럽게 이어 씀)"""
    parts = re.split(r'<br\s*/?>', html_part)
    out = parts[0]
    for nxt in parts[1:]:
        prev = re.sub(r'<[^>]+>', '', out).rstrip()
        if prev[-1:] in '.!?…':
            out += '<br>' + nxt
        else:
            out += ('' if out.endswith(' ') else ' ') + '<br class="bk">' + nxt
    return out


def _brk(inner):
    out = '<br>'.join(_brk_long(x) for x in _brk_sentences(inner).split('<br>'))
    for pair in MANUAL_BREAKS:
        a, b = pair.split('|')
        out = out.replace(f'{a} {b}', f'{a} <br>{b}')
    return _soft(out)


def readable(html_text):
    """문단(p) 안에서 문장이 끝나면 다음 줄로. 좁은 카드 안에서는 쉼표에서도 끊는다.
    script·style·head와 첫 화면(hero) 문단은 건드리지 않는다."""
    head_end = html_text.find('</head>')
    if head_end < 0:
        return html_text
    head_part, body = html_text[:head_end], html_text[head_end:]
    keep = []
    body = re.sub(r'<(script|style)\b.*?</\1>', lambda m: keep.append(m.group(0)) or f'\x00{len(keep) - 1}\x00', body, flags=re.S)

    def para(m):
        attrs, inner = m.group(1) or '', m.group(2)
        if 'hero' in attrs:
            return m.group(0)
        return f'<p{attrs}>{_brk(inner)}</p>'
    body = re.sub(r'<p(\s[^>]*)?>(.*?)</p>', para, body, flags=re.S)
    body = re.sub(r'(<div class="curr-desc">)(.*?)(</div>)', lambda m: m.group(1) + _brk(m.group(2)) + m.group(3), body, flags=re.S)
    body = re.sub(r'\x00(\d+)\x00', lambda m: keep[int(m.group(1))], body)
    return head_part + body


def write(path, text):
    if path.endswith('.html'):
        text = readable(text)
    full = os.path.join(ROOT_DIR, path)
    os.makedirs(os.path.dirname(full) or ROOT_DIR, exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(text)


def build():
    write('index.html', home_legacy())
    for key, (body, extra, scripts) in BUILD.items():
        write(PAGES[key]['path'] + 'index.html', page(key, body, extra, scripts))
    write('404.html', page('notfound', notfound_body, root=BASE))

    # robots.txt
    bots = ['Googlebot', 'Yeti', 'Bingbot', 'GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot',
            'Claude-User', 'PerplexityBot', 'Google-Extended']
    rb = 'User-agent: *\nAllow: /\nDisallow: /dashboard.html\nDisallow: /admin.html\n\n'
    rb += '\n'.join(f'User-agent: {b}\nAllow: /\nDisallow: /dashboard.html\nDisallow: /admin.html' for b in bots)
    rb += f'\n\nSitemap: {BASE}sitemap.xml\n'
    write('robots.txt', rb)

    # sitemap.xml (숨긴 페이지 제외)
    pri = {'home': '1.0', 'class': '0.9', 'oneday': '0.9', 'oneday-apply': '0.9', 'youth': '0.8', 'about': '0.8',
           'coaches': '0.8', 'local': '0.8', 'contact': '0.8', 'faq': '0.7', 'private': '0.7', 'intl': '0.7', 'guide': '0.7'}
    keys = [k for k in PAGES if shown(k)]
    urls = ''.join(f'<url><loc>{url(k)}</loc><lastmod>{UPDATED}</lastmod><priority>{pri.get(k, "0.6")}</priority></url>\n' for k in keys)
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')

    # llms.txt
    write('llms.txt', LLMS.replace('[주소]', BASE.rstrip('/')))
    # 예전 주소 → 새 주소로 자동 이동
    for old, key, label in [('story/hiand-day/', 'hiand', 'Hi : And Day'), ('class/group/club/', 'team', '팀클래스')]:
        new = url(key)
        write(old + 'index.html', f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{label}</title>'
              f'<meta name="robots" content="noindex"><link rel="canonical" href="{new}"><meta http-equiv="refresh" content="0; url={new}">'
              f'</head><body><p><a href="{new}">{label} 페이지로 이동</a></p></body></html>')
    print(f'생성 완료: 공개 페이지 {len(keys)}개 (홈 포함), 숨긴 페이지 {len([k for k in BUILD if not shown(k)])}개, 404, robots, sitemap, llms')


LLMS = '''# 하이앤드 발리볼 아카데미 (HIGH END Volleyball Academy)

> 상암 인근 프리미엄 배구 아카데미(배구 학원·배구교실). 국가대표·프로 선수의 훈련 방식을 시스템으로 만들었고, 국가대표·프로 출신 하이앤드 코치진이 초등학생부터 성인까지 가르칩니다. 슬로건: 알고 하면 쉬운 배구.

## 공식 사이트
- 홈페이지: [주소]
- 네이버 플레이스: https://naver.me/G8fjuvBh
- 인스타그램: https://www.instagram.com/highend_volleyball
- 유튜브: https://www.youtube.com/@Highendvolleyball
- 네이버 블로그: https://m.blog.naver.com/highendv0lly

## 코치
- 김재휘 (대표 · 헤드코치 · 센터): 대한민국 국가대표 2016~2022, 2018 자카르타·팔렘방 아시안게임 은메달, 프로배구 V리그 2015~2025 (현대캐피탈, KB손해보험, 우리카드, 삼성화재), V리그 우승 4회, FIVB 코치 레벨1, 전문스포츠지도사 2급(배구)
- 황준태 (코치 · 리베로): 서울 우리카드 배구단 2022~2024, 제50회·제52회 대통령배 배구대회 리베로상

## 프로그램
- 원데이 클래스: 토요일 정규 수업에 그대로 함께하는 체험 수업, 토요일 12:00 · 13:30 · 16:30, 네이버 예약으로 신청 (금액은 네이버 예약에서 확인). 정규 등록 시 원데이 비용 차감
- 유소년반 (초등학생): 토요일 12:00, 80분
- 초급반 (중학생 이상 입문): 토요일 13:30, 80분
- 중급반 (중학생 이상, 배구 경력 6개월 이상): 토요일 16:30, 80분
- 개인레슨 60분: 1회 25만 원, 10회 등록 시 회당 20만 원
- 정규 수강권: 카카오톡 상담으로 안내
- 시합반: U15(13세 이상 · 중학생) · U18(16세 이상 · 고등학생) 연령별 대표팀 선발 · 대회 목표, 초등 고학년 · 성인은 상담
- 팀클래스: 배구 동호회 · 학교 · 기업 단체, 주 1회 정기 수업, 수강료는 카카오톡 상담
- 국제학교 · 외국인학교 · 해외 거주 학생 배구 레슨: 익숙한 영어 배구 용어 사용, 방학 단기 집중 레슨 · 캠프, 바시티(Varsity)·JV 팀 트라이아웃 준비 (상담)
- 하이앤드에서 배운 학생들의 학교: 서울용산국제학교(YISS), 서울외국인학교(SFS), 드와이트 외국인학교(Dwight School Seoul), 서울국제학교(SIS), 한국외국인학교(KIS), 세인트폴 서울(SPPS), 청라달튼외국인학교(CDS)
- 국가대표가 찾아가는 배구교실 (국가대표 출신 코치진이 학교로 찾아가는 배구교실): 2026년 등촌고등학교(7/21), 은평중학교(7/21), 가재울중학교(8/28). 학교 체육 시간·방과후·학교스포츠클럽 신청은 카카오톡 상담

## 수업 방식
- 하이앤드 코칭 시스템 "알고 하면 쉬운 배구": 하이앤드 3단계 수업 (왜? 필요한지 → 어떻게? 움직이는지 → 해보기! 직접 해 보기)
- 하이앤드 MAPS 워밍업 (Mobility · Activation · Plyometrics · Stability)
- 하이앤드 정밀 교정: Ask 먼저 묻기 → Point 코치가 짚기 → Watch 영상으로 확인 (리시브 몸 방향 · 플랫폼, 스파이크 치킨윙 교정)
- 하이앤드 운동일지 "Today & Next Ball"
- 줄 서서 기다리지 않고 모두 동시에 움직이는 80분 정규수업
- 하이앤드 성장 레벨 LV.1 입문 · LV.2 기본 · LV.3 심화 · LV.4 시합
- 200평 풀코트

## 이런 검색에 해당합니다
- 프리미엄 배구 아카데미, 프리미엄 배구학원, 상암배구학원, 서울배구학원, 배구아카데미, 배구학원, 배구교실, 배구레슨, 배구개인레슨, 배구원데이클래스, 배구 레슨, 배구 아카데미, 배구 개인레슨, 배구 원데이 클래스
- 초등학생 배구, 유소년 배구교실, 어린이 배구, 초등학교 배구부 준비, 중학생 배구
- 성인 배구 취미, 배구 초보, 배구 기본기, 배구 자세 교정
- 국가대표 출신 코치 배구 레슨, 프로 출신 배구 코치
- 국제학교배구, 외국인학교배구, 바시티대표팀배구, 바시티 트라이아웃, JV 배구, 해외 거주 학생 방학 배구 레슨, volleyball lessons for international school students, volleyball lesson Seoul
- 초등배구, 어린이배구, 유소년배구, 배구입문, 성인배구, 배구동호회, 배구선수반, 엘리트유소년배구
- 찾아가는배구교실, 학교배구재능기부, 학교스포츠클럽배구, 유소년배구저변확대
- 지역: 상암, 수색, DMC, 은평, 서대문, 강서, 고양, 덕양, 서울 서북부 (상암배구, 은평배구, 서대문배구, 강서배구, 고양배구)

## 위치 · 연락
- 상암 인근 · 현천동 180-1 (건물 앞 주차 가능)
- 전화: 010-4463-1177
- 카카오톡 채널: http://pf.kakao.com/_pCEzX
- 이메일: highendv0lly@gmail.com

## 주요 페이지
- 하이앤드 소개: [주소]/about/
- 코칭 스태프 (김재휘 헤드코치 · 황준태 코치): [주소]/about/coaches/
- Hi : And Day (국가대표 출신 · 현역 프로배구 선수와 함께하는 하이앤드 특별 배구 클래스, 2026.07.25): [주소]/story/hiandday/
- 국가대표가 찾아가는 배구교실 (국가대표 출신 코치진이 학교로 찾아가는 배구교실, 2026년 가재울중 · 등촌고 · 은평중): [주소]/story/school-class/
- 하이앤드 코칭 시스템: [주소]/method/
- 4단계 성장 레벨: [주소]/method/level/
- 클래스 전체 안내: [주소]/class/
- 원데이 클래스: [주소]/class/oneday/
- 원데이 클래스 신청: [주소]/class/oneday/apply/
- 유소년반: [주소]/class/regular/youth/
- 초급반: [주소]/class/regular/beginner/
- 중급반: [주소]/class/regular/intermediate/
- 개인레슨: [주소]/class/private/
- INTERNATIONAL (국제학교 · 외국인학교 · 해외 학생): [주소]/class/international/
- 시합반 (팀 클래스): [주소]/class/team/competition/
- 팀클래스 (동호회 · 학교 · 기업 단체): [주소]/class/team-class/
- 수강 · 결제 안내: [주소]/class/guide/
- 클래스 사진: [주소]/class/photos/
- 자주 묻는 질문: [주소]/contact/faq/
- 오시는 길: [주소]/contact/
- 상암·은평·고양 배구학원: [주소]/sangam-volleyball-academy/
'''

# ════════════════════════ 홈 = 지금 실제 홈페이지 그대로 ════════════════════════
# 대표 지시(2026-10-26): 첫 화면은 기존 홈페이지(tools/home_legacy.html) 그대로,
# 흰색 메뉴바는 그대로 두고 하위 메뉴만 3단계로, 검색용 머리말 추가

HOME_CSS = '''<style>
/* 한글 줄바꿈: 단어 중간에서 끊지 않기 */
body{word-break:keep-all;overflow-wrap:break-word}
h1,h2,h3,.lead,.sec-title,.sec-desc,.hero-title,.hero-desc{text-wrap:balance}
p,li,dd,summary{text-wrap:balance}
@media (max-width:600px){br.bk{display:none}}

#hero .hero-bg{background-image:url('assets/img/hero-group.jpg');background-position:center 62%;}
.nvi{position:relative;}
.nav-links .nvi>a{display:block;font-weight:600;}
.nvi:hover>a,.nvi:focus-within>a{color:var(--blue);background:rgba(26,83,212,.07);}
.nvd{display:none;position:absolute;top:100%;left:0;min-width:200px;background:#fff;border:1px solid var(--border);border-radius:10px;box-shadow:var(--shadow-lg);padding:6px 0;z-index:200;list-style:none;margin:0;}
.nvi:hover>.nvd,.nvi:focus-within>.nvd{display:block;}
.nvd li{position:relative;}
.nav-links .nvd a{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:9px 16px;border-radius:0;font-size:14px;white-space:nowrap;}
.nav-links .nvd a:hover{background:var(--bg);color:var(--blue);}
.nvd .arr{color:var(--muted);}
.nvd .g3h{display:none;position:absolute;left:100%;top:-7px;min-width:180px;background:#fff;border:1px solid var(--border);border-radius:10px;box-shadow:var(--shadow-lg);padding:6px 0;list-style:none;margin:0;}
.nvd li:hover>.g3h,.nvd li:focus-within>.g3h{display:block;}
.mobile-menu a.mtop{font-weight:700;color:var(--text);}
.mobile-menu a.msub{padding-left:36px;font-size:14px;}
.mobile-menu a.msub3{padding-left:56px;font-size:13px;}
.mobile-menu .mgrp{display:block;padding:12px 20px 4px 36px;font-size:13px;font-weight:700;color:var(--muted);border-bottom:none;}
.footer-kw{margin-top:16px;max-width:860px;font-size:12.5px;line-height:1.9;color:rgba(255,255,255,.5);word-break:keep-all}
/* 로켓츠식 남색 메뉴바 (2026-11-09) */
:root{--hdh:86px;--hdnavy:#003960}
@media (max-width:760px){:root{--hdh:48px}}
#nav{background:var(--hdnavy);border-bottom:0;box-shadow:0 2px 14px rgba(0,20,45,.25)}
.nav-inner{height:var(--hdh)}
#hero{padding-top:var(--hdh)}
.nav-links .nvi>a{color:#fff;font-size:15px;font-weight:800;letter-spacing:.06em;background:transparent}
.nvi:hover>a,.nvi:focus-within>a{color:#f5c400;background:transparent}
.btn-login-nav{background:transparent;border-color:rgba(255,255,255,.55);color:#fff}
.btn-login-nav:hover{border-color:#f5c400;color:#f5c400}
@media (max-width:760px){.nav-logo img.lg-emb{height:32px!important}.nav-logo img.lg-word{height:20px!important}}
/* 남색 구분선: 내용 종류가 바뀔 때만 (코치·수업 소개 / 사진·영상 / 문의·오시는 길) */
#coach,#gallery,#cta{border-top:10px solid var(--hdnavy)}
@media (max-width:760px){#coach,#gallery,#cta{border-top-width:6px}}
</style>
'''


def home_legacy():
    s = open(os.path.join(ROOT_DIR, 'tools', 'home_legacy.html'), encoding='utf-8').read()

    def swap(old, new):
        nonlocal s
        assert s.count(old) == 1, old[:60]
        s = s.replace(old, new)

    swap('대외 우승을 위한 집중 코칭. 실전 경기 전략 및 멘탈 훈련.', '대회를 목표로 한 집중 코칭. 실전 경기 전략 및 멘탈 훈련.')
    # 0) 브랜드 표기 기준 v2 (2026-10-27)
    swap('부상 없이 오래 할 수 있는 배구, 즐겁게 지속할 수 있는 배구', '안전하게 오래 하는 배구, 즐겁게 지속하는 배구')
    swap('국가대표 기준 고급 기술 습득. 실질적 팀플레이 완성 및 경기 분석.', '국가대표·프로 선수의 훈련 방식을 바탕으로 한 고급 기술 습득. 실질적 팀플레이 완성 및 경기 분석.')
    swap('개인별 목표 맞춤 집중 지도. 국가대표 수준 기술 전수.', '개인별 목표 맞춤 집중 지도. 국가대표·프로 출신 코치진의 1:1 기술 지도.')

    # E) 메인 오류 수정 (2026-11-09): 없는 "심화반" 빼고 유소년반 넣기, KB스타즈 -> KB손해보험
    swap('현대캐피탈·KB스타즈', '현대캐피탈·KB손해보험')
    a = s.index('<div class="curr-cards">')
    b = s.index('<div class="curr-card reveal rd3">', a)
    cards = [('', '1', '유소년반', '초등학생', '배구에 재미 붙이기. 올바른 자세와 기본기를 즐겁게 익힙니다.'),
             (' rd1', '2', '초급반', '중학생 이상 입문', '기초 기술 습득. 올바른 자세와 기본기 완성.'),
             (' rd2', '3', '중급반', '배구 경력 6개월 이상', '기술 완성도 향상, 신체 밸런스 강화. 실전 적용 능력 개발.')]
    s = s[:a] + '<div class="curr-cards">\n' + ''.join(
        f'      <div class="curr-card reveal{c}">\n        <div class="curr-lv">{n}</div>\n        <div class="curr-name">{t}</div>\n'
        f'        <div class="curr-target">{g}</div>\n        <div class="curr-desc">{d}</div>\n      </div>\n' for c, n, t, g, d in cards) + '      ' + s[b:]

    # 1) 머리말: 검색 제목·설명문·공유 미리보기·구조화 데이터
    h = head('home', '', [])
    seo = h[h.index('<title>'):h.index('<link rel="icon"')].replace('<meta name="theme-color" content="#003960">\n', '')
    swap('<title>하이앤드 발리볼 아카데미 | HIGH END VOLLEYBALL ACADEMY</title>', seo.strip())
    site = {'@type': 'WebSite', '@id': BASE + '#site', 'url': BASE, 'name': NAME, 'inLanguage': 'ko-KR',
            'publisher': {'@id': BASE + '#org'}}
    swap(SN['favicon'], icons(''))
    swap('</head>', HOME_CSS + ld(org_graph() + [site]) + '\n</head>')

    # 2) 흰색 메뉴바 그대로, 하위 메뉴만 3단계 (마우스·키보드로 열림)
    desk = []
    mob = []
    for top, label, subs in NAV:
        lis = []
        mob.append(f'<a class="mtop" href="{rel("", top)}">{label}</a>')
        for it in nav_items(subs):
            if it[0] is None:
                kids = ''.join(f'<li><a href="{rel("", k)}">{escape(t)}</a></li>' for k, t in it[2])
                lis.append(f'<li><a href="{rel("", it[2][0][0])}">{escape(it[1])}<span class="arr" aria-hidden="true">›</span></a><ul class="g3h">{kids}</ul></li>')
                mob.append(f'<span class="mgrp">{escape(it[1])}</span>' + ''.join(f'<a class="msub3" href="{rel("", k)}">{escape(t)}</a>' for k, t in it[2]))
            else:
                lis.append(f'<li><a href="{rel("", it[0])}">{escape(it[1])}</a></li>')
                mob.append(f'<a class="msub" href="{rel("", it[0])}">{escape(it[1])}</a>')
        desk.append(f'<div class="nvi"><a href="{rel("", top)}">{label}</a><ul class="nvd">{"".join(lis)}</ul></div>')
    start = s.index('<div class="nav-links">')
    end = s.index('</div>', start) + len('</div>')
    s = s[:start] + f'<div class="nav-links">{"".join(desk)}</div>' + s[end:]
    start = s.index('<div class="mobile-menu" id="mobileMenu">')
    end = s.index('</div>', start)
    tail = s[start:end]
    keep = tail[tail.index('<a href="https://m.place.naver.com'):]   # 원데이·회원 로그인 버튼은 그대로
    s = s[:start] + '<div class="mobile-menu" id="mobileMenu">\n    ' + ''.join(mob) + '\n    ' + keep + s[end:]

    # 주소 표기는 회사 규칙대로 (도로명 주소는 홈페이지에 쓰지 않음)
    swap('<div class="loc-addr">', '<div class="loc-addr" data-x="addr">')
    i = s.index('data-x="addr">'); j = s.index('</div>', i)
    seg = s[i:j]
    s = s[:i] + seg.replace('경기 고양시 덕양구 대덕로86번길 116-11', ADDR).replace(' data-x="addr"', '') + s[j:]
    s = s.replace('<div class="loc-addr" data-x="addr">', '<div class="loc-addr">')
    # 3) 첫 화면: 배경 단체 사진(흐림 효과는 기존 그대로), 오른쪽 대표 사진 카드 빼기
    start = s.index('    <div class="hero-image-wrap')
    end = s.index('  </div>\n</section>', start)
    s = s[:start].rstrip() + '\n' + s[end:]
    # 4) 코치 소개: 사진 넘김 빼고 메인 사진 1장 고정 (넘김 스크립트는 사진 칸이 없으면 스스로 멈춤)
    start = s.index('<div class="coach-carousel" id="coachCarousel">')
    end = s.index('\n      </div>\n      <div class="coach-text-col">', start)
    s = (s[:start] + '<img src="./1. 코치 사진 자료/1.jpg" alt="메인코치 김재휘: 대한민국 국가대표 2016~2022, 현대캐피탈·KB손해보험·우리카드·삼성화재" loading="lazy">'
         + s[end:])
    # 6) 상단 로고: AI 사무실 로고 파일(엠블럼 + 글자 로고)
    lo = s.index('<a href="#hero" class="nav-logo">')
    lo_end = s.index('</a>', lo)
    s = (s[:lo] + '<a href="#hero" class="nav-logo"><img class="lg-emb" src="assets/img/logo-emblem.webp" alt="" width="36" height="40">'
         '<img class="lg-word" src="assets/img/logo-text-white.webp" alt="HIGH END VOLLEYBALL ACADEMY 하이앤드 발리볼 아카데미" width="88" height="26">' + s[lo_end:])
    # 6-1) 떠 있는 아이콘 4개 → 하위 페이지와 같은 "문의" 버튼 하나
    fb = s.index('<!-- FLOAT -->')
    fb_end = s.index('</div>', s.index('<div class="float-bar">', fb)) + len('</div>')
    s = s[:fb] + fab_html() + s[fb_end:]
    a = s.index("// ── FLOAT BAR")
    b = s.index("// ── REELS SLIDER", a)
    s = s[:a] + """// ── 문의 버튼: 누르면 4개 펼침, 오시는 길·푸터에서는 숨김 ──
(function(){
  const fab=document.getElementById('fab'),fb=document.getElementById('fabBtn');
  if(!fab||!fb)return;
  fb.addEventListener('click',()=>{const o=fab.classList.toggle('open');fb.setAttribute('aria-expanded',o?'true':'false');});
  const targets=[document.getElementById('location'),document.querySelector('footer')].filter(Boolean);
  if(!targets.length||!('IntersectionObserver' in window))return;
  const seen=new Set();
  const io2=new IntersectionObserver(es=>{
    es.forEach(e=>e.isIntersecting?seen.add(e.target):seen.delete(e.target));
    fab.classList.toggle('away',seen.size>0);
  },{threshold:0.15});
  targets.forEach(t=>io2.observe(t));
})();
""" + s[b:]
    # 6-2) 위쪽 메뉴의 원데이 예약 버튼 빼기 (원데이 페이지·다른 네이버 예약 링크는 그대로)
    nb = s.index('class="btn-naver">원데이클래스</a>')
    a_start = s.rindex('<a ', 0, nb)
    s = s[:a_start].rstrip() + '\n      ' + s[nb + len('class="btn-naver">원데이클래스</a>'):].lstrip()
    # 7) ☰ 전체 메뉴: 하위 페이지와 같은 로켓츠식 왼쪽 메뉴 (PC·휴대폰 모두 로고 왼쪽에 ☰)
    hb_start = s.index('<button class="hamburger" id="menuBtn"')
    hb_end = s.index('</button>', hb_start) + len('</button>')
    s = s[:hb_start].rstrip() + '\n' + s[hb_end:]
    lg = s.index('<a href="#hero" class="nav-logo">')
    lg_end = s.index('</a>', lg) + len('</a>')
    s = (s[:lg] + '<div class="hm-brand">'
         + f'<button class="hamburger hm-all" id="menuBtn" type="button" aria-label="전체 메뉴 열기" aria-expanded="false" aria-controls="drawer" data-drawer-open>{SN["menu"]}</button>'
         + s[lg:lg_end] + '</div>' + s[lg_end:])
    mm = s.index('<div class="mobile-menu" id="mobileMenu">')
    s = s[:mm] + s[s.index('</div>', mm) + len('</div>'):]
    a = s.index("// ── MOBILE MENU")
    b = s.index("function closeMnu()", a)
    b = s.index("\n", b) + 1
    s = s[:a] + "function closeMnu(){}\n" + s[b:]
    css = open(os.path.join(ROOT_DIR, 'assets', 'css', 'site.css'), encoding='utf-8').read()
    css = css[css.index('/* ☰ 전체 메뉴 (로켓츠식 왼쪽 메뉴) */'):css.index('/* ☰ 끝 */')]
    site_css = open(os.path.join(ROOT_DIR, 'assets', 'css', 'site.css'), encoding='utf-8').read()
    css += site_css[site_css.index('/* 떠 있는 "문의" 버튼'):site_css.index('/* 나타나기 효과')]
    css += '#fab{--navy:#003960}\n'
    css += '.hm-brand{display:flex;align-items:center;gap:6px;flex-shrink:0}\n.nav-logo{gap:8px}.nav-logo img.lg-emb{width:auto;height:40px;border-radius:0;object-fit:contain}.nav-logo img.lg-word{width:auto;height:26px;border-radius:0}\n.hamburger.hm-all{display:flex;align-items:center;justify-content:center;width:40px;height:40px;margin-right:4px;color:#fff}\n.hamburger.hm-all svg{width:26px;height:26px}\n'
    # 지역 키워드 줄: 흰 칸 대신 남색 맨 아래 칸 안으로 (2026-11-09 대표 결정)
    swap('<div class="footer-copy" style="margin-top:8px;">', '<div class="footer-kw">상암배구 · 상암배구학원 · 수색배구 · DMC배구 · 은평배구 · 서대문배구 · 마포배구 · 강서배구 · 고양배구 · 행신배구 · 향동배구 · 덕은배구 · 창릉배구 · 도래울배구 · 삼송배구<br>하이앤드 발리볼 아카데미 상암점 · 상암 인근 · 현천동 180-1</div>\n      <div class="footer-copy" style="margin-top:10px;">')
    swap('</body>', f'{drawer_html("", "home")}\n<style>{css}</style>\n<script src="assets/js/drawer.js?v={ver("assets/js/drawer.js")}" defer></script>\n</body>')
    # 8) 첫 화면 교체 (2026-11-09 시안 3): tools/home_hero.html
    hero = open(os.path.join(ROOT_DIR, 'tools', 'home_hero.html'), encoding='utf-8').read()
    hero = (hero.replace('{V1}', ver('assets/img/hero-hiand-1.webp')).replace('{V2}', ver('assets/img/hero-play.webp'))
                .replace('{V3}', ver('assets/img/hero-hiand-2.webp')))
    h0 = s.index('<!-- HERO -->')
    h1 = s.index('<!-- STATS -->')
    s = s[:h0] + hero + '\n' + s[h1:]
    # 9) 수업 일정 달력 → 수업 고르기 사진 칸 (2026-11-09). 달력은 회원 로그인·수강 안내 페이지에 그대로 있음
    tiles = hk_tiles('')
    html = f'    <div class="hk-grid">{"".join(tiles)}</div>'
    sc = open(os.path.join(ROOT_DIR, 'assets', 'css', 'site.css'), encoding='utf-8').read()
    hkcss = sc[sc.index('/* 수업 고르기 사진 칸'):sc.index('/* 수업 고르기 끝 */')]
    blk = open(os.path.join(ROOT_DIR, 'tools', 'home_classes.html'), encoding='utf-8').read().replace('{HKCSS}', hkcss).replace('{CARDS}', html)
    c0 = s.index('<!-- PUBLIC SCHEDULE -->')
    c1 = s.index('<!-- COACH -->')
    s = s[:c0] + blk + '\n' + s[c1:]
    # 10) 파란 숫자 띠·커리큘럼 칸(포스터 2장 포함) 빼기 (2026-11-09 대표 확정: 수업 고르기 칸과 겹침, 경력은 코치 칸에 있음)
    for x0, x1 in [('<!-- STATS -->', '<!-- 메인: 수업 고르기 사진 칸'), ('<!-- CURRICULUM -->', '<!-- GALLERY -->')]:
        p0 = s.index(x0); p1 = s.index(x1, p0)
        s = s[:p0] + s[p1:]
    # 11) 하이라이트 영상 빼기 + 코치 칸 아래 '수업은 이렇게 진행됩니다'(B안) (2026-11-09 대표 확정)
    p0 = s.index('    <!-- REELS / VIDEO SLIDER -->')
    p1 = s.index('  </div>\n</section>\n<div class="lightbox"', p0)
    s = s[:p0].rstrip() + '\n' + s[p1:]
    flow = open(os.path.join(ROOT_DIR, 'tools', 'home_flow.html'), encoding='utf-8').read().replace('{FLOW}', rel('', 'flow'))
    g = s.index('<!-- GALLERY -->')
    s = s[:g] + flow + '\n' + s[g:]
    j0 = s.index('// ── FIREBASE (READ ONLY)')
    j1 = s.index("document.getElementById('calNext').onclick=()=>changeMonth(1);\n") + len("document.getElementById('calNext').onclick=()=>changeMonth(1);\n")
    s = s[:j0] + s[j1:]
    for tag in ['<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js"></script>\n',
                '<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-database-compat.js"></script>\n']:
        swap(tag, '')
    swap('<a href="#schedule">수업일정</a>', f'<a href="{rel("", "guide")}">수업일정</a>')
    # 12) CONTACT 칸: 원데이·회원 로그인 카드 빼기 (원데이는 첫 화면 버튼, 로그인은 맨 위 메뉴에 있음). 카톡 띠 + 오시는 길만
    p0 = s.index('    <div class="cta-cards cta-cards-2 reveal">')
    p1 = s.index('    <div class="kakao-banner reveal">', p0)
    s = s[:p0] + s[p1:]
    # 13) 카톡 상담 띠를 오시는 길(지도) 아래로 (2026-11-09 대표)
    k0 = s.index('    <div class="kakao-banner reveal">')
    k1 = s.index('    <!-- 오시는 길 -->', k0)
    kb = s[k0:k1]
    s = s[:k0] + s[k1:]
    e = s.index('  </div>\n</section>\n\n<!-- FOOTER -->')
    s = s[:e] + kb + s[e:]
    # 14) CONTACT 제목·설명 빼기, 지도는 네이버 지도 하나만 (2026-11-11 대표)
    c0 = s.index('    <div class="sec-label reveal" style="text-align:center">CONTACT</div>')
    c1 = s.index('    </p>\n', c0) + len('    </p>\n')
    s = s[:c0] + s[c1:]
    m0 = s.index('      <div class="loc-map"><iframe')
    m1 = s.index('</div>\n', m0) + len('</div>\n')
    s = s[:m0] + '      ' + naver_map_img() + '\n' + s[m1:]
    b0 = s.index('      <div class="loc-btns">', m0)
    b1 = s.index('      </div>\n', b0) + len('      </div>\n')
    s = s[:b0] + '      ' + MAP_BTNS + '\n' + s[b1:]
    return s


if __name__ == '__main__':
    build()
