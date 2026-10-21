(function(){
  const toggle=document.getElementById('menu-toggle');
  const nav=document.getElementById('top-nav');
  if(!toggle||!nav)return;
  toggle.addEventListener('click',function(){const isOpen=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(isOpen));toggle.textContent=isOpen?'×':'☰';});
  nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');toggle.textContent='☰';}));
})();
