"""
PROTOTYPE — build the embedded demo apps, one HTML file per page tone.

The portfolio's whole premise is that already-built things RUN inside the page.
That only works visually if the running thing shares the page's ground; a
near-black demo panel dropped into a mid-slate page reads as a hole, and it
wrecks any judgement about the page tone itself.

So the two demos are written once, with colour tokens, and built once per tone.
Edit PALETTES or the templates below and re-run:

    python3 demos/build.py
"""
import pathlib

PALETTES = {
    # tone     scheme  bg         fg         border     barbg      muted      inset      accent     ok         warn       bad
    "slate": ("dark",  "#191e24", "#dfe4ea", "#333b45", "#212831", "#7d8894", "#14181d", "#6cb6ff", "#57ab5a", "#d4a13a", "#e5534b"),
    "fog":   ("dark",  "#272e36", "#e8ecf1", "#454e5a", "#303842", "#94a0ad", "#222831", "#8cc6ff", "#6cc26c", "#dbb04a", "#ec6d63"),
    "ash":   ("light", "#eaedf0", "#1a1f26", "#bcc4cc", "#dfe3e7", "#6b7681", "#f4f6f8", "#0d4f9c", "#26703a", "#8a6100", "#b3261e"),
}

REGEX_LAB = r"""
<style>
  :root { color-scheme: __SCHEME__; }
  * { box-sizing: border-box; }
  body { margin:0; font: 13px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;
         background:__BG__; color:__FG__; }
  .wrap { border:1px solid __BORDER__; border-radius:10px; overflow:hidden; }
  .bar { display:flex; align-items:center; gap:8px; padding:8px 12px;
         background:__BARBG__; border-bottom:1px solid __BORDER__; font-size:11px;
         letter-spacing:.08em; text-transform:uppercase; color:__MUTED__; }
  .dot { width:9px; height:9px; border-radius:50%; background:__OK__; }
  .body { padding:14px; }
  input, textarea { width:100%; background:__BG__; color:__FG__;
    border:1px solid __BORDER__; border-radius:6px; padding:8px 10px;
    font: inherit; outline:none; }
  input:focus, textarea:focus { border-color:__ACCENT__; }
  label { display:block; font-size:10px; letter-spacing:.1em; text-transform:uppercase;
          color:__MUTED__; margin:10px 0 5px; }
  mark { background:__MARKBG__; color:__MARKFG__; border-radius:3px;
         box-shadow:0 0 0 1px __MARKRING__; }
</style>

<div class="wrap">
  <div class="bar"><span class="dot"></span> regex lab &middot; live</div>
  <div class="body">
    <label>pattern</label>
    <input id="pat" value="(\w+)@(\w+)\.com" spellcheck="false"/>
    <label>subject</label>
    <textarea id="txt" rows="4" spellcheck="false">Ping sam@example.com or ops@meridian.com.
Fallback: noreply@northgate.com (do not reply)</textarea>
    <label>matches</label>
    <div id="out" style="padding:10px;border:1px solid __BORDER__;border-radius:6px;
         background:__INSET__;white-space:pre-wrap;min-height:56px"></div>
    <div id="groups" style="margin-top:10px;color:__MUTED__;font-size:12px"></div>
  </div>
</div>
<script>
  const pat = document.getElementById('pat'), txt = document.getElementById('txt'),
        out = document.getElementById('out'), grp = document.getElementById('groups');
  const esc = s => s.replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
  function run() {
    let re;
    try { re = new RegExp(pat.value, 'g'); }
    catch (e) { out.innerHTML = '<span style="color:__BAD__">' + esc(e.message) + '</span>';
                grp.textContent = ''; return; }
    const s = txt.value; let html = '', last = 0, n = 0, rows = [];
    for (const m of s.matchAll(re)) {
      if (m[0] === '') { re.lastIndex++; continue; }
      n++;
      html += esc(s.slice(last, m.index)) + '<mark>' + esc(m[0]) + '</mark>';
      last = m.index + m[0].length;
      rows.push('#' + n + '  ' + m.slice(1).map((g,i) => '$'+(i+1)+'=' + (g??'—')).join('  '));
    }
    html += esc(s.slice(last));
    out.innerHTML = html || '<span style="color:__MUTED__">no matches</span>';
    grp.textContent = n + ' match' + (n===1?'':'es') + (rows.length ? '  ·  ' + rows.join('   ') : '');
  }
  pat.addEventListener('input', run); txt.addEventListener('input', run); run();
</script>
"""

DEPLOY_BOARD = r"""
<style>
  :root { color-scheme: __SCHEME__; }
  * { box-sizing: border-box; }
  body { margin:0; font: 13px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;
         background:__BG__; color:__FG__; }
  .wrap { border:1px solid __BORDER__; border-radius:10px; overflow:hidden; }
  .bar { display:flex; align-items:center; gap:8px; padding:8px 12px;
         background:__BARBG__; border-bottom:1px solid __BORDER__; font-size:11px;
         letter-spacing:.08em; text-transform:uppercase; color:__MUTED__; }
  .dot { width:9px; height:9px; border-radius:50%; background:__OK__; }
  .body { padding:14px; }
  input, textarea { width:100%; background:__BG__; color:__FG__;
    border:1px solid __BORDER__; border-radius:6px; padding:8px 10px;
    font: inherit; outline:none; }
  input:focus, textarea:focus { border-color:__ACCENT__; }
  label { display:block; font-size:10px; letter-spacing:.1em; text-transform:uppercase;
          color:__MUTED__; margin:10px 0 5px; }
  mark { background:__MARKBG__; color:__MARKFG__; border-radius:3px;
         box-shadow:0 0 0 1px __MARKRING__; }
</style>

<div class="wrap">
  <div class="bar"><span class="dot"></span> deploy board &middot; streaming</div>
  <div class="body">
    <div id="grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(132px,1fr));gap:7px"></div>
    <div style="margin-top:12px;display:flex;gap:16px;color:__MUTED__;font-size:11px">
      <span><b id="ok" style="color:__OK__">0</b> healthy</span>
      <span><b id="deg" style="color:__WARN__">0</b> degraded</span>
      <span><b id="bad" style="color:__BAD__">0</b> failing</span>
      <span style="margin-left:auto">refreshed <b id="age">0</b>s ago</span>
    </div>
  </div>
</div>
<script>
  const names = ['auth','billing','cart','checkout','search','inventory','email','pricing',
    'ledger','webhook','media','ingest','router','sessions','tax','shipping','fraud','notify'];
  const grid = document.getElementById('grid');
  const cells = names.map(n => {
    const d = document.createElement('div');
    d.style.cssText = 'border:1px solid __BORDER__;border-radius:7px;padding:8px 9px;background:__INSET__';
    d.innerHTML = '<div style="color:__FG__;font-size:12px">'+n+'</div>' +
      '<div class="s" style="font-size:10px;letter-spacing:.08em;text-transform:uppercase"></div>' +
      '<div class="l" style="color:__MUTED__;font-size:10px;margin-top:3px"></div>';
    grid.appendChild(d); return d;
  });
  let t = 0;
  function tick() {
    let ok=0, deg=0, bad=0;
    cells.forEach((d,i) => {
      const r = Math.sin(t/7 + i*1.7) * 0.5 + 0.5;
      const state = r > 0.92 ? 'failing' : r > 0.78 ? 'degraded' : 'healthy';
      const col = state==='healthy' ? '__OK__' : state==='degraded' ? '__WARN__' : '__BAD__';
      state==='healthy' ? ok++ : state==='degraded' ? deg++ : bad++;
      const s = d.querySelector('.s'); s.textContent = state; s.style.color = col;
      d.style.borderColor = state==='healthy' ? '__BORDER__' : col + '66';
      d.querySelector('.l').textContent = 'p95 ' + Math.round(60 + r*340) + 'ms';
    });
    document.getElementById('ok').textContent = ok;
    document.getElementById('deg').textContent = deg;
    document.getElementById('bad').textContent = bad;
    document.getElementById('age').textContent = t % 5;
    t++;
  }
  tick(); setInterval(tick, 1000);
</script>
"""

TEMPLATES = {"regex_lab": REGEX_LAB, "deploy_board": DEPLOY_BOARD}


def alpha(hex_colour, aa):
    return hex_colour + aa


def build():
    here = pathlib.Path(__file__).parent
    for tone, (scheme, bg, fg, border, barbg, muted, inset, accent, ok, warn, bad) in PALETTES.items():
        repl = {
            "__SCHEME__": scheme, "__BG__": bg, "__FG__": fg, "__BORDER__": border,
            "__BARBG__": barbg, "__MUTED__": muted, "__INSET__": inset,
            "__ACCENT__": accent, "__OK__": ok, "__WARN__": warn, "__BAD__": bad,
            "__MARKBG__": alpha(accent, "2e"), "__MARKRING__": alpha(accent, "88"),
            "__MARKFG__": fg,
        }
        for name, tpl in TEMPLATES.items():
            out = tpl
            for k, v in repl.items():
                out = out.replace(k, v)
            path = here / f"{name}_{tone}.html"
            path.write_text("<!doctype html><meta charset='utf-8'>\n" + out)
            print("wrote", path.name)


if __name__ == "__main__":
    build()
