/* Pinheiro 3D: cresce em camadas sobre uma janela de navegador deitada */
function makePine(canvas, grow) {
  var stage = canvas.parentNode;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var renderer;
  try {
    if (!window.THREE) throw new Error('three');
    renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
  } catch (e) { stage.classList.add('no3d'); return { setStep: function () {} }; }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(32, 1, 0.1, 100);
  camera.position.set(0, 4.6, 11.8);
  camera.lookAt(0, 1.5, 0);
  scene.add(new THREE.HemisphereLight(0xF4F6F1, 0x163A2C, 0.55));
  var sun = new THREE.DirectionalLight(0xffffff, 0.6); sun.position.set(4, 9, 6); scene.add(sun);
  var glow = new THREE.PointLight(0xF2A541, 0, 6); glow.position.set(0, 3.6, 1); scene.add(glow);

  var mat = function (c, extra) { return new THREE.MeshStandardMaterial(Object.assign({ color: c, flatShading: true, roughness: .75 }, extra || {})); };
  var world = new THREE.Group(); scene.add(world);

  // Janela de navegador
  var edge = new THREE.Mesh(new THREE.BoxGeometry(5.6, 0.22, 4.6), mat(0x0E2A1F)); edge.position.y = -0.12; world.add(edge);
  var page = new THREE.Mesh(new THREE.BoxGeometry(5.3, 0.2, 4.3), mat(0xF4F6F1)); world.add(page);
  var topbar = new THREE.Mesh(new THREE.BoxGeometry(5.3, 0.06, 0.7), mat(0x163A2C)); topbar.position.set(0, 0.12, -1.8); world.add(topbar);
  [-2.25, -1.95, -1.65].forEach(function (x) {
    var d = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 0.06, 16), mat(0x8FD694)); d.position.set(x, 0.17, -1.8); world.add(d);
  });
  var bar = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.04, 0.24), mat(0xD9E0D8)); bar.position.set(-1.3, 0.12, 1.5); world.add(bar);
  var bar2 = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.04, 0.24), mat(0xF2A541)); bar2.position.set(1.6, 0.12, 1.5); world.add(bar2);

  // Árvore
  var tree = new THREE.Group(); tree.position.y = 0.1; world.add(tree);
  var part = function (geo, m, y) { var o = new THREE.Mesh(geo, m); var g = new THREE.Group(); g.position.y = y; g.add(o); tree.add(g); return g; };
  var cone = function (r, h) { var g = new THREE.ConeGeometry(r, h, 7); g.translate(0, h / 2, 0); return g; };
  var trunkGeo = new THREE.CylinderGeometry(0.2, 0.26, 0.9, 8); trunkGeo.translate(0, 0.45, 0);
  var green = mat(0x2E7D5B);
  var parts = [
    part(new THREE.SphereGeometry(0.22, 12, 10), mat(0xF2A541), 0.2),        // semente
    part(trunkGeo, mat(0x163A2C), 0),                                        // tronco
    part(cone(1.55, 1.4), green, 0.75),                                     // galho de baixo
    part(cone(1.2, 1.2), green, 1.55),                                      // galho do meio
    part(cone(0.85, 1.05), green, 2.3),                                     // galho de cima
    part(new THREE.OctahedronGeometry(0.24), mat(0xF2A541, { emissive: 0xF2A541, emissiveIntensity: .4 }), 3.55) // estrela
  ];
  var sparks = new THREE.Group(); tree.add(sparks);
  for (var i = 0; i < 12; i++) {
    var s = new THREE.Mesh(new THREE.OctahedronGeometry(0.07), mat(0x8FD694, { emissive: 0x8FD694, emissiveIntensity: .6 }));
    var a = i / 12 * Math.PI * 2;
    s.userData = { a: a, r: 2 + (i % 3) * 0.35, y: 0.8 + (i % 4) * 0.7, sp: 0.3 + (i % 5) * 0.06 };
    sparks.add(s);
  }
  parts.push(sparks);

  // O que aparece em cada passo: semente, tronco, 3 galhos, estrela, brilhos
  var plan = [
    [1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1]
  ];
  var target = grow ? plan[0].slice() : plan[5].slice();
  var cur = target.map(function (v) { return grow ? v : v; });
  parts.forEach(function (p, k) { p.scale.setScalar(Math.max(cur[k], 0.0001)); });

  var tilt = { x: 0, y: 0 }, want = { x: 0, y: 0 };
  stage.addEventListener('pointermove', function (e) {
    var r = stage.getBoundingClientRect();
    want.y = ((e.clientX - r.left) / r.width - 0.5) * 0.9;
    want.x = ((e.clientY - r.top) / r.height - 0.5) * 0.25;
  });
  stage.addEventListener('pointerleave', function () { want.x = 0; want.y = 0; });

  var visible = true;
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(stage);

  var spin = 0, t0 = performance.now();
  function size() {
    var w = canvas.clientWidth, h = canvas.clientHeight;
    if (canvas.width !== Math.floor(w * renderer.getPixelRatio()) || canvas.height !== Math.floor(h * renderer.getPixelRatio())) {
      renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
    }
  }
  function frame(now) {
    requestAnimationFrame(frame);
    if (!visible) return;
    size();
    var t = (now - t0) / 1000;
    if (!reduce) spin += 0.0035;
    tilt.x += (want.x - tilt.x) * 0.06; tilt.y += (want.y - tilt.y) * 0.06;
    world.rotation.y = -0.5 + spin + tilt.y;
    world.rotation.x = tilt.x;
    parts.forEach(function (p, k) {
      cur[k] += (target[k] - cur[k]) * (reduce ? 1 : 0.07);
      p.scale.setScalar(Math.max(cur[k], 0.0001));
    });
    parts[5].rotation.y = t * 1.5;
    sparks.children.forEach(function (s) {
      var u = s.userData; var a = u.a + t * u.sp;
      s.position.set(Math.cos(a) * u.r, u.y + Math.sin(t * 1.6 + u.a) * 0.15, Math.sin(a) * u.r);
      s.rotation.y = t * 2;
    });
    glow.intensity = cur[5] * 1.2;
    renderer.render(scene, camera);
  }
  requestAnimationFrame(frame);
  return { setStep: function (n) { target = plan[n].slice(); } };
}

(function () {
  var root = document.documentElement;
  function setLang(l) {
    root.dataset.lang = l;
    root.lang = l === 'en' ? 'en' : 'pt-BR';
    document.querySelectorAll('[data-set-lang]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.setLang === l));
    });
    document.title = l === 'en' ? 'Website Design for Small Businesses | PineWeb' : 'Criação de Sites para Pequenos Negócios | PineWeb';
    document.querySelector('meta[name="description"]').content = l === 'en' ? 'PineWeb designs, launches and looks after small business websites: custom, mobile-first and built to be found on Google. US and Brazil. Get a free quote.' : 'A PineWeb cria, publica e cuida do site do seu negócio: sob medida, feito para o celular e para aparecer no Google. Brasil e EUA. Peça seu orçamento.';
    try { localStorage.setItem('pineweb-lang', l); } catch (e) {}
  }
  var saved = null, param = /[?&]lang=(pt|en)\b/.exec(location.search);
  try { saved = localStorage.getItem('pineweb-lang'); } catch (e) {}
  setLang(param ? param[1] : saved || (/^pt/i.test(navigator.language || '') ? 'pt' : 'en'));
  document.querySelectorAll('[data-set-lang]').forEach(function (b) {
    b.addEventListener('click', function () { setLang(b.dataset.setLang); });
  });

  var copyBtn = document.getElementById('copy-email');
  copyBtn.addEventListener('click', function () {
    var text = document.getElementById('email').textContent;
    var done = function () {
      var old = copyBtn.innerHTML;
      copyBtn.textContent = root.dataset.lang === 'en' ? 'Copied' : 'Copiado';
      setTimeout(function () { copyBtn.innerHTML = old; }, 1600);
    };
    var select = function () {
      var r = document.createRange(); r.selectNodeContents(document.getElementById('email'));
      var s = getSelection(); s.removeAllRanges(); s.addRange(r);
    };
    try { navigator.clipboard.writeText(text).then(done, select); } catch (e) { select(); }
  });

  // Pinheiros 3D
  makePine(document.getElementById('hero-3d'), false);
  var pine = makePine(document.getElementById('show-3d'), true);

  // Apresentação de como funciona
  var slides = document.querySelectorAll('.slide');
  var dots = document.querySelectorAll('[data-go]');
  var prev = document.getElementById('show-prev'), next = document.getElementById('show-next');
  var play = document.getElementById('show-play');
  var step = 0, timer = null;
  function go(n) {
    step = Math.max(0, Math.min(5, n));
    slides.forEach(function (s, i) { s.hidden = i !== step; });
    dots.forEach(function (d, i) {
      d.classList.toggle('done', i < step);
      if (i === step) d.setAttribute('aria-current', 'step'); else d.removeAttribute('aria-current');
    });
    prev.disabled = step === 0; next.disabled = step === 5;
    pine.setStep(step);
  }
  function stop() { clearInterval(timer); timer = null; }
  dots.forEach(function (d) { d.addEventListener('click', function () { stop(); go(+d.dataset.go); }); });
  prev.addEventListener('click', function () { stop(); go(step - 1); });
  next.addEventListener('click', function () { stop(); go(step + 1); });
  play.addEventListener('click', function () {
    stop(); go(0);
    timer = setInterval(function () { if (step >= 5) stop(); else go(step + 1); }, 3200);
  });
  go(0);
})();
