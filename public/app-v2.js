/* ============================================================
   CASCADE LOCAL SEO - v2 interactions
   ============================================================ */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Hero entrance is an enhancement layered over an already-visible base state.
  document.body.classList.add("anim");

  // Hero live tracker count-up
  (function () {
    var el = document.getElementById("htNum");
    if (!el) return;
    if (reduce) { el.textContent = "1,186"; return; }
    var target = 1186, t0 = null;
    function step(ts) {
      if (!t0) t0 = ts;
      var p = Math.min((ts - t0) / 1100, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))).toLocaleString();
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  })();

  /* ---------- scroll progress + section rail ---------- */
  var progress = document.querySelector(".progress");
  var railLinks = Array.prototype.slice.call(document.querySelectorAll(".scroll-rail a"));
  var sections = railLinks.map(function (a) { return document.querySelector(a.getAttribute("href")); });

  function onScroll() {
    var st = window.scrollY;
    var h = document.documentElement.scrollHeight - window.innerHeight;
    if (progress) progress.style.width = (h > 0 ? (st / h) * 100 : 0) + "%";
    var mid = st + window.innerHeight * 0.4;
    var active = 0;
    sections.forEach(function (s, i) { if (s && s.offsetTop <= mid) active = i; });
    railLinks.forEach(function (a, i) { a.classList.toggle("active", i === active); });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- reveal on scroll ---------- */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });

  /* ---------- hero spotlight follows pointer ---------- */
  var hero = document.querySelector(".hero");
  var spot = document.querySelector(".spotlight");
  if (hero && spot && !reduce) {
    hero.addEventListener("pointermove", function (e) {
      var r = hero.getBoundingClientRect();
      spot.style.left = (e.clientX - r.left) + "px";
      spot.style.top = (e.clientY - r.top) + "px";
    });
  }

  /* ---------- magnetic buttons ---------- */
  if (!reduce && window.matchMedia("(pointer:fine)").matches) {
    document.querySelectorAll(".btn-primary").forEach(function (btn) {
      btn.addEventListener("pointermove", function (e) {
        var r = btn.getBoundingClientRect();
        var x = (e.clientX - r.left - r.width / 2) * 0.25;
        var y = (e.clientY - r.top - r.height / 2) * 0.35;
        btn.style.transform = "translate(" + x + "px," + y + "px)";
      });
      btn.addEventListener("pointerleave", function () { btn.style.transform = ""; });
    });
  }

  /* ---------- count-up stats ---------- */
  function countUp(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var dec = (el.getAttribute("data-dec") | 0);
    var dur = 1400, t0 = null;
    function frame(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      var val = target * eased;
      el.textContent = (dec ? val.toFixed(dec) : Math.round(val)).toLocaleString();
      if (p < 1) requestAnimationFrame(frame);
      else el.textContent = (dec ? target.toFixed(dec) : target).toLocaleString();
    }
    requestAnimationFrame(frame);
  }
  var statIO = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { countUp(e.target); statIO.unobserve(e.target); }
    });
  }, { threshold: 0.6 });
  document.querySelectorAll("[data-count]").forEach(function (el) {
    if (reduce) { el.textContent = el.getAttribute("data-count"); } else { statIO.observe(el); }
  });

  /* ---------- live rank-climb demo ---------- */
  var rankList = document.querySelector(".rank-list");
  if (rankList) {
    var ROWH = 64;
    // baseline order (worst → in view): YOU starts low
    var data = [
      { id: "you", name: "Glow Aesthetics", rating: 4.2, reviews: 41, you: true },
      { id: "a", name: "Lumen Skin Bar", rating: 4.6, reviews: 88 },
      { id: "b", name: "Radiance Med Spa", rating: 4.4, reviews: 51 },
      { id: "c", name: "Aurora Aesthetics", rating: 4.3, reviews: 60 },
      { id: "d", name: "Velvet Skin Co.", rating: 4.1, reviews: 33 }
    ];
    var rows = {};
    function stars(r) {
      var full = Math.round(r);
      return "★★★★★".slice(0, full) + "☆☆☆☆☆".slice(0, 5 - full);
    }
    data.forEach(function (d) {
      var row = document.createElement("div");
      row.className = "rank-row" + (d.you ? " you" : "");
      row.innerHTML =
        '<span class="pin"></span>' +
        '<div><div class="biz">' + d.name + '</div>' +
        '<div class="meta"><span class="stars"></span> <span class="rv"></span></div></div>' +
        (d.you ? '<span class="you-tag">YOU</span>' : "");
      rankList.appendChild(row);
      rows[d.id] = row;
      d.el = row;
    });

    function paint(order, climbed) {
      var labels = ["A", "B", "C", "D", "E"];
      order.forEach(function (d, i) {
        d.el.style.top = (i * ROWH) + "px";
        d.el.querySelector(".pin").textContent = (i + 1) + labels[i];
        d.el.querySelector(".stars").textContent = stars(d.rating);
        d.el.querySelector(".rv").textContent = d.rating.toFixed(1) + " · " + d.reviews + " reviews";
        if (d.you) d.el.classList.toggle("top", climbed && i === 0);
      });
    }

    // initial: sorted worst-ish, YOU near bottom (rank 5)
    var start = [data[1], data[2], data[3], data[4], data[0]];
    paint(start, false);

    function runClimb() {
      // YOU's signals improve → climbs to #1
      data[0].rating = 5.0; data[0].reviews = 214;
      var end = [data[0], data[1], data[3], data[2], data[4]];
      paint(end, true);
    }
    function reset() {
      data[0].rating = 4.2; data[0].reviews = 41;
      paint(start, false);
    }

    if (!reduce) {
      var demoIO = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            setTimeout(runClimb, 900);
            setInterval(function () { reset(); setTimeout(runClimb, 1100); }, 7000);
            demoIO.unobserve(e.target);
          }
        });
      }, { threshold: 0.4 });
      demoIO.observe(rankList);
    } else {
      runClimb();
    }
  }

  /* ---------- AI answer typewriter ---------- */
  var aiEl = document.querySelector("[data-typewriter]");
  if (aiEl) {
    // Each segment is a run of text; "mark" runs render inside <mark>.
    var segments = [
      { t: "For a first visit, ", mark: false },
      { t: "Glow Aesthetics", mark: true },
      { t: " is the standout, a 5.0 rating across 200+ reviews, clear first-time pricing, and clients consistently mention how thorough the consultation is. A great place to start.", mark: false }
    ];
    var fullHTML = '<span class="tlabel">AI ANSWERS</span>For a first visit, <mark>Glow Aesthetics</mark> is the standout, a 5.0 rating across 200+ reviews, clear first-time pricing, and clients consistently mention how thorough the consultation is. A great place to start.';

    function typeOut() {
      aiEl.innerHTML = '<span class="tlabel">AI ANSWERS</span><span class="body"></span><span class="tw-cursor"></span>';
      var body = aiEl.querySelector(".body");
      var si = 0, ci = 0, node = null;
      function tick() {
        if (si >= segments.length) { return; }
        var seg = segments[si];
        if (ci === 0) {
          node = seg.mark ? document.createElement("mark") : document.createElement("span");
          body.appendChild(node);
        }
        node.textContent = seg.t.slice(0, ci + 1);
        ci++;
        if (ci >= seg.t.length) { si++; ci = 0; }
        setTimeout(tick, seg.mark ? 46 : 15);
      }
      tick();
    }

    if (reduce) {
      aiEl.innerHTML = fullHTML;
    } else {
      var twIO = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            typeOut();
            setInterval(typeOut, 12000);
            twIO.unobserve(e.target);
          }
        });
      }, { threshold: 0.5 });
      twIO.observe(aiEl);
    }
  }

  /* ---------- FAQ ---------- */
  document.querySelectorAll(".faq-q").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var item = btn.closest(".faq-item");
      var a = item.querySelector(".faq-a");
      var open = item.classList.contains("open");
      document.querySelectorAll(".faq-item.open").forEach(function (o) {
        o.classList.remove("open");
        o.querySelector(".faq-a").style.maxHeight = null;
      });
      if (!open) { item.classList.add("open"); a.style.maxHeight = a.scrollHeight + "px"; }
    });
  });

  /* ---------- mobile menu ---------- */
  var mb = document.querySelector(".menu-btn");
  var mm = document.querySelector(".mobile-menu");
  if (mb && mm) {
    mb.addEventListener("click", function () { mm.classList.toggle("show"); });
    mm.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { mm.classList.remove("show"); }); });
  }

  /* ---------- audit form (real submit → audit-request edge fn) ---------- */
  var form = document.querySelector("#auditForm");
  if (form) {
    var fb = document.querySelector("#form-feedback");
    var btn = form.querySelector("button[type=submit]");
    var btnDefault = btn ? btn.textContent : "Send me my audit";
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (btn) { btn.disabled = true; btn.textContent = "Sending…"; }
      if (fb) { fb.className = ""; fb.textContent = ""; }

      var email = (form.email.value || "").trim().toLowerCase();
      var payload = {
        business_name: (form.business_name.value || "").trim(),
        city: form.city.value,
        industry: form.industry.value,
        email: email,
        submitted_at: new Date().toISOString(),
        source: "cascadelocalseo.com"
      };

      fetch("https://ijpgsoeajxyeyqkjivhi.supabase.co/functions/v1/audit-request", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          if (j && j.success) {
            if (fb) { fb.className = "ok"; fb.textContent = "Thanks. Your audit is queued. Check " + email + " within 24 hours. If you don't see it, check spam."; }
            form.reset();
          } else {
            if (fb) { fb.className = "err"; fb.textContent = "Something went wrong: " + ((j && j.error) || "unknown error") + ". Email jonathan@cascadelocalseo.com and I'll handle it manually."; }
          }
        })
        .catch(function () {
          if (fb) { fb.className = "err"; fb.textContent = "Network error. Email jonathan@cascadelocalseo.com and I'll handle it manually."; }
        })
        .then(function () {
          if (btn) { btn.disabled = false; btn.textContent = btnDefault; }
        });
    });
  }
})();
