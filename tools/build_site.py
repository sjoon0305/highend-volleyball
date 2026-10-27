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
CAREER = '국가대표 7년 · 프로(V리그) 10년, 선수 17년'

SN = json.load(open(os.path.join(ROOT_DIR, 'tools', 'snippets.json'), encoding='utf-8'))
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
              desc='국가대표·프로 선수의 훈련 방식을 시스템으로 만든 프리미엄 배구 아카데미 하이앤드. 상암 인근 · 현천동 180-1, 국가대표·프로 출신 코치진이 초등학생부터 성인까지 가르칩니다. 원데이 클래스 25,000원, 문의 010-4463-1177'),
    # ABOUT US
    'about': P(path='about/', crumb='ABOUT US', title='하이앤드 소개 | 상암·고양 프리미엄 배구 아카데미',
               desc='가장 완벽한 기본, 그것이 우리가 말하는 하이앤드입니다. 국가대표·프로 선수의 훈련 방식을 시스템으로 만든 상암 인근 프리미엄 배구 아카데미(배구 학원·배구교실). 초등학생부터 성인까지, 원데이 25,000원 · 010-4463-1177',
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
                desc='이유를 알고 하는 반복이 몸을 바꿉니다. 국가대표·프로 선수의 훈련 방식을 시스템으로 만든 하이앤드 코칭 시스템: 몸 방향, 플랫폼, 왜 → 어떻게 → 해보기, 묻기 → 짚기 → 영상 확인, 운동일지 Today & Next Ball.',
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
    'class': P(path='class/', crumb='CLASS', title='배구 클래스 안내 | 원데이 · 유소년 · 초급 · 중급 · 개인레슨 · 하이앤드',
               desc='프리미엄 배구 학원 · 배구교실 하이앤드 클래스 전체 안내: 원데이 클래스 25,000원(오픈 이벤트 50% 할인가), 유소년반 · 초급반 · 중급반 80분 정규수업, 1:1 개인레슨, 국제학교 학생 배구 레슨. 상암 인근 · 현천동 180-1',
               banner=('CLASS', '클래스 전체 안내', '나에게 맞는 수업을 골라 보세요'), bg='class-4', cta='어떤 반이 맞을지 모르겠다면',
               cta_sub='나이와 배구 경력, 가능한 시간을 남겨 주시면 맞는 반을 추천해 드립니다.'),
    'oneday': P(path='class/oneday/', crumb='원데이 안내', title='배구 원데이 클래스 25,000원 | 하이앤드',
                desc='배구 원데이 클래스 25,000원(오픈 이벤트 50% 할인가). 토요일 12:00 · 13:30 · 16:30, 정규 수업에 그대로 함께합니다. 정규 등록 시 원데이비 차감. 상암 인근 · 현천동 180-1',
                banner=('ONE DAY CLASS', '원데이 클래스', '처음이라면, 실제 수업 그대로 경험해 보세요'), bg='class-5'),
    'oneday-apply': P(path='class/oneday/apply/', crumb='원데이 신청', title='원데이 클래스 신청 | 네이버 예약 · 하이앤드',
                      desc='하이앤드 배구 원데이 클래스 신청은 네이버 예약으로 받습니다. 25,000원, 토요일 12:00 · 13:30 · 16:30. 준비물: 실내 운동화, 물, 편한 운동복. 수업 10분 전 도착.',
                      banner=('APPLY', '원데이 클래스 신청', '네이버 예약으로 간편하게 신청하세요')),
    'oneday-reviews': P(path='class/oneday/reviews/', crumb='원데이 후기', hidden=True, title='원데이 클래스 후기 | 하이앤드',
                        desc='하이앤드 원데이 클래스 후기', banner=('REVIEW', '원데이 클래스 후기', '네이버 방문자 리뷰에서 확인하세요')),
    'youth': P(path='class/regular/youth/', crumb='유소년반', title='유소년 배구교실 · 초등학생 배구 | 하이앤드 유소년반',
               desc='초등학생 배구교실부터 학교 배구부 · 엘리트 진학 준비까지. 프리미엄 배구 아카데미 하이앤드 유소년반(초·중·고) 80분 정규수업. 국가대표·프로 출신 코치진이 바른 자세와 기본기를 처음부터 가르칩니다.',
               banner=('YOUTH', '유소년반', '초등학생부터 중·고등학생까지, 처음부터 제대로'), bg='class-5'),
    'beginner': P(path='class/regular/beginner/', crumb='초급반', title='배구 초급반 · 배구 처음 배우기 | 하이앤드',
                  desc='배구를 처음 배우는 중학생 이상을 위한 하이앤드 초급반. 기초 기술 습득과 배구에 재미 붙이기, 80분 정규수업. 국가대표 · 프로 출신 코치진이 가르칩니다.',
                  banner=('BEGINNER', '초급반', '중학생 이상, 배구를 처음 배우는 분'), bg='class-3'),
    'intermediate': P(path='class/regular/intermediate/', crumb='중급반', title='배구 중급반 · 기술 향상 | 하이앤드',
                      desc='중학생 이상, 배구 경력 6개월 이상을 위한 하이앤드 중급반. 볼 컨트롤 정밀화와 신체 정렬 코칭, 80분 정규수업. 국가대표 · 프로 출신 코치진이 가르칩니다.',
                      banner=('INTERMEDIATE', '중급반', '중학생 이상, 배구 경력 6개월 이상'), bg='class-4'),
    'regular-reviews': P(path='class/regular/reviews/', crumb='정규 후기', hidden=True, title='정규 클래스 후기 | 하이앤드',
                         desc='하이앤드 정규 클래스 후기', banner=('REVIEW', '정규 클래스 후기', '네이버 방문자 리뷰에서 확인하세요')),
    'competition': P(path='class/team/competition/', crumb='시합반', title='배구 시합반 · 대회 준비 | 하이앤드 팀 클래스',
                     desc='하이앤드 시합반: 연령별 대표팀 선발과 대회를 목표로 한 집중 코칭. 실전 경기 리딩, 경기 운영과 상황 판단, 팀 전술. 초등 고학년 · 중고등 · 성인, 상담으로 맞춤 진행.',
                     banner=('TEAM CLASS', '시합반', '연령별 대표팀 선발과 대회를 목표로 한 집중 코칭')),
    'club': P(path='class/group/club/', crumb='동호회 · 단체 레슨', title='배구 동호회 · 단체 레슨 | 하이앤드 단체 클래스',
              desc='배구 동호회, 학교, 기관 단체 레슨은 인원과 목표에 맞춰 상담으로 진행합니다. 국가대표·프로 출신 하이앤드 코치진이 가르칩니다. 상암 인근 하이앤드 발리볼 아카데미',
              banner=('GROUP CLASS', '동호회 · 단체 레슨', '인원과 목표에 맞춰 상담으로 진행합니다')),
    'private': P(path='class/private/', crumb='개인레슨', title='배구 개인레슨 1:1 | 국가대표·프로 출신 코치진 · 하이앤드',
                 desc='프리미엄 배구 아카데미 하이앤드의 1:1 개인레슨 60분. 1회 25만 원, 10회 등록 시 회당 20만 원. 서브 · 리시브 · 스파이크 약점을 내 몸에 맞게 교정합니다. 상암 인근 하이앤드',
                 banner=('PRIVATE LESSON', '1:1 개인레슨', '60분 동안 한 사람만 봅니다'), bg='class-6'),
    'intl': P(path='class/international/', crumb='국제학교 · 해외 학생', title='국제학교 배구 레슨 · 해외 거주 학생 방학 배구 | 하이앤드',
              desc='국제학교 · 외국인학교 학생과 방학마다 한국을 찾는 해외 거주 학생을 위한 배구 레슨. 익숙한 영어 배구 용어, 한 명 한 명 기본기 교정, 방학 단기 집중 레슨. 국가대표·프로 출신 하이앤드 코치진 지도',
              banner=('INTERNATIONAL SCHOOL', '국제학교 · 해외 학생', 'Volleyball lessons for international school students')),
    'guide': P(path='class/guide/', crumb='수강 · 결제 안내', title='배구 수업 시간표 · 수강 · 결제 안내 | 하이앤드',
               desc='하이앤드 토요일 정규수업 시간표(유소년반 12:00 · 초급반 13:30 · 중급반 16:30, 80분)와 수업 일정 달력, 정규 수강권 · 결제 안내. 회원 로그인 후 수업 예약',
               banner=('SCHEDULE & PAYMENT', '수강 · 결제 안내', '시간표와 수업 일정, 수강권 · 결제 방법')),
    'photos': P(path='class/photos/', crumb='클래스 사진', title='배구 수업 사진 | 하이앤드 수업 현장',
                desc='하이앤드 발리볼 아카데미 토요일 수업 현장 사진과 영상. 리시브 · 패스 · 토스 · 스파이크를 배우는 유소년반 · 초급반 · 중급반 수업 모습.',
                banner=('HIGH END PHOTOS', '클래스 사진', '토요일 수업 현장 사진과 영상')),
    # STORY
    'story': P(path='story/', crumb='STORY', title='하이앤드 수업 이야기 | 배구 수업 기록',
               desc='하이앤드 발리볼 아카데미 토요일 수업 이야기. 네이버 블로그 수업기록, 방문자 리뷰, 인스타그램 · 유튜브. 상암 인근 프리미엄 배구 아카데미 하이앤드',
               banner=('CLASS STORY', '수업 이야기', '매주 토요일 수업에서 있었던 일을 기록합니다'), cta='다음 이야기의 주인공이 되어 보세요'),
    'hiand': P(path='story/hiand-day/', crumb='Hi:And Day', hidden=True, title='Hi:And Day | 하이앤드',
               desc='하이앤드 행사 Hi:And Day', banner=('EVENT', 'Hi:And Day', '하이앤드 행사 소식은 인스타그램에서 확인하세요')),
    'note': P(path='story/note/', crumb='배구 노트', hidden=True, title='배구 노트 | 하이앤드',
              desc='하이앤드 배구 노트', banner=('VOLLEYBALL NOTE', '배구 노트', '하이앤드 코치진의 배구 이야기를 준비하고 있습니다')),
    # CONTACT
    'contact': P(path='contact/', crumb='CONTACT', title='오시는 길 | 하이앤드 발리볼 아카데미 상암점',
                 desc='하이앤드 발리볼 아카데미 오시는 길: 상암 인근 · 현천동 180-1, 건물 앞 주차 가능. 네이버 지도 · 구글 지도, 토요일 정규수업. 문의 010-4463-1177',
                 banner=('LOCATION', '오시는 길', ADDR), cta='가까운 곳에서, 처음부터 제대로'),
    'local': P(path='sangam-volleyball-academy/', crumb='상암·은평·고양 배구학원', title='상암·은평·고양 배구학원 | 하이앤드 발리볼 아카데미',
               desc='상암·은평·고양 프리미엄 배구 아카데미 하이앤드(배구 학원·배구교실). 상암 인근 · 현천동 180-1, 국가대표·프로 출신 코치진이 초등학생부터 성인까지 가르칩니다. 원데이 25,000원, 토요일 수업 · 010-4463-1177',
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
    ('class', 'CLASS', [(None, '원데이클래스', [('oneday', '원데이클래스'), ('oneday-apply', '원데이클래스 신청'), ('oneday-reviews', '원데이클래스 후기')]),
                        (None, '정규 클래스', [('youth', '유소년반'), ('beginner', '초급반'), ('intermediate', '중급반'), ('regular-reviews', '정규 클래스 후기')]),
                        (None, '팀 클래스', [('competition', '시합반')]),
                        (None, '단체 클래스', [('club', '동호회 · 단체 레슨'), ('intl', '국제학교 · 해외 학생')]),
                        ('private', '개인레슨'), ('guide', '수강 · 결제 안내'), ('photos', '클래스 사진')]),
    ('story', 'STORY', [('story', '수업 이야기'), ('hiand', 'Hi:And Day'), ('note', '배구 노트')]),
    ('contact', 'CONTACT', [('contact', '오시는 길'), ('local', '상암·은평·고양 배구학원'), ('faq', '자주 묻는 질문'), ('ask', '상담하기')]),
]


def shown(k):
    return not PAGES[k].get('hidden')


def nav_items(subs):
    """숨긴 페이지를 뺀 2단계 목록"""
    out = []
    for it in subs:
        if it[0] is None:
            kids = [(k, t) for k, t in it[2] if shown(k)]
            if kids:
                out.append((None, it[1], kids))
        elif shown(it[0]):
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
    return f'<img{c} src="{root}assets/img/{name}.{ext}" alt="{escape(alt)}" width="{w}" height="{h}"{attrs}>'


# ════════════════════════ 구조화 데이터 ════════════════════════
SAME_AS = [INSTA, YOUTUBE, NAVER_PLACE, BLOG, KAKAO]


def org_graph():
    return [
        {'@type': 'Organization', '@id': BASE + '#org', 'name': NAME, 'alternateName': NAME_EN, 'url': BASE,
         'logo': BASE + 'assets/img/logo.png', 'email': EMAIL, 'telephone': PHONE_INTL, 'sameAs': SAME_AS,
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
         'priceRange': '₩25,000~₩250,000', 'sameAs': SAME_AS, 'parentOrganization': {'@id': BASE + '#org'}},
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
    if key != top:
        out.append((PAGES[key]['crumb'], key))
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
def head(key, root, extra_ld):
    p = PAGES[key]
    graph = org_graph() + [x for x in [breadcrumb_ld(key)] + list(extra_ld) if x]
    if key == 'home':
        graph.append({'@type': 'WebSite', '@id': BASE + '#site', 'url': BASE, 'name': NAME, 'inLanguage': 'ko-KR',
                      'publisher': {'@id': BASE + '#org'}})
    robots = 'noindex,follow' if p.get('hidden') else 'index,follow,max-image-preview:large'
    canon = '' if key == 'notfound' else f'<link rel="canonical" href="{url(key)}">\n'
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
{SN['favicon']}
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
    # ☰ 전체 메뉴 (PC: 한눈에 펼침 / 휴대폰: 눌러서 펼침)
    cols = []
    for top, label, subs in NAV:
        items = []
        for it in nav_items(subs):
            if it[0] is None:
                kids = ''.join(f'<a class="am3" href="{rel(root, k)}">{escape(t)}</a>' for k, t in it[2])
                items.append(f'<div class="am-grp"><span class="am-gl">{escape(it[1])}</span>{kids}</div>')
            else:
                items.append(f'<a class="am2" href="{rel(root, it[0])}">{escape(it[1])}</a>')
        cols.append(f'<div class="am-col"><button class="am-top" type="button" aria-expanded="false">{label}</button><div class="am-list">{"".join(items)}</div></div>')
    return f'''<body data-page="{key}">
<a class="skip" href="#main">본문 바로가기</a>
<header class="hd3">
  <div class="hd3-in">
    <button class="hd3-all" id="menuBtn" type="button" aria-label="전체 메뉴 열기" aria-expanded="false" aria-controls="allmenu" data-close='{SN['close']}'>{SN['menu']}</button>
    <a class="hd3-logo" href="{rel(root, 'home')}"><img src="{root}assets/img/logo.webp" alt="하이앤드 발리볼 아카데미 로고" width="34" height="34"><span><b>HIGH END</b><small>VOLLEYBALL ACADEMY</small></span></a>
    <nav class="gnb3" aria-label="주요 메뉴">{"".join(g1)}</nav>
    <div class="hd3-act">
      <a class="hd3-book" href="{rel(root, 'oneday-apply')}">원데이 예약</a>
      <a class="hd3-login" href="{root}dashboard.html" aria-label="회원 로그인">{USER_ICON}<span>로그인</span></a>
    </div>
  </div>
</header>
<div class="allmenu" id="allmenu" hidden>
  <nav class="am-in" aria-label="전체 메뉴">
    <a class="am-home" href="{rel(root, 'home')}">HOME</a>
    <div class="am-cols">{"".join(cols)}</div>
    <div class="am-cta"><a href="{rel(root, 'oneday-apply')}">원데이 클래스 신청</a><a href="{root}dashboard.html">회원 로그인</a></div>
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
<div class="fab" id="fab">
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
    cta = cta_band(root, p.get('cta', '처음부터 제대로.'), p.get('cta_sub', '')) if key != 'notfound' else ''
    return (head(key, root, extra_ld) + '\n' + header(key, root) + '\n<main id="main">\n'
            + sechead(key, root) + '\n' + crumbs(key, root) + '\n' + pagehead(key, root) + '\n'
            + body(root) + '\n' + cta + '\n</main>\n' + footer(root) + '\n'
            + f'<script src="{root}assets/js/site.js?v={ver("assets/js/site.js")}" defer></script>{sc}\n</body>\n</html>\n')


def go(r, key, text, cls='s'):
    return f'<a class="btn {cls}" href="{rel(r, key)}">{escape(text)}</a>'


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
    <img class="ai-logo reveal" src="{r}assets/img/logo.webp" alt="하이앤드 발리볼 아카데미 엠블럼" width="160" height="160" loading="lazy">
    <h2 class="ai-title">가장 완벽한 기본</h2>
    <p class="ai-tag">프리미엄 배구 아카데미, 하이앤드</p>
    <p class="ai-p">하이앤드 발리볼 아카데미는 국가대표·프로 선수의 훈련 방식을 시스템으로 만든 프리미엄 배구 아카데미입니다.<br>처음 배구를 시작하는 <strong>초등학생부터</strong> 학교 배구부·엘리트를 준비하는 학생, <strong>취미로 배우는 성인까지</strong> 지금 실력에 맞는 단계에서 배웁니다.</p>
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
                   ('method', '하이앤드 코칭 시스템', '알고 하면 쉬운 배구: 왜 → 어떻게 → 해보기.', ''),
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
    <div class="btns">{go(r, 'method', '수업 방식 보기')}{go(r, 'oneday-apply', '원데이클래스 신청', 'p')}</div>
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
      <div class="card reveal"><div class="big-letter">왜</div><p style="margin-top:12px">오늘 배울 동작이 왜 필요한지, 몸이 어떻게 움직여야 하는지 먼저 이해합니다.</p></div>
      <div class="card reveal"><div class="big-letter">어떻게</div><p style="margin-top:12px">한 사람씩 자세를 보고, 몸에 맞게 정밀하게 교정합니다.</p></div>
      <div class="card reveal"><div class="big-letter">해보기</div><p style="margin-top:12px">배운 원리를 게임과 실전 상황에서 직접 써 봅니다.</p></div>
    </div>
    <div class="principle reveal"><div class="t">하이앤드가 가장 먼저 가르치는 원리</div><p>몸 방향이 공에서 멀어지면, 플랫폼(두 팔로 만든 판)과 공을 보낼 곳이 몸에서 멀어집니다. 그러면 몸통의 힘이 공에 전달되기 어렵습니다. 리시브, 토스, 스파이크 모두 <strong>몸 방향</strong>에서 시작합니다.</p></div>
  </div>
</section>
<section class="sec alt">
  <div class="wrap">
    <h2>스스로 고칠 수 있는 선수</h2>
    <p class="lead">코치가 없을 때도 "방금 공이 왜 저쪽으로 갔는지" 스스로 알아차리는 것이 목표입니다. 그래서 교정할 때 세 가지를 함께 씁니다.</p>
    <div class="grid3 mt">
      <div class="card reveal"><div class="big-letter">묻기</div><p style="margin-top:12px">"방금 어땠어요?" 수강생이 먼저 느낀 점을 말합니다.</p></div>
      <div class="card reveal"><div class="big-letter">짚기</div><p style="margin-top:12px">코치가 원인과 고칠 점 하나를 짚어 줍니다.</p></div>
      <div class="card reveal"><div class="big-letter">영상</div><p style="margin-top:12px">찍은 영상을 함께 보며 내 몸이 실제로 어떻게 움직였는지 확인합니다.</p></div>
    </div>
    <div class="principle reveal"><div class="t">하이앤드 운동일지 "Today &amp; Next Ball"</div><p>국가대표·프로 선수들이 피드백을 기록하던 습관을 하이앤드 운동일지로 만들었습니다. 개인레슨과 시합반은 매 수업이 끝나면 오늘의 좋았던 순간, 배운 점, 고칠 점을 적고 <strong>다음 공(Next Ball)</strong>을 준비합니다.</p></div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <h2>하이앤드 코칭 시스템을 이루는 것</h2>
    {linkcards(r, [('maps', 'MAPS 워밍업', '가동성 · 활성화 · 순발력 · 안정성. 안전하게 오래 하는 몸 만들기.', 'maps'),
                   ('correction', '정밀 교정', '묻기 → 짚기 → 영상 확인. 리시브와 스파이크를 한 사람씩.', 'fix'),
                   ('flow', '수업 80분 흐름', 'MAPS 워밍업 → 왜 → 어떻게 → 해보기.', 'flow'),
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
    <div class="btns">{go(r, 'flow', '수업 80분 흐름 보기')}</div>
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
    <div class="btns">{go(r, 'private', '1:1 개인레슨 보기')}</div>
  </div>
</section>'''


def flow_body(r):
    return f'''<section class="sec">
  <div class="wrap">
    <ol class="steps">
      <li class="reveal"><div class="k">STEP 1</div><h2 class="t">MAPS 워밍업</h2><p>가동성 → 활성화 → 순발력 → 안정성. 안전하게 움직이는 몸 준비</p></li>
      <li class="reveal"><div class="k">STEP 2</div><h2 class="t">왜: 원리 이해</h2><p>오늘 배울 동작과 그 이유를 짧게. 목표를 알고 연습해야 오래 남습니다</p></li>
      <li class="reveal"><div class="k">STEP 3</div><h2 class="t">어떻게: 교정 반복</h2><p>처음엔 같은 동작을 반복하고, 익숙해지면 공의 방향 · 높이 · 순서를 바꿔 가며</p></li>
      <li class="reveal"><div class="k">STEP 4</div><h2 class="t">해보기: 게임</h2><p>작은 게임에서 실전 게임으로. 배운 동작을 판단과 함께 써 봅니다</p></li>
    </ol>
    <div class="grid3 mt">
      <div class="card reveal"><h2 class="t">매 수업 같은 순서</h2><p>토요일 정규수업은 매번 이 순서로 진행합니다.</p></div>
      <div class="card reveal"><h2 class="t">기다리지 않는 연습</h2><p>한 사람이 공을 만지는 횟수가 중요합니다. 모두가 동시에 움직이도록 수업을 짭니다.</p></div>
      <div class="card reveal"><h2 class="t">게임으로 마무리</h2><p>게임은 수업마다 다르게 준비합니다. 유소년 수업에서는 아이들이 즐겁게 몰입하는 놀이형 게임을 많이 합니다.</p></div>
    </div>
    <div class="btns">{go(r, 'level', '성장 레벨 보기')}{go(r, 'oneday', '원데이 클래스로 경험하기', 'p')}</div>
  </div>
</section>'''


def level_body(r):
    return f'''<section class="sec">
  <div class="wrap">
    <p class="lead">배구는 나이보다 <strong>"지금 할 수 있는 동작"</strong>이 중요합니다. 하이앤드 성장 레벨은 국가대표·프로 선수의 훈련 방식을 바탕으로, 처음 배우는 분부터 배구부·엘리트 진학과 대회를 준비하는 학생까지 지금 실력에 맞는 단계에서 시작해 한 단계씩 올라가도록 만들었습니다. 프리미엄 배구 학원 · 배구교실 · 배구 아카데미를 찾는 초등학생부터 성인까지, 누구나 이유를 알고 배우는 배구를 경험할 수 있습니다.</p>
    <div class="lvx-grid mt">
      <article class="lvx reveal">
        <div class="lvx-hd"><b>LV.1</b><div><h2>입문 · 초급반</h2><p>기초 기술 습득 · 배구에 재미 붙이기</p></div></div>
        <p class="lvx-who"><strong>이런 분께</strong> 배구를 처음 시작하는 분. 중학생 이상은 초급반, 처음 배우는 초등학생은 유소년반에서 시작합니다.</p>
        <ul class="plain"><li>기본 매커니즘 습득: 패스, 서브, 리시브</li><li>배구 놀이를 바탕으로 한 신체 감각 강화</li><li>팀워크 경험으로 배구의 재미 발견</li></ul>
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


def class_body(r):
    cards = [('oneday', '0820-03', '원데이클래스', '처음이라면 · 25,000원', 'oneday'),
             ('youth', 'class-5', '유소년반', '초·중·고 · 80분 정규수업', 'youth'),
             ('beginner', 'class-3', '초급반', '중학생 이상 입문 · 80분', 'group'),
             ('intermediate', 'class-4', '중급반', '중학생 이상 · 경력 6개월 이상', ''),
             ('competition', 'class-6', '시합반', '팀 클래스 · 대회 준비', ''),
             ('club', 'class-2', '동호회 · 단체 레슨', '단체 클래스 · 상담', ''),
             ('intl', '0820-09', '국제학교 · 해외 학생', '방학 단기 집중 레슨', 'intl'),
             ('private', '0820-04', '1:1 개인레슨', '60분 · 한 사람만 보는 수업', 'private'),
             ('guide', 'class-1', '수강 · 결제 안내', '시간표 · 수업 일정 달력', 'schedule'),
             ('photos', '0820-07', '클래스 사진', '토요일 수업 현장', '')]
    out = []
    for key, im, t, d, aid in cards:
        a = f' id="{aid}"' if aid else ''
        ext = 'jpg' if im.startswith('0820') else 'webp'
        out.append(f'<a class="ccard reveal"{a} href="{rel(r, key)}"><span class="ccard-img" style="background-image:url(\'{r}assets/img/{im}.{ext}\')" role="img" aria-label="{escape(t)} 수업 사진"></span><span class="ccard-txt"><b>{escape(t)}</b><span>{escape(d)}</span></span></a>')
    return f'''<section class="sec">
  <div class="wrap">
    <p class="lead">국가대표·프로 출신 하이앤드 코치진이 가르칩니다. 처음이라면 원데이 클래스로, 실력과 나이에 맞춰 정규 클래스로 이어집니다.</p>
    <div class="ccards mt">{"".join(out)}</div>
  </div>
</section>'''


def oneday_body(r):
    return f'''<section class="sec">
  <div class="wrap">
    <div class="oneday">
      <div class="price-card reveal">
        <span class="tag">오픈 이벤트 50% 할인가</span>
        <div class="pr">25,000원</div>
        <ul class="ticks">
          <li>토요일 12:00 · 13:30 · 16:30</li>
          <li>처음 배구를 하는 초등학생부터 성인까지</li>
          <li>정규 등록 시 원데이 비용 25,000원 차감</li>
          <li>수업 시작 10분 전 도착 · 실내 운동화, 물, 편한 운동복</li>
        </ul>
        <a class="btn w" href="{rel(r, 'oneday-apply')}">원데이 클래스 신청</a>
      </div>
      <div class="card reveal">
        <div class="cta-card-icon" style="margin-bottom:10px">{SN['ticket']}</div>
        <h2 class="t">원데이 클래스에서 하는 것</h2>
        <p>원데이 클래스는 정규 수업에 그대로 함께합니다. 실제 수업을 그대로 경험해 보세요.</p>
        <ol class="plain" style="margin-top:10px"><li>MAPS 워밍업</li><li>왜: 오늘 배울 동작의 원리</li><li>어떻게: 한 사람씩 정밀 교정</li><li>해보기: 게임</li></ol>
      </div>
    </div>
  </div>
</section>'''


def apply_body(r):
    return f'''<section class="sec">
  <div class="wrap">
    <div class="apply reveal">
      <div class="apply-main">
        <span class="tag">오픈 이벤트 50% 할인가</span>
        <div class="pr">25,000원</div>
        <p>토요일 12:00 · 13:30 · 16:30 중 원하시는 시간을 네이버 예약에서 골라 주세요.</p>
        <a class="btn naverbook" href="{NAVER_BOOK}" target="_blank" rel="noopener">{SN['naverN']}네이버 예약으로 신청하기</a>
      </div>
      <ul class="apply-list">
        <li><b>준비물</b>실내 운동화, 물, 편한 운동복</li>
        <li><b>도착</b>수업 시작 10분 전까지 와 주세요</li>
        <li><b>주차</b>건물 앞 주차 가능</li>
        <li><b>정규 등록</b>원데이 후 정규 수업을 등록하시면 원데이 비용 25,000원을 차감해 드립니다</li>
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
      <p>바른 자세와 기본기를 처음부터 제대로 익힙니다. 초등학생 학부모님께는 "우리 아이가 제대로 배우고 있다"는 안심을, 중·고등학생에게는 "내 몸이 이해되는 순간"을 드리고 싶습니다.</p>
      <ul class="ticks"><li>토요일 12:00 · 80분 정규수업</li><li>대상: 초·중·고</li><li>형제는 수강권을 함께 쓸 수 있습니다</li></ul>
      <div class="btns">{go(r, 'oneday-apply', '원데이 클래스로 시작', 'p')}{go(r, 'level', '성장 레벨 보기')}</div>
    </div>
  </div>
</section>'''


def beginner_body(r):
    return f'''<section class="sec">
  <div class="wrap split rev">
    <figure class="reveal">{img(r, 'class-3', '수강생들이 콘을 두고 리시브 자세를 연습하는 초급반 수업 장면', 1200, 1600)}</figure>
    <div class="reveal">
      <h2>기초 기술 습득 · 배구에 재미 붙이기</h2>
      <p>배구를 처음 시작하는 중학생 이상을 위한 반입니다. 패스, 서브, 리시브의 기본 매커니즘을 익히고, 팀워크 경험으로 배구의 재미를 발견합니다.</p>
      <ul class="ticks"><li>토요일 13:30 · 80분 정규수업</li><li>대상: 중학생 이상, 처음 배우는 분</li><li>처음 배우는 초등학생은 유소년반에서 시작합니다</li></ul>
      <div class="btns">{go(r, 'oneday-apply', '원데이 클래스로 시작', 'p')}{go(r, 'intermediate', '중급반 보기')}</div>
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
      <div class="btns">{go(r, 'oneday-apply', '원데이 클래스로 시작', 'p')}{go(r, 'level', '성장 레벨 보기')}</div>
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
      <p class="note">대상: 초등 고학년, 중·고등학생, 성인 · 수업 시간과 구성은 별도 상담으로 맞춰 드립니다.</p>
      <div class="btns"><a class="btn k" href="{KAKAO_CHAT}" target="_blank" rel="noopener">{SN['kakao']}카카오톡으로 상담</a>{go(r, 'level', '4단계 성장 레벨 보기')}</div>
    </div>
  </div>
</section>'''


def club_body(r):
    return f'''<section class="sec">
  <div class="wrap split rev">
    <figure class="reveal">{img(r, 'class-2', '함께 수업을 마친 하이앤드 수강생 단체 사진', 1600, 1200)}</figure>
    <div class="reveal">
      <h2>함께 배우는 배구</h2>
      <p>배구 동호회, 학교, 기관 단체 레슨은 인원과 목표에 맞춰 상담으로 진행합니다. 국가대표·프로 출신 하이앤드 코치진이 기본기부터 팀 전술까지 가르칩니다.</p>
      <ul class="ticks"><li>배구 동호회 단체 레슨</li><li>학교 · 기관 배구 수업 (상담)</li><li>지역 학교 배구 수업 진행 중</li></ul>
      <div class="btns"><a class="btn k" href="{KAKAO_CHAT}" target="_blank" rel="noopener">{SN['kakao']}단체 레슨 문의</a>{go(r, 'intl', '국제학교 · 해외 학생')}</div>
    </div>
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
      <div class="btns"><a class="btn k" href="{KAKAO_CHAT}" target="_blank" rel="noopener">{SN['kakao']}카카오톡으로 예약 문의</a></div>
    </div>
  </div>
</section>'''


def intl_body(r):
    return f'''<section class="sec intl">
  <div class="wrap">
    <h2>국제학교 · 해외 거주 학생 배구 레슨</h2>
    <p class="lead">국제학교 · 외국인학교 학생과, 방학마다 한국을 찾는 해외 거주 학생도 함께 배웁니다. 국가대표·프로 출신 하이앤드 코치진이 지도합니다.</p>
    <p class="intl-en" lang="en">Volleyball lessons for international school students and families visiting Korea during school breaks, coached by a former Korean national team player.</p>
    <div class="intl-grid mt">
      <div class="intl-card reveal"><span class="n">01</span><h3>익숙한 배구 용어로</h3><p>Underpass · Set · Spike · Serve. 해외 학교와 클럽에서 쓰던 용어를 함께 써서, 영어가 편한 아이들도 자연스럽게 적응합니다. 영어 수업이 아니라 익숙한 용어로 몸의 움직임을 이해하는 데 초점을 둡니다.</p></div>
      <div class="intl-card reveal"><span class="n">02</span><h3>한 명 한 명, 기본기 교정</h3><p>팀 훈련과는 별개로 리시브할 때 발의 위치, 공을 맞히는 팔의 각도, 스파이크를 위한 몸의 움직임을 세밀하게 교정합니다. 작아 보이는 차이가 쌓여 실력의 차이가 됩니다.</p></div>
      <div class="intl-card reveal"><span class="n">03</span><h3>방학마다 이어지는 성장</h3><p>첫 방학에는 기본기, 다음 방학에는 기술 향상, 그다음에는 실전. 매번 처음부터 다시 시작하지 않고 지난 훈련을 다음 방학으로 이어갑니다.</p></div>
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
        <tr><td>12:00</td><td><a href="{rel(r, 'youth')}">유소년반</a> (80분)</td><td>초·중·고</td><td>가능</td></tr>
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


def photos_body(r):
    grid = ''.join(
        f'<button class="insta-item" type="button" onclick="openLb(\'{r}assets/img/0820-{i + 1:02d}.jpg\')" aria-label="사진 크게 보기: {escape(a)}">{img(r, f"0820-{i + 1:02d}", "하이앤드 토요일 수업: " + a, 1200, 900)}</button>'
        for i, a in enumerate(PHOTOS_0820))
    more = [('class-1', '체육관에서 수강생들이 리시브를 연습하는 토요일 수업 장면', 720, 960),
            ('class-2', '수업을 마친 하이앤드 수강생 단체 사진', 1600, 1200),
            ('class-3', '콘을 두고 리시브 자세를 연습하는 수강생들', 1200, 1600),
            ('class-4', '공 카트 옆에서 패스를 연습하는 청소년 수강생', 1200, 1600),
            ('class-5', '코치 설명을 듣는 어린이 수강생들', 1200, 1600),
            ('class-6', '점프해서 스파이크를 하는 수강생', 1200, 1600)]
    grid += ''.join(
        f'<button class="insta-item" type="button" onclick="openLb(\'{r}assets/img/{n}.webp\')" aria-label="사진 크게 보기: {escape(a)}">{img(r, n, a, w, h)}</button>'
        for n, a, w, h in more)
    vids = ''.join(
        f'<div class="reel-slide" data-idx="{i}"><video src="{r}4.%20%EC%88%98%EC%97%85%20%EC%82%AC%EC%A7%84/%EB%8F%99%EC%98%81%EC%83%81/{i + 1}.mp4" loop muted playsinline preload="none" aria-label="하이앤드 수업 영상 {i + 1}"></video><div class="reel-play-layer" id="rpl{i}"><div class="reel-play-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></div></div></div>'
        for i in range(4))
    dots = ''.join(f'<div class="s-dot{" active" if i == 0 else ""}"></div>' for i in range(5))
    return f'''<section class="sec">
  <div class="wrap">
    <p class="lead">토요일 유소년반 · 초급반 · 중급반 수업 현장입니다. 기본기부터 차근차근 배우는 모습을 담았습니다.</p>
    <div class="insta-grid mt">{grid}</div>
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
</section>
<div class="lightbox" id="lightbox" onclick="closeLb()"><button class="lb-close" onclick="closeLb()" aria-label="닫기">{SN['close']}</button><img id="lbImg" src="data:," alt="크게 본 수업 사진"></div>'''


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
</section>'''


def soon_body(r):
    return f'''<section class="sec"><div class="wrap center"><p class="lead">준비 중입니다. 소식은 인스타그램과 블로그에서 먼저 전해 드립니다.</p><div class="btns"><a class="btn s" href="{INSTA}" target="_blank" rel="noopener">인스타그램</a><a class="btn s" href="{BLOG}" target="_blank" rel="noopener">블로그</a></div></div></section>'''


# ════════════════════════ 본문: CONTACT ════════════════════════
CONTACT_FAQ = [
    ('배구를 처음 하는 초등학생도 배울 수 있나요?', '네. 유소년반은 처음 배우는 초등학생부터 시작합니다. 먼저 원데이 클래스(25,000원)로 수업을 경험해 보실 수 있습니다.'),
    ('누가 가르치나요?', '국가대표·프로 출신 하이앤드 코치진이 가르칩니다. 헤드코치 김재휘(국가대표 7년 · 프로(V리그) 10년, 선수 17년)는 FIVB 코치 레벨1, 전문스포츠지도사 2급(배구) 자격이 있습니다.'),
    ('수업은 언제 있나요?', '매주 토요일 12:00 유소년반, 13:30 초급반, 16:30 중급반이 있고 각 80분입니다. 개인레슨(60분)은 따로 예약합니다.'),
    ('수강료는 얼마인가요?', '원데이 클래스는 25,000원(오픈 이벤트 50% 할인가)입니다. 개인레슨은 1회 25만 원, 10회 등록 시 회당 20만 원입니다. 정규 수강권은 카카오톡 상담으로 안내드립니다.'),
    ('준비물은 무엇인가요?', '실내 운동화, 물, 편한 운동복을 준비해 주세요. 수업 시작 10분 전까지 도착해 주세요.'),
    ('주차할 수 있나요?', '건물 앞에 주차할 수 있습니다.'),
    ('원데이 클래스 후 정규 등록하면 어떻게 되나요?', '정규 수업을 등록하시면 원데이 비용 25,000원을 차감해 드립니다.'),
    ('형제가 함께 다녀도 되나요?', '네. 형제는 모든 수강권을 함께 나눠 쓸 수 있습니다.'),
    ('결제는 어떻게 하나요?', '원데이 클래스는 네이버 예약으로 신청하고, 그 밖의 수강료는 계좌이체 · 현금 · 카드 모두 가능합니다.'),
    ('국제학교 학생도 배울 수 있나요?', '네. 국제학교 · 외국인학교 학생과 방학마다 한국을 찾는 해외 거주 학생도 함께 배웁니다. 익숙한 영어 배구 용어를 함께 쓰고, 방학 단기 집중 레슨은 상담으로 일정을 맞춰 드립니다.'),
]

LOCAL_FAQ = [
    ('상암·은평·고양 근처에 배구학원이 있나요?', '상암 인근 · 현천동 180-1에 프리미엄 배구 아카데미 하이앤드가 있습니다. 매주 토요일 유소년반(12:00), 초급반(13:30), 중급반(16:30) 수업을 하고, 개인레슨은 따로 예약합니다.'),
    ('국가대표 출신 코치에게 배울 수 있나요?', '네. 하이앤드는 국가대표·프로 출신 코치진이 가르칩니다. 헤드코치 김재휘(국가대표 7년 · 프로(V리그) 10년)는 2018 아시안게임 은메달, V리그 우승 4회 경력과 FIVB 코치 레벨1 자격이 있습니다.'),
    ('초등학생 배구교실도 있나요?', '네. 유소년반(초·중·고)은 토요일 12:00, 80분 수업입니다. 처음 배우는 초등학생도 원데이 클래스로 시작할 수 있습니다.'),
    ('배구학원 비용은 얼마인가요?', '원데이 클래스 25,000원(오픈 이벤트 50% 할인가), 개인레슨 1회 25만 원(10회 등록 시 회당 20만 원)입니다. 정규 수강권은 카카오톡 상담으로 안내드립니다.'),
    ('주차할 수 있나요?', '건물 앞에 주차할 수 있습니다.'),
]


def map_block():
    return f'''<div class="loc-map"><iframe src="{GOOGLE_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="하이앤드 발리볼 아카데미 상암점 위치 지도"></iframe></div>
      <div class="loc-btns"><a class="loc-btn naver" href="{NAVER_MAP}" target="_blank" rel="noopener">{SN['naverN']}네이버 지도 열기</a><a class="loc-btn google" href="{GOOGLE_MAP}" target="_blank" rel="noopener">{SN['google']}Google 지도</a></div>'''


def contact_body(r):
    return f'''<section class="sec" id="map">
  <div class="wrap">
    <div class="contact-grid">
      <div class="reveal">{map_block()}</div>
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
    return f'''<section class="sec"><div class="wrap">{faq_html(CONTACT_FAQ)}<div class="btns">{go(r, 'ask', '더 궁금한 점 문의하기')}</div></div></section>'''


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
                   ('method', '알고 하면 쉬운 배구', '왜 → 어떻게 → 해보기. 이유를 알고 하는 반복으로 기본기를 만듭니다.', ''),
                   ('oneday', '원데이 클래스 25,000원', '토요일 12:00 · 13:30 · 16:30. 정규 수업에 그대로 함께합니다.', '')])}
  </div>
</section>
<section class="sec alt">
  <div class="wrap">
    <h2>상암 · 은평 · 고양 덕양 가까이에 있습니다</h2>
    <div class="areas"><div>상암 · 수색 · DMC</div><div>은평</div><div>고양 덕양</div></div>
    <p class="note">건물 앞 주차 가능 · 수업 시작 10분 전 도착 · <a href="{rel(r, 'contact')}">오시는 길</a></p>
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
                {'@type': 'Offer', 'price': '25000', 'priceCurrency': 'KRW', 'category': '오픈 이벤트 50% 할인가',
                 'url': NAVER_BOOK, 'availability': 'https://schema.org/InStock'})
YOUTH = course('youth', '유소년 배구교실 (유소년반)', '초·중·고 대상 80분 정규수업. 바른 자세와 기본기를 처음부터 제대로 익힙니다.', ('12:00',))
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
    'youth': (youth_body, [YOUTH], []), 'beginner': (beginner_body, [BEGINNER], []), 'intermediate': (intermediate_body, [INTER], []),
    'regular-reviews': (reviews_body, [], []), 'competition': (competition_body, [], []), 'club': (club_body, [], []), 'private': (private_body, [PRIVATE], []), 'intl': (intl_body, [], []),
    'guide': (guide_body, [], FIREBASE + ['assets/js/schedule.js']), 'photos': (photos_body, [], ['assets/js/media.js']),
    'story': (story_body, [], []), 'hiand': (soon_body, [], []), 'note': (soon_body, [], []),
    'contact': (contact_body, [], []), 'local': (local_body, [faq_ld(LOCAL_FAQ)], []), 'faq': (faq_body, [faq_ld(CONTACT_FAQ)], []),
    'ask': (ask_body, [], []),
}


def write(path, text):
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
- 원데이 클래스: 25,000원 (오픈 이벤트 50% 할인가), 토요일 12:00 · 13:30 · 16:30, 네이버 예약. 정규 등록 시 원데이비 차감
- 유소년반 (초·중·고): 토요일 12:00, 80분
- 초급반 (중학생 이상 입문): 토요일 13:30, 80분
- 중급반 (중학생 이상, 배구 경력 6개월 이상): 토요일 16:30, 80분
- 개인레슨 60분: 1회 25만 원, 10회 등록 시 회당 20만 원
- 정규 수강권: 카카오톡 상담으로 안내
- 시합반 (팀 클래스): 연령별 대표팀 선발 · 대회 목표, 초등 고학년 · 중고등 · 성인, 상담
- 동호회 · 단체 레슨: 동호회 · 학교 · 기관, 상담
- 국제학교 · 외국인학교 · 해외 거주 학생 배구 레슨: 익숙한 영어 배구 용어 사용, 방학 단기 집중 레슨 · 캠프, 학교 배구팀 트라이아웃 준비 (상담)

## 수업 방식
- 하이앤드 코칭 시스템 "알고 하면 쉬운 배구": 하이앤드 3단계 수업 (Why · How · Play = 왜 → 어떻게 → 해보기)
- 하이앤드 MAPS 워밍업 (Mobility · Activation · Plyometrics · Stability)
- 하이앤드 정밀 교정: 묻기 → 짚기 → 영상 확인 (리시브 몸 방향 · 플랫폼, 스파이크 치킨윙 교정)
- 하이앤드 운동일지 "Today & Next Ball"
- 줄 서서 기다리지 않고 모두 동시에 움직이는 80분 정규수업
- 하이앤드 성장 레벨 LV.1 입문 · LV.2 기본 · LV.3 심화 · LV.4 시합
- 200평 풀코트

## 이런 검색에 해당합니다
- 프리미엄 배구 아카데미, 프리미엄 배구학원, 배구학원, 배구교실, 배구 레슨, 배구 아카데미, 배구 개인레슨, 배구 원데이 클래스
- 초등학생 배구, 유소년 배구교실, 어린이 배구, 초등학교 배구부 준비, 중학생 배구
- 성인 배구 취미, 배구 초보, 배구 기본기, 배구 자세 교정
- 국가대표 출신 코치 배구 레슨, 프로 출신 배구 코치
- 국제학교 배구, 국제학교 배구 레슨, 외국인학교 배구, 해외 거주 학생 방학 배구 레슨, volleyball lessons for international school students
- 지역: 상암, 수색, DMC, 은평, 고양, 덕양, 서울 서북부

## 위치 · 연락
- 상암 인근 · 현천동 180-1 (건물 앞 주차 가능)
- 전화: 010-4463-1177
- 카카오톡 채널: http://pf.kakao.com/_pCEzX
- 이메일: highendv0lly@gmail.com

## 주요 페이지
- 하이앤드 소개: [주소]/about/
- 코칭 스태프 (김재휘 헤드코치 · 황준태 코치): [주소]/about/coaches/
- 하이앤드 코칭 시스템: [주소]/method/
- 4단계 성장 레벨: [주소]/method/level/
- 클래스 전체 안내: [주소]/class/
- 원데이 클래스: [주소]/class/oneday/
- 원데이 클래스 신청: [주소]/class/oneday/apply/
- 유소년반: [주소]/class/regular/youth/
- 초급반: [주소]/class/regular/beginner/
- 중급반: [주소]/class/regular/intermediate/
- 개인레슨: [주소]/class/private/
- 국제학교 · 해외 학생: [주소]/class/international/
- 시합반 (팀 클래스): [주소]/class/team/competition/
- 동호회 · 단체 레슨: [주소]/class/group/club/
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
</style>
'''


def home_legacy():
    s = open(os.path.join(ROOT_DIR, 'tools', 'home_legacy.html'), encoding='utf-8').read()

    def swap(old, new):
        nonlocal s
        assert s.count(old) == 1, old[:60]
        s = s.replace(old, new)

    # 0) 브랜드 표기 기준 v2 (2026-10-27)
    swap('부상 없이 오래 할 수 있는 배구, 즐겁게 지속할 수 있는 배구', '안전하게 오래 하는 배구, 즐겁게 지속하는 배구')
    swap('국가대표 기준 고급 기술 습득. 실질적 팀플레이 완성 및 경기 분석.', '국가대표·프로 선수의 훈련 방식을 바탕으로 한 고급 기술 습득. 실질적 팀플레이 완성 및 경기 분석.')
    swap('개인별 목표 맞춤 집중 지도. 국가대표 수준 기술 전수.', '개인별 목표 맞춤 집중 지도. 국가대표·프로 출신 코치진의 1:1 기술 지도.')

    # 1) 머리말: 검색 제목·설명문·공유 미리보기·구조화 데이터
    h = head('home', '', [])
    seo = h[h.index('<title>'):h.index(SN['favicon'])].replace('<meta name="theme-color" content="#003960">\n', '')
    swap('<title>하이앤드 발리볼 아카데미 | HIGH END VOLLEYBALL ACADEMY</title>', seo.strip())
    site = {'@type': 'WebSite', '@id': BASE + '#site', 'url': BASE, 'name': NAME, 'inLanguage': 'ko-KR',
            'publisher': {'@id': BASE + '#org'}}
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
    return s


if __name__ == '__main__':
    build()
