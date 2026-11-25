# Musique originale générée (120 BPM), libre de droits : composée ici, aucun échantillon externe.
import sys, json, numpy as np, wave

SR = 48000
BPM = 120; BEAT = 60 / BPM
rng = np.random.default_rng(3)

def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d)

def kick():
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t / 0.04)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env(n, 0.002, 0.16) * 1.0 + 0.3 * np.tanh(4 * np.sin(ph)) * env(n, 0.001, 0.03)

def lp(x, a):  # filtre passe-bas un pôle
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc += a * (v - acc); y[i] = acc
    return y

def hp(x, a): return x - lp(x, a)

def clap():
    n = int(0.3 * SR); nz = rng.standard_normal(n)
    nz = hp(nz, 0.25)
    e = env(n, 0.001, 0.08)
    for k in (0.011, 0.022):
        i = int(k * SR); e[i:] += 0.6 * env(n - i, 0.001, 0.01)
    return nz * e * 0.45

def hat(open_=False):
    n = int((0.25 if open_ else 0.06) * SR)
    return hp(rng.standard_normal(n), 0.6) * env(n, 0.0005, 0.08 if open_ else 0.015) * 0.22

def saw(freq, n, detune=(0, -7, 7)):
    t = np.arange(n) / SR; out = np.zeros(n)
    for c in detune:
        f = freq * 2 ** (c / 1200)
        out += 2 * ((t * f) % 1) - 1
    return out / len(detune)

def note(m): return 440 * 2 ** ((m - 69) / 12)

def impact():
    n = int(1.2 * SR); t = np.arange(n) / SR
    f = 30 + 70 * np.exp(-t / 0.08)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.45)
    nz = lp(rng.standard_normal(n), 0.08) * env(n, 0.001, 0.25)
    return (boom + 0.6 * nz) * 0.9

def riser(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n)
    out = np.zeros(n); acc = 0.0
    a = 0.01 + 0.5 * (t / dur) ** 2
    for i in range(n):
        acc += a[i] * (x[i] - acc); out[i] = acc
    return out * (t / dur) ** 1.5 * 0.5

def make(total, hits, end_t, out):
    n = int((total + 0.6) * SR)
    drums = np.zeros(n); bass = np.zeros(n); pad = np.zeros(n); fx = np.zeros(n)
    K, CL, HC, HO = kick(), clap(), hat(), hat(True)
    def add(buf, s, t):
        i = int(t * SR); j = min(n, i + len(s))
        if i < n: buf[i:j] += s[:j - i]
    prog = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [55, 60, 64]), (55, [55, 59, 62])]  # Lam  Fa  Do  Sol
    nbeats = int(total / BEAT) + 1
    end_b = int(round(end_t / BEAT))
    for b in range(nbeats):
        t = b * BEAT
        last = b >= end_b + 4
        if b < end_b or b == end_b:
            add(drums, K, t)
        elif not last and b % 1 == 0 and b < end_b + 6:
            add(drums, K * 0.8, t)
        if b < end_b:
            if b % 2 == 1: add(drums, CL, t)
            add(drums, HC, t); add(drums, HO, t + BEAT / 2)
            add(drums, HC * 0.6, t + BEAT * 0.75)
        bar = (b // 4) % 4
        root, ch = prog[bar]
        if b < end_b + 6:
            for half in (0.5,):  # basse sur le contretemps (style house)
                nn = int(BEAT * 0.45 * SR)
                s = lp(saw(note(root - 12), nn, (0, 5)), 0.08) * env(nn, 0.004, 0.12) * 0.55
                add(bass, s, t + BEAT * half)
        if b % 4 == 0 and b < end_b + 6:
            nn = int(4 * BEAT * SR)
            chord = sum(saw(note(m), nn) for m in ch) / 3
            chord = lp(chord, 0.05) * np.minimum(np.arange(nn) / (0.05 * SR), 1) * np.exp(-np.arange(nn) / SR / 1.6)
            add(pad, chord * 0.22, t)
    # pompe (sidechain) sur la basse et le pad
    pump = np.ones(n)
    for b in range(nbeats):
        i = int(b * BEAT * SR); m = int(0.25 * SR)
        if i < n:
            j = min(n, i + m); pump[i:j] = np.minimum(pump[i:j], 0.35 + 0.65 * (np.arange(j - i) / m) ** 0.7)
    for t in hits: add(fx, impact() * 0.8, t)
    add(fx, riser(2 * BEAT), max(end_t - 2 * BEAT, 0))
    add(fx, impact(), end_t)
    mix = drums * 0.9 + (bass + pad) * pump + fx * 0.7
    fade = int(0.6 * SR)
    mix[int(total * SR) - fade:int(total * SR)] *= np.linspace(1, 0, fade)
    mix[int(total * SR):] = 0
    mix = np.tanh(mix * 1.4) / np.tanh(1.4)
    mix = mix[:int(total * SR)]
    st = np.stack([mix, mix], 1)
    pcm = (st / max(np.abs(st).max(), 1e-6) * 0.89 * 32767).astype('<i2')
    with wave.open(out, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

# Usage :
#   python3 outils/musique.py DUREE_S DEBUT_CARTON_FIN_S sortie.wav   (ex. : 24.5 19.5 musique.wav)
#   python3 outils/musique.py fichier.json sortie.wav                 (json : total, end, hits)
if __name__ == '__main__':
    if sys.argv[1].endswith('.json'):
        meta = json.load(open(sys.argv[1])); out = sys.argv[2]
    else:
        meta = {'total': float(sys.argv[1]), 'end': float(sys.argv[2]), 'hits': [0.0]}; out = sys.argv[3]
    make(meta['total'], meta['hits'], meta['end'], out)
