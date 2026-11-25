# Voix off de synthèse (Piper, voix française SIWIS, licence CC BY 4.0) calée sur une vidéo,
# puis mixage : version « voix seule » et version « voix + musique » (musique baissée sous la voix).
#
# Usage (depuis _montages/) :
#   python3 outils/voix_off.py SCRIPT.json VIDEO_SANS_MUSIQUE.mp4 MUSIQUE.wav SORTIE_PREFIXE
# SCRIPT.json : {"lignes": [[début_s, "texte"], ...]}  — écrire les mots comme ils se prononcent
#   (« Blak Fraille-dé » pour Black Friday, « Zak » pour ZAC, nombres en toutes lettres).
import json, os, subprocess, sys, tempfile, wave
import numpy as np
from piper import PiperVoice, SynthesisConfig

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELE = ROOT + '/voix/modeles/fr_FR-siwis-medium.onnx'
SR = 22050
GAP = 0.08          # silence minimum entre deux phrases
MAX_TEMPO = 1.3     # accélération maximale (sans changer la hauteur)

def synth(voice, text, scale):
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f: path = f.name
    with wave.open(path, 'wb') as w:
        voice.synthesize_wav(text, w, SynthesisConfig(length_scale=scale, noise_scale=0.6, noise_w_scale=0.7))
    with wave.open(path) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    os.remove(path)
    # retire les silences de début et de fin
    idx = np.where(np.abs(a) > 0.02)[0]
    return a[max(idx[0] - 200, 0): idx[-1] + 800] if len(idx) else a

def tempo(a, t):
    if t <= 1.0001: return a
    p = subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-',
                        '-af', f'atempo={t:.4f}', '-f', 'f32le', '-'], input=a.tobytes(), capture_output=True)
    return np.frombuffer(p.stdout, np.float32)

def piste_voix(lignes, total, out_wav):
    voice = PiperVoice.load(MODELE)
    buf = np.zeros(int((total + 1) * SR), np.float32)
    fin_prec = 0.0
    rapport = []
    for i, (t0, texte) in enumerate(lignes):
        a = synth(voice, texte, 0.86)
        debut = max(t0, fin_prec + GAP)
        limite = lignes[i + 1][0] if i + 1 < len(lignes) else total - 0.3
        dispo = limite - debut - GAP
        d = len(a) / SR
        t = min(max(d / dispo, 1.0), MAX_TEMPO) if dispo > 0 else MAX_TEMPO
        a = tempo(a, t)
        d = len(a) / SR
        i0 = int(debut * SR)
        buf[i0:i0 + len(a)] += a[:len(buf) - i0]
        fin_prec = debut + d
        rapport.append((round(debut, 2), round(fin_prec, 2), round(t, 2), texte))
    buf = buf[:int(total * SR)]
    pcm = (np.clip(buf, -1, 1) * 32767).astype('<i2')
    with wave.open(out_wav, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    return rapport

VOIX_FX = ('aresample=48000,highpass=f=90,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1.2:g=3,'
           'acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=4,aformat=channel_layouts=stereo')

def mixer(video, voix_wav, musique, prefixe):
    # 1) voix seule
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', video, '-i', voix_wav,
                    '-filter_complex', f'[1:a]{VOIX_FX},loudnorm=I=-14:TP=-1.5:LRA=7,aresample=48000,alimiter=limit=0.8:attack=1:release=60:level=false[a]',
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', '-movflags', '+faststart', prefixe + '_voix_sans_musique.mp4'], check=True)
    # 2) voix + musique (la musique baisse quand la voix parle)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', video, '-i', voix_wav, '-i', musique,
                    '-filter_complex',
                    f'[1:a]{VOIX_FX},asplit=2[v][key];'
                    '[2:a]aresample=48000,volume=-9dB[m];'
                    '[m][key]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[md];'
                    '[v][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000,alimiter=limit=0.8:attack=1:release=60:level=false[a]',
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', '-movflags', '+faststart', prefixe + '_voix_et_musique.mp4'], check=True)

if __name__ == '__main__':
    script, video, musique, prefixe = sys.argv[1:5]
    lignes = json.load(open(script))['lignes']
    total = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', video],
                                 capture_output=True, text=True).stdout)
    voix_wav = prefixe + '_voix.wav'
    for deb, fin, t, texte in piste_voix(lignes, total, voix_wav):
        print(f'{deb:5.2f} → {fin:5.2f} s  (x{t})  {texte}')
    mixer(video, voix_wav, musique, prefixe)
    os.remove(voix_wav)
    print('ok', prefixe)
