#!/usr/bin/env python3
"""하이앤드 여러 페이지 홈페이지 생성기.

문구 원본: 구글 드라이브 2026-10-26_홈페이지시안/v2_여러페이지 (검수결과_v2 반영)
사실·표기 규칙: highend-ai-office/CLAUDE.md
실행: 저장소 맨 위에서 `python3 tools/build_site.py`
결과: index.html, about/, method/, class/, story/, contact/, sangam-volleyball-academy/,
      404.html, robots.txt, sitemap.xml, llms.txt (모두 완성된 정적 HTML·텍스트)
"""
import json
import os
import urllib.parse
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

PAGES = {
    'home': {'path': '', 'title': '상암·고양 배구학원 하이앤드 발리볼 아카데미 | 국가대표 출신 코치',
             'desc': '상암 인근 · 현천동 180-1 배구학원 하이앤드 발리볼 아카데미. 국가대표 7년 · 프로(V리그) 10년 김재휘 코치가 초등학생부터 성인까지 가르칩니다. 원데이 클래스 25,000원, 문의 010-4463-1177'},
    'about': {'path': 'about/', 'title': '국가대표 출신 김재휘 코치 | 하이앤드 발리볼 아카데미', 'label': 'ABOUT',
              'desc': '국가대표 7년 · 프로(V리그) 10년, 선수 17년 김재휘 코치. 2018 아시안게임 은메달, V리그 우승 4회, FIVB 코치 레벨1. 상암 인근 하이앤드 발리볼 아카데미, 원데이 25,000원 · 010-4463-1177'},
    'method': {'path': 'method/', 'title': '알고 하면 쉬운 배구 | 하이앤드 수업 방식', 'label': 'METHOD',
               'desc': '알고 하면 쉬운 배구. 왜 → 어떻게 → 해보기, 이유를 알고 하는 반복으로 가르칩니다. MAPS 워밍업과 생체역학 기반 정밀 교정. 상암 인근 하이앤드, 원데이 25,000원 · 010-4463-1177'},
    'class': {'path': 'class/', 'title': '배구 원데이 클래스 · 유소년 배구교실 · 개인레슨 | 하이앤드', 'label': 'CLASS',
              'desc': '배구 원데이 클래스 25,000원(오픈 이벤트 50% 할인가), 유소년반 · 초급반 · 중급반 80분 정규수업, 국제학교 학생 배구 레슨, 1:1 개인레슨. 상암 인근 · 현천동 180-1, 국가대표 출신 코치. 문의 010-4463-1177'},
    'story': {'path': 'story/', 'title': '하이앤드 수업 이야기 · 배구 노트', 'label': 'STORY',
              'desc': '하이앤드 발리볼 아카데미 토요일 수업 이야기와 수업 사진 · 영상. 상암 인근 배구교실, 국가대표 출신 김재휘 코치. 원데이 클래스 25,000원 · 문의 010-4463-1177'},
    'contact': {'path': 'contact/', 'title': '오시는 길 · 자주 묻는 질문 | 하이앤드 발리볼 아카데미', 'label': 'CONTACT',
                'desc': '하이앤드 발리볼 아카데미 오시는 길(상암 인근 · 현천동 180-1, 건물 앞 주차)과 자주 묻는 질문. 수업 시간, 수강료, 준비물 안내. 원데이 25,000원, 카카오톡 상담 · 010-4463-1177'},
    'local': {'path': 'sangam-volleyball-academy/', 'title': '상암·은평·고양 배구학원 | 하이앤드 발리볼 아카데미', 'label': '상암·은평·고양 배구학원',
              'desc': '상암·은평·고양 배구학원 하이앤드 발리볼 아카데미. 상암 인근 · 현천동 180-1, 국가대표 출신 코치가 초등학생부터 성인까지 가르칩니다. 원데이 25,000원, 토요일 수업 · 010-4463-1177'},
}

# ── 메뉴 ([ ] 확인 대기인 Hi:And Day · 배구 노트는 숨김) ──
MENU = [
    ('about', 'ABOUT', [('하이앤드 소개', '#intro'), ('김재휘 코치 경력', '#career'), ('황준태 코치', '#hwang'), ('시설 (200평 풀코트)', '#place')]),
    ('method', 'METHOD', [('알고 하면 쉬운 배구', '#know'), ('MAPS 워밍업', '#maps'), ('정밀 교정', '#fix'), ('수업 80분 흐름', '#flow'), ('4단계 성장 레벨', '#level')]),
    ('class', 'CLASS', [('원데이 클래스 예약', '#oneday'), ('유소년반', '#youth'), ('초급반 · 중급반', '#group'), ('국제학교 · 해외 학생', '#intl'), ('개인레슨', '#private'), ('시간표 · 수강 안내', '#schedule')]),
    ('story', 'STORY', [('수업 이야기', '#class-story'), ('수업 사진 · 영상', '#gallery')]),
    ('contact', 'CONTACT', [('오시는 길', '#map'), ('상암·은평·고양 배구학원', '@local'), ('자주 묻는 질문', '#faq'), ('상담하기', '#ask')]),
]


def ver(path):
    import hashlib
    return hashlib.md5(open(os.path.join(ROOT_DIR, path), 'rb').read()).hexdigest()[:8]


def url(key, frag=''):
    return BASE + PAGES[key]['path'] + frag


def rel(root, key, frag=''):
    return root + PAGES[key]['path'] + frag if PAGES[key]['path'] else (root or './') + frag


def img(root, name, alt, w, h, lazy=True, cls=''):
    attrs = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="{root}assets/img/{name}.webp" alt="{escape(alt)}" width="{w}" height="{h}"{attrs}>'


def media_path(root, p):
    return root + urllib.parse.quote(p)


# ── 구조화 데이터 ──
SAME_AS = [INSTA, YOUTUBE, NAVER_PLACE, BLOG, KAKAO]


def org_graph():
    return [
        {'@type': 'Organization', '@id': BASE + '#org', 'name': NAME, 'alternateName': NAME_EN, 'url': BASE,
         'logo': BASE + 'assets/img/logo.png', 'email': EMAIL, 'telephone': PHONE_INTL, 'sameAs': SAME_AS,
         'founder': {'@id': url('about') + '#kim'}},
        {'@type': 'SportsActivityLocation', '@id': BASE + '#place', 'name': NAME + ' 상암점', 'url': BASE,
         'image': BASE + 'assets/img/og-image.jpg', 'telephone': PHONE_INTL, 'email': EMAIL,
         'description': '상암 인근 배구 아카데미. ' + CAREER + ' 김재휘 코치와 국가대표 · 프로 출신 코치진이 초등학생부터 성인까지 가르칩니다.',
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


def breadcrumb(key):
    if key == 'home':
        return None
    items = [{'@type': 'ListItem', 'position': 1, 'name': 'HOME', 'item': BASE},
             {'@type': 'ListItem', 'position': 2, 'name': PAGES[key]['label'], 'item': url(key)}]
    return {'@type': 'BreadcrumbList', 'itemListElement': items}


def faq_ld(faqs):
    return {'@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]}


def faq_html(faqs, first_open=True):
    out = []
    for i, (q, a) in enumerate(faqs):
        op = ' open' if (i == 0 and first_open) else ''
        out.append(f'<details{op}><summary>{escape(q)}</summary><p>{escape(a)}</p></details>')
    return '<div class="faq">' + ''.join(out) + '</div>'


# ── 공통 틀 ──
def head(key, root, extra_ld, extra_head=''):
    p = PAGES[key]
    graph = org_graph() + [x for x in [breadcrumb(key)] + extra_ld if x]
    if key == 'home':
        graph.append({'@type': 'WebSite', '@id': BASE + '#site', 'url': BASE, 'name': NAME, 'inLanguage': 'ko-KR',
                      'publisher': {'@id': BASE + '#org'}})
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(p['title'])}</title>
<meta name="description" content="{escape(p['desc'])}">
<link rel="canonical" href="{url(key)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{escape(p['title'])}">
<meta property="og:description" content="{escape(p['desc'])}">
<meta property="og:url" content="{url(key)}">
<meta property="og:image" content="{BASE}assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="하이앤드 발리볼 아카데미 수강생 단체 사진">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(p['title'])}">
<meta name="twitter:description" content="{escape(p['desc'])}">
<meta name="twitter:image" content="{BASE}assets/img/og-image.jpg">
{SN['favicon']}
<link rel="preload" href="{root}fonts/Paperlogy-9Black.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}fonts/Paperlogy-4Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/css/base.css?v={ver('assets/css/base.css')}">
<link rel="stylesheet" href="{root}assets/css/site.css?v={ver('assets/css/site.css')}">
{extra_head}{ld(graph)}
</head>'''


def header(key, root):
    items = []
    for k, label, subs in MENU:
        links = ''.join(
            f'<a href="{rel(root, "local") if f == "@local" else rel(root, k, f)}">{escape(t)}</a>' for t, f in subs)
        on = ' on' if (key == k or (key == 'local' and k == 'contact')) else ''
        cur = ' aria-current="page"' if key == k else ''
        items.append(f'<div class="nv{on}"><a href="{rel(root, k)}"{cur}>{label}</a><div class="dd">{links}</div></div>')
    m_items = []
    for k, label, subs in MENU:
        links = f'<a href="{rel(root, k)}">{label} 전체 보기</a>' + ''.join(
            f'<a href="{rel(root, "local") if f == "@local" else rel(root, k, f)}">{escape(t)}</a>' for t, f in subs)
        m_items.append(f'<details><summary>{label}</summary>{links}</details>')
    home_cur = ' aria-current="page"' if key == 'home' else ''
    return f'''<body data-page="{key}">
<script>window.HE_ROOT="{root}";</script>
<a class="skip" href="#main">본문 바로가기</a>
<header class="hd">
  <div class="hd-in">
    <a class="hd-logo" href="{rel(root, 'home')}"{home_cur}><img src="{root}assets/img/logo.webp" alt="하이앤드 발리볼 아카데미 로고" width="36" height="36"><span><b>HIGH END</b><small>VOLLEYBALL ACADEMY</small></span></a>
    <nav class="gnb" aria-label="주요 메뉴">
      <div class="nv{' on' if key == 'home' else ''}"><a href="{rel(root, 'home')}">HOME</a></div>
      {''.join(items)}
    </nav>
    <div class="hd-act">
      <a class="hd-btn p" href="{rel(root, 'class', '#oneday')}">원데이 예약</a>
      <a class="hd-btn s" href="{root}dashboard.html">회원 로그인</a>
      <button class="hd-menu" id="menuBtn" aria-label="메뉴 열기" aria-expanded="false" aria-controls="mnav" data-close='{SN['close']}'>{SN['menu']}</button>
    </div>
  </div>
</header>
<nav class="mnav" id="mnav" aria-label="휴대폰 메뉴">
  <a class="m-home" href="{rel(root, 'home')}">HOME</a>
  {''.join(m_items)}
  <div class="m-cta"><a href="{rel(root, 'class', '#oneday')}">원데이 예약</a><a href="{root}dashboard.html">회원 로그인</a></div>
</nav>'''


def subnav(label, links):
    return f'<nav class="subnav" aria-label="{label} 하위 메뉴"><div>' + ''.join(
        f'<a href="{h}">{escape(t)}</a>' for t, h in links) + '</div></nav>'


def crumbs(key, root):
    return (f'<nav class="crumb wrap" aria-label="현재 위치"><ol><li><a href="{rel(root, "home")}">HOME</a></li>'
            f'<li aria-current="page">{escape(PAGES[key]["label"])}</li></ol></nav>')


def cta_band(root, title, sub='', buttons=None):
    # 모든 페이지 하단: 밝은 바탕 + 원데이 신청 박스 · 수업 문의 박스 (대표 지시 2026-10-26, buttons는 쓰지 않음)
    s = f'<p class="cta2-sub">{sub}</p>' if sub else ''
    return f'''<section class="sec cta2"><div class="wrap"><div class="cta2-in reveal"><h2>{title}</h2>{s}
<div class="cta2-boxes">
<a class="cta2-box p" href="{NAVER_BOOK}" target="_blank" rel="noopener"><b>원데이 클래스 신청하기</b><span class="go">네이버 예약 →</span></a>
<a class="cta2-box s" href="{KAKAO_CHAT}" target="_blank" rel="noopener"><b>수업 문의하기</b><span class="go">카카오톡 상담 →</span></a>
</div></div></div></section>'''


def footer(root):
    return f'''<footer class="ft">
  <div class="wrap">
    <div class="ft-top">
      <div>
        <div class="ft-name">{NAME}</div>
        <div class="ft-info"><span>대표 김재휘</span><span>{ADDR}</span><span><a href="tel:01044631177">{PHONE}</a></span><span><a href="mailto:{EMAIL}">{EMAIL}</a></span></div>
        <nav class="ft-nav" aria-label="하단 메뉴"><a href="{rel(root, 'home')}">HOME</a><a href="{rel(root, 'about')}">ABOUT</a><a href="{rel(root, 'method')}">METHOD</a><a href="{rel(root, 'class')}">CLASS</a><a href="{rel(root, 'story')}">STORY</a><a href="{rel(root, 'contact')}">CONTACT</a><a href="{rel(root, 'local')}">상암·은평·고양 배구학원</a><a href="{root}dashboard.html">회원 로그인</a></nav>
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
<div class="float-bar">
  <a href="tel:01044631177" class="float-btn fb-phone" title="전화 문의" aria-label="전화 문의">{SN['phone']}</a>
  <a href="{KAKAO}" target="_blank" rel="noopener" class="float-btn fb-kakao" title="카카오 채널" aria-label="카카오톡 채널">{SN['kakao']}</a>
  <a href="{INSTA}" target="_blank" rel="noopener" class="float-btn fb-insta" title="인스타그램" aria-label="인스타그램">{SN['insta']}</a>
  <a href="{NAVER_PLACE}" target="_blank" rel="noopener" class="float-btn fb-naver" title="네이버 플레이스" aria-label="네이버 플레이스">{SN['naver']}</a>
</div>'''


def page(key, body, extra_ld=(), scripts=(), extra_head=''):
    root = '' if key == 'home' else '../'
    sc = ''.join(f'<script src="{s if s.startswith("http") else root + s + "?v=" + ver(s)}" defer></script>' for s in scripts)
    return (head(key, root, list(extra_ld), extra_head) + '\n' + header(key, root) + '\n<main id="main">\n'
            + body(root) + '\n</main>\n' + footer(root) + '\n'
            + f'<script src="{root}assets/js/site.js?v={ver("assets/js/site.js")}" defer></script>{sc}\n</body>\n</html>\n')


# ════════════════════════ 페이지 본문 ════════════════════════

HERO_VIDEO = 'intro'   # 'intro' = 하이라이트 첫 영상(아카데미 소개, 앞 10.4초) / 'court' = 가로 경기 영상
HERO_VIDEOS = {'intro': ('hero-intro', '하이앤드 수업 장면 영상'), 'court': ('hero-court', '하이앤드 체육관 경기 장면 영상')}


def home_body(r):
    vid, vlabel = HERO_VIDEOS[HERO_VIDEO]
    return f'''<section id="hero">
  <div class="hero-bg"><video id="heroVideo" muted loop playsinline preload="none" poster="{r}assets/img/{vid}-poster.webp" data-src="{r}assets/video/{vid}.mp4" aria-label="{vlabel}"></video></div>
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <div class="hero-text">
      <div class="hero-eyebrow">HIGH END VOLLEYBALL ACADEMY</div>
      <h1 class="hero-title">국가대표와 함께하는<br><em>배구교실</em></h1>
      <p class="hero-sub">속도보다 방향, 결과보다 지속<br>가장 완벽한 기본을 가르치겠습니다<br><br>
        <strong style="color:var(--text);">FIVB 코치 레벨1 · 국가대표 7년 · 프로 10년</strong>
      </p>
      <div class="hero-btns">
        <a href="{NAVER_BOOK}" target="_blank" rel="noopener" class="btn-primary">원데이클래스 신청</a>
        <a href="{r}dashboard.html" class="btn-secondary">회원 로그인 · 예약</a>
      </div>
      <div class="hero-contact"><a href="tel:01044631177">010-4463-1177</a> &nbsp;·&nbsp; 매주 토요일 운영</div>
    </div>
    <div class="hero-image-wrap">
      <img src="{r}assets/img/coach-kim-profile.webp" alt="메인코치 김재휘: 대한민국 국가대표 2016~2022, 현대캐피탈·KB손해보험·우리카드·삼성화재" class="hero-img-main" width="721" height="960" fetchpriority="high">
      <div class="hero-img-badge"><div class="hib-num">7년</div><div class="hib-label">국가대표 경력</div></div>
    </div>
  </div>
</section>
<section class="sec" aria-label="코치 경력 요약">
  <div class="wrap">
    <div class="stats">
      <a class="stat reveal" href="{rel(r, 'about', '#career')}"><b>7년</b><span>국가대표 (2016~2022)</span></a>
      <a class="stat reveal" href="{rel(r, 'about', '#career')}"><b>10년</b><span>프로(V리그) 선수</span></a>
      <a class="stat reveal" href="{rel(r, 'about', '#career')}"><b>4회</b><span>V리그 우승</span></a>
      <a class="stat reveal" href="{rel(r, 'about', '#career')}"><b>은메달</b><span>2018 아시안게임</span></a>
      <a class="stat reveal" href="{rel(r, 'about', '#career')}"><b>FIVB</b><span>코치 레벨1</span></a>
    </div>
  </div>
</section>
<section class="sec alt">
  <div class="wrap">
    <h2 class="reveal">하이앤드를 알아보는 3가지 길</h2>
    <div class="ways">
      <a class="way reveal" href="{rel(r, 'about')}"><div class="k">ABOUT</div><div class="t">누가<br>가르치나요?</div><div class="d">{CAREER}</div></a>
      <a class="way reveal" href="{rel(r, 'method')}"><div class="k">METHOD</div><div class="t">어떻게<br>가르치나요?</div><div class="d">왜 → 어떻게 → 해보기</div></a>
      <a class="way reveal" href="{rel(r, 'class')}"><div class="k">CLASS</div><div class="t">어떤 수업이<br>있나요?</div><div class="d">원데이 · 유소년 · 초급·중급 · 개인레슨</div></a>
    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <h2 class="reveal">이런 분께 맞습니다</h2>
    <div class="fits">
      <a class="fit reveal" href="{rel(r, 'class', '#youth')}"><div class="t">초등학생 배구교실을 찾는 학부모님</div><p>우리 아이가 제대로 배우고 있다는 안심. 처음부터 바른 자세와 기본기를 익힙니다.</p></a>
      <a class="fit reveal" href="{rel(r, 'class', '#youth')}"><div class="t">배구부 · 엘리트를 준비하는 중·고등학생</div><p>왜 이렇게 움직여야 하는지 알면, 내 몸이 이해되는 순간을 경험합니다.</p></a>
      <a class="fit reveal" href="{rel(r, 'class', '#group')}"><div class="t">취미로 배구를 배우고 싶은 성인</div><p>처음 배우는 분도, 기본기를 다시 잡고 싶은 분도. 안전하게 오래 하는 배구.</p></a>
    </div>
  </div>
</section>
{cta_band(r, '처음부터 제대로.', '토요일 12:00 · 13:30 · 16:30, 원데이 클래스로 먼저 만나 보세요.', [('원데이 클래스 예약', rel(r, 'class', '#oneday'), 'w'), ('오시는 길 · 상담', rel(r, 'contact'), 'k')])}'''


def about_body(r):
    return f'''{crumbs('about', r)}
{subnav('ABOUT', [('하이앤드 소개', '#intro'), ('김재휘 코치 경력', '#career'), ('황준태 코치', '#hwang'), ('시설', '#place')])}
<section class="ph" id="intro">
  <div class="wrap">
    <p class="eyebrow">ABOUT HIGH END</p>
    <h1>가장 완벽한 기본,<br>그것이 우리가 말하는<br>하이앤드입니다</h1>
    <p class="lead">하이앤드 발리볼 아카데미는 국가대표 7년, 프로(V리그) 10년, 선수 17년을 뛴 김재휘 코치가 세운 배구 아카데미입니다. 상암 인근 · 현천동 180-1에서 초등학생부터 성인까지 배구를 가르칩니다.</p>
    <p class="lead">하이앤드의 목표는 하나입니다. 수강생이 "김재휘를 만나 내 배구가 완전히 바뀌었다"고 말하는 것. 그래서 동작을 외우게 하지 않고, 왜 그렇게 움직이는지 이해하게 합니다.</p>
  </div>
</section>
<section class="sec alt" id="career">
  <div class="wrap">
    <p class="eyebrow">HEAD COACH</p>
    <h2>김재휘 코치</h2>
    <div class="career mt">
      <div class="reveal">
        <img class="coach-photo" src="{r}assets/img/coach-kim-profile.webp" alt="메인코치 김재휘 프로필: 대한민국 국가대표 2016~2022, 현대캐피탈·KB손해보험·우리카드·삼성화재" width="721" height="960" loading="lazy" decoding="async">
      </div>
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
        <div class="reveal">
          <img class="coach-photo" src="{r}assets/img/coach-hwang-profile.jpg" alt="황준태 코치 프로필: 리베로, 서울 우리카드 배구단 2022~2024, 대통령배 배구대회 리베로상" width="720" height="960" loading="lazy" decoding="async">
        </div>
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
  </div>
</section>
<section class="sec">
  <div class="wrap center reveal">
    <h2>선수 경험을 "가르치는 말"로 바꿉니다</h2>
    <p class="lead">국가대표와 V리그에서 쌓은 경험에, 국제 기준의 지도자 교육을 더했습니다. 하이앤드 수업은 "잘하는 사람의 감"이 아니라, 쉽게 이해할 수 있는 원리로 설명합니다. 국제학교와 해외 체류 학생을 지도한 경험도 있습니다.</p>
    <div class="btns"><a class="btn s" href="{rel(r, 'method')}">수업 방식 자세히 보기</a></div>
  </div>
</section>
<section class="sec" id="place">
  <div class="wrap">
    <p class="eyebrow">FACILITY</p>
    <h2>200평 풀코트에서 배웁니다</h2>
    <div class="photos">
      <figure class="reveal">{img(r, 'class-1', '하이앤드 200평 풀코트 체육관에서 진행되는 배구 수업 전경', 720, 960)}</figure>
      <figure class="reveal">{img(r, 'class-3', '네트 앞에서 수강생들이 리시브 자세를 연습하는 수업 장면', 1200, 1600)}</figure>
    </div>
    <p class="note">상암 인근 · 현천동 180-1 · 건물 앞 주차 가능 · <a href="{rel(r, 'contact', '#map')}">오시는 길 보기</a></p>
  </div>
</section>
{cta_band(r, '국가대표 출신 코치에게 직접 배워 보세요')}'''


def method_body(r):
    return f'''{crumbs('method', r)}
{subnav('METHOD', [('알고 하면 쉬운 배구', '#know'), ('MAPS 워밍업', '#maps'), ('정밀 교정', '#fix'), ('수업 80분 흐름', '#flow'), ('4단계 성장 레벨', '#level')])}
<section class="ph" id="know">
  <div class="wrap">
    <p class="eyebrow">OUR METHOD</p>
    <h1>알고 하면<br>쉬운 배구</h1>
    <p class="lead">같은 동작을 백 번 반복해도, 왜 하는지 모르면 몸은 쉽게 바뀌지 않습니다. 하이앤드는 <strong>이유를 알고 하는 반복</strong>으로 가르칩니다. 수강생이 스스로 동작을 이해하고, 스스로 고칠 수 있게 하는 것이 목표입니다.</p>
    <div class="grid3 mt">
      <div class="card reveal"><div class="big-letter">왜</div><p class="mt" style="margin-top:12px">이 동작이 왜 필요한지, 몸이 어떻게 움직여야 하는지 먼저 설명합니다.</p></div>
      <div class="card reveal"><div class="big-letter">어떻게</div><p style="margin-top:12px">한 사람씩 자세를 보고, 몸에 맞게 정밀하게 교정합니다.</p></div>
      <div class="card reveal"><div class="big-letter">해보기</div><p style="margin-top:12px">배운 원리를 게임과 실전 상황에서 직접 써 봅니다.</p></div>
    </div>
    <div class="principle reveal"><div class="t">김재휘 코치가 가장 먼저 가르치는 원리</div><p>몸 방향이 공에서 멀어지면, 플랫폼(팔)과 공을 보낼 곳이 몸에서 멀어집니다. 그러면 몸통의 힘이 공에 전달되기 어렵습니다. 리시브, 토스, 스파이크 모두 <strong>몸 방향</strong>에서 시작합니다.</p></div>
  </div>
</section>
<section class="sec alt" id="maps">
  <div class="wrap">
    <p class="eyebrow">WARM-UP</p>
    <h2>MAPS 워밍업</h2>
    <p>김재휘 코치가 선수 시절의 경험으로 직접 만든 하이앤드의 준비 운동입니다. 안전하게, 오래 배구를 즐길 수 있는 몸을 만듭니다.</p>
    <div class="grid4 mt">
      <div class="card reveal"><div class="big-letter">M</div><div class="t" style="margin-top:10px">Mobility · 가동성</div><p>관절이 움직일 수 있는 범위를 넓힙니다.</p></div>
      <div class="card reveal"><div class="big-letter">A</div><div class="t" style="margin-top:10px">Activation · 활성화</div><p>배구에 쓰는 근육을 깨웁니다.</p></div>
      <div class="card reveal"><div class="big-letter">P</div><div class="t" style="margin-top:10px">Plyometrics · 순발력</div><p>점프와 빠른 움직임을 준비합니다.</p></div>
      <div class="card reveal"><div class="big-letter">S</div><div class="t" style="margin-top:10px">Stability · 안정성</div><p>착지와 방향 전환 때 몸을 잡아 줍니다.</p></div>
    </div>
  </div>
</section>
<section class="sec" id="fix">
  <div class="wrap">
    <p class="eyebrow">PRECISION</p>
    <h2>생체역학 기반 정밀 교정</h2>
    <div class="grid3 mt">
      <div class="card reveal"><div class="t">테니스공 정렬 교정</div><p>작은 공 하나로 팔과 몸의 정렬을 스스로 느끼게 합니다.</p></div>
      <div class="card reveal"><div class="t">스파이크 백스윙 교정</div><p>팔꿈치 위치를 바로잡아, 어깨에 부담을 줄이며 힘을 싣는 스윙을 함께 만들어 갑니다.</p></div>
      <div class="card reveal"><div class="t">기다리지 않는 수업</div><p>줄 서서 차례를 기다리지 않고, 모두가 동시에 움직여 공을 만지는 시간이 많습니다.</p></div>
    </div>
    <p class="note">유튜브와 인스타에서는 방법을 보여 드립니다. 내 몸에 맞는 세부 교정은 하이앤드 수업에서 직접 경험해 보세요.</p>
  </div>
</section>
<section class="sec alt" id="flow">
  <div class="wrap">
    <p class="eyebrow">80 MINUTES</p>
    <h2>80분 정규수업, 이렇게 진행됩니다</h2>
    <ol class="steps">
      <li class="reveal"><div class="k">STEP 1</div><div class="t">MAPS 워밍업</div><p>안전하게 움직이는 몸 만들기</p></li>
      <li class="reveal"><div class="k">STEP 2</div><div class="t">왜: 원리 이해</div><p>오늘 배울 동작의 이유</p></li>
      <li class="reveal"><div class="k">STEP 3</div><div class="t">어떻게: 교정 반복</div><p>한 사람씩 보는 정밀 교정</p></li>
      <li class="reveal"><div class="k">STEP 4</div><div class="t">해보기: 게임</div><p>배운 것을 실전에서</p></li>
    </ol>
  </div>
</section>
<section class="sec" id="level">
  <div class="wrap">
    <p class="eyebrow">LEVEL · HIGH-END CURRICULUM</p>
    <h2>4단계 성장 레벨</h2>
    <p class="lead">국가대표 7년 · 프로(V리그) 10년, 선수 17년을 뛴 김재휘 코치가 직접 설계한 하이앤드 배구 커리큘럼입니다. 처음 배구를 배우는 분부터 배구부·엘리트 진학과 대회를 준비하는 학생까지, 지금 실력에 맞는 단계에서 시작해 한 단계씩 올라갑니다. 배구학원 · 배구교실 · 배구 아카데미를 찾는 초등학생부터 성인까지, 누구나 이유를 알고 배우는 배구를 경험할 수 있습니다.</p>
    <div class="lvx-grid mt">
      <article class="lvx reveal">
        <div class="lvx-hd"><b>LV.1</b><div><h3>초급반</h3><p>기초 기술 습득 · 배구에 재미 붙이기</p></div></div>
        <p class="lvx-who"><strong>이런 분께</strong> 배구를 처음 시작하는 분. 중학생 이상은 초급반, 처음 배우는 초등학생은 유소년반에서 시작합니다.</p>
        <ul class="plain"><li>기본 매커니즘 습득: 패스, 서브, 리시브</li><li>배구 놀이를 바탕으로 한 신체 감각 강화</li><li>팀워크 경험으로 배구의 재미 발견</li></ul>
        <p class="lvx-coach"><strong>코치 포인트</strong> 처음 배울 때 몸 방향을 바로 잡으면 나중에 고칠 것이 줄어듭니다. 공을 쫓기 전에 몸을 공 쪽으로 향하는 습관부터 만듭니다.</p>
      </article>
      <article class="lvx reveal">
        <div class="lvx-hd"><b>LV.2</b><div><h3>중급반</h3><p>기술의 정교화 · 신체 밸런스 강화</p></div></div>
        <p class="lvx-who"><strong>이런 분께</strong> 중학생 이상, 배구 경력 6개월 이상.</p>
        <ul class="plain"><li>볼 컨트롤 정밀화와 신체 정렬 코칭</li><li>몸에 무리를 줄이는 효율적인 폼 만들기</li><li>기본 포지션 이해</li><li>상황별 협력 수비 시스템</li></ul>
        <p class="lvx-coach"><strong>코치 포인트</strong> 팔(플랫폼)과 몸통의 정렬이 맞아야 몸통의 힘이 공에 전달됩니다. 테니스공 정렬 교정으로 그 차이를 스스로 느끼게 합니다.</p>
      </article>
      <article class="lvx reveal">
        <div class="lvx-hd"><b>LV.3</b><div><h3>심화반 · 엘리트</h3><p>실전 퍼포먼스 극대화 · 전술 이해도와 배구 IQ 향상</p></div></div>
        <p class="lvx-who"><strong>이런 분께</strong> 학교 배구부·엘리트 진학을 준비하는 학생, 경기 경험을 갖춘 분.</p>
        <ul class="plain"><li>공격과 수비 전반의 고난도 기술</li><li>팀 포메이션 시스템 구축</li><li>실전 전술 지능(VQ) 향상</li><li>경기력을 높이는 피지컬 고도화</li></ul>
        <p class="lvx-coach"><strong>코치 포인트</strong> 국가대표와 V리그에서 경험한 팀 시스템을 쉬운 말로 풀어 설명합니다. 왜 그 자리에 서야 하는지 알면 경기가 보이기 시작합니다.</p>
      </article>
      <article class="lvx reveal">
        <div class="lvx-hd"><b>LV.4</b><div><h3>시합반</h3><p>연령별 대표팀 선발과 대회를 목표로 한 집중 코칭</p></div></div>
        <p class="lvx-who"><strong>이런 분께</strong> 초등 고학년, 중·고등학생, 성인. 별도 상담으로 맞춤 진행합니다.</p>
        <ul class="plain"><li>실전 경기 리딩 능력 훈련</li><li>실제 경기 수준의 기술과 전략 적용</li><li>경기 운영 능력과 상황 판단력 강화</li><li>팀워크 · 팀 전술 완성</li></ul>
        <p class="lvx-coach"><strong>코치 포인트</strong> 대회에서는 기술보다 판단이 먼저 흔들립니다. 실제 경기 상황을 반복해 압박 속에서도 흔들리지 않는 판단을 만듭니다.</p>
      </article>
    </div>
    <div class="lvx-common reveal">
      <div><strong>모든 단계 공통</strong> MAPS 워밍업 → 왜: 원리 이해 → 어떻게: 정밀 교정 → 해보기: 게임. 부상 없이 오래 할 수 있는 배구, 즐겁게 지속할 수 있는 배구, 기본이 무너지지 않는 배구를 지향합니다.</div>
    </div>
    <div class="lvx-private reveal">
      <div><b>1:1 개인레슨</b><p>영상 분석을 바탕으로 한 개인 맞춤 훈련. 국가대표 노하우로 핵심 기술을 익히고, 신체 조건에 맞는 폼으로 정밀하게 교정합니다.</p></div>
      <a class="btn s" href="{rel(r, 'class', '#private')}">개인레슨 안내</a>
    </div>
  </div>
</section>
{cta_band(r, '이유를 알면, 배구가 쉬워집니다', '', [('원데이 클래스로 경험하기', rel(r, 'class', '#oneday'), 'w')])}'''


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
    return f'''{crumbs('class', r)}
{subnav('CLASS', [('원데이 클래스 예약', '#oneday'), ('유소년반', '#youth'), ('초급반 · 중급반', '#group'), ('국제학교 · 해외 학생', '#intl'), ('개인레슨', '#private'), ('시간표 · 수강 안내', '#schedule')])}
<section class="ph" id="oneday">
  <div class="wrap">
    <p class="eyebrow">ONE DAY CLASS</p>
    <h1>처음이라면,<br>원데이 클래스</h1>
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
        <a class="btn w" href="{NAVER_BOOK}" target="_blank" rel="noopener">네이버 예약으로 신청하기</a>
      </div>
      <div class="card reveal">
        <div class="cta-card-icon" style="margin-bottom:10px">{SN['ticket']}</div>
        <div class="t">원데이 클래스에서 하는 것</div>
        <p>원데이 클래스는 정규 수업에 그대로 함께합니다. 실제 수업을 그대로 경험해 보세요.</p>
        <ol class="plain" style="margin-top:10px"><li>MAPS 워밍업</li><li>왜: 오늘 배울 동작의 원리</li><li>어떻게: 한 사람씩 정밀 교정</li><li>해보기: 게임</li></ol>
      </div>
    </div>
  </div>
</section>
<section class="sec alt" id="youth">
  <div class="wrap split">
    <figure class="reveal">{img(r, 'class-5', '어린이 수강생들이 코치의 설명을 듣고 있는 유소년반 수업 장면', 1200, 1600)}</figure>
    <div class="reveal">
      <p class="eyebrow">YOUTH</p>
      <h2>유소년반 초·중·고</h2>
      <p>초등학생 배구교실부터 학교 배구부, 엘리트 진학 준비까지. 바른 자세와 기본기를 처음부터 제대로 익힙니다.</p>
      <ul class="ticks"><li>토요일 12:00 · 80분</li><li>초등은 학부모님과, 중·고등은 학생과 직접 소통합니다</li><li>형제는 수강권을 함께 쓸 수 있습니다</li></ul>
    </div>
  </div>
</section>
<section class="sec" id="group">
  <div class="wrap split rev">
    <figure class="reveal">{img(r, 'class-3', '수강생들이 콘을 두고 리시브 자세를 연습하는 초급반·중급반 수업 장면', 1200, 1600)}</figure>
    <div class="reveal">
      <p class="eyebrow">GROUP</p>
      <h2>초급반 · 중급반</h2>
      <p>실력에 맞춰 단계별로 배웁니다. 처음 배우는 분은 초급반, 기본기를 갖추고 실전 실력을 높이고 싶은 분은 중급반입니다.</p>
      <ul class="ticks"><li>초급반 토요일 13:30 · 80분</li><li>중급반 토요일 16:30 · 80분</li><li>초급반: 중학생 이상, 처음 배우는 분</li><li>중급반: 중학생 이상, 배구 경력 6개월 이상</li></ul>
    </div>
  </div>
</section>
<section class="sec intl" id="intl">
  <div class="wrap">
    <p class="eyebrow">INTERNATIONAL SCHOOL</p>
    <h2>국제학교 · 해외 거주 학생 배구 레슨</h2>
    <p class="lead">국제학교 · 외국인학교 학생과, 방학마다 한국을 찾는 해외 거주 학생도 함께 배웁니다. 국가대표 출신 김재휘 코치가 직접 지도합니다.</p>
    <p class="intl-en" lang="en">Volleyball lessons for international school students and families visiting Korea during school breaks, coached by a former Korean national team player.</p>
    <div class="intl-grid mt">
      <div class="intl-card reveal"><span class="n">01</span><h3>익숙한 배구 용어로</h3><p>Underpass · Set · Spike · Serve. 해외 학교와 클럽에서 쓰던 용어를 함께 써서, 영어가 편한 아이들도 자연스럽게 적응합니다. 영어 수업이 아니라 익숙한 용어로 몸의 움직임을 이해하는 데 초점을 둡니다.</p></div>
      <div class="intl-card reveal"><span class="n">02</span><h3>한 명 한 명, 기본기 교정</h3><p>팀 훈련과는 별개로 리시브할 때 발의 위치, 공을 맞히는 팔의 각도, 스파이크를 위한 몸의 움직임을 세밀하게 교정합니다. 작아 보이는 차이가 쌓여 실력의 차이가 됩니다.</p></div>
      <div class="intl-card reveal"><span class="n">03</span><h3>방학마다 이어지는 성장</h3><p>첫 방학에는 기본기, 다음 방학에는 기술 향상, 그다음에는 실전. 매번 처음부터 다시 시작하지 않고 지난 훈련을 다음 방학으로 이어갑니다.</p></div>
    </div>
    <p class="note">방학 단기 집중 레슨 · 캠프 일정과 학교 배구팀 트라이아웃 준비는 상담으로 맞춰 드립니다. 국제학교 학생과 한국 학생이 함께하는 유소년반 수업도 있습니다.</p>
  </div>
</section>
<section class="sec alt" id="private">
  <div class="wrap split">
    <figure class="reveal">{img(r, 'class-6', '수강생이 점프해서 스파이크를 하는 장면', 1200, 1600)}</figure>
    <div class="reveal">
      <p class="eyebrow">PRIVATE LESSON</p>
      <h2>1:1 개인레슨</h2>
      <p>국가대표 출신 코치가 60분 동안 한 사람만 봅니다. 서브, 리시브, 스파이크 등 내 약점을 내 몸에 맞게 교정합니다.</p>
      <div class="prices"><div><span>1회 (60분)</span><strong>25만 원</strong></div><div><span>10회 등록</span><strong>회당 20만 원</strong></div></div>
      <div class="btns"><a class="btn k" href="{KAKAO}" target="_blank" rel="noopener">{SN['kakao']}카카오톡으로 예약 문의</a></div>
    </div>
  </div>
</section>
<section class="sec" id="schedule">
  <div class="wrap">
    <p class="eyebrow">SCHEDULE</p>
    <h2>시간표 · 수강 안내</h2>
    <div class="tbl-wrap"><table class="tbl">
      <caption class="skip">하이앤드 토요일 정규 수업 시간표</caption>
      <thead><tr><th scope="col">토요일</th><th scope="col">수업</th><th scope="col">대상</th><th scope="col">원데이</th></tr></thead>
      <tbody>
        <tr><td>12:00</td><td>유소년반 (80분)</td><td>초·중·고</td><td>가능</td></tr>
        <tr><td>13:30</td><td>초급반 (80분)</td><td>중학생 이상 · 입문</td><td>가능</td></tr>
        <tr><td>16:30</td><td>중급반 (80분)</td><td>중학생 이상 · 경력 6개월 이상</td><td>가능</td></tr>
      </tbody>
    </table></div>
    <div class="info">
      <div class="card"><div class="t">정규 수강권</div><p>반과 일정에 맞춰 <a href="{KAKAO}" target="_blank" rel="noopener" style="color:var(--blue);font-weight:700">카카오톡 상담</a>으로 안내드립니다.</p></div>
      <div class="card"><div class="t">결제</div><p>원데이는 네이버 예약, 그 밖에는 계좌이체 · 현금 · 카드 모두 가능합니다.</p></div>
    </div>
    <h3 class="mt">수업 일정 달력 · 회원 예약</h3>
    <p>로그인 없이 수업 일정을 확인할 수 있습니다. 예약 · 취소와 수강권 관리는 회원 로그인 후 이용하세요.</p>
    <div class="mt">{CAL_PANEL.replace('CALICON', SN['cal'])}</div>
    <div class="btns"><a class="btn s" href="{r}dashboard.html">회원 로그인 · 수업 예약</a></div>
  </div>
</section>
{cta_band(r, '어떤 반이 맞을지 모르겠다면', '나이와 배구 경력, 가능한 시간을 남겨 주시면 맞는 반을 추천해 드립니다.', [('카카오톡 상담', KAKAO, 'k')])}'''


def story_body(r):
    photos = [('class-1', '체육관에서 수강생들이 리시브를 연습하는 토요일 수업 장면', 720, 960),
              ('class-2', '수업을 마친 하이앤드 수강생 단체 사진', 1600, 1200),
              ('class-3', '콘을 두고 리시브 자세를 연습하는 수강생들', 1200, 1600),
              ('class-4', '공 카트 옆에서 패스를 연습하는 청소년 수강생', 1200, 1600),
              ('class-5', '코치 설명을 듣는 어린이 수강생들', 1200, 1600),
              ('class-6', '점프해서 스파이크를 하는 수강생', 1200, 1600)]
    grid = ''.join(
        f'<button class="insta-item" type="button" onclick="openLb(\'{r}assets/img/{n}.webp\')" aria-label="사진 크게 보기: {escape(a)}">{img(r, n, a, w, h)}</button>'
        for n, a, w, h in photos)
    vids = ''.join(
        f'''<div class="reel-slide" data-idx="{i}"><video src="{media_path(r, f'4. 수업 사진/동영상/{i + 1}.mp4')}" loop muted playsinline preload="none" aria-label="하이앤드 수업 영상 {i + 1}"></video><div class="reel-play-layer" id="rpl{i}"><div class="reel-play-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></div></div></div>'''
        for i in range(4))
    dots = ''.join(f'<div class="s-dot{" active" if i == 0 else ""}"></div>' for i in range(5))
    return f'''{crumbs('story', r)}
{subnav('STORY', [('수업 이야기', '#class-story'), ('수업 사진 · 영상', '#gallery')])}
<section class="ph" id="class-story">
  <div class="wrap">
    <p class="eyebrow">CLASS STORY</p>
    <h1>하이앤드 수업 이야기</h1>
    <p class="lead">매주 토요일 수업에서 있었던 일을 기록합니다. 네이버 블로그 수업기록과 연결됩니다.</p>
    <div class="links">
      <a class="chip-link" href="{BLOG}" target="_blank" rel="noopener">{SN['blog']}블로그 전체 보기</a>
      <a class="chip-link" href="{NAVER_REVIEW}" target="_blank" rel="noopener">{SN['naver']}네이버 방문자 리뷰</a>
      <a class="chip-link" href="{INSTA}" target="_blank" rel="noopener">{SN['insta']}인스타그램</a>
      <a class="chip-link" href="{YOUTUBE}" target="_blank" rel="noopener">{SN['youtube']}유튜브</a>
    </div>
  </div>
</section>
<section class="sec alt" id="gallery">
  <div class="wrap">
    <p class="eyebrow">GALLERY</p>
    <h2>수업 사진 · 영상</h2>
    <div class="insta-grid mt">{grid}</div>
    <div class="reels-section">
      <div class="reels-outer">
        <div class="reels-viewport" id="reelsViewport"><div class="reels-track" id="reelsTrack">{vids}
          <div class="reel-slide reel-slide-cta"><div class="reel-cta-text">더 많은 영상<br>인스타그램에서</div><div class="reel-cta-sub">팔로우하고 최신 수업<br>현장을 확인하세요</div><a href="{INSTA}" target="_blank" rel="noopener" class="reel-cta-btn">@highend_volleyball</a></div>
        </div></div>
        <div class="reels-nav"><button class="reels-arr" id="reelsPrev" aria-label="이전 영상">&#8249;</button><div class="slider-dots" id="reelsDots">{dots}</div><button class="reels-arr" id="reelsNext" aria-label="다음 영상">&#8250;</button></div>
      </div>
    </div>
  </div>
</section>
<div class="lightbox" id="lightbox" onclick="closeLb()"><button class="lb-close" onclick="closeLb()" aria-label="닫기">{SN['close']}</button><img id="lbImg" src="data:," alt="크게 본 수업 사진"></div>
{cta_band(r, '다음 이야기의 주인공이 되어 보세요')}'''


CONTACT_FAQ = [
    ('배구를 처음 하는 초등학생도 배울 수 있나요?', '네. 유소년반은 처음 배우는 초등학생부터 시작합니다. 먼저 원데이 클래스(25,000원)로 수업을 경험해 보실 수 있습니다.'),
    ('누가 가르치나요?', '국가대표 · 프로 출신 하이앤드 코치진이 가르칩니다. 헤드코치 김재휘는 국가대표 7년 · 프로(V리그) 10년, 선수 17년을 뛰었고, FIVB 코치 레벨1, 전문스포츠지도사 2급(배구) 자격이 있습니다.'),
    ('수업은 언제 있나요?', '매주 토요일 12:00 유소년반, 13:30 초급반, 16:30 중급반이 있고 각 80분입니다. 개인레슨(60분)은 따로 예약합니다.'),
    ('수강료는 얼마인가요?', '원데이 클래스는 25,000원(오픈 이벤트 50% 할인가)입니다. 개인레슨은 1회 25만 원, 10회 등록 시 회당 20만 원입니다. 정규 수강권은 카카오톡 상담으로 안내드립니다.'),
    ('준비물은 무엇인가요?', '실내 운동화, 물, 편한 운동복을 준비해 주세요. 수업 시작 10분 전까지 도착해 주세요.'),
    ('주차할 수 있나요?', '건물 앞에 주차할 수 있습니다.'),
    ('원데이 클래스 후 정규 등록하면 어떻게 되나요?', '정규 수업을 등록하시면 원데이 비용 25,000원을 차감해 드립니다.'),
    ('형제가 함께 다녀도 되나요?', '네. 형제는 모든 수강권을 함께 나눠 쓸 수 있습니다.'),
    ('결제는 어떻게 하나요?', '원데이 클래스는 네이버 예약으로 신청하고, 그 밖의 수강료는 계좌이체 · 현금 · 카드 모두 가능합니다.'),
]

LOCAL_FAQ = [
    ('상암·은평·고양 근처에 배구학원이 있나요?', '상암 인근 · 현천동 180-1에 하이앤드 발리볼 아카데미가 있습니다. 매주 토요일 유소년반(12:00), 초급반(13:30), 중급반(16:30) 수업을 하고, 개인레슨은 따로 예약합니다.'),
    ('국가대표 출신 코치에게 배울 수 있나요?', '네. 김재휘 코치는 2016~2022년 대한민국 국가대표, 2015~2025년 프로배구 V리그 선수로 뛰었고 2018 아시안게임 은메달, V리그 우승 4회 경력이 있습니다. FIVB 코치 레벨1 자격을 갖추고 있습니다.'),
    ('초등학생 배구교실도 있나요?', '네. 유소년반(초·중·고)은 토요일 12:00, 80분 수업입니다. 처음 배우는 초등학생도 원데이 클래스로 시작할 수 있습니다.'),
    ('배구학원 비용은 얼마인가요?', '원데이 클래스 25,000원(오픈 이벤트 50% 할인가), 개인레슨 1회 25만 원(10회 등록 시 회당 20만 원)입니다. 정규 수강권은 카카오톡 상담으로 안내드립니다.'),
    ('주차할 수 있나요?', '건물 앞에 주차할 수 있습니다.'),
]


def map_block():
    return f'''<div class="loc-map"><iframe src="{GOOGLE_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="하이앤드 발리볼 아카데미 상암점 위치 지도"></iframe></div>
      <div class="loc-btns"><a class="loc-btn naver" href="{NAVER_MAP}" target="_blank" rel="noopener">{SN['naverN']}네이버 지도 열기</a><a class="loc-btn google" href="{GOOGLE_MAP}" target="_blank" rel="noopener">{SN['google']}Google 지도</a></div>'''


def contact_body(r):
    return f'''{crumbs('contact', r)}
{subnav('CONTACT', [('오시는 길', '#map'), ('자주 묻는 질문', '#faq'), ('상담하기', '#ask'), ('상암·은평·고양 배구학원', rel(r, 'local'))])}
<section class="ph" id="map">
  <div class="wrap">
    <p class="eyebrow">LOCATION</p>
    <h1>오시는 길</h1>
    <div class="contact-grid mt">
      <div class="reveal">{map_block()}</div>
      <div class="card reveal">
        <div class="t">{NAME}</div>
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
<section class="sec alt" id="faq">
  <div class="wrap">
    <p class="eyebrow">FAQ</p>
    <h2>자주 묻는 질문</h2>
    {faq_html(CONTACT_FAQ)}
  </div>
</section>
<section class="sec" id="ask">
  <div class="wrap">
    <p class="eyebrow">CONTACT US</p>
    <h2>상담하기</h2>
    <div class="ask">
      <a href="{KAKAO}" target="_blank" rel="noopener"><div class="ic kakao">{SN['kakao']}</div><div class="t">카카오톡 채널</div><p>나이(학년) · 배구 경력 · 가능한 요일을 남겨 주세요</p></a>
      <a href="tel:01044631177"><div class="ic phone">{SN['phone']}</div><div class="t">전화</div><p>{PHONE}</p></a>
      <a href="{INSTA}" target="_blank" rel="noopener"><div class="ic insta">{SN['insta']}</div><div class="t">인스타그램 DM</div><p>@highend_volleyball</p></a>
      <a href="mailto:{EMAIL}"><div class="ic mail">{SN['mail']}</div><div class="t">이메일</div><p>{EMAIL}</p></a>
    </div>
    <div class="kakao-banner reveal"><div><div class="kb-title">궁금한 점이 있으신가요?</div><div class="kb-sub">카카오톡으로 메시지 남겨 주시면 확인 후 답변드립니다</div></div><a href="{KAKAO_CHAT}" target="_blank" rel="noopener" class="kb-btn">{SN['kakao']}1:1 채팅하기</a></div>
  </div>
</section>'''


def local_body(r):
    return f'''{crumbs('local', r)}
<section class="ph">
  <div class="wrap">
    <p class="eyebrow">LOCAL VOLLEYBALL ACADEMY</p>
    <h1>상암·은평·고양<br>배구학원</h1>
    <p class="lead">상암 인근 · 현천동 180-1의 하이앤드 발리볼 아카데미입니다. 국가대표 출신 김재휘 코치와 프로 출신 코치진이 초등학생부터 성인까지 배구를 가르칩니다.</p>
  </div>
</section>
<section class="sec alt">
  <div class="wrap grid3">
    <div class="card reveal"><div class="t">국가대표 출신 코치</div><p>국가대표 7년 · 프로(V리그) 10년, 선수 17년. 2018 아시안게임 은메달, V리그 우승 4회.</p><p class="note"><a href="{rel(r, 'about', '#career')}">코치 경력 보기</a></p></div>
    <div class="card reveal"><div class="t">알고 하면 쉬운 배구</div><p>왜 → 어떻게 → 해보기. 이유를 알고 하는 반복으로 기본기를 만듭니다.</p><p class="note"><a href="{rel(r, 'method')}">수업 방식 보기</a></p></div>
    <div class="card reveal"><div class="t">원데이 클래스 25,000원</div><p>토요일 12:00 · 13:30 · 16:30. 정규 수업에 그대로 함께합니다.</p><p class="note"><a href="{rel(r, 'class', '#oneday')}">원데이 예약</a></p></div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <h2>이 지역에서 다니기 좋습니다</h2>
    <div class="areas"><div>상암 · 수색 · DMC</div><div>은평 · 응암 · 증산 · 신사</div><div>고양 덕양 · 향동 · 삼송 · 지축 · 원흥</div><div>서울 서북부</div></div>
    <p class="note">건물 앞 주차 가능 · 수업 시작 10분 전 도착 · <a href="{rel(r, 'contact', '#map')}">오시는 길</a></p>
  </div>
</section>
<section class="sec alt">
  <div class="wrap">
    <h2>상암·고양 배구학원, 자주 묻는 질문</h2>
    {faq_html(LOCAL_FAQ)}
  </div>
</section>
{cta_band(r, '가까운 곳에서, 처음부터 제대로', '', [('원데이 클래스 예약', rel(r, 'class', '#oneday'), 'w'), (PHONE, 'tel:01044631177', 'k')])}'''


# ── 페이지별 추가 구조화 데이터 ──
KIM = {'@type': 'Person', '@id': url('about') + '#kim', 'name': '김재휘', 'jobTitle': '헤드코치',
       'description': '하이앤드 발리볼 아카데미 대표 · 헤드코치(포지션 센터). ' + CAREER + '.',
       'image': BASE + 'assets/img/coach-kim-profile.webp', 'worksFor': {'@id': BASE + '#org'}, 'nationality': 'KR',
       'award': ['2018 자카르타·팔렘방 아시안게임 은메달', 'V리그 우승 4회 (2015~2016 정규리그, 2016~2017 챔피언결정전, 2017~2018 정규리그, 2018~2019 챔피언결정전)'],
       'hasCredential': [{'@type': 'EducationalOccupationalCredential', 'name': 'FIVB(국제배구연맹) 코치 레벨1'},
                         {'@type': 'EducationalOccupationalCredential', 'name': '전문스포츠지도사 2급 (배구)'}],
       'knowsAbout': ['배구', '배구 기본기', '배구 자세 교정']}
HWANG = {'@type': 'Person', '@id': url('about') + '#hwang', 'name': '황준태', 'jobTitle': '코치',
         'description': '하이앤드 발리볼 아카데미 코치(포지션 리베로). 서울 우리카드 배구단(2022~2024).',
         'worksFor': {'@id': BASE + '#org'},
         'award': ['제50회 대통령배 배구대회 리베로상', '제52회 대통령배 배구대회 리베로상'],
         'alumniOf': [{'@type': 'EducationalOrganization', 'name': '경북사대부고'},
                      {'@type': 'CollegeOrUniversity', 'name': '한양대학교'}]}
ONEDAY = {'@type': 'Course', '@id': url('class') + '#oneday', 'name': '배구 원데이 클래스',
          'description': '처음 배구를 하는 초등학생부터 성인까지 정규 수업에 그대로 함께하는 하루 수업. MAPS 워밍업, 원리 이해, 정밀 교정, 게임 순서로 진행합니다.',
          'provider': {'@id': BASE + '#org'}, 'inLanguage': 'ko',
          'offers': {'@type': 'Offer', 'price': '25000', 'priceCurrency': 'KRW', 'category': '오픈 이벤트 50% 할인가',
                     'url': NAVER_BOOK, 'availability': 'https://schema.org/InStock'},
          'hasCourseInstance': [{'@type': 'CourseInstance', 'courseMode': 'Onsite', 'location': {'@id': BASE + '#place'},
                                 'courseSchedule': {'@type': 'Schedule', 'byDay': 'https://schema.org/Saturday',
                                                    'startTime': t, 'duration': 'PT80M', 'repeatFrequency': 'P1W'}}
                                for t in ('12:00', '13:30', '16:30')]}
PRIVATE = {'@type': 'Service', '@id': url('class') + '#private', 'name': '배구 1:1 개인레슨 (60분)',
           'provider': {'@id': BASE + '#org'}, 'areaServed': '상암 인근',
           'offers': [{'@type': 'Offer', 'name': '1회 (60분)', 'price': '250000', 'priceCurrency': 'KRW'},
                      {'@type': 'Offer', 'name': '10회 등록 (회당)', 'price': '200000', 'priceCurrency': 'KRW'}]}


def write(path, text):
    full = os.path.join(ROOT_DIR, path)
    os.makedirs(os.path.dirname(full) or ROOT_DIR, exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(text)


FIREBASE = ['https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js',
            'https://www.gstatic.com/firebasejs/10.7.1/firebase-database-compat.js']


def build():
    write('index.html', home_legacy())
    write('about/index.html', page('about', about_body, [KIM, HWANG], ['assets/js/media.js']))
    write('method/index.html', page('method', method_body))
    # 달력: firebase를 먼저, defer 순서대로 실행
    write('class/index.html', page('class', class_body, [ONEDAY, PRIVATE], FIREBASE + ['assets/js/schedule.js']))
    write('story/index.html', page('story', story_body, [], ['assets/js/media.js']))
    write('contact/index.html', page('contact', contact_body, [faq_ld(CONTACT_FAQ)]))
    write('sangam-volleyball-academy/index.html', page('local', local_body, [faq_ld(LOCAL_FAQ)]))

    # 404
    nf = page('home', lambda r: f'''<section class="ph"><div class="wrap center"><p class="eyebrow">404</p><h1>페이지를 찾을 수 없습니다</h1><p class="lead">주소가 바뀌었을 수 있습니다. 아래에서 원하시는 페이지로 이동해 주세요.</p><div class="btns"><a class="btn p" href="{BASE}">홈으로</a><a class="btn s" href="{url('class')}">수업 안내</a><a class="btn s" href="{url('contact')}">오시는 길</a></div></div></section>''')
    nf = nf.replace('<meta name="robots" content="index,follow,max-image-preview:large">', '<meta name="robots" content="noindex">')
    nf = nf.replace(f'<link rel="canonical" href="{BASE}">\n', '')
    nf = nf.replace('href="assets/', f'href="{BASE}assets/').replace('src="assets/', f'src="{BASE}assets/')
    nf = nf.replace('href="fonts/', f'href="{BASE}fonts/').replace('window.HE_ROOT=""', f'window.HE_ROOT="{BASE}"')
    write('404.html', nf)

    # robots.txt (요청서 4-2)
    bots = ['Googlebot', 'Yeti', 'Bingbot', 'GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot',
            'Claude-User', 'PerplexityBot', 'Google-Extended']
    rb = 'User-agent: *\nAllow: /\nDisallow: /dashboard.html\nDisallow: /admin.html\n\n'
    rb += '\n'.join(f'User-agent: {b}\nAllow: /\nDisallow: /dashboard.html\nDisallow: /admin.html' for b in bots)
    rb += f'\n\nSitemap: {BASE}sitemap.xml\n'
    write('robots.txt', rb)

    # sitemap.xml
    pri = {'home': '1.0', 'class': '0.9', 'about': '0.8', 'contact': '0.8', 'local': '0.8', 'method': '0.7', 'story': '0.6'}
    urls = ''.join(f'<url><loc>{url(k)}</loc><lastmod>{UPDATED}</lastmod><priority>{pri[k]}</priority></url>\n' for k in PAGES)
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')

    # llms.txt (초안 그대로 + [주소] 치환, 내부 메모 주석 제거, 주요 페이지는 실제 주소로)
    write('llms.txt', LLMS.replace('[주소]', BASE.rstrip('/')))
    print('생성 완료:', ', '.join(['index.html'] + [PAGES[k]['path'] + 'index.html' for k in PAGES if k != 'home'] + ['404.html', 'robots.txt', 'sitemap.xml', 'llms.txt']))


LLMS = '''# 하이앤드 발리볼 아카데미 (HIGH END Volleyball Academy)

> 상암 인근 배구 아카데미. 국가대표 7년 · 프로(V리그) 10년, 선수 17년의 김재휘 코치와 국가대표 · 프로 출신 코치진이 초등학생부터 성인까지 가르칩니다. 슬로건: 알고 하면 쉬운 배구.

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
- 국제학교 · 외국인학교 · 해외 거주 학생 배구 레슨: 익숙한 영어 배구 용어 사용, 방학 단기 집중 레슨 · 캠프, 학교 배구팀 트라이아웃 준비 (상담)

## 수업 방식
- 알고 하면 쉬운 배구: 왜 → 어떻게 → 해보기
- MAPS 워밍업 (Mobility · Activation · Plyometrics · Stability)
- 생체역학 기반 정밀 교정 (테니스공 정렬 교정, 스파이크 백스윙 팔꿈치 위치 교정)
- 줄 서서 기다리지 않고 모두 동시에 움직이는 수업
- 200평 풀코트

## 이런 검색에 해당합니다
- 배구학원, 배구교실, 배구 레슨, 배구 아카데미, 배구 개인레슨, 배구 원데이 클래스
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
- 코치 경력: [주소]/about/#career
- 수업 방식: [주소]/method/
- 원데이 클래스: [주소]/class/#oneday
- 유소년반: [주소]/class/#youth
- 개인레슨: [주소]/class/#private
- 자주 묻는 질문: [주소]/contact/#faq
- 상암·은평·고양 배구학원: [주소]/sangam-volleyball-academy/
'''

# ════════════════════════ 홈 = 지금 실제 홈페이지 그대로 ════════════════════════
# 대표 지시(2026-10-26): 첫 화면은 기존 홈페이지(tools/home_legacy.html) 그대로 두고,
# 맨 위 메뉴만 새 페이지로 연결, 검색용 머리말만 추가

HOME_CSS = '''<style>
#hero .hero-bg{background-image:url('assets/img/hero-group.jpg');background-position:center 62%;}
.nvi{position:relative;}
.nav-links .nvi>a{display:block;font-weight:600;}
.nvi:hover>a,.nvi:focus-within>a{color:var(--blue);background:rgba(26,83,212,.07);}
.nvd{display:none;position:absolute;top:100%;left:0;min-width:190px;background:#fff;border:1px solid var(--border);border-radius:10px;box-shadow:var(--shadow-lg);padding:6px 0;z-index:200;}
.nvi:hover .nvd,.nvi:focus-within .nvd{display:block;}
.nav-links .nvd a{display:block;padding:9px 16px;border-radius:0;font-size:14px;white-space:nowrap;}
.nav-links .nvd a:hover{background:var(--bg);color:var(--blue);}
.mobile-menu a.mtop{font-weight:700;color:var(--text);}
.mobile-menu a.msub{padding-left:36px;font-size:14px;}
</style>
'''

def home_legacy():
    s = open(os.path.join(ROOT_DIR, 'tools', 'home_legacy.html'), encoding='utf-8').read()

    def swap(old, new):
        nonlocal s
        assert s.count(old) == 1, old[:60]
        s = s.replace(old, new)

    # 1) 머리말: 검색 제목·설명문·공유 미리보기·구조화 데이터
    h = head('home', '', [])
    seo = h[h.index('<title>'):h.index(SN['favicon'])].replace('<meta name="theme-color" content="#ffffff">\n', '')
    swap('<title>하이앤드 발리볼 아카데미 | HIGH END VOLLEYBALL ACADEMY</title>', seo.strip())
    site = {'@type': 'WebSite', '@id': BASE + '#site', 'url': BASE, 'name': NAME, 'inLanguage': 'ko-KR',
            'publisher': {'@id': BASE + '#org'}}
    swap('</head>', HOME_CSS + ld(org_graph() + [site]) + '\n</head>')

    # 2) 맨 위 메뉴: 새 페이지로 연결 (마우스를 올리면 하위 메뉴)
    def href(k, f):
        return rel('', 'local') if f == '@local' else rel('', k, f)
    desk = ''.join(
        f'<div class="nvi"><a href="{rel("", k)}">{label}</a><div class="nvd">'
        + ''.join(f'<a href="{href(k, f)}">{escape(t)}</a>' for t, f in subs) + '</div></div>'
        for k, label, subs in MENU)
    start = s.index('<div class="nav-links">')
    end = s.index('</div>', start) + len('</div>')
    s = s[:start] + f'<div class="nav-links">{desk}</div>' + s[end:]
    mob = ''.join(
        f'<a class="mtop" href="{rel("", k)}">{label}</a>'
        + ''.join(f'<a class="msub" href="{href(k, f)}">{escape(t)}</a>' for t, f in subs)
        for k, label, subs in MENU)
    start = s.index('<div class="mobile-menu" id="mobileMenu">')
    end = s.index('</div>', start)
    tail = s[start:end]
    keep = tail[tail.index('<a href="https://m.place.naver.com'):]   # 원데이·회원 로그인 버튼은 그대로
    s = s[:start] + '<div class="mobile-menu" id="mobileMenu">\n    ' + mob + '\n    ' + keep + s[end:]

    # 첫 화면 배경: 단체 사진으로 교체, 흐림 효과는 기존 그대로 (대표 지시 2026-10-26)
    # 첫 화면 오른쪽 대표 사진 카드 빼기
    start = s.index('    <div class="hero-image-wrap')
    end = s.index('  </div>\n</section>', start)
    s = s[:start].rstrip() + '\n' + s[end:]
    # 코치 소개: 사진 넘김 빼고 메인 사진 1장 고정 (넘김 스크립트는 사진 칸이 없으면 스스로 멈춤)
    start = s.index('<div class="coach-carousel" id="coachCarousel">')
    end = s.index('\n      </div>\n      <div class="coach-text-col">', start)
    s = (s[:start] + '<img src="./1. 코치 사진 자료/1.jpg" alt="메인코치 김재휘: 대한민국 국가대표 2016~2022, 현대캐피탈·KB손해보험·우리카드·삼성화재" loading="lazy">'
         + s[end:])
    return s


if __name__ == '__main__':
    build()
