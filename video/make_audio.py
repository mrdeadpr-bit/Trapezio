"""Voz (Piper pt-BR via sherpa-onnx), efeitos e timeline.js para a cena 3D.

Vozes: PIPER_DIR/vits-piper-pt_BR-<nome>-medium  (faber, cadu, jeff).
Para usar áudio seu/ElevenLabs: coloque AUDIO_DIR/l<N>.wav (N = índice da fala) e ele substitui a voz sintética.
"""
import json, os, subprocess
import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
PIPER_DIR = os.environ.get("PIPER_DIR", os.path.join(HERE, "models"))
AUDIO_DIR = os.environ.get("AUDIO_DIR", "")
FIT = json.load(open(os.environ["FIT"])) if os.environ.get("FIT") else None   # [[inicio, fim], ...]: encaixa as falas em tempos já renderizados
from episodes import EPISODES
EP = os.environ.get("EP", "esc"); META = EPISODES[EP]; SCRIPT = META["script"]
WORK = os.path.join(HERE, "work", EP); os.makedirs(WORK, exist_ok=True)
SR, FPS, GAP = 44100, 24, 0.22

# who: u = você (boneco), c = Claude (mascote). shot/expressões são lidos pela cena 3D.

import voice
from voice import PARAMS
voice.PIPER_DIR = PIPER_DIR

def voice_line(i, who, text, tone="norm"):
    ext = os.path.join(AUDIO_DIR, f"l{i}.wav") if AUDIO_DIR else ""
    if ext and os.path.exists(ext):                                  # áudio gravado por você substitui a voz sintética
        out = os.path.join(WORK, f"l{i}.wav"); voice.finish(ext, out, who, PARAMS)
        a, _ = sf.read(out, dtype="float32"); return a
    a = voice.synth_line(who, text, tone, PARAMS, WORK)
    sf.write(os.path.join(WORK, f"l{i}.wav"), a, SR); return a

t = META.get('t0', 0.5); lines = []
for i, ln in enumerate(SCRIPT):
    tone = ln.get('tone') or ('mock' if ln.get('last') else ('dry' if ln['who'] == 'c' else 'norm'))
    a = voice_line(i, ln["who"], ln["spoken"], tone)
    if FIT:                                                     # encaixa a fala nos tempos antigos (atempo preserva o tom)
        t = FIT[i][0]; tgt = FIT[i][1] - FIT[i][0]; r = (len(a)/SR) / tgt
        fi_, fo_ = os.path.join(WORK, f"fit{i}_in.wav"), os.path.join(WORK, f"fit{i}_out.wav")
        sf.write(fi_, a, SR); subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", fi_, "-af", f"atempo={r:.5f}", fo_], check=True)
        a, _ = sf.read(fo_, dtype="float32"); a = a[:int(tgt*SR)]
    dur = len(a)/SR
    ln.update(start=round(t, 3), end=round(t+dur, 3)); lines.append(a)
    n = int(dur*FPS)+2; amp = []
    for f in range(n):
        seg = a[int(f/FPS*SR): int((f+1)/FPS*SR)]
        amp.append(round(float(np.sqrt(np.mean(seg**2))) if len(seg) else 0.0, 4))
    ln["amp"] = amp
    if "screen" in ln:
        ln["screen"]["cut"] = ln["start"]; ln["screen"]["seg"] = round(dur+GAP*0.5, 3)
    t += dur + GAP
TOTAL = t + 1.0
N = int(TOTAL*SR)

voice = np.zeros(N, np.float32)
for ln, a in zip(SCRIPT, lines):
    s0 = int(ln["start"]*SR); voice[s0:s0+len(a)] += a

rng = np.random.default_rng(11)
# ambiente de quarto bem baixo
amb = rng.standard_normal(N).astype(np.float32)
k = np.ones(220, np.float32)/220; amb = np.convolve(amb, k, mode="same")*0.9
# cliques de teclado
clicks = np.zeros(N, np.float32)
def click():
    n_ = int(0.035*SR); x = np.diff(rng.standard_normal(n_).astype(np.float32), prepend=0)
    return x*np.exp(-np.arange(n_)/(0.007*SR))*0.30
# whoosh a cada corte de câmera
whoosh = np.zeros(N, np.float32)
def swoosh(dur=0.22):
    n_ = int(dur*SR); x = rng.standard_normal(n_).astype(np.float32)
    x = np.convolve(x, np.ones(18)/18, mode="same")
    env = np.sin(np.linspace(0, np.pi, n_))**2
    return x*env*0.55
for ln in SCRIPT:
    a_ = max(0, int((ln["start"]-0.12)*SR)); w = swoosh(); whoosh[a_:a_+len(w)] += w[:N-a_]
    sc = ln.get("screen")
    if sc:
        for ci in range(int(sc["seg"]*9)):
            ct = sc["cut"]+0.15+ci/9+rng.uniform(-0.02, 0.02); a_ = int(ct*SR)
            if a_ < N-2000: clicks[a_:a_+int(0.035*SR)] += click()*rng.uniform(.6, 1)
        for ev in sc["events"]:
            if ev["kind"] == "banner":
                a_ = int((sc["cut"]+ev["f"]*sc["seg"])*SR)
                n_ = int(0.5*SR); x = np.arange(n_)/SR
                d = (np.sin(2*np.pi*660*x)+np.sin(2*np.pi*990*x)*0.6)*np.exp(-x*7)*0.10
                clicks[a_:a_+n_] += d[:N-a_].astype(np.float32)

# ---------- música de fundo contínua (pad + baixo + teclas, sem bateria) ----------
def synth_music(N):
    bpm = 72; beat = 60/bpm; bar = 4*beat
    chords = [(55.0, [220.0, 261.63, 329.63, 392.0]), (43.65, [174.61, 220.0, 261.63, 329.63]),
              (65.41, [196.0, 261.63, 329.63, 392.0]), (49.0, [196.0, 246.94, 293.66, 392.0])]
    chords = chords[META.get('music', 0):] + chords[:META.get('music', 0)]
    L = np.zeros(N, np.float32); R = np.zeros(N, np.float32)
    def add(buf, sig, t0):
        a_ = max(0, int(t0*SR))
        if a_ >= N: return
        buf[a_:a_+len(sig)] += sig[:N-a_]
    rg = np.random.default_rng(3)
    nbars = int(N/SR/bar)+2
    for b_ in range(nbars):
        root, notes = chords[b_ % 4]; t0 = b_*bar
        dur = bar+0.9; x = np.arange(int(dur*SR))/SR
        env = np.minimum(1, x/0.9)*np.minimum(1, (dur-x)/0.9)
        for i, f in enumerate(notes):
            for d_, pan in ((0.997, 0.7), (1.003, 0.3)):
                w = np.sin(2*np.pi*f*d_*x)+0.45*np.sin(4*np.pi*f*d_*x)+0.2*np.sin(6*np.pi*f*d_*x)
                sig = (w*env*0.022).astype(np.float32)
                add(L, sig*(1-pan)*1.4, t0); add(R, sig*pan*1.4, t0)
        xb = np.arange(int((bar+0.3)*SR))/SR
        eb = np.minimum(1, xb/0.04)*np.exp(-xb*0.35)*np.minimum(1, (bar+0.3-xb)/0.3)
        bass = ((np.sin(2*np.pi*root*xb)+0.35*np.sin(4*np.pi*root*xb))*eb*0.20).astype(np.float32)
        add(L, bass, t0); add(R, bass, t0)
        pat = [0, 2, 1, 3, 2, 1, 3, 2]
        for k, ix in enumerate(pat):
            f = notes[ix]*2*(1 if k % 4 else 1); tk = t0 + k*beat/2 + rg.uniform(-0.012, 0.012)
            xk = np.arange(int(1.1*SR))/SR
            key = ((np.sin(2*np.pi*f*xk)+0.35*np.sin(4*np.pi*f*xk))*np.exp(-xk*3.2)*np.minimum(1, xk/0.004)*0.045).astype(np.float32)
            pan = 0.35 + 0.3*(k % 2)
            add(L, key*(1-pan)*1.6, tk); add(R, key*pan*1.6, tk)
    return L, R
mL, mR = synth_music(N)
tmp = os.path.join(WORK, "music_raw.wav"); sf.write(tmp, np.stack([mL, mR], 1), SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-af", "lowpass=f=3200,aecho=0.8:0.65:70|140:0.22|0.12", os.path.join(WORK, "music.wav")], check=True)
mus, _ = sf.read(os.path.join(WORK, "music.wav"), dtype="float32"); mus = mus[:N]
mus = mus / (np.sqrt(np.mean(mus**2)) + 1e-9) * 0.032
fi, fo = int(0.8*SR), int(1.6*SR); mus[:fi] *= np.linspace(0, 1, fi)[:, None]; mus[-fo:] *= np.linspace(1, 0, fo)[:, None]
env_v = np.convolve(np.abs(voice), np.ones(int(.2*SR))/int(.2*SR), mode="same")
mus *= (1 - 0.30*np.clip(env_v*10, 0, 1))[:, None]
mono = voice*0.9 + amb*0.010 + clicks*0.55 + whoosh*0.07
mix = np.stack([mono, mono], 1) + mus
fd = int(0.8*SR); mix[-fd:] *= np.linspace(1, 0, fd)[:, None]
mix = np.clip(mix/np.abs(mix).max()*0.92, -1, 1)
sf.write(os.path.join(WORK, "mix.wav"), mix, SR)

tl = json.dumps(dict(total=round(TOTAL, 3), fps=FPS, lines=SCRIPT), ensure_ascii=False)
os.makedirs(os.path.join(HERE, "scene"), exist_ok=True)
open(os.path.join(HERE, "scene", EP + ".timeline.js"), "w").write("window.TIMELINE = " + tl + ";")
print("OK", round(TOTAL, 1), "s;", len(SCRIPT), "falas")
