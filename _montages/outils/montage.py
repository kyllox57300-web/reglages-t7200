# Moteur de montage « motion design » (textes animés, étiquettes prix, carton de fin)
# utilisé pour la pub Black Friday 2026. Usage : voir black_friday_2026.py
import subprocess, sys, math, json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # dossier _montages
MED = ROOT + '/rushs/2026-11-black-friday/'
A = MED + 'produits-enduit-caisson-peinture-vasque.mov'
B = MED + 'produits-vasque-cadre-caisson.mov'
C = MED + 'facade-nuit-allees-outillage.mov'
W, H, FPS = 1080, 1920, 30
YEL = (250, 182, 31); BLUE = (0, 120, 191); BLACK = (17, 17, 17); WHITE = (255, 255, 255)
BEBAS = ROOT + '/polices/BebasNeue-Regular.ttf'
BARLOW = ROOT + '/polices/BarlowCondensed-ExtraBold.ttf'
NB = ' '
MAXW = 840  # largeur max des textes (zone sûre TikTok)

UP = "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920"
DAY = "eq=contrast=1.12:brightness=0.015:saturation=1.38:gamma=1.04,colorbalance=rs=0.02:bs=-0.03:rm=0.02:bm=-0.02,unsharp=5:5:0.9:5:5:0.0"
NIGHT = "eq=contrast=1.18:brightness=0.03:saturation=1.45:gamma=1.18,colorbalance=bs=0.03,unsharp=5:5:0.7:5:5:0.0"

# ---------- textes ----------
def font(path, size): return ImageFont.truetype(path, size)

def fit(text, path, size, maxw, stroke=0):
    while size > 20:
        f = font(path, size)
        b = f.getbbox(text, stroke_width=stroke)
        if b[2] - b[0] <= maxw: return f
        size -= 4
    return font(path, size)

def shadowed(img, off=10, blur=14, op=150):
    a = img.split()[3]
    sh = Image.new('RGBA', (img.width + 2 * blur + off, img.height + 2 * blur + off), (0, 0, 0, 0))
    m = Image.new('L', sh.size, 0); m.paste(a, (blur + off, blur + off))
    m = m.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: v * op // 255)
    sh.putalpha(m)
    sh.paste(img, (blur, blur), img)
    return sh

def big(text, size, fill=WHITE, stroke=12, sfill=BLACK, path=BEBAS, maxw=MAXW):
    f = fit(text, path, size, maxw, stroke)
    b = f.getbbox(text, stroke_width=stroke)
    im = Image.new('RGBA', (b[2] - b[0] + 4, b[3] - b[1] + 4), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((-b[0] + 2, -b[1] + 2), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)
    return shadowed(im)

def pill(text, size, fg=YEL, bg=BLACK, path=BEBAS, padx=34, pady=20, radius=18, maxw=MAXW, border=None):
    f = fit(text, path, size, maxw - 2 * padx)
    b = f.getbbox(text)
    w, h = b[2] - b[0] + 2 * padx, b[3] - b[1] + 2 * pady
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius, fill=bg, outline=border, width=6 if border else 0)
    d.text((padx - b[0], pady - b[1]), text, font=f, fill=fg)
    return shadowed(im, 8, 12, 120)

def price_tag(price, badge='-50' + NB + '%'):
    f = font(BEBAS, 250)
    b = f.getbbox(price)
    pw, ph = b[2] - b[0], b[3] - b[1]
    w, h = pw + 110, ph + 80
    R = 95
    im = Image.new('RGBA', (w + R, h + R // 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    y0 = R // 2
    d.rounded_rectangle((0, y0, w, y0 + h), 26, fill=YEL, outline=BLACK, width=8)
    d.text((55 - b[0], y0 + 40 - b[1]), price, font=f, fill=BLACK)
    # pastille -50 %
    cx, cy = w - 10, y0 + 6
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=BLACK, outline=YEL, width=6)
    fb = fit(badge, BEBAS, 82, 2 * R - 34)
    bb = fb.getbbox(badge)
    d.text((cx - (bb[2] + bb[0]) / 2, cy - (bb[3] + bb[1]) / 2), badge, font=fb, fill=YEL)
    return shadowed(im, 12, 16, 160)

def panel(w, h, alpha=165):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), 40, fill=(10, 10, 10, alpha))
    return im

# ---------- animations ----------
def ease_out_back(x, k=1.9):
    x = min(max(x, 0), 1); return 1 + (k + 1) * (x - 1) ** 3 + k * (x - 1) ** 2
def ease_out(x):
    x = min(max(x, 0), 1); return 1 - (1 - x) ** 3

def anim(kind, u):
    """retourne (échelle, opacité, dx, dy, rotation)"""
    if kind == 'pop':
        return 0.25 + 0.75 * ease_out_back(u / 0.28), min(u / 0.07, 1), 0, 0, 0
    if kind == 'slam':
        return 1 + 1.3 * (1 - ease_out(u / 0.18)), min(u / 0.05, 1), 0, 0, 0
    if kind == 'up':
        return 1, min(u / 0.12, 1), 0, 90 * (1 - ease_out(u / 0.28)), 0
    if kind == 'left':
        return 1, min(u / 0.1, 1), -700 * (1 - ease_out(u / 0.26)), 0, 0
    if kind == 'right':
        return 1, min(u / 0.1, 1), 700 * (1 - ease_out(u / 0.26)), 0, 0
    if kind == 'tag':
        s = 0.2 + 0.8 * ease_out_back(u / 0.3, 2.4)
        return s, min(u / 0.07, 1), 0, 0, -4 * min(u / 0.3, 1)
    if kind == 'pulse':
        s = 0.25 + 0.75 * ease_out_back(u / 0.28)
        if u > 0.3: s = 1 + 0.045 * abs(math.sin(math.pi * (u - 0.3) * 2))
        return s, min(u / 0.07, 1), 0, 0, 0
    return 1, 1, 0, 0, 0

class El:
    def __init__(self, img, t0, t1, cx, cy, kind='pop'):
        self.img, self.t0, self.t1, self.cx, self.cy, self.kind = img, t0, t1, cx, cy, kind

def draw_el(canvas, e, t):
    if not (e.t0 <= t < e.t1): return
    s, a, dx, dy, rot = anim(e.kind, t - e.t0)
    im = e.img
    if abs(s - 1) > 1e-3:
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BICUBIC)
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    if a < 1:
        al = im.split()[3].point(lambda v: int(v * a)); im = im.copy(); im.putalpha(al)
    canvas.alpha_composite(im, (int(e.cx + dx - im.width / 2), int(e.cy + dy - im.height / 2)))

# ---------- vidéo ----------
def read_seg(src, ss, dur, grade):
    n = int(round(dur * FPS))
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(ss), '-i', src, '-t', str(dur + 0.5),
           '-vf', f'fps={FPS},{UP},{grade}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    frames = []
    last = None
    for i in range(n):
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            frames.append(last); continue
        last = Image.frombuffer('RGB', (W, H), buf); frames.append(last)
    p.stdout.close(); p.kill()
    return frames

def kenburns(fr, z, fx, fy, sx=0, sy=0):
    cw, ch = W / z, H / z
    x0 = min(max(fx * W - cw / 2 + sx, 0), W - cw)
    y0 = min(max(fy * H - ch / 2 + sy, 0), H - ch)
    return fr.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch))

yy, xx = np.mgrid[0:H, 0:W]
VIG = (1 - 0.38 * np.clip(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.72)) ** 2, 0, 1)).astype(np.float32)[..., None]

LOWG = np.clip((yy - H * 0.45) / (H * 0.25), 0, 1).astype(np.float32)[..., None]

def apply_vig(img, dim=0, dimlow=0):
    m = VIG * (1 - dim)
    if dimlow: m = m * (1 - dimlow * LOWG)
    a = np.asarray(img, dtype=np.float32) * m
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))

# ---------- carton de fin ----------
LOGO = Image.open(ROOT + '/logo/brico-cash-fameck.jpg').convert('RGB')

def logo_card(width=780):
    lw = width - 60
    lg = LOGO.resize((lw, int(LOGO.height * lw / LOGO.width)), Image.LANCZOS)
    im = Image.new('RGBA', (width, lg.height + 60), (0, 0, 0, 0))
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), 34, fill=255)
    card = Image.new('RGBA', im.size, WHITE + (255,)); card.putalpha(m)
    card.paste(lg, (30, 30))
    return shadowed(card, 14, 22, 170)

def end_bg(frames, blur=True):
    out = []
    stripes = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(stripes)
    # 3 bandes jaunes en haut à gauche (rappel de la charte)
    for i in range(3):
        o = i * 95
        d.polygon([(-40 + o, 0), (40 + o, 0), (-220 + o, 330), (-300 + o, 330)], fill=YEL + (255,))
    for i in range(3):
        o = i * 95
        d.polygon([(W + 40 - o, H), (W - 40 - o, H), (W + 220 - o, H - 330), (W + 300 - o, H - 330)], fill=YEL + (255,))
    res = []
    for k, fr in enumerate(frames):
        if k % 2 == 0 or not res:
            b = fr.resize((W // 6, H // 6), Image.BILINEAR).filter(ImageFilter.GaussianBlur(5)).resize((W, H), Image.BICUBIC)
            a = np.asarray(b, dtype=np.float32) * 0.42
            a = a * 0.75 + np.array([0, 30, 60], np.float32) * 0.25  # teinte bleu nuit
            img = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')
            img.alpha_composite(stripes)
            cur = img.convert('RGB')
        res.append(cur)
    return res

# ---------- rendu ----------
def render(plan, elements, flashes, shakes, out, total):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                          '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-profile:v', 'high', '-level', '4.2', '-pix_fmt', 'yuv420p',
                          '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
                          '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    t0 = 0.0; fi = 0
    rng = np.random.default_rng(7)
    for seg in plan:
        if seg['src'] == 'END':
            frames = end_bg(read_seg(C, seg['ss'], seg['dur'], DAY))
        else:
            frames = read_seg(seg['src'], seg['ss'], seg['dur'], seg.get('grade', DAY))
        n = len(frames)
        for k, fr in enumerate(frames):
            t = fi / FPS; u = k / max(n - 1, 1)
            if seg['src'] != 'END':
                z = seg['z0'] + (seg['z1'] - seg['z0']) * (u * u * (3 - 2 * u) * 0.35 + u * 0.65)
                lt = k / FPS
                z *= 1 + 0.07 * (1 - ease_out(lt / 0.2))  # petit « punch » à chaque coupe
                sx = sy = 0
                for st, sd in shakes:
                    if st <= t < st + sd:
                        amp = 26 * (1 - (t - st) / sd); sx, sy = rng.uniform(-amp, amp, 2)
                fx = seg['fx'][0] + (seg['fx'][1] - seg['fx'][0]) * u
                fy = seg['fy'][0] + (seg['fy'][1] - seg['fy'][0]) * u
                img = apply_vig(kenburns(fr, z, fx, fy, sx, sy), seg.get('dim', 0), seg.get('dimlow', 0))
            else:
                img = fr
            canvas = img.convert('RGBA')
            for e in elements: draw_el(canvas, e, t)
            for ft in flashes:
                if ft <= t < ft + 0.17:
                    a = int(200 * (1 - (t - ft) / 0.17))
                    canvas.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, a)))
            p.stdin.write(canvas.convert('RGB').tobytes())
            fi += 1
        t0 += seg['dur']
    p.stdin.close(); p.wait()
    print(out, fi, 'images', fi / FPS, 's')
