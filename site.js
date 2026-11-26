/* ===== Contra shared header + footer injector (identical on every page) ===== */
(function(){
  "use strict";
  var isHome = !!document.body.getAttribute('data-home');          // index sets data-home
  var HOME = isHome ? '' : 'contra7-1.html';                       // prefix for links back to index sections
  var q = HOME + '#request';                                        // quote target
  var coll = HOME + '#collections';

  var ARR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  var header =
  '<header class="site-head" id="siteHead"><div class="wrap head-in">'+
    '<a class="logo" href="'+(HOME||'#')+'"><img src="contra_logo_black.png" alt="Contra"></a>'+
    '<nav class="nav" aria-label="Main">'+
      '<div class="nav-item"><a class="nav-link" href="'+coll+'">Collections</a></div>'+
      '<div class="nav-item"><a class="nav-link" href="about.html">About</a></div>'+
      '<div class="nav-item"><a class="nav-link" href="clients.html">Clients</a></div>'+
      '<div class="nav-item"><a class="nav-link" href="contact.html">Contact</a></div>'+
    '</nav>'+
    '<div class="head-right">'+
      '<a class="btn btn-acc btn-quote-desktop" href="'+q+'">Request a quote '+ARR+'</a>'+
      '<button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="drawer"><span class="bars"><i></i><i></i><i></i></span>MENU</button>'+
    '</div>'+
  '</div></header>'+
  '<div class="drawer" id="drawer" aria-hidden="true">'+
    '<div class="drawer-top"><a class="logo" href="'+(HOME||'#')+'"><img src="contra_logo_black.png" alt="Contra"></a><button class="drawer-close" id="drawerClose" aria-label="Close menu">✕</button></div>'+
    '<div class="drawer-nav">'+
      '<a href="'+coll+'">Collections</a>'+
      '<a href="about.html">About</a>'+
      '<a href="clients.html">Clients</a>'+
      '<a href="contact.html">Contact</a>'+
    '</div>'+
    '<div class="drawer-cta"><a class="btn btn-acc" href="'+q+'">Request a quote '+ARR+'</a></div>'+
  '</div>';

  var footer =
  '<footer class="site-foot"><div class="foot-grid">'+
    '<div class="foot-brand">'+
      '<a class="logo" href="'+(HOME||'#')+'"><img src="contra_logo_black.png" alt="Contra"></a>'+
      '<p class="foot-tag">Factory-direct teamwear, made in-house for clubs, schools, academies &amp; brands across the EU.</p>'+
      '<div class="foot-social">'+
        '<a href="#" aria-label="Instagram"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="2.5" y="2.5" width="19" height="19" rx="5.5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg></a>'+
        '<a href="#" aria-label="LinkedIn"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="2.5" y="2.5" width="19" height="19" rx="4"/><path d="M7 10v7M7 7v.01M11 17v-4a2 2 0 014 0v4M11 10v7" stroke-linecap="round"/></svg></a>'+
        '<a href="#" aria-label="YouTube"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="2.5" y="5.5" width="19" height="13" rx="3.5"/><path d="M10 9.5l5 2.5-5 2.5z" fill="currentColor" stroke="none"/></svg></a>'+
        '<a href="#" aria-label="TikTok"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M14 4c.5 2.5 2 4 4.5 4.3V11c-1.7 0-3.2-.5-4.5-1.4V15a5 5 0 11-5-5v2.7A2.3 2.3 0 1011.3 15V4H14z"/></svg></a>'+
      '</div>'+
    '</div>'+
    '<div class="foot-contact"><h4>Get in touch</h4><ul>'+
      '<li><span class="ci"><svg viewBox="0 0 24 24"><path d="M12 21s-7-5.3-7-11a7 7 0 1114 0c0 5.7-7 11-7 11z" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="10" r="2.5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></span>Warsaw, Poland · EU</li>'+
      '<li><span class="ci"><svg viewBox="0 0 24 24"><path d="M5 4h4l2 5-3 2a12 12 0 005 5l2-3 5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg></span><a href="tel:+48221234567">+48 22 123 45 67</a></li>'+
      '<li><span class="ci"><svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M4 7l8 6 8-6" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></span><a href="mailto:info@contraon.com">info@contraon.com</a></li>'+
    '</ul></div>'+
  '</div>'+
  '<div class="foot-base"><span>© 2026 Contra Teamwear · Built bulk, worn proud.</span><div class="legal"><a href="#">Privacy Policy</a><a href="#">Terms &amp; Conditions</a></div></div>'+
  '</footer>';

  // inject
  var h = document.getElementById('site-header');
  var f = document.getElementById('site-footer');
  if(h) h.outerHTML = header; else document.body.insertAdjacentHTML('afterbegin', header);
  if(f) f.outerHTML = footer; else document.body.insertAdjacentHTML('beforeend', footer);

  // drawer behavior
  var drawer=document.getElementById('drawer'),menuBtn=document.getElementById('menuBtn'),drawerClose=document.getElementById('drawerClose');
  function openD(){drawer.classList.add('is-open');drawer.setAttribute('aria-hidden','false');menuBtn.setAttribute('aria-expanded','true');document.body.style.overflow='hidden';}
  function closeD(){drawer.classList.remove('is-open');drawer.setAttribute('aria-hidden','true');menuBtn.setAttribute('aria-expanded','false');document.body.style.overflow='';}
  if(menuBtn)menuBtn.addEventListener('click',openD);
  if(drawerClose)drawerClose.addEventListener('click',closeD);
  if(drawer)drawer.querySelectorAll('a').forEach(function(a){a.addEventListener('click',closeD);});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')closeD();});

  // scroll shadow
  var head=document.getElementById('siteHead'),tick=false;
  function setHead(){if(head)head.classList.toggle('is-scrolled',window.scrollY>20);tick=false;}
  window.addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(setHead);}},{passive:true});
  setHead();
})();
