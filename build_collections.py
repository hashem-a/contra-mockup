#!/usr/bin/env python3
# Generates collection-<handle>.html pages from local contra-products/ folders.
# Re-run after curating (deleting images) — it reads whatever remains on disk.
import json, io, os, html, re

BASE = os.path.dirname(os.path.abspath(__file__))
PRODUCTS = os.path.join(BASE, "contra-products")
MANIFEST = os.path.join(BASE, "contra-products_manifest.json")

COLLECTIONS = [
    ("club",    "Club",    "Professional Clubs Apparel",   "Match, training & travel kit for professional and amateur clubs — your crest, your colours, every squad."),
    ("school",  "School",  "Premium School Uniforms",      "PE kit, uniforms and squad wear for schools and universities, in full size runs, reorderable every term."),
    ("academy", "Academy", "Specialized Academy Apparel",  "Match and training kit built for sport academies and development programmes."),
    ("company", "Company", "Corporate Wear Solutions",     "Branded staff, event and corporate teamwear — your logo, delivered fast."),
]

# title lookup from manifest (handle -> title)
titles = {}
try:
    m = json.load(io.open(MANIFEST, encoding="utf-8"))
    for coll, items in m.items():
        for it in items:
            titles[(coll, it["handle"])] = it["title"]
except Exception:
    pass

def nice(handle, coll):
    t = titles.get((coll, handle))
    if t:
        return t
    return handle.replace("-", " ").title()

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Contra — {TITLE} Collection</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="site.css">
<style>
:root{
  --ink:#171a12;--lime:#d4ed99;--lime-bright:#e4f7a8;--lime-deep:#b8dd6a;--lime-dark:#9cc24e;
  --accent:#5a7d12;--pop-lime:#DBFC37;--olive:#3f4a2e;
  --white:#fff;--soft:#f7f8f2;--soft-2:#eef1e6;--border:#e3e6da;--muted:#7c8368;--muted-2:#616753;
  --font-d:"Inter Tight",sans-serif;--font-b:"Inter",sans-serif;--font-m:"JetBrains Mono",monospace;
  --wrap:1280px;--gut:clamp(1.25rem,4vw,4.5rem);--ease:cubic-bezier(.22,.61,.36,1);--head-h:72px;--r:14px;--r-lg:22px;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:var(--font-b);color:var(--ink);background:var(--white);line-height:1.55;-webkit-font-smoothing:antialiased;padding-top:var(--head-h)}
img{display:block;max-width:100%}
a{color:inherit;text-decoration:none}
button{font:inherit;cursor:pointer;border:none;background:none;color:inherit}
::selection{background:var(--lime);color:var(--ink)}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px;border-radius:6px}
.wrap{max-width:var(--wrap);margin:0 auto;padding-inline:var(--gut)}
.btn{display:inline-flex;align-items:center;gap:.55rem;font-family:var(--font-d);font-weight:600;font-size:1rem;padding:.9rem 1.6rem;border-radius:999px;transition:background .2s,transform .2s}
.btn svg{width:17px;height:17px;stroke:currentColor;fill:none}
.btn-acc{background:var(--ink);color:#fff}.btn-acc:hover{background:#000;transform:translateY(-1px)}
/* hero band */
.col-hero{background:linear-gradient(170deg,var(--lime-bright),var(--lime) 60%,var(--lime-deep));padding:clamp(3rem,7vw,5.5rem) 0}
.col-hero .crumb{font-family:var(--font-m);font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:var(--olive)}
.col-hero h1{font-family:var(--font-d);font-weight:700;letter-spacing:-.03em;text-transform:uppercase;font-size:clamp(2.6rem,1.4rem+4vw,5rem);line-height:.9;margin-top:.6rem}
.col-hero p{margin-top:1rem;max-width:52ch;color:var(--olive);font-size:1.1rem}
.col-hero .count{margin-top:1.2rem;font-family:var(--font-m);font-size:.74rem;letter-spacing:.08em;text-transform:uppercase;color:var(--ink);background:rgba(255,255,255,.6);display:inline-block;padding:.4rem .8rem;border-radius:999px}
/* grid */
.grid-sec{padding:clamp(3rem,6vw,5rem) 0}
.pgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:1.2rem}
.pcard{background:#fff;border:1px solid var(--border);border-radius:var(--r-lg);overflow:hidden;cursor:pointer;transition:transform .3s var(--ease),box-shadow .3s,border-color .3s;display:flex;flex-direction:column;text-align:left}
.pcard:hover{transform:translateY(-5px);box-shadow:0 22px 48px rgba(25,25,25,.12);border-color:var(--lime-dark)}
.pcard .pc-img{position:relative;aspect-ratio:1;background:var(--soft);overflow:hidden}
.pcard .pc-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .6s var(--ease)}
.pcard:hover .pc-img img{transform:scale(1.05)}
.pcard .pc-badge{position:absolute;top:.7rem;right:.7rem;background:rgba(255,255,255,.92);font-family:var(--font-m);font-size:.6rem;font-weight:600;letter-spacing:.06em;padding:.2rem .5rem;border-radius:5px;color:var(--muted-2)}
.pcard .pc-meta{padding:.9rem 1rem 1.1rem}
.pcard h3{font-family:var(--font-d);font-weight:600;font-size:1rem;line-height:1.2;color:var(--ink)}
.pcard .pc-cta{margin-top:.5rem;font-family:var(--font-m);font-size:.68rem;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
/* cta band */
.cta-band{background:var(--ink);color:#fff;text-align:center;padding:clamp(3rem,6vw,5rem) 0}
.cta-band h2{font-family:var(--font-d);font-weight:700;letter-spacing:-.02em;font-size:clamp(1.8rem,3vw,2.6rem)}
.cta-band p{margin:1rem auto 2rem;max-width:44ch;color:#b9bcc6}
.cta-band .btn-acc{background:var(--lime);color:var(--ink)}.cta-band .btn-acc:hover{background:var(--lime-deep)}
/* modal carousel */
.modal{position:fixed;inset:0;z-index:100;background:rgba(10,12,8,.9);display:none;align-items:center;justify-content:center;padding:2rem}
.modal.is-open{display:flex}
.modal-inner{position:relative;max-width:900px;width:100%;background:#fff;border-radius:var(--r-lg);overflow:hidden;display:flex;flex-direction:column;max-height:90vh}
.modal-stage{position:relative;background:var(--soft);aspect-ratio:1;max-height:70vh}
.modal-stage img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;opacity:0;transition:opacity .3s}
.modal-stage img.is-active{opacity:1}
.modal-nav{position:absolute;top:50%;transform:translateY(-50%);width:44px;height:44px;border-radius:50%;background:rgba(255,255,255,.95);display:grid;place-items:center;box-shadow:0 4px 14px rgba(0,0,0,.2);z-index:2}
.modal-nav svg{width:20px;height:20px;stroke:var(--ink);fill:none}
.modal-prev{left:1rem}.modal-next{right:1rem}
.modal-foot{padding:1rem 1.3rem;display:flex;align-items:center;justify-content:space-between;gap:1rem;border-top:1px solid var(--border)}
.modal-foot h3{font-family:var(--font-d);font-weight:700;font-size:1.15rem}
.modal-foot .dots{display:flex;gap:.3rem}
.modal-foot .dots i{width:7px;height:7px;border-radius:50%;background:var(--border)}
.modal-foot .dots i.is-active{background:var(--ink)}
.modal-close{position:absolute;top:1rem;right:1rem;z-index:3;width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,.95);display:grid;place-items:center;font-size:1.3rem;color:var(--ink);box-shadow:0 4px 14px rgba(0,0,0,.2)}
@media(max-width:1023px){.pgrid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:720px){.pgrid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:460px){.pgrid{grid-template-columns:1fr 1fr}}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
</style>
</head>
<body>
<div id="site-header"></div>

<section class="col-hero"><div class="wrap">
  <div class="crumb">Home / Collections / {TITLE}</div>
  <h1>{TITLE}</h1>
  <p>{DESC}</p>
  <div class="count">{COUNT} products</div>
</div></section>

<section class="grid-sec"><div class="wrap">
  <div class="pgrid">
{CARDS}
  </div>
</div></section>

<section class="cta-band"><div class="wrap">
  <h2>Kit your team in {TITLE} wear.</h2>
  <p>Request a quote and a Contra rep will build your first mockup — factory-direct, no commitment.</p>
  <a class="btn btn-acc" href="contra7-1.html#request">Request a quote <svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
</div></section>

<div id="site-footer"></div>

<div class="modal" id="modal" aria-hidden="true">
  <div class="modal-inner">
    <button class="modal-close" id="mClose" aria-label="Close">✕</button>
    <div class="modal-stage" id="mStage"></div>
    <button class="modal-nav modal-prev" id="mPrev" aria-label="Previous"><svg viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
    <button class="modal-nav modal-next" id="mNext" aria-label="Next"><svg viewBox="0 0 24 24"><path d="M9 6l6 6-6 6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
    <div class="modal-foot"><h3 id="mTitle"></h3><div class="dots" id="mDots"></div></div>
  </div>
</div>

<script>
var PRODUCTS = {DATA};
(function(){
  "use strict";
  var modal=document.getElementById('modal'),stage=document.getElementById('mStage'),
      titleEl=document.getElementById('mTitle'),dotsEl=document.getElementById('mDots'),
      prev=document.getElementById('mPrev'),next=document.getElementById('mNext'),
      close=document.getElementById('mClose');
  var imgs=[],idx=0;
  function render(){
    stage.querySelectorAll('img').forEach(function(im,i){im.classList.toggle('is-active',i===idx);});
    dotsEl.querySelectorAll('i').forEach(function(d,i){d.classList.toggle('is-active',i===idx);});
  }
  function open(p){
    imgs=p.images;idx=0;titleEl.textContent=p.title;
    stage.innerHTML='';dotsEl.innerHTML='';
    imgs.forEach(function(src,i){
      var im=document.createElement('img');im.src=src;im.alt=p.title;if(i===0)im.className='is-active';stage.appendChild(im);
      var d=document.createElement('i');if(i===0)d.className='is-active';dotsEl.appendChild(d);
    });
    var multi=imgs.length>1;prev.style.display=next.style.display=multi?'grid':'none';
    modal.classList.add('is-open');modal.setAttribute('aria-hidden','false');document.body.style.overflow='hidden';
  }
  function hide(){modal.classList.remove('is-open');modal.setAttribute('aria-hidden','true');document.body.style.overflow='';}
  prev.addEventListener('click',function(){idx=(idx-1+imgs.length)%imgs.length;render();});
  next.addEventListener('click',function(){idx=(idx+1)%imgs.length;render();});
  close.addEventListener('click',hide);
  modal.addEventListener('click',function(e){if(e.target===modal)hide();});
  document.addEventListener('keydown',function(e){
    if(!modal.classList.contains('is-open'))return;
    if(e.key==='Escape')hide();
    else if(e.key==='ArrowLeft'){idx=(idx-1+imgs.length)%imgs.length;render();}
    else if(e.key==='ArrowRight'){idx=(idx+1)%imgs.length;render();}
  });
  document.querySelectorAll('[data-prod]').forEach(function(card){
    card.addEventListener('click',function(){open(PRODUCTS[card.getAttribute('data-prod')]);});
  });
})();
</script>
<script src="site.js"></script>
</body>
</html>
"""

def build():
    data_all = {}
    for handle_coll, TITLE, SUB, DESC in COLLECTIONS:
        coll = handle_coll
        cdir = os.path.join(PRODUCTS, coll)
        if not os.path.isdir(cdir):
            continue
        cards = []
        pdata = {}
        prod_handles = sorted(os.listdir(cdir))
        live = 0
        for ph in prod_handles:
            pdir = os.path.join(cdir, ph)
            if not os.path.isdir(pdir):
                continue
            imgs = sorted(f for f in os.listdir(pdir) if f.lower().endswith(".jpg"))
            if not imgs:
                continue
            live += 1
            rels = [f"contra-products/{coll}/{ph}/{im}" for im in imgs]
            title = nice(ph, coll)
            key = ph
            pdata[key] = {"title": title, "images": rels}
            cover = rels[0]
            extra = f'<span class="pc-badge">+{len(rels)-1}</span>' if len(rels) > 1 else ""
            cards.append(
                f'    <button class="pcard" data-prod="{html.escape(key)}">'
                f'<div class="pc-img"><img loading="lazy" src="{html.escape(cover)}" alt="{html.escape(title)}">{extra}</div>'
                f'<div class="pc-meta"><h3>{html.escape(title)}</h3>'
                f'<div class="pc-cta">View photos</div></div></button>'
            )
        page = HEAD.replace("{TITLE}", TITLE).replace("{DESC}", html.escape(DESC)) \
                   .replace("{COUNT}", str(live)) \
                   .replace("{CARDS}", "\n".join(cards)) \
                   .replace("{DATA}", json.dumps(pdata, ensure_ascii=False))
        out = os.path.join(BASE, f"collection-{coll}.html")
        io.open(out, "w", encoding="utf-8").write(page)
        print(f"wrote collection-{coll}.html ({live} products)")

if __name__ == "__main__":
    build()
