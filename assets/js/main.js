/* ==========================================================================
   JS DO SITE (vanilla, sem dependencias). Base: template Corporate Navy.
   ========================================================================== */
(function(){
  const $ = (s, r=document) => r.querySelector(s);
  const $$ = (s, r=document) => [...r.querySelectorAll(s)];

  /* NAV: solida ao rolar + menu mobile */
  const nav = $('.nav');
  if (nav) {
    const solid = nav.hasAttribute('data-solid');
    const onScroll = () => nav.classList.toggle('is-scrolled', solid || window.scrollY > 40);
    window.addEventListener('scroll', onScroll, {passive:true}); onScroll();
    const toggle = $('.nav__toggle');
    toggle?.addEventListener('click', () => {
      const open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open);
    });
    $$('.nav__links a').forEach(a => a.addEventListener('click', () => nav.classList.remove('is-open')));
    $$('.nav__drop>button').forEach(b => b.addEventListener('click', () => {
      const open = b.parentElement.classList.toggle('is-open');
      b.setAttribute('aria-expanded', open);
    }));
  }

  /* MARQUEE: repete os itens ate um bloco cobrir a tela e duplica o bloco;
     a animacao anda exatamente um bloco (-50%), entao o ultimo logo emenda no primeiro sem lacuna */
  $$('[data-marquee]').forEach(t => {
    const base = t.innerHTML, box = t.parentElement;
    let set = base, n = 1;
    t.innerHTML = set;
    while (t.scrollWidth < box.clientWidth + 200 && n < 12) { set += base; n++; t.innerHTML = set; }
    const w = t.scrollWidth;
    t.innerHTML = set + set;
    t.style.animationDuration = Math.max(20, w / 45) + 's';   /* ~45 px por segundo */
  });

  /* CARROSSEL: setas + dots sincronizados com o scroll */
  $$('[data-carousel]').forEach(c => {
    const track = $('[data-carousel-track]', c);
    const section = c.closest('section');
    const items = [...track.children];
    const dotsWrap = $('[data-carousel-dots]', c);
    const dots = items.map((_, i) => {
      const d = document.createElement('button');
      d.className = 'carousel__dot'; d.setAttribute('aria-label', 'Ir para item ' + (i+1));
      d.addEventListener('click', () => track.scrollTo({left: items[i].offsetLeft - track.offsetLeft, behavior:'smooth'}));
      dotsWrap.appendChild(d); return d;
    });
    const step = () => items[0].getBoundingClientRect().width + 16;
    $('[data-carousel-prev]', section)?.addEventListener('click', () => track.scrollBy({left:-step(), behavior:'smooth'}));
    $('[data-carousel-next]', section)?.addEventListener('click', () => track.scrollBy({left: step(), behavior:'smooth'}));
    const sync = () => {
      const i = Math.round(track.scrollLeft / step());
      dots.forEach((d, k) => d.classList.toggle('is-active', k === Math.min(i, dots.length-1)));
    };
    track.addEventListener('scroll', sync, {passive:true}); sync();
  });

  /* CONTADOR: anima [data-count] quando entra na tela */
  const countIO = new IntersectionObserver(entries => entries.forEach(e => {
    if (!e.isIntersecting) return;
    const el = e.target, end = +el.dataset.count, pre = el.dataset.prefix || '', suf = el.dataset.suffix || '';
    const t0 = performance.now(), dur = 1400;
    const tick = t => { const p = Math.min((t - t0)/dur, 1), v = Math.round(end * (1 - Math.pow(1-p, 3)));
      el.textContent = pre + v.toLocaleString('pt-BR') + suf; if (p < 1) requestAnimationFrame(tick); };
    requestAnimationFrame(tick); countIO.unobserve(el);
  }), {threshold:.5});
  $$('[data-count]').forEach(el => countIO.observe(el));

  /* REVEAL: fade + slide ao entrar na tela, com pequeno escalonamento */
  const revIO = new IntersectionObserver(entries => entries.forEach(e => {
    if (!e.isIntersecting) return;
    const sibs = [...e.target.parentElement.children].filter(n => n.hasAttribute('data-reveal'));
    e.target.style.transitionDelay = (sibs.indexOf(e.target) * 70) + 'ms';
    e.target.classList.add('is-visible'); revIO.unobserve(e.target);
  }), {threshold:.12, rootMargin:'0px 0px -40px 0px'});
  $$('[data-reveal]').forEach(el => revIO.observe(el));

  /* COOKIE */
  const cookie = $('[data-cookie]');
  if (cookie) {
    try { if (localStorage.getItem('cookie-ok')) { cookie.hidden = true; document.body.classList.remove('has-cookie'); } } catch(e){}
    $('[data-cookie-ok]').addEventListener('click', () => {
      cookie.hidden = true; document.body.classList.remove('has-cookie');
      try { localStorage.setItem('cookie-ok', '1'); } catch(e){}
    });
  }

  /* ANO no rodape */
  $$('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
})();
