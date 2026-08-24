(function(){
  var root=document.documentElement;
  function theme(){var t=root.getAttribute('data-theme');if(t==='light'||t==='dark')return t;return window.matchMedia&&window.matchMedia('(prefers-color-scheme: light)').matches?'light':'dark';}
  try{var saved=localStorage.getItem('air-theme');if(saved==='light'||saved==='dark')root.setAttribute('data-theme',saved);}catch(e){}
  document.addEventListener('click',function(e){
    var t=e.target.closest('[data-theme-toggle]');if(t){var next=theme()==='light'?'dark':'light';root.setAttribute('data-theme',next);try{localStorage.setItem('air-theme',next);}catch(x){}}
    var m=e.target.closest('[data-menu-toggle]');if(m){var nav=document.getElementById('nav');if(nav)nav.classList.toggle('open');}
  });
  var here=location.pathname.split('/').pop()||'index.html';document.querySelectorAll('#nav a').forEach(function(a){if(a.getAttribute('href')===here)a.classList.add('active');});

  var eyes=document.querySelectorAll('.air-eye');if(!eyes.length)return;
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  eyes.forEach(function(eye){
    var pupil=eye.querySelector('.air-pupil, circle');if(!pupil)return;
    pupil.classList.add('air-pupil');
    var bx=parseFloat(pupil.getAttribute('cx'))||32,by=parseFloat(pupil.getAttribute('cy'))||32;
    var cx=bx,cy=by,tx=bx,ty=by,raf=0;
    function paint(){cx+=(tx-cx)*.28;cy+=(ty-cy)*.28;pupil.setAttribute('cx',cx.toFixed(2));pupil.setAttribute('cy',cy.toFixed(2));if(Math.abs(tx-cx)>.03||Math.abs(ty-cy)>.03){raf=requestAnimationFrame(paint);}else{cx=tx;cy=ty;pupil.setAttribute('cx',cx.toFixed(2));pupil.setAttribute('cy',cy.toFixed(2));raf=0;}}
    function wake(){if(!raf)raf=requestAnimationFrame(paint);}function centre(){tx=bx;ty=by;wake();}
    if(!reduce){
      window.addEventListener('pointermove',function(e){if(e.pointerType&&e.pointerType!=='mouse')return;var r=eye.getBoundingClientRect();if(!r.width||!r.height)return;var dx=e.clientX-(r.left+r.width/2),dy=e.clientY-(r.top+r.height/2),d=Math.sqrt(dx*dx+dy*dy);if(d<.001){centre();return;}var travel=8.5*Math.min(d/110,1);tx=bx+(dx/d)*travel;ty=by+(dy/d)*travel;wake();},{passive:true});
      window.addEventListener('mouseout',function(e){if(!e.relatedTarget)centre();});window.addEventListener('blur',centre);
      document.addEventListener('click',function(){eye.classList.remove('blink');void eye.offsetWidth;eye.classList.add('blink');});eye.addEventListener('animationend',function(){eye.classList.remove('blink');});
    }
  });
})();
