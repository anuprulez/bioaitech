#!/usr/bin/env python3
"""Build the Markdown website using only Python's standard library."""
import html, re, shutil
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).parent; CONTENT=ROOT/'content'; DIST=ROOT/'dist'
def frontmatter(text):
    meta={}
    if text.startswith('---\n'):
        raw,text=text[4:].split('\n---\n',1)
        for line in raw.splitlines():
            key,_,value=line.partition(':'); meta[key.strip()]=value.strip()
    return meta,text
def inline(text):
    value=html.escape(text,quote=False)
    value=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',value); value=re.sub(r'\*([^*]+)\*',r'<em>\1</em>',value)
    return re.sub(r'\[([^]]+)]\(([^)]+)\)',r'<a href="\2">\1</a>',value)
def markdown(text):
    out=[]; paragraph=[]; in_html=False
    def flush():
        if paragraph: out.append(f"<p>{inline(' '.join(paragraph))}</p>"); paragraph.clear()
    for line in text.splitlines():
        s=line.strip()
        if s.startswith('<') or in_html:
            flush(); out.append(line); in_html=not(s.startswith('</') or s.endswith('</section>'))
        elif not s: flush()
        elif (m:=re.match(r'^(#{1,3})\s+(.+)$',s)):
            flush(); n=len(m.group(1)); out.append(f'<h{n}>{inline(m.group(2))}</h{n}>')
        else: paragraph.append(s)
    flush(); return '\n'.join(out)
def build():
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir(); shutil.copytree(ROOT/'static',DIST/'assets'); template=(ROOT/'templates/base.html').read_text()
    for source in CONTENT.glob('*.md'):
        meta,body=frontmatter(source.read_text()); slug=source.stem; path='/' if slug=='index' else f'/{slug}/'; target=DIST/'index.html' if slug=='index' else DIST/slug/'index.html'; target.parent.mkdir(parents=True,exist_ok=True)
        values={'title':meta.get('title','BioAI Tech'),'description':meta.get('description','AI in life science'),'path':path,'page_class':'home' if slug=='index' else 'prose-page','content':markdown(body),'year':str(datetime.now().year)}; page=template
        for key,value in values.items(): page=page.replace('{{ '+key+' }}',value)
        target.write_text(page)
    shutil.copy(ROOT/'CNAME',DIST/'CNAME'); (DIST/'.nojekyll').touch(); (DIST/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://bioaitech.org/sitemap.xml\n'); (DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://bioaitech.org/</loc></url><url><loc>https://bioaitech.org/privacy/</loc></url></urlset>')
    print(f'Built {len(list(CONTENT.glob("*.md")))} pages in {DIST}')
if __name__=='__main__': build()
