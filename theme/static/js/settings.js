/* Viewer settings, the daily quote, and click-to-load embeds.
   Everything degrades: with no JavaScript the page renders at the defaults,
   the first quote shows, and an embed offers a plain link instead. */
(function () {
  "use strict";
  var KEY = "nac.settings";
  var root = document.documentElement;
  var STEPS = [80, 90, 100, 110, 120, 130, 140, 150];

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { return {}; }
  }
  function write(s) {
    try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) { /* private mode */ }
  }

  var state = read();
  if (!state.mode) state.mode = "dark";
  if (!state.hue) state.hue = "blue";
  if (!state.motion) state.motion = "off";      // reduced motion is the default
  if (!state.pct) state.pct = 100;

  function apply() {
    root.dataset.mode = state.mode;
    root.dataset.hue = state.hue;
    ["contrast", "readable", "underline"].forEach(function (k) {
      if (state[k] === "on") root.dataset[k] = "on"; else delete root.dataset[k];
    });
    /* `motion` is stored as "motion is ALLOWED", so reduced motion is
       motion === "off". Everything about this setting reads backwards; keep the
       inversion in exactly these two places and nowhere else. */
    if (state.motion === "off") root.dataset.motion = "off";
    else delete root.dataset.motion;
    root.style.setProperty("--size", (state.pct / 100).toFixed(2));
    state.size = (state.pct / 100).toFixed(2);

    document.querySelectorAll("[data-set]").forEach(function (b) {
      b.setAttribute("aria-checked", String(state[b.dataset.set] === b.dataset.val));
    });
    document.querySelectorAll("[data-toggle]").forEach(function (b) {
      var k = b.dataset.toggle;
      /* The control is labelled "Reduce motion", so it is pressed when motion
         is NOT allowed. Reading state.motion directly here showed the box
         unchecked while reduced motion was active. */
      var on = k === "motion" ? state.motion === "off" : state[k] === "on";
      b.setAttribute("aria-pressed", String(on));
    });

    var reset = document.getElementById("sizereset");
    if (reset) {
      reset.textContent = state.pct + "%";
      var atDefault = state.pct === 100;
      reset.setAttribute("aria-label", atDefault
        ? "Text size, currently 100 percent"
        : "Text size, currently " + state.pct + " percent. Reset to 100 percent");
      reset.disabled = atDefault;
    }
    var i = STEPS.indexOf(state.pct);
    document.querySelectorAll("[data-step]").forEach(function (b) {
      var d = Number(b.dataset.step);
      if (d === -1) b.disabled = i <= 0;
      if (d === 1) b.disabled = i >= STEPS.length - 1;
    });

    var sum = document.getElementById("summary");
    if (sum) {
      var bits = [state.mode + " mode", state.hue, "text " + state.pct + "%"];
      if (state.contrast === "on") bits.push("high contrast");
      if (state.readable === "on") bits.push("readable font");
      if (state.underline === "on") bits.push("underlined links");
      if (state.motion === "off") bits.push("reduced motion");
      sum.textContent = bits.join(" · ");
    }
    write(state);
  }

  document.addEventListener("click", function (e) {
    var b = e.target.closest("button");
    if (!b) return;
    if (b.dataset.set) { state[b.dataset.set] = b.dataset.val; apply(); }
    else if (b.dataset.toggle) {
      var k = b.dataset.toggle;
      state[k] = state[k] === "on" ? "off" : "on";
      apply();
    } else if (b.dataset.step !== undefined) {
      var d = Number(b.dataset.step);
      if (d === 0) state.pct = 100;
      else {
        var i = STEPS.indexOf(state.pct);
        if (i < 0) i = STEPS.indexOf(100);
        state.pct = STEPS[Math.max(0, Math.min(STEPS.length - 1, i + d))];
      }
      apply();
    } else if (b.classList.contains("run")) {
      var host = b.closest(".embed");
      var f = document.createElement("iframe");
      f.src = host.dataset.src;
      f.title = "Live demo";
      f.loading = "lazy";
      host.textContent = "";
      host.appendChild(f);
    }
  });

  /* The quote changes once a day, not once a reload — seeded from the ordinal
     date, so every visitor sees the same line on the same day and nothing is
     stored anywhere. */
  try {
    var el = document.getElementById("quotes");
    var quotes = el ? JSON.parse(el.textContent) : [];
    if (quotes.length) {
      var now = new Date();
      var ord = Math.floor((now - new Date(now.getFullYear(), 0, 0)) / 86400000);
      var q = quotes[ord % quotes.length];
      var box = document.getElementById("quote");
      if (box) {
        box.innerHTML = "";
        var qq = document.createElement("q"); qq.textContent = q.text;
        var ci = document.createElement("cite"); ci.textContent = q.attribution;
        box.appendChild(qq); box.appendChild(ci);
      }
    }
  } catch (e) { /* leave the server-rendered quote in place */ }

  apply();
})();
