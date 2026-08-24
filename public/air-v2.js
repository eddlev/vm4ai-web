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

  var heroGrid=document.querySelector('.hero-grid');
  var heroArt=document.querySelector('.hero-art');
  if(heroGrid)heroGrid.style.alignItems='start';
  if(heroArt){
    heroArt.classList.add('canonical-triad');
    heroArt.style.padding='18px';
    heroArt.style.display='block';
    heroArt.style.overflow='hidden';
    heroArt.innerHTML='<img data-air-triad alt="Focused. Fluid. AIR." width="566" height="260" style="display:block;width:100%;height:auto">';
  }

  function alignHero(){
    if(heroArt)heroArt.style.marginTop=window.innerWidth<=900?'0':'3rem';
  }
  alignHero();
  window.addEventListener('resize',alignHero,{passive:true});

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

      /* Click blink: direct radius change avoids SVG transform inconsistencies. */
      var blinkTimer=0;
      document.addEventListener('click',function(){
        clearTimeout(blinkTimer);
        pupil.setAttribute('r',(baseR*0.28).toFixed(2));
        blinkTimer=setTimeout(function(){pupil.setAttribute('r',baseR.toFixed(2));},120);
      });
    }
  }
})();
