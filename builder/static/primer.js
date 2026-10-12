// Mono-U Stiflenought primer: theme toggle, contents sidebar, card previews and lightbox.
// Everything on the page works without this script; it only adds behaviour.

const root = document.documentElement;
const imageUrl = (size, id) => `https://cards.scryfall.io/${size}/front/${id[0]}/${id[1]}/${id}.jpg`;

// ---- Theme -------------------------------------------------------------------------------------
function setThemeLabel() {
  const dark = root.dataset.theme !== 'light';
  document.querySelectorAll('.theme-toggle .label').forEach(l => {
    const b = l.closest('.theme-toggle'); l.textContent = dark ? b.dataset.light : b.dataset.dark;
  });
}
document.querySelectorAll('[data-theme-toggle]').forEach(b => b.addEventListener('click', () => {
  const next = root.dataset.theme === 'light' ? 'dark' : 'light';
  root.dataset.theme = next;
  try { localStorage.setItem('theme', next); } catch (e) {}
  setThemeLabel();
}));
setThemeLabel();

// ---- Contents: fold-out chapters, current section, phone drawer ---------------------------------
function setOpen(li, open) {
  li.classList.toggle('open', open);
  const b = li.querySelector('.disclose');
  if (b) b.setAttribute('aria-expanded', String(open));
}
// Chapters the reader opens stay open; chapters opened by scrolling close again when the reader moves on.
const pinned = new Set();
let autoOpened = null;
document.querySelectorAll('.toc .disclose').forEach(b => b.addEventListener('click', () => {
  const li = b.closest('li'); const open = !li.classList.contains('open');
  setOpen(li, open);
  if (open) pinned.add(li); else pinned.delete(li);
}));

const links = [...document.querySelectorAll('.toc a[href^="#"]:not(.brand)')];
const targets = links.map(a => document.getElementById(a.hash.slice(1))).filter(Boolean);
const where = document.getElementById('where');
let current = null;
// A section the reader jumped to stays current while it is on screen: short sections near the end would
// otherwise hand the highlight to the next heading, which is also near the top of the window.
let jumpedTo = null;
function spy() {
  let cur = targets[0];
  for (const t of targets) { if (t.getBoundingClientRect().top < innerHeight * 0.3) cur = t; else break; }
  if (jumpedTo) cur = jumpedTo;
  if (!cur || cur === current) return;
  current = cur;
  let active = null;
  links.forEach(a => { const on = a.hash === '#' + cur.id; a.classList.toggle('current', on); if (on) active = a; });
  if (!active) return;
  const parent = active.closest('li.has-kids');
  if (autoOpened && autoOpened !== parent && !pinned.has(autoOpened)) setOpen(autoOpened, false);
  autoOpened = parent;
  if (parent) setOpen(parent, true);
  if (where) where.textContent = active.textContent;
  const toc = document.querySelector('.toc');
  const r = active.getBoundingClientRect(), tr = toc.getBoundingClientRect();
  if (r.top < tr.top + 40 || r.bottom > tr.bottom - 80) active.scrollIntoView({ block: 'nearest' });
}
let spyQueued = false;
addEventListener('scroll', () => { if (!spyQueued) { spyQueued = true; requestAnimationFrame(() => { spyQueued = false; spy(); }); } }, { passive: true });
function jump() {
  const t = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
  if (t && targets.includes(t)) { jumpedTo = t; requestAnimationFrame(spy); }
}
addEventListener('hashchange', jump);
// the reader scrolling by hand hands the highlight back to the position on the page
for (const ev of ['wheel', 'touchmove', 'keydown']) addEventListener(ev, () => { if (jumpedTo) { jumpedTo = null; requestAnimationFrame(spy); } }, { passive: true });
jump();
spy();

document.querySelector('[data-open-nav]').addEventListener('click', () => document.body.classList.add('nav-open'));
document.querySelector('[data-close-nav]').addEventListener('click', () => document.body.classList.remove('nav-open'));
links.forEach(a => a.addEventListener('click', () => {
  document.body.classList.remove('nav-open');
  const t = document.getElementById(a.hash.slice(1));
  if (t) { jumpedTo = t; requestAnimationFrame(spy); }   // also when the hash is already this one
}));

// ---- Lightbox ----------------------------------------------------------------------------------
const zoom = document.getElementById('zoom');
function openZoom(el) {
  const im = zoom.querySelector('img');
  im.src = imageUrl('large', el.dataset.img);
  im.alt = el.dataset.card;
  zoom.querySelector('a').href = el.dataset.page || el.getAttribute('href');
  zoom.showModal();
}
zoom.addEventListener('click', e => { if (e.target === zoom || e.target.matches('[data-close-zoom]')) zoom.close(); });
document.addEventListener('click', e => {
  const img = e.target.closest('img.mtg');
  if (img) { openZoom(img); return; }
  const a = e.target.closest('a.cardref');
  if (!a || e.metaKey || e.ctrlKey || e.shiftKey) return;
  e.preventDefault(); hidePeek(); openZoom(a);
});

// ---- Hover / focus preview for card names --------------------------------------------------------
const peek = document.createElement('div');
peek.className = 'peek'; peek.setAttribute('aria-hidden', 'true');
peek.innerHTML = '<img alt="" width="488" height="680">';
document.body.append(peek);
const peekImg = peek.querySelector('img');
let peekTimer = null;
function showPeek(a) {
  clearTimeout(peekTimer);
  const t = peekTimer = setTimeout(() => {
    peekImg.onload = null;
    peekImg.src = imageUrl('normal', a.dataset.img);
    const r = a.getBoundingClientRect(), w = 240, h = w * 680 / 488, gap = 12;
    let x = r.right + gap; if (x + w > innerWidth - 8) x = Math.max(8, r.left - w - gap);
    let y = r.top + r.height / 2 - h / 2; y = Math.min(Math.max(8, y), innerHeight - h - 8);
    peek.style.transform = `translate(${x}px, ${y}px)`;
    const on = () => { if (peekTimer === t) peek.classList.add('on'); };
    if (peekImg.complete && peekImg.naturalWidth) on(); else peekImg.onload = on;
  }, 90);
}
function hidePeek() { clearTimeout(peekTimer); peekTimer = null; peek.classList.remove('on'); }
const canHover = matchMedia('(hover: hover) and (pointer: fine)').matches;
document.addEventListener('pointerover', e => { const a = e.target.closest('a.cardref'); if (a && canHover) showPeek(a); });
document.addEventListener('pointerout', e => { if (e.target.closest('a.cardref')) hidePeek(); });
document.addEventListener('focusin', e => { const a = e.target.closest('a.cardref'); if (a) showPeek(a); });
document.addEventListener('focusout', e => { if (e.target.closest('a.cardref')) hidePeek(); });
addEventListener('scroll', hidePeek, { passive: true });

// ---- Heading anchors copy the section's address ----------------------------------------------
document.addEventListener('click', e => {
  const a = e.target.closest('a.anchor');
  if (!a || !navigator.clipboard) return;
  navigator.clipboard.writeText(location.href.split('#')[0] + a.getAttribute('href')).then(() => {
    a.classList.add('copied'); setTimeout(() => a.classList.remove('copied'), 1500);
  }, () => {});
});

// ---- Review edition: ?changed shows only the sections that contain a change (for a short PDF) ----
if (new URLSearchParams(location.search).has('changed') && document.querySelector('.rv-panel')) {
  document.querySelectorAll('img[loading="lazy"]').forEach(i => { i.loading = 'eager'; });
  const prose = document.querySelector('.prose');
  let group = [], keep = false;
  const flush = () => { if (!keep) group.forEach(el => { el.style.display = 'none'; }); group = []; keep = false; };
  for (const el of [...prose.children]) {
    if (el.matches('header.title, .rv-panel, .confidential, .confidential-print, footer')) continue;
    if (el.matches('h2, h3')) flush();
    group.push(el);
    if (el.matches('.rv') || el.querySelector('.rv')) keep = true;
  }
  flush();
  document.querySelectorAll('.print-toc').forEach(n => { n.style.display = 'none'; });
}

// ---- Print: load every lazy image first --------------------------------------------------------
addEventListener('beforeprint', () => document.querySelectorAll('img[loading="lazy"]').forEach(i => { i.loading = 'eager'; }));
// In print the practice answers are simply shown.
addEventListener('beforeprint', () => document.querySelectorAll('details.pz-answer').forEach(d => { d.open = true; }));

// ---- Practice boards: an arrow from each targeting spell or ability on the stack to its target -----
// Positions depend on the layout, so the arrows are drawn here and redrawn whenever the board resizes.
const SVGNS = 'http://www.w3.org/2000/svg';
function arrow(svg, sx, sy, cx, cy, ex, ey, colour) {
  const path = document.createElementNS(SVGNS, 'path');
  path.setAttribute('d', `M${sx},${sy} Q${cx},${cy} ${ex},${ey}`);
  path.setAttribute('stroke', colour);
  svg.appendChild(path);
  // the head, pointing along the curve's last tangent
  const ang = Math.atan2(ey - cy, ex - cx), s = 8;
  const head = document.createElementNS(SVGNS, 'path');
  head.setAttribute('d', `M${ex},${ey} L${ex - s * Math.cos(ang - 0.45)},${ey - s * Math.sin(ang - 0.45)} L${ex - s * Math.cos(ang + 0.45)},${ey - s * Math.sin(ang + 0.45)} Z`);
  head.setAttribute('fill', colour);
  svg.appendChild(head);
}
function drawTargets(fig) {
  fig.querySelector(':scope > svg.pz-arrows')?.remove();
  const items = fig.querySelectorAll('.pz-item[data-pz-target]');
  if (!items.length) return;
  const box = fig.getBoundingClientRect();
  const svg = document.createElementNS(SVGNS, 'svg');
  svg.setAttribute('class', 'pz-arrows');
  svg.setAttribute('width', box.width); svg.setAttribute('height', box.height);
  svg.setAttribute('aria-hidden', 'true');
  items.forEach((li, n) => {
    const target = fig.querySelector(`[data-pz-ref="${li.dataset.pzTarget}"]`);
    if (!target) return;
    const face = li.querySelector('.pz-card, .pz-abil') || li;
    const a = face.getBoundingClientRect();
    const onStack = target.matches('.pz-item');
    const b = (onStack ? target.querySelector('.pz-card, .pz-abil') || target : target).getBoundingClientRect();
    li.classList.add('pz-aimed');
    const colour = getComputedStyle(li).getPropertyValue('--pz-arrow').trim() || 'currentColor';
    if (onStack) {
      // within the stack the cards overlap, so the arrow arcs over the top, from one card's top edge to the other's
      const sx = a.left + a.width / 2 - box.left, sy = a.top - box.top - 7;
      const ex = b.left + b.width / 2 - box.left, ey = b.top - box.top - 2;
      const cx = (sx + ex) / 2, cy = Math.min(sy, ey) - 28 - Math.abs(ex - sx) * 0.15;
      arrow(svg, sx, sy, cx, cy, ex, ey, colour);
      return;
    }
    const ax = a.left + a.width / 2 - box.left, ay = a.top + a.height / 2 - box.top;
    const bcx = b.left + b.width / 2 - box.left, bcy = b.top + b.height / 2 - box.top;
    // start at the edge of the item and end at the edge of the target, on the line between their centres
    const edge = (cx, cy, w, h, dx, dy) => {
      const t = Math.min(Math.abs((w / 2) / (dx || 1e-6)), Math.abs((h / 2) / (dy || 1e-6)));
      return [cx + dx * t, cy + dy * t];
    };
    const [sx, sy] = edge(ax, ay, a.width + 14, a.height + 14, bcx - ax, bcy - ay);
    const [ex, ey] = edge(bcx, bcy, b.width + 8, b.height + 8, ax - bcx, ay - bcy);
    // a gentle curve, bowed sideways so arrows between neighbours don't sit on top of each other
    const mx = (sx + ex) / 2, my = (sy + ey) / 2, len = Math.hypot(ex - sx, ey - sy) || 1;
    const bow = Math.min(60, len * 0.25) * (n % 2 ? -1 : 1);
    const cx = mx - (ey - sy) / len * bow, cy = my + (ex - sx) / len * bow;
    arrow(svg, sx, sy, cx, cy, ex, ey, colour);
  });
  fig.appendChild(svg);
}
const boards = document.querySelectorAll('figure.puzzle');
const redraw = () => boards.forEach(drawTargets);
if (boards.length) {
  if ('ResizeObserver' in window) { const ro = new ResizeObserver(() => redraw()); boards.forEach(f => ro.observe(f)); }
  addEventListener('load', redraw);
  addEventListener('beforeprint', redraw);
  addEventListener('afterprint', redraw);
  matchMedia('print').addEventListener?.('change', redraw);
  redraw();
}

// ---- The PDF build (?pdf): load every image now, retry the ones Scryfall turns away, report the rest -----
if (new URLSearchParams(location.search).has('pdf')) {
  const imgs = [...document.images].filter(img => img.getAttribute('src') && !img.closest('dialog'));
  // board cards print at about a centimetre wide: the small scans are plenty, and they keep the file light
  document.querySelectorAll('.puzzle img.mtg').forEach(img => { img.removeAttribute('srcset'); img.src = img.src.replace('/normal/', '/small/'); });
  const failed = img => img.complete && !img.naturalWidth;
  const retry = img => {
    const n = (+img.dataset.tries || 0) + 1;
    img.dataset.tries = n;
    if (n > 6) return;
    setTimeout(() => { img.removeAttribute('srcset'); img.src = img.src.split('?')[0] + '?retry=' + n; }, 800 * n + Math.random() * 2000);
  };
  imgs.forEach(img => { img.loading = 'eager'; img.addEventListener('error', () => retry(img)); });
  const settle = setInterval(() => {
    for (const img of imgs) if (failed(img) && !img.dataset.tries) retry(img);   // failed before we were listening
    const busy = imgs.some(img => !img.complete || (failed(img) && +img.dataset.tries <= 6));
    if (busy || document.readyState !== 'complete') return;
    clearInterval(settle);
    document.documentElement.dataset.brokenImages = String(imgs.filter(failed).length);
  }, 1000);
}
