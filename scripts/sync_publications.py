#!/usr/bin/env python3
"""Refresh publications_auto.yml using the OpenAlex API (not Google Scholar scraping).

Requires OPENALEX_API_KEY (free from https://openalex.org/settings/api).
The author identity is resolved by intersecting authors in at least two verified
DOI seed papers; it is not inferred from name alone.
Failures leave existing data unchanged.
"""
from __future__ import annotations
import json,os,sys,urllib.parse,urllib.request
from collections import Counter
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[1]
API = 'https://api.openalex.org'
KEY = os.environ.get('OPENALEX_API_KEY','').strip()
NAME = 'woonghee jung'

def norm_name(s):
    return ''.join(c.lower() for c in (s or '') if c.isalpha())

def norm_doi(s):
    d=(s or '').strip().lower()
    return d.removeprefix('https://doi.org/').removeprefix('http://dx.doi.org/').strip()

def fetch(url, params=None):
    if not KEY: raise RuntimeError('OPENALEX_API_KEY is missing. No changes made.')
    params=dict(params or {}); params['api_key']=KEY
    url=url+('?' if '?' not in url else '&')+urllib.parse.urlencode(params)
    request=urllib.request.Request(url,headers={'User-Agent':'SHARE-Lab-Site/1.0 (academic bibliography updater)','Accept':'application/json'})
    with urllib.request.urlopen(request,timeout=25) as resp:
        return json.load(resp)

def author_id_from_seed(curated):
    # Seed papers used to disambiguate against similarly named researchers.
    counts=Counter()
    for row in curated:
        d=norm_doi(row.get('doi'))
        if not d: continue
        data=fetch(API+'/works/https://doi.org/'+urllib.parse.quote(d,safe='/'))
        ids=set()
        for a in data.get('authorships',[]):
            author=a.get('author') or {}
            if norm_name(author.get('display_name')) == norm_name(NAME):
                aid=author.get('id','').rsplit('/',1)[-1]
                if aid: ids.add(aid)
        counts.update(ids)
        if len(counts)>0 and max(counts.values())>=2:break
    if not counts or max(counts.values())<2:
        raise RuntimeError('Could not verify one unique OpenAlex author ID across at least two seed publications.')
    ranked=counts.most_common()
    if len(ranked)>1 and ranked[0][1]==ranked[1][1]:
        raise RuntimeError('Ambiguous OpenAlex author identity. Review the verified DOI seeds.')
    return ranked[0][0]

def main():
    curated=yaml.safe_load((ROOT/'publications_curated.yml').read_text('utf-8')).get('publications',[])
    author_id=os.environ.get('OPENALEX_AUTHOR_ID','').strip() or author_id_from_seed(curated)
    author_id=author_id.rsplit('/',1)[-1]
    if not author_id.startswith('A') or not author_id[1:].isdigit():
        raise RuntimeError('OpenAlex author ID has an unexpected format')
    existing=yaml.safe_load((ROOT/'publications_auto.yml').read_text('utf-8')) or {}
    auto_existing=existing.get('publications') or []
    exclude_path=ROOT/'publications_exclude.txt'
    excluded={norm_doi(s.split('#')[0]) for s in exclude_path.read_text('utf-8').splitlines() if s.strip() and not s.startswith('#')} if exclude_path.exists() else set()
    curated_dois={norm_doi(r.get('doi')) for r in curated}
    response=fetch(API+'/works', {'filter':f'author.id:{author_id}', 'per_page':100,'page':1,'sort':'publication_date:desc'})
    if int(response.get('meta',{}).get('count',0))>100:
        raise RuntimeError('More than 100 works found; pagination must be reviewed manually.')
    found=[]
    for w in response.get('results',[]):
        doi=norm_doi(w.get('doi'))
        if not doi or doi in excluded or doi in curated_dois:continue
        if w.get('type')!='article':continue
        auth=w.get('authorships',[])
        if not any(norm_name((a.get('author') or {}).get('display_name'))==norm_name(NAME) and (a.get('author') or {}).get('id','').endswith(author_id) for a in auth):continue
        names=[(a.get('author') or {}).get('display_name','') for a in auth if (a.get('author') or {}).get('display_name')]
        source=(((w.get('primary_location') or {}).get('source') or {}).get('display_name'))
        if not source or not w.get('title') or not w.get('publication_year'):continue
        found.append({'year':int(w['publication_year']), 'title':w['title'].strip(), 'authors':', '.join(names[:8]) + (' et al.' if len(names)>8 else ''), 'venue':source, 'doi':doi})
    if not found:
        # Preserve already reviewed automatic records when the upstream source is temporarily empty.
        if auto_existing:
            raise RuntimeError('No records found for the resolved author, keeping previously fetched records.')
        print('No new OpenAlex articles; initial list remains curated.'); return
    found.sort(key=lambda x:(x['year'],x['title'].lower()),reverse=True)
    dest=ROOT/'publications_auto.yml'
    # Atomic replacement. Do not erase manually curated entries.
    out=yaml.safe_dump({'publications':found},sort_keys=False,allow_unicode=True,width=145)
    if out!=dest.read_text('utf-8'):
        temporary=dest.with_suffix('.tmp')
        temporary.write_text(out,encoding='utf-8')
        temporary.replace(dest)
        print('Updated',len(found),'additional articles for',author_id)
    else: print('Up-to-date',len(found),'additional articles for',author_id)

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('Publication sync could not complete; existing bibliography is unchanged:',exc,file=sys.stderr)
        sys.exit(1)
