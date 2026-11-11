#!/usr/bin/env python3
"""/video-edit template: the finished build of the first reel made with this skill (a 25s reel about editing videos
with Claude, cut from 5 phone clips). Copy it into a project, keep the machinery, rewrite the content.

Sections of the example (segment ids come from segments.json, written by scripts/assemble.py):
  hook/course/cta   bold look: kinetic lowercase words, the big ones BEHIND the head (cutout on top)
                    hook + course: other creators' reels pop in as cards, @handles credited on screen
  girl              cool girl: warm faded grade, yellow serif italic; the creator's own reels orbit them on
                    "cool girl... like this", then a Claude desktop recreation (agents/claude-desktop) plays BEHIND
                    them: clips dropped in, /video-edit typed, Claude working
  dude + tech       cool dude: dark editorial grade, tracked caps + serif punch words, wide shot then 4K close-up
  cta              Instagram profile recreation (agents/ig-follow): tap Follow, comment EDIT, with tap sounds

Machinery to keep: dude_words(), cards(), girl(), orbit(), core(), claude_window(), skill_card(), ig_overlay(),
grades(), audio(), SAFE_GUIDE, cut times from segments.json, S(t).
Content to rewrite: GROUPS, CARDS, GIRL_BLOCKS, TRACK, SERIF, overlay files + in-times, SFX, SHIFT reference times.

Run from the project folder with PY, the skill's Python (see SKILL.md):
PY build.py            writes index.html
PY build.py --safe     same + red Instagram safe-zone guide (snapshots only, never render with it)
                       (`SAFE=1 python3 build.py` still works in bash/zsh; --safe also works in PowerShell)
"""
import json
import math
import os
import shutil
import subprocess
import sys

SAFE = '--safe' in sys.argv or bool(os.environ.get('SAFE'))
DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                            'stream=duration', '-of', 'csv=p=0', 'assets/aroll.mp4'],
                           capture_output=True, encoding='utf-8', errors='replace').stdout.strip().split(',')[0])
YEL = '#FAE67A'
with open('segments.json', encoding='utf-8') as _f:
    SEG = {s['id']: s for s in json.load(_f)}
# cut times = exact first frame of each segment, nudged 2ms early so a tl.set lands ON that frame
T = {k: s['frame'] / 30 - .002 if s['frame'] else 0.0 for k, s in SEG.items()}
CUTS = [T['course'], T['girl'], T['dude'], T['tech'], T['cta']]
GIRL_A, DUDE_A, CTA_A = T['girl'], T['dude'], T['cta']


def src_to_cut(seg, src_t):
    """time in the cut for a moment in a segment's source clip"""
    return SEG[seg]['frame'] / 30 + (src_t - SEG[seg]['src_in'])


CLAUDE_IN = src_to_cut('girl', 49.10)       # agents/claude-desktop timeline 0
CLAUDE_DUR = 4.35
IG_IN = src_to_cut('cta', 37.25)            # agents/ig-follow timeline 0
IG_DUR = 2.90
IG_TAPS = (0.70, 1.75)

DUDE_F = 'contrast(1.07) saturate(.9) brightness(.97)'
GIRL_F = 'sepia(.18) saturate(.9) contrast(.93) brightness(1.05) hue-rotate(-5deg)'
DARK_F = 'contrast(1.1) saturate(.84) brightness(.8) hue-rotate(-4deg)'      # room moody, not crushed (v5: was too dark)
DARK_SUBJ = 'contrast(1.06) saturate(.86) brightness(.98) hue-rotate(-4deg)'  # speaker (cutout) stays lit

# Word times below were measured on the v4 cut, where the cool dude clip started at src 10.95 (cut 13.933) and
# 'tech' at 16.400. v5 trims the dead air before "Or" (clip now starts at src 11.28), so every time from the cool
# dude section on is shifted by the measured change of the 'tech' cut.
SHIFT = SEG['tech']['frame'] / 30 - 16.400


def S(t):
    return t + SHIFT


# Instagram Reels safe zone: top 220, bottom 450 (nothing below y=1470), sides 35, right 100 from y~1155.
# Behind-head words: baseline about 30% of the x-height below his head top, so they stay readable.
C = 'left:0;right:0;text-align:center;'
# v6: lead-in lines centred right in front of him (chest band) instead of pinned to the left edge
LO1, LO2 = C + 'top:1010px', C + 'top:1100px'
GROUPS = [  # (start, end, [(t, text, classes, style)])  bold-look words, hook / course / cta
    (0.00, 1.84, [(0.00, "everybody's talking", 'sm', LO1), (0.92, 'about how', 'sm', LO2)]),
    (1.40, CUTS[0], [(1.48, 'claude', 'xl back', C + 'top:205px')]),
    (1.84, CUTS[0], [(1.86, 'can edit your', 'sm', LO1), (2.40, 'videos.', 'big y', C + 'top:1090px')]),
    (CUTS[0], 4.62, [(3.14, "but they're all", 'sm', LO1), (3.70, 'selling a', 'sm', LO2),
                     (4.18, 'course', 'xl back', C + 'top:275px')]),
    (4.62, 5.54, [(4.62, 'it makes', 'sm', C + 'top:950px'), (4.80, 'no sense', 'big y', C + 'top:1030px'),
                  (5.24, 'because', 'sm', C + 'top:1270px')]),
    # SKILL.md card owns the middle band here, so the lead-in is one small line above his head
    (5.54, CUTS[1], [(5.54, 'all you need is a well-written', 'sm2', C + 'top:232px'), (6.88, 'skill.', 'xl back y', C + 'top:270px')]),
    (CTA_A, IG_IN - .05, [(S(19.80), 'so if you want your', 'sm', LO1), (S(20.74), 'claude', 'xl back', C + 'top:205px'),
                          (S(20.92), 'to edit your videos', 'sm', LO2), (S(21.78), 'like this', 'md y', C + 'top:1190px')]),
    (IG_IN - .05, S(23.12), [(S(22.20), 'just drop me a follow', 'sm', C + 'top:240px')]),
    (S(23.12), S(23.78), [(S(23.16), 'comment', 'sm', C + 'top:240px'), (S(23.48), 'EDIT', 'md y', C + 'top:318px')]),
    (S(23.78), DUR, [(S(23.80), "and i'll send you the free skill.", 'sm2', C + 'top:244px')]),
]


def dude_words():
    html, tw = [], []
    for g, (a, b, words) in enumerate(GROUPS):
        for k, (t, txt, cls, st) in enumerate(words):
            wid = f'w{g}-{k}'
            html.append(f'<div id="{wid}" class="dw {cls}" style="{st}">{txt}</div>')
            tw.append(f"gsap.set('#{wid}',{{autoAlpha:0}});")
            tw.append(f"tl.fromTo('#{wid}',{{autoAlpha:0,scale:1.22,filter:'blur(22px)'}},{{autoAlpha:1,scale:1,filter:'blur(0px)',"
                      f"duration:.2,ease:'power3.out',immediateRender:false}},{max(a, t - .05):.3f});")
            if b < DUR - .01:
                tw.append(f"tl.to('#{wid}',{{autoAlpha:0,scale:.96,filter:'blur(16px)',duration:.12,ease:'power2.in'}},{b - .12:.3f});")
                tw.append(f"tl.set('#{wid}',{{autoAlpha:0}},{b:.3f});")
    return html, tw


# ------------------------------------------------------------------ opening: creator reels as cards
CARDS = [  # id, file, handle, in, out, left, top, rotation
    ('ccreator1', 'creator1_hook', '@creator.one', 0.15, CUTS[0] - .1, 55, 430, -7),
    ('ccreator2', 'creator2_hook', '@creator.two', 0.45, CUTS[0] - .1, 765, 400, 6),
    ('ccreator2b', 'creator2_course', '@creator.two', 3.62, 4.55, 745, 470, 5),
]


def cards():
    html, tw = [], []
    for k, (cid, f, handle, a, b, x, y, rot) in enumerate(CARDS):
        html.append(f'<div id="{cid}" class="ccard" style="left:{x}px;top:{y}px"><div class="ctile">'
                    f'<video id="v{cid}" src="assets/opening/{f}.mp4" muted playsinline data-start="{a - .05:.3f}" data-media-start="0" '
                    f'data-duration="{b - a + .1:.3f}" data-track-index="{40 + k}"></video></div><div class="chandle">{handle}</div></div>')
        tw += [f"gsap.set('#{cid}',{{autoAlpha:0,rotation:{rot},scale:.4,y:60}});",
               f"tl.to('#{cid}',{{autoAlpha:1,scale:1,y:0,duration:.42,ease:'back.out(1.6)'}},{a:.3f});",
               f"tl.to('#{cid}',{{autoAlpha:0,scale:.7,y:-40,rotation:{rot * 2},duration:.18,ease:'power2.in'}},{b - .18:.3f});",
               f"tl.set('#{cid}',{{autoAlpha:0}},{b:.3f});"]
    return html, tw


# ------------------------------------------------------------------ cool girl section
GIRL_SPLIT = 9.55   # top captions + orbit until here, then the Claude window takes the wall
GIRL_BLOCKS = [  # (id, top, start, end, small words, big words)
    ('gA', 330, GIRL_A, GIRL_SPLIT, [(7.62, 'and'), (7.88, 'you'), (7.98, 'can'), (8.10, 'get'), (8.26, 'the')],
     [(8.42, 'cool'), (8.56, 'girl')], [(8.78, 'aesthetic'), (9.04, 'like'), (9.34, 'this.')]),
    ('gB', 1180, GIRL_SPLIT, 11.20, [(9.64, 'all'), (9.84, 'you'), (9.96, 'need'), (10.06, 'to'), (10.26, 'do'), (10.40, 'is')],
     [(10.52, 'drop'), (10.82, 'your'), (10.96, 'clips')], []),
    ('gC', 1180, 11.20, 12.10, [(11.26, 'trigger'), (11.76, 'the')], [(11.94, 'skill')], []),
    ('gD', 1180, 12.10, DUDE_A, [(12.16, 'and'), (12.42, 'claude'), (12.64, 'takes'), (12.88, 'care'), (13.08, 'of'), (13.18, 'it'), (13.30, 'all')],
     [(13.44, 'for'), (13.66, 'you.')], []),
]


def girl():
    html, tw = [], []
    for bid, top, a, b, small, big, small2 in GIRL_BLOCKS:
        lines = []
        for li, (kind, words) in enumerate((('s', small), ('e', big), ('s', small2))):
            if not words:
                continue
            spans = []
            for k, (t, txt) in enumerate(words):
                gid = f'{bid}-{li}-{k}'
                spans.append(f'<span id="{gid}" class="gw">{txt}</span>')
                if kind == 's':
                    tw.append(f"tl.fromTo('#{gid}',{{autoAlpha:0,y:14}},{{autoAlpha:1,y:0,duration:.26,ease:'power2.out',immediateRender:false}},{max(a, t - .04):.3f});")
                else:
                    tw.append(f"tl.fromTo('#{gid}',{{autoAlpha:0,y:22,scale:.92}},{{autoAlpha:1,y:0,scale:1,duration:.4,ease:'power2.out',immediateRender:false}},{max(a, t - .04):.3f});")
            lines.append(f'<div class="{kind}">{" ".join(spans)}</div>')
        low = ' low' if top > 1000 else ''   # lower blocks sit over his legs: smaller italic so 3 words fit one line
        html.append(f'<div id="{bid}" class="gcap{low}" style="top:{top}px">{"".join(lines)}</div>')
        tw.append(f"gsap.set('#{bid} .gw',{{autoAlpha:0}});")
        tw.append(f"tl.to('#{bid}',{{autoAlpha:0,duration:.14}},{b - .14:.3f});")
        tw.append(f"tl.set('#{bid}',{{autoAlpha:0}},{b:.3f});")
    for k, (x, y, sz, t) in enumerate([(130, 470, 58, 8.48), (930, 560, 40, 8.62), (900, 330, 30, 8.85)]):
        html.append(f'<div id="sp{k}" class="spark" style="left:{x}px;top:{y}px;font-size:{sz}px">&#10022;</div>')
        tw += [f"gsap.set('#sp{k}',{{autoAlpha:0,scale:0}});",
               f"tl.to('#sp{k}',{{autoAlpha:1,scale:1,duration:.3,ease:'back.out(2.5)'}},{t:.3f});",
               f"tl.to('#sp{k}',{{scale:.7,duration:.4,yoyo:true,repeat:1,ease:'sine.inOut'}},{t + .3:.3f});",
               f"tl.to('#sp{k}',{{autoAlpha:0,duration:.14}},{GIRL_SPLIT - .14:.3f});",
               f"tl.set('#sp{k}',{{autoAlpha:0}},{GIRL_SPLIT:.3f});"]
    return html, tw


# his real reels orbit him like a ring on "you can get the cool girl aesthetic like this"
REELS = ['r1', 'r2', 'r3', 'r4', 'r5', 'r6']
CX, CY, RX, RY = 640, 1110, 460, 150
TW_, TH_ = 190, 338
ORBIT_IN, ORBIT_OUT, REV, STEP = 7.86, GIRL_SPLIT, 5.2, 0.1


def orbit():
    html, tw = [], []
    n = len(REELS)
    for i, r in enumerate(REELS):
        for side in ('b', 'f'):
            html.append(f'<div id="{side}{i}" class="orb {side}"><div class="pop"><div class="tile">'
                        f'<video id="v{side}{i}" src="assets/reels/{r}.mp4" muted playsinline data-start="{ORBIT_IN - .1:.2f}" '
                        f'data-media-start="0" data-duration="{ORBIT_OUT - ORBIT_IN + .1:.2f}" '
                        f'data-track-index="{20 + i * 2 + (side == "f")}"></video></div></div></div>')
        frames, t = [], ORBIT_IN
        while t <= ORBIT_OUT + 1e-6:
            th = 2 * math.pi * ((t - ORBIT_IN) / REV) + i * 2 * math.pi / n + 0.35
            s = math.sin(th)
            frames.append((t, CX + RX * math.cos(th), CY + RY * s, 0.6 + 0.4 * (s + 1) / 2, s))
            t = round(t + STEP, 4)
        for side in ('b', 'f'):
            sel = f'#{side}{i}'
            vis = (lambda s: 1 if s > 0 else 0) if side == 'f' else (lambda s: 0 if s > 0 else 1)
            t0, x0, y0, sc0, s0 = frames[0]
            tw.append(f"gsap.set('{sel}',{{xPercent:-50,yPercent:-50,x:{x0:.1f},y:{y0:.1f},scale:{sc0:.3f},autoAlpha:0}});")
            tw.append(f"tl.set('{sel}',{{autoAlpha:{vis(s0)}}},{t0:.3f});")
            kf = ','.join(f"{{x:{x:.1f},y:{y:.1f},scale:{sc:.3f},autoAlpha:{vis(s)},duration:{STEP},ease:'none'}}"
                          for _, x, y, sc, s in frames[1:])
            tw.append(f"tl.to('{sel}',{{keyframes:[{kf}]}},{t0:.3f});")
            tw.append(f"tl.set('{sel}',{{autoAlpha:0}},{ORBIT_OUT:.3f});")
            tw.append(f"gsap.set('{sel} .pop',{{scale:0}});")
            tw.append(f"tl.to('{sel} .pop',{{scale:1,duration:.45,ease:'back.out(1.8)'}},{ORBIT_IN + i * .07:.3f});")
            tw.append(f"tl.to('{sel} .pop',{{scale:0,duration:.2,ease:'power2.in'}},{ORBIT_OUT - .24 + i * .01:.3f});")
    return html, tw


def claude_window():
    """agents/claude-desktop render, placed behind the speaker on the wall of the wide shot"""
    f = 'agents/claude-desktop/renders/claude-desktop.webm'
    if not os.path.exists(f):
        return [], []
    html = [f'<div id="cwin"><video id="vcwin" src="{f}" muted playsinline data-start="{CLAUDE_IN:.3f}" data-media-start="0" '
            f'data-duration="{CLAUDE_DUR:.3f}" data-track-index="5"></video></div>']
    tw = ["gsap.set('#cwin',{autoAlpha:0});", f"tl.set('#cwin',{{autoAlpha:1}},{CLAUDE_IN:.3f});",
          f"tl.set('#cwin',{{autoAlpha:0}},{DUDE_A:.3f});"]
    return html, tw


SKILL_IN, SKILL_DUR = 5.42, 2.15   # "because all you need is a well-written skill"


def skill_card():
    """agents/skill-md render: SKILL.md scrolling, slightly tilted card under his face"""
    f = 'agents/skill-md/renders/skill-md.webm'
    if not os.path.exists(f):
        return [], []
    d = min(SKILL_DUR, CUTS[1] - SKILL_IN)
    html = [f'<div id="skillw"><video id="vskill" src="{f}" muted playsinline data-start="{SKILL_IN:.3f}" data-media-start="0" '
            f'data-duration="{d:.3f}" data-track-index="7"></video></div>']
    tw = ["gsap.set('#skillw',{autoAlpha:0});", f"tl.set('#skillw',{{autoAlpha:1}},{SKILL_IN:.3f});",
          f"tl.set('#skillw',{{autoAlpha:0}},{CUTS[1]:.3f});"]
    return html, tw


def ig_overlay():
    f = 'agents/ig-follow/renders/ig-follow.webm'
    if not os.path.exists(f):
        return [], []
    html = [f'<div id="igw"><video id="vig" src="{f}" muted playsinline data-start="{IG_IN:.3f}" data-media-start="0" '
            f'data-duration="{min(IG_DUR, DUR - IG_IN):.3f}" data-track-index="6"></video></div>']
    tw = ["gsap.set('#igw',{autoAlpha:0});", f"tl.set('#igw',{{autoAlpha:1}},{IG_IN:.3f});"]
    return html, tw


# ------------------------------------------------------------------ cool dude section (editorial studio look)
# tiny wide-tracked caps (Montserrat) + heavy lowercase serif punch words (DM Serif Display), dark grade,
# masked letter reveals, slow push-ins, one light sweep, moving film grain. Wide shot -> 4K close-up.
TECH_A = T['tech']
TRACK = [  # (id, start, end, top, spread across the width?, [(t, WORD)])
    ('tA', DUDE_A, S(14.96), 1210, True, [(S(14.33), 'OR'), (S(14.44), 'YOU'), (S(14.54), 'CAN'), (S(14.68), 'GET'), (S(14.84), 'THE')]),
    ('tC', S(15.40), TECH_A, 1395, False, [(S(15.42), 'AESTHETIC')]),
    ('tD', TECH_A, S(17.32), 1380, False, [(S(16.40), 'AND'), (S(16.58), 'THE'), (S(16.72), 'FUNNIEST'), (S(17.00), 'THING'), (S(17.18), 'IS')]),
    ('tE', S(17.32), S(18.48), 1380, False, [(S(17.36), "I'M"), (S(17.56), 'NOT'), (S(17.68), 'A'), (S(17.86), 'TECH'), (S(18.02), 'BRO'),
                                             (S(18.18), 'AT'), (S(18.34), 'ALL')]),
    ('tF', S(18.48), CTA_A, 1380, False, [(S(18.52), 'AND'), (S(18.72), 'I'), (S(18.90), 'SUCK'), (S(19.18), 'AT')]),
]
SERIF = [  # (id, t, end, text, top, size, italic)
    ('sB', S(15.00), S(15.70), 'cool dude', 1085, 210, False),
    ('sD', S(15.72), TECH_A, 'like this.', 1085, 210, False),
    ('sE', S(17.86), S(18.48), 'tech bro', 1060, 250, False),
    ('sF', S(19.36), CTA_A, 'design.', 1040, 270, True),
]


def core():
    html, tw = [], []
    for tid, a, b, top, spread, words in TRACK:
        spans = ''.join(f'<span id="{tid}-{k}" class="tw">{w}</span>' for k, (_, w) in enumerate(words))
        html.append(f'<div id="{tid}" class="track{" spread" if spread else ""}" style="top:{top}px">{spans}</div>')
        for k, (t, _) in enumerate(words):
            tw.append(f"gsap.set('#{tid}-{k}',{{autoAlpha:0}});")
            # "tracking in" done with scaleX (letterSpacing tweens stutter under frame-by-frame capture)
            tw.append(f"tl.fromTo('#{tid}-{k}',{{autoAlpha:0,scaleX:1.45,filter:'blur(8px)'}},{{autoAlpha:1,scaleX:1,"
                      f"filter:'blur(0px)',duration:.45,ease:'power3.out',immediateRender:false}},{max(a, t - .04):.3f});")
        if b < DUR - .01:
            tw += [f"tl.to('#{tid}',{{autoAlpha:0,filter:'blur(6px)',duration:.16}},{b - .16:.3f});", f"tl.set('#{tid}',{{autoAlpha:0}},{b:.3f});"]
    for sid, t, b, text, top, size, it in SERIF:
        chars = ''.join(f'<span class="mk"><span class="ch">{"&nbsp;" if c == " " else c}</span></span>' for c in text)
        html.append(f'<div id="{sid}" class="serif{" it" if it else ""}" style="top:{top}px;font-size:{size}px">{chars}</div>')
        tw += [f"gsap.set('#{sid}',{{autoAlpha:0}});",
               f"tl.set('#{sid}',{{autoAlpha:1}},{t - .04:.3f});",
               f"tl.fromTo('#{sid} .ch',{{yPercent:115}},{{yPercent:0,duration:.6,ease:'expo.out',stagger:.028,immediateRender:false}},{t - .04:.3f});",
               f"tl.fromTo('#{sid}',{{scale:1.06,filter:'blur(6px)'}},{{scale:1,filter:'blur(0px)',duration:.4,ease:'power3.out',immediateRender:false}},{t - .04:.3f});"]
        if b - t < .8:   # too short for an exit: hard cut with the shot
            tw.append(f"tl.set('#{sid}',{{autoAlpha:0}},{b:.3f});")
        elif b < DUR - .01:
            tw += [f"tl.to('#{sid}',{{autoAlpha:0,y:-14,filter:'blur(10px)',duration:.18,ease:'power2.in'}},{b - .18:.3f});",
                   f"tl.set('#{sid}',{{autoAlpha:0}},{b:.3f});"]
    # one soft light sweep as the section opens. (Film grain removed in v6: autoAlpha:1 overrode its CSS opacity,
    # so it ran at 100% and read as heavy noise. keep it clean.)
    html.append('<div id="sweep" class="fx"></div>')
    tw += ["gsap.set('#sweep',{autoAlpha:0});",
           f"tl.set('#sweep',{{autoAlpha:1}},{DUDE_A + .15:.3f});",
           f"tl.fromTo('#sweep',{{backgroundPosition:'130% 0%'}},{{backgroundPosition:'-30% 0%',duration:1.3,ease:'power2.inOut',immediateRender:false}},{DUDE_A + .15:.3f});",
           f"tl.set('#sweep',{{autoAlpha:0}},{DUDE_A + 1.5:.3f});"]
    return html, tw


def grades():
    tw = [f"gsap.set('.g',{{filter:'{DUDE_F}'}});",
          f"tl.set('.g',{{filter:'{GIRL_F}'}},{GIRL_A:.3f});",
          f"tl.set('.g',{{filter:'{DARK_F}'}},{DUDE_A:.3f});",
          f"tl.set('#cut',{{filter:'{DARK_SUBJ}'}},{DUDE_A:.3f});",
          f"tl.set('.g',{{filter:'{DUDE_F}'}},{CTA_A:.3f});",
          "gsap.set(['.girlfx','.darkfx'],{autoAlpha:0});",
          f"tl.set('.dudefx',{{autoAlpha:0}},{GIRL_A:.3f});", f"tl.set('.girlfx',{{autoAlpha:1}},{GIRL_A:.3f});",
          f"tl.set('.girlfx',{{autoAlpha:0}},{DUDE_A:.3f});", f"tl.set('.darkfx',{{autoAlpha:1}},{DUDE_A:.3f});",
          f"tl.set('.darkfx',{{autoAlpha:0}},{CTA_A:.3f});", f"tl.set('.dudefx',{{autoAlpha:1}},{CTA_A:.3f});"]
    for t in CUTS:
        if t in (DUDE_A, T['tech']):
            continue   # cool dude section gets slow push-ins instead of the punch
        tw.append(f"tl.fromTo('#stage',{{scale:1.05}},{{scale:1,duration:.32,ease:'power2.out',immediateRender:false}},{t:.3f});")
    tw += [f"tl.fromTo('#stage',{{filter:'blur(18px) brightness(1.35)'}},{{filter:'blur(0px) brightness(1)',"
           f"duration:.45,ease:'power3.out',immediateRender:false}},{DUDE_A:.3f});",
           f"tl.set('#stage',{{filter:'none'}},{DUDE_A + .47:.3f});",
           f"tl.fromTo('#stage',{{scale:1}},{{scale:1.05,duration:{T['tech'] - DUDE_A:.3f},ease:'none',immediateRender:false}},{DUDE_A:.3f});",
           f"tl.fromTo('#stage',{{scale:1}},{{scale:1.045,duration:{CTA_A - T['tech']:.3f},ease:'none',immediateRender:false}},{T['tech']:.3f});"]
    return tw


SFX = [('whoosh-short', .12, .25), ('whoosh-short', 3.58, .22), ('whoosh-short', GIRL_A, .3), ('sparkle', 8.40, .25),
       ('whoosh-short', CLAUDE_IN, .25), ('whoosh-short', DUDE_A, .3),
       ('pop', 2.40, .18), ('pop', 4.80, .18),
       ('click', IG_IN + IG_TAPS[0], .7), ('click-soft', IG_IN + IG_TAPS[1], .6)]
SFX_LEN = {'whoosh-short': .57, 'pop': .72, 'sparkle': 1.8, 'click': .3, 'click-soft': .37}
SFX_GAIN = 0.75   # sounds sit 25% under the original levels: subtle, never louder than the voice


def audio():
    out, lanes = [], []
    for k, (name, t, vol) in enumerate(sorted(SFX, key=lambda x: x[1])):
        d = min(SFX_LEN[name], DUR - t)
        lane = next((i for i, end in enumerate(lanes) if end <= t), None)
        if lane is None:
            lanes.append(0); lane = len(lanes) - 1
        lanes[lane] = t + d
        out.append(f'<audio id="sfx{k}" src="assets/sfx/{name}.mp3" data-start="{t:.3f}" data-duration="{d:.3f}" '
                   f'data-track-index="{10 + lane}" data-volume="{vol * SFX_GAIN:.3f}"></audio>')
    return out


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
#stage{{position:absolute;inset:0;transform-origin:50% 45%}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#bgv{{z-index:0}}
#cwin{{position:absolute;left:40px;top:230px;width:1000px;height:720px;z-index:2;filter:drop-shadow(0 30px 60px rgba(60,35,25,.35))}}
#cwin video{{width:1000px;height:720px;display:block}}
.dw.back{{z-index:3}}
#cutwrap{{position:absolute;inset:0;z-index:4}}
.orb{{position:absolute;left:0;top:0;width:{TW_}px;height:{TH_}px}}
.orb.b{{z-index:3;filter:brightness(.75)}}
.orb.f{{z-index:6}}
.pop{{width:100%;height:100%}}
.tile{{width:100%;height:100%;border-radius:28px;overflow:hidden;background:#111;border:5px solid rgba(255,248,239,.92);
  box-shadow:0 26px 60px rgba(0,0,0,.45),0 6px 16px rgba(0,0,0,.25)}}
.tile video{{width:100%;height:100%;object-fit:cover;display:block}}

/* opening creator cards */
.ccard{{position:absolute;z-index:8;width:260px}}
.ctile{{width:260px;height:462px;border-radius:30px;overflow:hidden;background:#111;border:5px solid #fff;box-shadow:0 30px 70px rgba(0,0,0,.5)}}
.ctile video{{width:100%;height:100%;object-fit:cover;display:block}}
.chandle{{margin:14px auto 0;width:max-content;max-width:330px;padding:8px 16px;border-radius:99px;background:rgba(10,10,12,.78);
  color:#fff;font:600 24px Inter;letter-spacing:-.2px}}

/* look overlays */
.fx{{position:absolute;inset:0;pointer-events:none}}
#dtone{{z-index:7;background:linear-gradient(180deg,rgba(20,55,75,.16),rgba(60,40,20,.08));mix-blend-mode:soft-light}}
#dvig{{z-index:7;background:radial-gradient(95% 62% at 50% 46%,rgba(0,0,0,0) 55%,rgba(0,0,0,.42) 100%)}}
#dgrad{{z-index:7;background:linear-gradient(180deg,rgba(0,0,0,.34) 0%,rgba(0,0,0,0) 22%,rgba(0,0,0,0) 58%,rgba(0,0,0,.30) 100%)}}
#gwarm{{z-index:7;background:linear-gradient(180deg,rgba(255,226,200,.10),rgba(255,196,170,.16));mix-blend-mode:soft-light}}
#gvig{{z-index:7;background:radial-gradient(120% 70% at 50% 45%,rgba(255,255,255,0) 52%,rgba(60,35,25,.34) 100%)}}
#ggrad{{z-index:7;background:linear-gradient(180deg,rgba(60,35,25,.30) 0%,rgba(60,35,25,0) 30%,rgba(60,35,25,0) 66%,rgba(40,24,18,.45) 100%)}}
#ktone{{z-index:7;background:linear-gradient(180deg,rgba(15,45,70,.30),rgba(10,20,35,.30));mix-blend-mode:soft-light}}
#kvig{{z-index:7;background:radial-gradient(80% 55% at 50% 44%,rgba(0,0,0,0) 40%,rgba(0,0,0,.5) 100%)}}
#kgrad{{z-index:7;background:linear-gradient(180deg,rgba(0,0,0,0) 66%,rgba(0,0,0,.38) 100%)}}

/* base type */
.dw{{position:absolute;z-index:8;color:#fff;font-family:'Inter Tight';font-weight:900;letter-spacing:-.05em;line-height:.9;
  text-shadow:0 10px 40px rgba(0,0,0,.55),0 2px 8px rgba(0,0,0,.35);transform-origin:50% 60%;white-space:nowrap}}
.sm{{font-size:84px;font-weight:800;letter-spacing:-.04em}}
.md{{font-size:150px}}
.big{{font-size:236px}}
.xl{{font-size:220px}}
.huge{{font-size:300px}}
.y{{color:{YEL}}}

/* cool girl type */
.gcap{{position:absolute;left:0;right:0;z-index:8;text-align:center;color:#FFF8EF;text-shadow:0 2px 26px rgba(60,30,20,.55)}}
.gcap .s{{font:500 64px Inter;letter-spacing:-1px}}
.gcap .e{{font:italic 400 200px 'Instrument Serif';line-height:.92;color:{YEL};margin:4px 0 8px}}
.gcap.low .e{{font-size:150px;white-space:nowrap}}
.gw{{display:inline-block}}
.spark{{position:absolute;z-index:8;color:{YEL};line-height:1;text-shadow:0 0 18px rgba(250,230,122,.5)}}

/* cool dude section: tracked caps + serif punch words */
.track{{position:absolute;left:70px;right:70px;z-index:8;text-align:center;color:#F2EFE9;font:500 34px Montserrat;
  text-shadow:0 2px 12px rgba(0,0,0,.6);white-space:nowrap}}
.track.spread{{display:flex;justify-content:space-between;right:110px}}
.track .tw{{display:inline-block;letter-spacing:.32em;margin:0 .1em;transform-origin:50% 50%}}
.serif{{position:absolute;left:0;right:0;z-index:8;text-align:center;color:#F7F4EE;font-family:'DM Serif Display';font-weight:400;
  line-height:1.12;letter-spacing:-.02em;white-space:nowrap;text-shadow:0 12px 40px rgba(0,0,0,.45)}}
.serif.it{{font-style:italic}}
.serif .mk{{display:inline-block;overflow:hidden;padding:0 .02em .14em;margin-bottom:-.14em;vertical-align:bottom}}
.serif .ch{{display:inline-block}}
#sweep{{z-index:7;mix-blend-mode:screen;background:linear-gradient(105deg,rgba(255,240,220,0) 38%,rgba(255,240,220,.22) 50%,rgba(255,240,220,0) 62%);
  background-size:260% 100%;background-repeat:no-repeat}}

/* skill.md card on "a well-written skill" */
/* scaled to .72 so the card ends above the y=1470 safe line */
#skillw{{position:absolute;left:110px;top:745px;width:860px;height:1000px;z-index:9;transform:perspective(1800px) rotateX(7deg) scale(.72);
  transform-origin:50% 0%;filter:drop-shadow(0 40px 80px rgba(0,0,0,.55))}}
#skillw video{{width:860px;height:1000px;display:block}}

/* cta instagram: scaled to .7 (532x700), sits under his chin and ends at the y=1470 safe line */
#igw{{position:absolute;left:274px;top:770px;width:760px;height:1000px;z-index:9;transform:scale(.7);transform-origin:0 0;
  filter:drop-shadow(0 40px 80px rgba(0,0,0,.55))}}
#igw video{{width:760px;height:1000px;display:block}}
.sm2{{font-size:56px;font-weight:800;letter-spacing:-.03em}}
'''


# PY build.py --safe: draws the Instagram safe zone (red = UI covers it) for snapshot checks, never for renders
SAFE_GUIDE = ('<div style="position:absolute;inset:0;z-index:99;pointer-events:none">'
              '<div style="position:absolute;left:0;right:0;top:0;height:220px;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;left:0;right:0;top:1470px;bottom:0;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;left:0;width:35px;top:220px;height:1250px;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;right:0;width:35px;top:220px;height:935px;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;right:0;width:100px;top:1155px;height:315px;background:rgba(255,0,0,.28)"></div></div>')


def build():
    w_html, w_tw = dude_words()
    back = [h for h in w_html if 'back' in h.split('class="')[1].split('"')[0]]
    front = [h for h in w_html if h not in back]
    c_html, c_tw = cards()
    g_html, g_tw = girl()
    o_html, o_tw = orbit()
    cw_html, cw_tw = claude_window()
    ig_html, ig_tw = ig_overlay()
    s_html, s_tw = core()
    sk_html, sk_tw = skill_card()
    tweens = grades() + cw_tw + o_tw + w_tw + c_tw + g_tw + s_tw + ig_tw + sk_tw
    nl = '\n'
    return f'''<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fonts/fonts.css" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.3f}" data-width="1080" data-height="1920">
  <audio id="bga" src="assets/aroll.mp4" data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="2" data-volume="1"></audio>
{nl.join(audio())}
  <div id="stage">
    <video id="bgv" class="full g" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video>
{nl.join(cw_html)}
{nl.join(back)}
    <div id="cutwrap"><video id="cut" class="full g" src="assets/subject.webm" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="1"></video></div>
{nl.join(o_html)}
  </div>
  <div id="dtone" class="fx dudefx"></div><div id="dvig" class="fx dudefx"></div><div id="dgrad" class="fx dudefx"></div>
  <div id="gwarm" class="fx girlfx"></div><div id="gvig" class="fx girlfx"></div><div id="ggrad" class="fx girlfx"></div>
  <div id="ktone" class="fx darkfx"></div><div id="kvig" class="fx darkfx"></div><div id="kgrad" class="fx darkfx"></div>
{nl.join(front)}
{nl.join(c_html)}
{nl.join(g_html)}
{nl.join(s_html)}
{nl.join(sk_html)}
{SAFE_GUIDE if SAFE else ''}
{nl.join(ig_html)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{nl.join(tweens)}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''


# utf-8 on every OS: the page declares charset UTF-8, and Windows would otherwise write cp1252 (broken accents, emoji)
with open('index.html', 'w', encoding='utf-8', newline='\n') as _f:
    _f.write(build())
print(f'wrote index.html {DUR:.3f}s  cuts {[round(c, 3) for c in CUTS]}  claude@{CLAUDE_IN:.3f}  ig@{IG_IN:.3f}')
