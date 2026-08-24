(function(){
  var root=document.documentElement;

  function currentTheme(){
    var t=root.getAttribute('data-theme');
    if(t==='light'||t==='dark')return t;
    return window.matchMedia&&window.matchMedia('(prefers-color-scheme: light)').matches?'light':'dark';
  }

  try{
    var stored=localStorage.getItem('air-theme');
    if(stored==='light'||stored==='dark')root.setAttribute('data-theme',stored);
  }catch(e){}

  /* Homepage hero: one centered brand stack, then the fixed-ratio three-state visual, then CTA. */
  var heroGrid=document.querySelector('.hero-grid');
  var heroArt=document.querySelector('.hero-art');
  if(heroGrid){
    var heroCopy=heroGrid.firstElementChild;
    if(heroCopy){
      heroGrid.classList.add('hero-stack-layout');
      heroCopy.classList.add('hero-lockup');

      var eyebrow=heroCopy.querySelector('.eyebrow');
      if(eyebrow)eyebrow.remove();

      var heroTitle=heroCopy.querySelector('h1');
      var signature=heroCopy.querySelector('.signature');
      var cta=heroCopy.querySelector('.hero-cta');
      var note=heroCopy.querySelector('.hero-note');

      var brandLockup=document.createElement('div');
      brandLockup.className='hero-brand-lockup';
      brandLockup.innerHTML='<svg class="mark hero-brand-mark" viewBox="0 0 64 64" aria-hidden="true"><rect x="9.5" y="9.5" width="45" height="45" rx="13" stroke-width="5"/><circle cx="32" cy="32" r="8.5"/></svg><div class="hero-air-word">AIR</div>';
      heroCopy.insertBefore(brandLockup,heroCopy.firstChild);

      if(signature&&heroTitle){
        brandLockup.after(signature);
        signature.after(heroTitle);
        heroTitle.classList.add('hero-promise-title');
      }

      if((cta||note)&&heroArt){
        var actions=document.createElement('div');
        actions.className='hero-actions-after-visual';
        if(cta)actions.appendChild(cta);
        if(note)actions.appendChild(note);
        heroArt.after(actions);
      }
    }
  }

  var heroStyle=document.createElement('style');
  heroStyle.textContent='\
.hero .hero-grid.hero-stack-layout{display:flex!important;flex-direction:column;align-items:center!important;gap:0;text-align:center}\
.hero .hero-lockup{width:min(100%,820px);display:flex;flex-direction:column;align-items:center}\
.hero .hero-brand-lockup{display:flex;flex-direction:column;align-items:center;margin:0 0 1.15rem}\
.hero .hero-brand-mark{width:86px;height:86px;margin:0 0 .85rem}\
.hero .hero-air-word{font-size:clamp(4rem,8vw,6.5rem);font-weight:700;line-height:.9;letter-spacing:-.055em;color:var(--text)}\
.hero .hero-lockup .signature{font-size:clamp(1.65rem,3vw,2.35rem);font-weight:500;color:var(--brass);margin:.4rem 0 .7rem}\
.hero .hero-lockup .hero-promise-title{font-size:clamp(1.35rem,2.2vw,1.85rem);font-weight:400;line-height:1.25;letter-spacing:-.02em;margin:0 0 .9rem;color:var(--text)}\
.hero .hero-lockup .sub{max-width:760px;margin:0;color:var(--muted);font-size:clamp(1rem,1.45vw,1.17rem)}\
.hero .hero-art.canonical-triad{width:min(100%,980px)!important;margin:2.25rem auto 0!important;padding:20px!important}\
.hero .hero-art.canonical-triad img{display:block;width:100%!important;height:auto!important}\
.hero .hero-actions-after-visual{display:flex;flex-direction:column;align-items:center;margin-top:1.35rem}\
.hero .hero-actions-after-visual .hero-cta{justify-content:center}\
.hero .hero-actions-after-visual .hero-note{text-align:center;margin:.9rem 0 0}\
@media(max-width:700px){.hero .hero-brand-mark{width:72px;height:72px}.hero .hero-art.canonical-triad{padding:12px!important;margin-top:1.6rem!important}.hero .hero-actions-after-visual{margin-top:1rem}}';
  document.head.appendChild(heroStyle);

  if(heroArt){
    heroArt.classList.add('canonical-triad');
    heroArt.style.display='block';
    heroArt.style.overflow='hidden';
    heroArt.innerHTML='<img data-air-triad alt="Focused. Fluid. AIR." width="566" height="260">';
  }

  function syncTriad(){
    var img=document.querySelector('[data-air-triad]');
    if(img)img.src=currentTheme()==='light'?'air-three-states-promo-light.svg':'air-three-states-promo-dark.svg';
  }
  syncTriad();

  document.addEventListener('click',function(e){
    var t=e.target.closest('[data-theme-toggle]');
    if(t){
      var now=currentTheme();
      var next=now==='light'?'dark':'light';
      root.setAttribute('data-theme',next);
      try{localStorage.setItem('air-theme',next);}catch(x){}
      syncTriad();
    }
    var m=e.target.closest('[data-menu-toggle]');
    if(m){
      var nav=document.getElementById('nav');
      if(nav)nav.classList.toggle('open');
    }
  });

  var here=location.pathname.split('/').pop()||'index.html';
  document.querySelectorAll('#nav a').forEach(function(a){
    if(a.getAttribute('href')===here)a.classList.add('active');
  });

  /* AIR attentive mark: move the ember by real SVG coordinates, not CSS transforms. */
  var eye=document.querySelector('.site-header .brand .mark');
  if(eye){
    eye.classList.add('air-eye');
    var pupil=eye.querySelector('circle');
    if(pupil){
      pupil.classList.add('air-pupil');

      var baseX=parseFloat(pupil.getAttribute('cx'))||32;
      var baseY=parseFloat(pupil.getAttribute('cy'))||32;
      var baseR=parseFloat(pupil.getAttribute('r'))||8.5;
      var currentX=baseX,currentY=baseY,targetX=baseX,targetY=baseY;
      var raf=0;
      var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;

      function paint(){
        currentX+=(targetX-currentX)*0.28;
        currentY+=(targetY-currentY)*0.28;
        pupil.setAttribute('cx',currentX.toFixed(2));
        pupil.setAttribute('cy',currentY.toFixed(2));
        if(Math.abs(targetX-currentX)>0.03||Math.abs(targetY-currentY)>0.03){
          raf=requestAnimationFrame(paint);
        }else{
          currentX=targetX;currentY=targetY;
          pupil.setAttribute('cx',currentX.toFixed(2));
          pupil.setAttribute('cy',currentY.toFixed(2));
          raf=0;
        }
      }

      function wake(){if(!raf)raf=requestAnimationFrame(paint);}
      function centre(){targetX=baseX;targetY=baseY;wake();}

      if(!reduce){
        window.addEventListener('pointermove',function(e){
          if(e.pointerType&&e.pointerType!=='mouse')return;
          var r=eye.getBoundingClientRect();
          if(!r.width||!r.height)return;
          var dx=e.clientX-(r.left+r.width/2);
          var dy=e.clientY-(r.top+r.height/2);
          var distance=Math.sqrt(dx*dx+dy*dy);
          if(distance<0.001){centre();return;}
          var strength=Math.min(distance/110,1);
          var travel=8.5*strength;
          targetX=baseX+(dx/distance)*travel;
          targetY=baseY+(dy/distance)*travel;
          wake();
        },{passive:true});
        window.addEventListener('mouseout',function(e){if(!e.relatedTarget)centre();});
        window.addEventListener('blur',centre);
      }

      var blinkTimer=0;
      document.addEventListener('click',function(){
        clearTimeout(blinkTimer);
        pupil.setAttribute('r',(baseR*0.28).toFixed(2));
        blinkTimer=setTimeout(function(){pupil.setAttribute('r',baseR.toFixed(2));},120);
      });
    }
  }
})();
