import os, re, html

def inline(s):
    s = html.escape(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<i>\1</i>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'(?<![">=/\w])https://([a-z0-9.\-]+\.[a-z]{2,}(?:/[^\s,)<]*)?)', r'<a href="https://\1">https://\1</a>', s)
    return s

BLOCK = re.compile(r'^(#{1,4} |\||- |\d+\. |\s*$)')

def md(text):
    lines = text.split('\n')
    out, i = [], 0
    para, item, items, ordered = [], [], [], False

    def flush_para():
        if para:
            out.append('<p>' + inline(' '.join(para)) + '</p>')
            para.clear()

    def flush_list():
        nonlocal items, item
        if item:
            items.append(' '.join(item)); item = []
        if items:
            tag = 'ol' if ordered else 'ul'
            out.append(f'<{tag}>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + f'</{tag}>')
            items = []

    while i < len(lines):
        raw = lines[i].rstrip()

        if raw.startswith('|'):
            flush_para(); flush_list()
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not set(''.join(cells)) <= set('-: '):
                    rows.append(cells)
                i += 1
            if rows:
                head = '<tr>' + ''.join(f'<th>{inline(c)}</th>' for c in rows[0]) + '</tr>'
                body = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in rows[1:])
                out.append(f'<table>{head}{body}</table>')
            continue

        m = re.match(r'^(#{1,4}) (.*)$', raw)
        if m:
            flush_para(); flush_list()
            lvl = len(m.group(1))
            out.append(f'<h{lvl}>{inline(m.group(2))}</h{lvl}>')
            i += 1; continue

        m = re.match(r'^(\d+)\. (.*)$', raw)
        if m:
            flush_para()
            if items and not ordered: flush_list()
            ordered = True
            if item: items.append(' '.join(item))
            item = [m.group(2)]
            i += 1; continue

        if raw.startswith('- '):
            flush_para()
            if items and ordered: flush_list()
            ordered = False
            if item: items.append(' '.join(item))
            item = [raw[2:]]
            i += 1; continue

        if not raw.strip():
            flush_para(); flush_list()
            i += 1; continue

        # continuation of whatever block we are in
        if item:
            item.append(raw.strip())
        else:
            para.append(raw.strip())
        i += 1

    flush_para(); flush_list()
    return '\n'.join(out)

CSS = """
  :root { --bg:#0A0C12; --panel:#121114; --line:#2D2B31; --t1:#fff; --t2:#E2E6EC; --t3:#8D8D9C; }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { background:var(--bg); color:var(--t3); font-family:Inter,-apple-system,sans-serif;
         font-size:15px; line-height:1.65; padding:44px 32px 90px; }
  .wrap { max-width:860px; margin-inline:auto; }
  h1 { color:var(--t1); font-size:26px; font-weight:600; letter-spacing:-.5px; margin-bottom:10px; }
  h2 { color:var(--t1); font-size:19px; font-weight:600; letter-spacing:-.2px; margin:40px 0 12px;
       padding-top:22px; border-top:1px solid var(--line); }
  h3 { color:var(--t2); font-size:16px; font-weight:600; margin:22px 0 8px; }
  p { margin:12px 0; }
  b { color:var(--t2); font-weight:600; }
  i { color:var(--t2); font-style:italic; }
  a { color:var(--t1); }
  code { font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:13px;
         background:var(--panel); border:1px solid var(--line); border-radius:3px; padding:1px 5px; color:var(--t2); }
  ul, ol { margin:12px 0 12px 22px; }
  li { margin:8px 0; }
  table { width:100%; border-collapse:collapse; margin:18px 0; font-size:14px; }
  th { text-align:left; color:var(--t2); font-weight:600; font-size:11px; letter-spacing:.1em;
       text-transform:uppercase; padding:9px 14px 9px 0; border-bottom:1px solid var(--line); }
  td { padding:10px 14px 10px 0; border-bottom:1px solid var(--line); vertical-align:top; }
  .strip { display:flex; gap:14px; overflow-x:auto; padding:4px 0 14px; }
  figure { flex:none; }
  figure img { display:block; border:1px solid var(--line); border-radius:6px; background:#04060D; }
  .d img { width:460px; }
  .p img { width:220px; }
  figcaption { margin-top:6px; font-size:10px; letter-spacing:.08em; color:var(--t3); }
  .full { max-width:1400px; }
"""

def strip_html(name, items, cls):
    figs = "\n".join(
      f'<figure class="{cls}"><img src="./shots/{s}" loading="lazy" alt="{name} screen {i:02d}"><figcaption>{i:02d}</figcaption></figure>'
      for i, s in enumerate(items))
    return f'<h2>{name}</h2>\n<div class="strip">\n{figs}\n</div>'

shots = sorted(os.listdir('review/shots'))
d = [s for s in shots if s.startswith('d-')]
p = [s for s in shots if s.startswith('p-')]
brief = open('review/brief.md').read()

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Review brief — shipfourteen.com</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
{md(brief)}
<p><i>Same text as plain markdown, easier to fetch: <a href="./brief.md">brief.md</a></i></p>
</div>
<div class="wrap full">
{strip_html('Desktop 1440', d, 'd')}
{strip_html('Phone 390', p, 'p')}
</div>
</body>
</html>
'''
open('review/index.html','w').write(page)
print('rendered', len(page), 'bytes')
