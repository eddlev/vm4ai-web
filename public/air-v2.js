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

  /* Homepage hero: compact brand lockup + the real three-state cards directly underneath. */
  var heroGrid=document.querySelector('.hero-grid');
  var heroArt=document.querySelector('.hero-art');
  var statesSection=document.querySelector('section.states');
  var stateGrid=statesSection&&statesSection.querySelector('.state-grid');
  var stateRule=statesSection&&statesSection.querySelector('.state-rule');

  if(heroGrid){
    var heroCopy=heroGrid.firstElementChild;
    if(heroCopy){
      heroGrid.classList.add('hero-stack-v4');
      heroCopy.classList.add('hero-lockup-v4');

      var eyebrow=heroCopy.querySelector('.eyebrow');
      if(eyebrow)eyebrow.remove();

      var title=heroCopy.querySelector('h1');
      var signature=heroCopy.querySelector('.signature');
      var sub=heroCopy.querySelector('.sub');
      var cta=heroCopy.querySelector('.hero-cta');
      var note=heroCopy.querySelector('.hero-note');

      if(!heroCopy.querySelector('.hero-brand-v4')){
        var brand=document.createElement('div');
        brand.className='hero-brand-v4';
        brand.innerHTML='<svg class="mark hero-brand-mark-v4" viewBox="0 0 64 64" aria-hidden="true"><rect x="9.5" y="9.5" width="45" height="45" rx="13" stroke-width="5"/><circle cx="32" cy="32" r="8.5"/></svg><div class="hero-air-v4">AIR</div><div class="hero-resource-v5">AI RESOURCE</div>';
        heroCopy.insertBefore(brand,heroCopy.firstChild);
      }

      /* Reading order: identity -> signature -> promise -> support. */
      var brandNode=heroCopy.querySelector('.hero-brand-v4');
      if(signature&&brandNode)brandNode.after(signature);
      if(title&&signature)signature.after(title);
      if(title)title.classList.add('hero-promise-v4');
      if(sub&&title){
        var divider=document.createElement('span');
        divider.className='hero-divider-v5';
        title.after(divider);
        divider.after(sub);
      }

      if(cta)cta.remove();
      if(note)note.remove();
      if(heroArt)heroArt.remove();

      if(stateGrid){
        stateGrid.classList.add('hero-state-grid-v4');
        heroGrid.appendChild(stateGrid);
      }
      if(stateRule){
        stateRule.classList.add('hero-state-rule-v4');
        heroGrid.appendChild(stateRule);
      }

      if(cta||note){
        var actions=document.createElement('div');
        actions.className='hero-actions-v4';
        if(cta)actions.appendChild(cta);
        if(note)actions.appendChild(note);
        heroGrid.appendChild(actions);
      }
    }
  }

  if(statesSection)statesSection.remove();

  var heroStyle=document.createElement('style');
  heroStyle.textContent='\
.hero{padding:clamp(3rem,5vw,4.5rem) 0 clamp(3.25rem,5vw,4.75rem)!important}\
.hero .hero-grid.hero-stack-v4{display:flex!important;flex-direction:column;align-items:center!important;gap:0;text-align:center}\
.hero .hero-lockup-v4{width:min(100%,780px);display:flex;flex-direction:column;align-items:center}\
.hero .hero-brand-v4{display:flex;flex-direction:column;align-items:center;margin:0 0 .65rem}\
.hero .hero-brand-mark-v4{width:68px;height:68px;margin:0 0 .48rem}\
.hero .hero-air-v4{font-size:clamp(3.8rem,6.2vw,5.25rem);font-weight:700;line-height:.88;letter-spacing:-.055em;color:var(--text)}\
.hero .hero-resource-v5{margin-top:.48rem;font:400 .67rem \'JetBrains Mono\',ui-monospace,monospace;letter-spacing:.18em;color:var(--subtle)}\
.hero .hero-lockup-v4 .signature{font-size:clamp(1.55rem,2.5vw,2rem);font-weight:500;color:var(--brass);margin:.6rem 0 .42rem}\
.hero .hero-lockup-v4 .hero-promise-v4{font-size:clamp(1.2rem,1.85vw,1.5rem);font-weight:400;line-height:1.25;letter-spacing:-.02em;margin:0;color:var(--text)}\
.hero .hero-divider-v5{display:block;width:78px;height:1px;background:var(--border2);margin:1rem auto .9rem}\
.hero .hero-lockup-v4 .sub{max-width:650px;margin:0;color:var(--muted);font-size:clamp(.95rem,1.15vw,1.04rem);line-height:1.55}\
.hero .hero-state-grid-v4{width:min(100%,1080px);margin:2rem auto 0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;text-align:left}\
.hero .hero-state-grid-v4 .state-card{min-height:365px;padding:24px;border-radius:18px}\
.hero .hero-state-grid-v4 .state-card h3{font-size:1.5rem}\
.hero .hero-state-grid-v4 .state-card .sub{font-size:.95rem;margin:.3rem 0 1.15rem}\
.hero .hero-state-grid-v4 .state-visual{min-height:205px;padding:16px;overflow:hidden}\
.hero .hero-state-grid-v4 .state-caption{font-size:.95rem;margin-top:14px}\
.hero .hero-state-grid-v4 .state-card:nth-child(3) .air-large{width:100%;gap:7px;justify-content:center;padding:0 2px}\
.hero .hero-state-grid-v4 .state-card:nth-child(3) .air-project{width:56px;height:56px;flex:0 0 56px;border-radius:12px}\
.hero .hero-state-grid-v4 .state-card:nth-child(3) .air-project .state-mark{width:30px;height:30px;border-width:3px;border-radius:9px}\
.hero .hero-state-grid-v4 .state-card:nth-child(3) .air-project .state-mark:after{width:8px;height:8px}\
.hero .hero-state-grid-v4 .state-card:nth-child(3) .arrow{font-size:.82rem;line-height:1;flex:0 0 auto}\
.hero .hero-state-rule-v4{width:min(100%,1080px);margin:16px auto 0;padding:14px 18px;font-size:1rem}\
.hero .hero-actions-v4{display:flex;flex-direction:column;align-items:center;margin-top:1.25rem}\
.hero .hero-actions-v4 .hero-cta{justify-content:center}\
.hero .hero-actions-v4 .hero-note{text-align:center;margin:.8rem 0 0}\
.air-eye .air-pupil{transform-box:fill-box;transform-origin:center}\
.air-eye.blink .air-pupil{animation:air-blink .26s ease-in-out}\
@keyframes air-blink{0%,100%{transform:scaleY(1)}50%{transform:scaleY(.08)}}\
@media(max-width:900px){.hero .hero-state-grid-v4{grid-template-columns:1fr;max-width:680px}.hero .hero-state-grid-v4 .state-card{min-height:auto}.hero .hero-state-grid-v4 .state-visual{min-height:220px}}\
@media(max-width:600px){.hero{padding-top:2.25rem!important}.hero .hero-brand-mark-v4{width:60px;height:60px}.hero .hero-state-grid-v4{margin-top:1.5rem;gap:12px}.hero .hero-state-grid-v4 .state-card{padding:18px}.hero .hero-state-rule-v4{font-size:.9rem}}';
  document.head.appendChild(heroStyle);

  document.addEventListener('click',function(e){
    var t=e.target.closest('[data-theme-toggle]');
    if(t){
      var next=currentTheme()==='light'?'dark':'light';
      root.setAttribute('data-theme',next);
      try{localStorage.setItem('air-theme',next);}catch(x){}
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

  /* AIR attentive header mark: reliable coordinate tracking + How-it-works blink. */
  var eye=document.querySelector('.site-header .brand .mark');
  if(eye){
    eye.classList.add('air-eye');
    var pupil=eye.querySelector('circle');
    if(pupil){
      pupil.classList.add('air-pupil');
      var baseX=parseFloat(pupil.getAttribute('cx'))||32;
      var baseY=parseFloat(pupil.getAttribute('cy'))||32;
      var currentX=baseX,currentY=baseY,targetX=baseX,targetY=baseY;
      var raf=0;
      var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;

      function paint(){
        currentX+=(targetX-currentX)*0.28;
        currentY+=(targetY-currentY)*0.28;
        pupil.setAttribute('cx',currentX.toFixed(2));
        pupil.setAttribute('cy',currentY.toFixed(2));
        if(Math.abs(targetX-currentX)>0.03||Math.abs(targetY-currentY)>0.03){raf=requestAnimationFrame(paint);}else{currentX=targetX;currentY=targetY;pupil.setAttribute('cx',currentX.toFixed(2));pupil.setAttribute('cy',currentY.toFixed(2));raf=0;}
      }
      function wake(){if(!raf)raf=requestAnimationFrame(paint);}
      function centre(){targetX=baseX;targetY=baseY;wake();}

      if(!reduce){
        window.addEventListener('pointermove',function(e){
          if(e.pointerType&&e.pointerType!=='mouse')return;
          var r=eye.getBoundingClientRect();
          if(!r.width||!r.height)return;
          var dx=e.clientX-(r.left+r.width/2),dy=e.clientY-(r.top+r.height/2);
          var distance=Math.sqrt(dx*dx+dy*dy);
          if(distance<.001){centre();return;}
          var travel=8.5*Math.min(distance/110,1);
          targetX=baseX+(dx/distance)*travel;
          targetY=baseY+(dy/distance)*travel;
          wake();
        },{passive:true});
        window.addEventListener('mouseout',function(e){if(!e.relatedTarget)centre();});
        window.addEventListener('blur',centre);
      }

      if(!reduce){
        document.addEventListener('click',function(){
          eye.classList.remove('blink');
          void eye.offsetWidth;
          eye.classList.add('blink');
        });
        eye.addEventListener('animationend',function(){eye.classList.remove('blink');});
      }
    }
  }
})();