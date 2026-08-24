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

  var heroArt=document.querySelector('.hero-art');
  if(heroArt){
    heroArt.classList.add('canonical-triad');
    heroArt.style.padding='18px';
    heroArt.style.display='block';
    heroArt.style.overflow='hidden';
    heroArt.innerHTML='<img data-air-triad alt="Focused. Fluid. AIR." width="566" height="260" style="display:block;width:100%;height:auto">';
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

  /* attentive header mark: ember follows pointer and blinks on click */
  var eye=document.querySelector('.site-header .brand .mark');
  if(eye){
    eye.classList.add('air-eye');
    var pupil=eye.querySelector('circle');
    if(pupil)pupil.classList.add('air-pupil');

    var style=document.createElement('style');
    style.textContent='.air-eye .air-pupil{transform-box:fill-box;transform-origin:center;transform:translate(var(--ex,0px),var(--ey,0px));transition:transform .12s ease-out}.air-eye.blink .air-pupil{animation:air-blink .26s ease-in-out}@keyframes air-blink{0%,100%{transform:translate(var(--ex,0px),var(--ey,0px)) scaleY(1)}50%{transform:translate(var(--ex,0px),var(--ey,0px)) scaleY(.08)}}';
    document.head.appendChild(style);

    var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if(!reduce){
      window.addEventListener('mousemove',function(e){
        var r=eye.getBoundingClientRect();
        var dx=e.clientX-(r.left+r.width/2),dy=e.clientY-(r.top+r.height/2);
        var a=Math.atan2(dy,dx),d=Math.min(Math.sqrt(dx*dx+dy*dy)/60,1),mag=3.5;
        eye.style.setProperty('--ex',(Math.cos(a)*mag*d).toFixed(2)+'px');
        eye.style.setProperty('--ey',(Math.sin(a)*mag*d).toFixed(2)+'px');
      },{passive:true});
    }

    document.addEventListener('click',function(){
      eye.classList.remove('blink');
      void eye.offsetWidth;
      eye.classList.add('blink');
    });
    eye.addEventListener('animationend',function(){eye.classList.remove('blink');});
  }
})();
