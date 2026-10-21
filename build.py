#!/usr/bin/env python3
"""Generate a SHARE Lab website and Quarto-compatible QMD sources from content.yml.

Requires: pip install pyyaml jinja2
Then: python build.py
"""
from pathlib import Path
import shutil
from collections import defaultdict
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'docs'
DIST.mkdir(exist_ok=True)
with (ROOT / 'content.yml').open(encoding='utf-8') as f:
    content = yaml.safe_load(f)

def load_publications(path):
    if not path.exists(): return []
    return yaml.safe_load(path.read_text(encoding='utf-8')).get('publications', []) or []

def normalized_doi(d):
    return str(d or '').lower().replace('https://doi.org/', '').replace('http://dx.doi.org/', '').strip()

publications = load_publications(ROOT/'publications_curated.yml') + load_publications(ROOT/'publications_auto.yml')
publications.extend(content.get('publications', []))
seen = set(); merged = []
for pub in publications:
    key = normalized_doi(pub.get('doi')) or pub.get('title','').casefold().strip()
    if not key or key in seen: continue
    seen.add(key)
    merged.append(pub)
merged.sort(key=lambda p: (int(p.get('year') or 0),p.get('title','').lower()), reverse=True)
content['publications'] = merged

env = Environment(loader=FileSystemLoader(str(ROOT / 'templates')), autoescape=select_autoescape(['html']), trim_blocks=True, lstrip_blocks=True)
menu=[
    {'id':'home','title':'Home','url':'index.html'},
    {'id':'people','title':'People','url':'people.html'},
    {'id':'research','title':'Research','url':'research.html'},
    {'id':'publications','title':'Publications','url':'publications.html'},
    {'id':'news','title':'News','url':'news.html'},
    {'id':'contact','title':'Contact','url':'contact.html'},
]
ctx={**content,'menu':menu}
shell=env.get_template('shell.html')
for page in ['home','people','research','publications','news','contact']:
    filename='index' if page=='home' else page
    body=env.get_template(f'{page}.html').render(**ctx)
    whole=shell.render(**ctx, active=page, page_body=body)
    html=f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#ffffff">
<title>{'SHARE Lab' if page=='home' else page.capitalize()+' | SHARE Lab'}</title>
<meta name="description" content="SHARE Lab at Dankook University – Systems and Hazards Analysis for Resilience to Extremes.">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg"><link rel="stylesheet" href="assets/styles.css"></head>
<body>{whole}</body></html>'''
    (DIST / f'{filename}.html').write_text(html,encoding='utf-8')
    # Quarto-compatible source for those who prefer managing a Quarto website.
    qmd=f'''---
title: "{'SHARE Lab' if page=='home' else page.capitalize()}"
page-layout: full
title-block-banner: false
---

{whole}
'''
    (ROOT / f'{filename}.qmd').write_text(qmd,encoding='utf-8')
shutil.copytree(ROOT / 'assets',DIST / 'assets',dirs_exist_ok=True)
(DIST / '.nojekyll').write_text('',encoding='utf-8')
print('Generated:', ', '.join(p.name for p in DIST.glob('*.html')))
print(f'Publications rendered: {len(content["publications"])} (curated + OpenAlex auto)')
