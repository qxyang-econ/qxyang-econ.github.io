"""Generate a dependency-free academic website. Run: python3 generate.py."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
OUT = ROOT / 'docs'
OUT.mkdir(parents=True, exist_ok=True)
CONFIG = json.loads((ROOT / 'site_config.json').read_text(encoding='utf-8'))
ORIGIN = CONFIG.get('site_url', '').strip().rstrip('/')

def link(text, url, **attrs):
    extra = ''.join(f' {key}="{escape(str(value), quote=True)}"' for key, value in attrs.items())
    return f'<a href="{escape(url, quote=True)}"{extra}>{escape(text)}</a>'

def paper(p, minimal=False):
    if minimal:
        return f'<article class="paper" id="{p["id"]}"><h3>{escape(p["title"])}</h3><p class="coauthors">with {escape(p["coauthors"])}</p></article>'
    title = link(p['title'], p['links'][0][1]) if p['links'] else escape(p['title'])
    language = f' <span class="journal-language">({escape(p["language"])})</span>' if p.get('language') else ''
    journal = f'<p class="journal"><em>{escape(p["journal"])}</em>{language}<span> · {escape(p["citation"])}</span></p>' if 'journal' in p else ''
    links = ''.join(link(label, url) for label, url in p['links'])
    if p.get('abstract_url'):
        links += link('Abstract ↗', p['abstract_url'])
    abstract = f'<details><summary>Abstract</summary><p>{escape(p["abstract"])}</p></details>' if p.get('abstract') else ''
    actions = f'<div class="paper-links">{links}</div>' if links else ''
    return f'<article class="paper" id="{p["id"]}"><h3>{title}</h3><p class="coauthors">with {escape(p["coauthors"])}</p>{journal}{actions}{abstract}</article>'

def render(filename, title, main, home=False, with_profile=True):
    nav = ''.join(f'<a href="{url}"'+(' aria-current="page"' if url == filename else '')+f'>{label}</a>' for label,url in [('Home','index.html'),('Research','research.html'),('Teaching','teaching.html'),('CV','cv.html')])
    person = {'@context':'https://schema.org', '@type':'Person', 'name':'Qingxu Yang', 'alternateName':'杨卿栩', 'jobTitle':'Assistant Professor of Economics', 'affiliation':{'@type':'CollegeOrUniversity','name':'Fudan University'}, 'url':ORIGIN, 'email':'qxyang@fudan.edu.cn'}
    profile = f'''<aside class="profile" aria-label="Profile">
<div class="profile-name">Qingxu Yang<span lang="zh-Hans">杨卿栩</span></div>
<p class="position">Assistant Professor of Economics</p><p class="affiliation">School of Economics<br>Fudan University</p>
<div class="profile-rule"></div>
<div class="sidebar-section fields"><p class="label">Research fields</p><p>Digital Economics<br>Labor Economics</p></div>
<div class="sidebar-section"><p class="label">Contact</p><a class="email" href="mailto:qxyang@fudan.edu.cn">qxyang@fudan.edu.cn</a><p class="location">Shanghai, China</p></div>
</aside>''' if with_profile else ''
    if not ORIGIN:
        person.pop('url', None)
    canonical_url = f'{ORIGIN}/{filename}'
    canonical = f'<link rel="canonical" href="{escape(canonical_url, quote=True)}">' if ORIGIN else ''
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | Qingxu Yang</title>
<meta name="description" content="Qingxu Yang is an Assistant Professor of Economics at Fudan University. Research in digital economics, labor economics, artificial intelligence, and expert decision-making.">
<meta name="theme-color" content="#173e61">{canonical}
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css">
<script type="application/ld+json">{json.dumps(person,ensure_ascii=False)}</script></head>
<body><a class="skip" href="#main">Skip to content</a>
<div class="page {'page-home' if home else 'page-inner'}"><header class="site-header"><a class="wordmark" href="index.html">Qingxu Yang</a><nav aria-label="Main navigation">{nav}</nav></header>
<div class="layout{'' if with_profile else ' layout-single'}">{profile}<main id="main" class="{'home' if home else ''}">{main}</main></div>
<footer><span>© 2026 Qingxu Yang</span></footer></div>
</body></html>'''
    (OUT / filename).write_text(html, encoding='utf-8')

bio = '''<section class="intro"><p class="eyebrow">Fudan University · School of Economics</p><h1>Welcome to my website!</h1>
<p>I am an Assistant Professor of Economics at the <a href="https://econ.fudan.edu.cn/">School of Economics, Fudan University</a>.</p>
<p>I study digital economics and labor economics, with two research agendas. The first examines how AI reshapes expert decision-making and affects welfare. The second investigates how social norms shape human capital investment and fertility.</p>
<p>I received my Ph.D. in Economics from the Guanghua School of Management at Peking University in 2024. From 2024 to 2026, I was a Postdoctoral Fellow at HKU Business School.</p>
<p>Please feel free to contact me at <a href="mailto:qxyang@fudan.edu.cn">qxyang@fudan.edu.cn</a>.</p>
</section>'''
home = bio
render('index.html','Home',home,True)

research = '<div class="page-title"><p class="eyebrow">Research</p><h1>Papers & projects</h1></div><nav class="section-nav" aria-label="Research sections"><a href="#working-papers">Working papers</a><a href="#publications">Publications</a><a href="#work-in-progress">Work in progress</a></nav>'
for key,title in [('working_papers','Working papers'),('publications','Publications'),('work_in_progress','Work in progress')]:
    research += f'<section class="research-section" id="{key.replace("_","-")}"><h2>{title}</h2>' + ''.join(paper(p, minimal=key == 'work_in_progress') for p in DATA[key]) + '</section>'
render('research.html','Research',research)

teaching = '''<div class="page-title"><p class="eyebrow">Teaching</p><h1>Courses</h1></div>
<section class="teaching-section"><div class="section-heading"><h2>Fudan University</h2></div>
<article class="course"><h3>Panel Data Analysis</h3><p>Undergraduate · Instructor</p></article>
<article class="course"><h3>Digital Economy</h3><p>Graduate · Instructor</p></article>
<article class="course"><h3>Digital Industrial Policy</h3><p>Graduate · Instructor</p></article></section>
<section class="teaching-section"><div class="section-heading"><h2>The University of Hong Kong</h2></div>
<article class="course"><h3>Selected Topics in Digital Economy</h3><p>MECON · Instructor</p></article></section>
<p class="teaching-contact">For course enquiries, please contact <a href="mailto:qxyang@fudan.edu.cn">qxyang@fudan.edu.cn</a>.</p>'''
render('teaching.html','Teaching',teaching)

# The CV file is intentionally absent, so this link opens a 404 page.
cv = '<p><a href="files/Qingxu_Yang_CV.pdf">Download CV</a></p>'
render('cv.html','CV',cv,with_profile=False)
print('Generated 4 pages.')
