# Page-level measurements behind data/shop/brief-status.json (session 38650305). Run from the repo root.
import pathlib,re,json,sys
root=pathlib.Path('.')
SKIP={'.git','archive','docs','sessions','node_modules','__pycache__'}
pages=[p for p in root.rglob('*.html') if not (set(p.parts)&SKIP)]
print('published html pages (excl archive/docs/sessions):',len(pages))
t=d=og=ld=0; nodesc=[]; notitle=[]
for p in pages:
    h=p.read_text(encoding='utf-8',errors='replace')
    if re.search(r'<title>[^<]+</title>',h,re.I): t+=1
    else: notitle.append(str(p))
    if re.search(r'<meta[^>]+name=["\']description["\'][^>]*content=["\'][^"\']+',h,re.I): d+=1
    else: nodesc.append(str(p))
    if re.search(r'property=["\']og:image',h,re.I): og+=1
    if 'application/ld+json' in h: ld+=1
print('title',t,'desc',d,'og:image',og,'ld+json',ld)
print('no-title',notitle[:5],'no-desc',nodesc[:5])
# sponsored check
PH=re.compile(r'https?://(?:[a-z0-9-]+\.)*(?:amazon\.[a-z.]+|link\.amazon\.com|link\.amazon|amzn\.to|a\.co)/',re.I)
tot=bad=0; badp=[]
for p in pages:
    h=p.read_text(encoding='utf-8',errors='replace')
    for m in re.finditer(r'<a\b[^>]*>',h,re.I):
        tag=m.group(0); hm=re.search(r'href=["\']([^"\']+)',tag)
        if not hm or not PH.match(hm.group(1)): continue
        if 'affiliate-program.amazon.com' in hm.group(1): continue
        tot+=1
        rm=re.search(r'rel=["\']([^"\']*)',tag)
        if not rm or 'sponsored' not in rm.group(1).split(): bad+=1; badp.append(str(p))
print('product links',tot,'not sponsored',bad,badp[:5])
# images
imgs={}
for p in pages:
    h=p.read_text(encoding='utf-8',errors='replace')
    for s in re.findall(r'<img\b[^>]*src=["\']([^"\']+)',h,re.I):
        imgs[s]=imgs.get(s,0)+1
print('img srcs:',sorted(imgs.items(),key=lambda x:-x[1])[:25])
for kw in ['which one is for you','per centimet','per cm','cm of counter','trending','Which one is for you','counter-space','counter space']:
    hits=[str(p) for p in pages if kw.lower() in p.read_text(encoding='utf-8',errors='replace').lower()]
    print(repr(kw),len(hits),hits[:6])
