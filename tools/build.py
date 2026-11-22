"""Build the site: wrap src/<slug>.html fragments into chapter pages, write assets/chapters.js and index.html.
Run: python3 tools/build.py"""
import json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = 'Build an Agent Harness'
data = json.load(open(os.path.join(ROOT, 'chapters.json')))
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700'
         '&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=JetBrains+Mono:wght@400;600&display=swap">')


def head(title, prefix):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
{FONTS}
<link rel="stylesheet" href="{prefix}assets/book.css">
</head>'''


def split_scripts(frag):
    m = re.search(r'<!--SCRIPT-->(.*)$', frag, re.S)
    return (frag[:m.start()], m.group(1)) if m else (frag, '')


chapters = []
for st in data['stages']:
    for n, title, slug in st['chapters']:
        ready = os.path.exists(os.path.join(ROOT, 'src', slug + '.html'))
        chapters.append({'n': n, 'title': title, 'slug': slug, 'stage': st['n'], 'ready': ready})
open(os.path.join(ROOT, 'assets', 'chapters.js'), 'w').write('window.IE_CHAPTERS = ' + json.dumps(chapters, indent=0) + ';\n')

for c in chapters:
    if not c['ready']:
        continue
    frag, scripts = split_scripts(open(os.path.join(ROOT, 'src', c['slug'] + '.html')).read())
    page = head(f"{c['n']}. {c['title']}", '../') + f'''
<body data-chapter="{c['n']}" data-stage="{c['stage']}">
<div class="topbar" style="padding-left:0;padding-right:0"><a href="../index.html">← {BOOK}</a><span>Stage {c['stage']} · Chapter {c['n']}</span></div>
<div class="shell">
<nav class="toc" aria-label="Chapter contents"></nav>
<main><article>
{frag}
<div class="navfoot"></div>
</article></main>
</div>
<script src="../assets/chapters.js"></script>
<script src="../assets/book.js"></script>
{scripts}
</body>
</html>
'''
    open(os.path.join(ROOT, 'chapters', c['slug'] + '.html'), 'w').write(page)

guides = []
gdir = os.path.join(ROOT, 'src', 'guides')
for fn in sorted(os.listdir(gdir)) if os.path.isdir(gdir) else []:
    if not fn.endswith('.html'):
        continue
    frag, scripts = split_scripts(open(os.path.join(gdir, fn)).read())
    t = re.sub('<[^>]+>', '', re.search(r'<h1>(.*?)</h1>', frag, re.S).group(1))
    guides.append((f'guides/{fn}', t))
    page = head(t, '../') + f'''
<body data-chapter="" data-stage="">
<div class="topbar" style="padding-left:0;padding-right:0"><a href="../index.html">← {BOOK}</a><span>Guide</span></div>
<div class="shell">
<nav class="toc" aria-label="Contents"></nav>
<main><article>
{frag}
</article></main>
</div>
<script src="../assets/chapters.js"></script>
<script src="../assets/book.js"></script>
{scripts}
</body>
</html>
'''
    open(os.path.join(ROOT, 'guides', fn), 'w').write(page)

cards = []
for st in data['stages']:
    lis = []
    for n, title, slug in st['chapters']:
        c = next(x for x in chapters if x['n'] == n)
        if c['ready']:
            lis.append(f'<li class="ready"><span class="num">{n}</span><a href="chapters/{slug}.html">{html.escape(title)}</a><span class="tag">ready</span></li>')
        else:
            lis.append(f'<li><span class="num">{n}</span><span>{html.escape(title)}</span></li>')
    cards.append(f'<section class="part" id="stage-{st["n"]}"><div class="pn">Stage {st["n"]} · {st["weeks"]}</div>'
                 f'<h2>{html.escape(st["title"])}</h2><ol>{"".join(lis)}</ol>'
                 f'<p class="note" style="margin:12px 0 0">Gate: {html.escape(st["gate"])}</p></section>')
ready = sum(c['ready'] for c in chapters)
glinks = ''.join(f'<li><a href="{h}">{html.escape(t)}</a></li>' for h, t in guides)
idx = head(BOOK, '') + f'''
<body class="index">
<div class="iwrap">
<h1>{BOOK}</h1>
<p class="lede">An agent is a model plus a harness. This book builds a harness from scratch in Python, one component per chapter, and reads the real source code of four very different open-source harnesses along the way: Vercel's eve, Vercel Labs' fx, Earendil's Pi and Pi Durable, and nanocode. Each chapter explains a component from first principles, compares how each product built it and why, covers the research and how Chinese teams approach it, and ends with what we build. Written in public, one chapter a week.</p>
<div class="legend"><span><b class="t-pre">Model</b> is indigo</span><span><b class="t-kv">Harness</b> is teal</span><span><b class="t-dec">Environment</b> is amber</span><span>The same colours are used in every diagram.</span></div>
{('<div class="box real"><span class="lbl">Guides</span><ul>' + glinks + '</ul></div>') if glinks else ''}
<div class="igrid">{''.join(cards)}</div>
<p class="note" style="margin-top:40px">{ready} of {len(chapters)} chapters published. One new chapter a week. Facts carry the date they were checked; code references point to the commits listed in each chapter.</p>
</div>
<script src="assets/book.js"></script>
</body>
</html>
'''
open(os.path.join(ROOT, 'index.html'), 'w').write(idx)
print('ready:', [c['n'] for c in chapters if c['ready']])
