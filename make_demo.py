#!/usr/bin/env python3
import json, base64, os, html, numpy as np
D="/root/.claude/jobs/854d3f65/tmp/demo"
SITE="/workspace/unise-demo"
d=json.load(open(f"{D}/demo.json"))
SYS=[("clean","Clean","reference"),("noisy","Noisy","unprocessed input"),
     ("sgmse","SGMSE+","generative baseline"),("ditse","DiTSE","generative, standard SSL"),
     ("unise","UNISE (Ours)","proposed")]
PAPER="p248-357"
import shutil
os.makedirs(f"{SITE}/assets/audio",exist_ok=True); os.makedirs(f"{SITE}/assets/spec",exist_ok=True)
def asset(src,sub):
    dst=f"{SITE}/assets/{sub}/{os.path.basename(src)}"
    if not os.path.exists(dst): shutil.copy2(src,dst)
    return f"assets/{sub}/{os.path.basename(src)}"

cards=[]
for u in sorted(d):
    v=d[u]; panels=[]
    for key,label,note in SYS:
        sy=v["sys"][key]
        aud=asset(f"{D}/mp3/{sy['mp3']}","audio")
        img=asset(f"{D}/png/{key}_{u}.jpg","spec")
        panels.append(f'''<figure class="panel{' ours' if key=='unise' else ''}">
<figcaption class="pl">{label}</figcaption>
<img loading="lazy" width="450" height="325" alt="Mel spectrogram, {label}, {u}" src="{img}">
<p class="ht">{html.escape(sy["hyp"]) or "&mdash;"}</p>
<audio controls preload="none" src="{aud}"></audio>
</figure>''')
    cards.append(f'''<details class="card">
<summary><span class="uid">{u}</span><span class="ref">{html.escape(v["ref"])}</span></summary>
<div class="panels">{"".join(panels)}</div>
</details>''')

doc=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Listening samples for UNISE: unified noise-invariant learning for speech enhancement toward improved content preservation.">
<title>UNISE Listening Samples</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<style>
:root{{
  --paper:#f6f7f9; --card:#ffffff; --ink:#15181f; --dim:#5c6472; --line:#dfe3e9;
  --accent:#0e9384; --accent-soft:#e2f4f1;
  --good:#2f7d5f; --good-bg:#e7f3ec; --warn:#8a6516; --warn-bg:#f7efdf; --poor:#b04a3f; --poor-bg:#f9e9e6;
  --sans:"IBM Plex Sans",system-ui,sans-serif; --serif:"Source Serif 4",Georgia,serif; --mono:"IBM Plex Mono",ui-monospace,monospace;
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{
  --paper:#0f1216; --card:#171b22; --ink:#e6e9ee; --dim:#98a2b3; --line:#262c36;
  --accent:#3fc9b8; --accent-soft:#123430;
  --good:#6ec99b; --good-bg:#13291f; --warn:#d6ab5c; --warn-bg:#2b2314; --poor:#e08878; --poor-bg:#2e1a17;
}}}}
:root[data-theme="dark"]{{
  --paper:#0f1216; --card:#171b22; --ink:#e6e9ee; --dim:#98a2b3; --line:#262c36;
  --accent:#3fc9b8; --accent-soft:#123430;
  --good:#6ec99b; --good-bg:#13291f; --warn:#d6ab5c; --warn-bg:#2b2314; --poor:#e08878; --poor-bg:#2e1a17;
}}
*{{box-sizing:border-box}}\nimg{{max-width:100%}}\nhtml{{color-scheme:light dark}}
body{{background:var(--paper);color:var(--ink);font-family:var(--sans);margin:0;
  padding:clamp(20px,4vw,52px) clamp(16px,4vw,28px);line-height:1.55;-webkit-font-smoothing:antialiased}}
main{{max-width:920px;margin:0 auto;display:flex;flex-direction:column;gap:26px}}
h1{{font-size:clamp(1.35rem,3.4vw,1.9rem);font-weight:600;margin:0;letter-spacing:-.015em;text-wrap:balance}}
.sub{{color:var(--dim);margin:0;max-width:64ch;font-size:.95rem}}
.venue{{font-family:var(--mono);font-size:.7rem;letter-spacing:.13em;text-transform:uppercase;color:var(--accent);margin:0 0 10px}}
.stats{{display:flex;flex-wrap:wrap;gap:8px}}
.stat{{flex:1 1 130px;background:var(--card);border:1px solid var(--line);border-radius:7px;padding:11px 13px;
  display:flex;flex-direction:column;gap:2px}}
.stat.ours{{border-color:var(--accent);background:var(--accent-soft)}}
.sv{{font-family:var(--mono);font-size:1.28rem;font-variant-numeric:tabular-nums}}
.sv i{{font-style:normal;font-size:.72rem;color:var(--dim);margin-left:1px}}
.sl{{font-size:.76rem;color:var(--dim)}}
.note{{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--accent);
  border-radius:0 7px 7px 0;padding:13px 16px;font-size:.87rem;color:var(--dim)}}
.note b{{color:var(--ink);font-weight:600}}
.cards{{display:flex;flex-direction:column;gap:9px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden}}
.card[open]{{border-color:var(--accent)}}
summary{{cursor:pointer;padding:13px 16px;display:flex;flex-wrap:wrap;align-items:baseline;gap:10px;list-style:none}}
summary::-webkit-details-marker{{display:none}}
summary:focus-visible{{outline:2px solid var(--accent);outline-offset:-2px}}
.uid{{font-family:var(--mono);font-size:.83rem;color:var(--accent);font-weight:500}}
.tag{{font-family:var(--mono);font-size:.62rem;letter-spacing:.09em;text-transform:uppercase;
  background:var(--accent-soft);color:var(--accent);padding:2px 7px;border-radius:3px}}
.ref{{font-family:var(--serif);font-size:.97rem;color:var(--dim);flex:1 1 100%}}
.card[open] .ref{{color:var(--ink)}}
.panels{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;padding:14px 16px 16px;
  border-top:1px solid var(--line);background:var(--paper)}}
.panel{{margin:0;display:flex;flex-direction:column;gap:6px;min-width:0}}
.panel.ours .pl{{color:var(--accent)}}
.pl{{font-size:.76rem;font-weight:600;color:var(--dim);letter-spacing:.01em}}
.panel img{{width:100%;height:auto;display:block;border-radius:4px;border:1px solid var(--line)}}
.panel.ours img{{border-color:var(--accent)}}
.ht{{font-family:var(--serif);font-size:.83rem;line-height:1.4;color:var(--dim);margin:0;
  hyphens:auto;overflow-wrap:break-word}}
.panel.ours .ht{{color:var(--ink)}}
audio{{width:100%;height:30px;margin-top:auto}}
@media (max-width:900px){{.panels{{grid-template-columns:repeat(2,1fr)}}}}
@media (max-width:520px){{.panels{{grid-template-columns:1fr}}}}
footer{{color:var(--dim);font-size:.8rem;border-top:1px solid var(--line);padding-top:16px}}
.spec{{margin:0;padding:14px 16px 16px;border-top:1px solid var(--line);background:var(--paper)}}
.spec img{{width:100%;height:auto;display:block;border:1px solid var(--line);border-radius:5px;background:#fff}}
.spec figcaption{{font-size:.75rem;color:var(--dim);margin:7px 0 0}}
.hyps{{list-style:none;margin:12px 0 0;padding:0;display:flex;flex-direction:column;gap:1px}}
.hyps li{{display:grid;grid-template-columns:132px minmax(0,1fr);gap:14px;align-items:baseline;
  padding:6px 8px;border-radius:4px}}
.hyps li.ours{{background:var(--accent-soft)}}
.hl{{font-size:.79rem;font-weight:600;color:var(--dim)}}
.hyps li.ours .hl{{color:var(--accent)}}
.ht{{font-family:var(--serif);font-size:.92rem;color:var(--ink)}}
@media (max-width:620px){{.hyps li{{grid-template-columns:1fr;gap:2px}}}}
@media (max-width:620px){{
  .row{{grid-template-columns:1fr}}
}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important;animation:none!important}}}}
</style>
<main>
<header>
  <p class="venue">ICASSP 2027 &middot; submission</p>
  <h1>UNISE: Unified Noise-Invariant Learning for Speech Enhancement toward Improved Content Preservation</h1>
  <p class="sub">Generative enhancement can sound clean while quietly rewriting what was said. These 18 VoiceBank&ndash;DEMAND utterances let you hear and see that difference: audio, Whisper&nbsp;large-v3 transcripts, and mel spectrograms for every system.</p>
</header>
<p class="note"><b>How to read this.</b> Each utterance opens to five columns &mdash; mel spectrogram on a shared scale, the Whisper&nbsp;large-v3 transcript of that audio, then the audio itself. Read across to compare systems on the same moment of speech, and against the reference above to see where a system changed the words rather than the noise. <b>Clean</b> is the studio recording and <b>Noisy</b> the unprocessed input.</p>
<section class="cards">{"".join(cards)}</section>
<footer>Audio and spectrograms are cropped to the speech region of the clean reference; audio is 16&nbsp;kHz MP3. SGMSE+ and DiTSE outputs are the authors&rsquo; released VoiceBank&ndash;DEMAND samples; UNISE is the current model. Reference text is from VCTK.</footer>
</main>\n</body>\n</html>'''
open(f"{SITE}/index.html","w").write(doc)
import subprocess
sz=subprocess.run(["du","-sh",SITE],capture_output=True,text=True).stdout.split()[0]
print(f"site: {SITE}  index.html {os.path.getsize(f'{SITE}/index.html')/1024:.0f} KB, assets {sz} total, {len(d)} utterances")
