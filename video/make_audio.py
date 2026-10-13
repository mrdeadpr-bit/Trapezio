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
WORK = os.path.join(HERE, "work"); os.makedirs(WORK, exist_ok=True)
SR, FPS, GAP = 44100, 24, 0.22

# who: u = você (boneco), c = Claude (mascote). shot/expressões são lidos pela cena 3D.
SCRIPT = [
 dict(who="u", spoken="Claude... você apagou o arquivo errado.", cap="Claude... você apagou\no arquivo errado.",
      shot=dict(name="cuUser", a=0.3), uexp="worry", mexp="neutral"),
 dict(who="c", spoken="Eu sei.", cap="Eu sei.",
      shot=dict(name="cuMascot", a=0.35), uexp="worry", mexp="deadpan"),
 dict(who="u", spoken="Eu sei?! E agora?!", cap="Eu sei?! E agora?!",
      shot=dict(name="cuUser", a=-0.3), uexp="panic", mexp="deadpan"),
 dict(who="c", spoken="Calma. Aperta Esc, Esc.", cap="Calma. Aperta Esc, Esc.",
      shot=dict(name="cuMascot", a=0.5), uexp="panic", mexp="neutral"),
 dict(who="u", spoken="Esc, Esc? E o que isso faz?", cap="Esc, Esc?\nE o que isso faz?",
      shot=dict(name="two"), uexp="worry", mexp="neutral"),
 dict(who="c", spoken="Volta no tempo. O código e a conversa.", cap="Volta no tempo.\nO código e a conversa.",
      shot=dict(name="screen", a=0.35), uexp="worry", mexp="neutral",
      screen=dict(hist=[["> apaga os testes antigos", "#ffffff"], ["● Removendo src/login.tsx…", "#ff7b72"]],
                  footer=[[0.0, "esc to interrupt"], [0.2, "esc again to rewind"]],
                  events=[dict(f=0.22, kind="line", text="⎋  ⎋   rewind", color="#e8a07c"),
                          dict(f=0.45, kind="line", text="▸ Restaurar código + conversa", color="#ffffff"),
                          dict(f=0.55, kind="banner", text="✓ código restaurado", color="#19b46b")])),
 dict(who="u", spoken="E por que você nunca me contou isso?!", cap="E por que você nunca\nme contou isso?!",
      shot=dict(name="cuUser", a=0.3), uexp="angry", mexp="neutral"),
 dict(who="c", spoken="Você nunca perguntou.", cap="Você nunca perguntou.",
      shot=dict(name="cuMascot", a=0.3), uexp="angry", mexp="smug"),
 dict(who="u", spoken="E pra você parar de mexer sem pedir?", cap="E pra você parar de\nmexer sem pedir?",
      shot=dict(name="cuUser", a=-0.25), uexp="sly", mexp="smug"),
 dict(who="c", spoken="Shift Tab. Modo plano. Eu só opino.", cap="Shift + Tab. Modo plano.\nEu só opino.",
      shot=dict(name="screen", a=-0.35), uexp="sly", mexp="neutral",
      screen=dict(hist=[["> refatora o login", "#ffffff"]],
                  footer=[[0.0, "? for shortcuts"], [0.12, "⏵⏵ accept edits on"], [0.3, "⏸ plan mode on"]],
                  events=[dict(f=0.34, kind="line", text="● Plano (só leitura):", color="#e8a07c"),
                          dict(f=0.45, kind="line", text="  1. ler login.tsx", color="#ffffff"),
                          dict(f=0.55, kind="line", text="  2. propor mudanças", color="#ffffff"),
                          dict(f=0.65, kind="banner", text="⏸ modo plano", color="#7c4dff")])),
 dict(who="u", spoken="Então anota aí: nunca mais apague nada sem me avisar.", cap="Então anota aí: nunca mais\napague nada sem me avisar.",
      shot=dict(name="cuUser", a=0.3), uexp="angry", mexp="neutral"),
 dict(who="c", spoken="Isso eu vou fingir que não ouvi.", cap="Isso eu vou fingir\nque não ouvi.",
      shot=dict(name="cuMascot", a=0.2), uexp="angry", mexp="deadpan"),
 dict(who="c", spoken="Salva esse vídeo. Seu código agradece.", cap="Salva esse vídeo.\nSeu código agradece.",
      shot=dict(name="wide"), uexp="happy", mexp="happy", last=True),
]
VOICES = {"u": "cadu", "c": "faber"}

_tts = {}
def get_tts(name):
    if name in _tts: return _tts[name]
    import sherpa_onnx
    d = os.path.join(PIPER_DIR, f"vits-piper-pt_BR-{name}-medium")
    cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(
        model=f"{d}/pt_BR-{name}-medium.onnx", tokens=f"{d}/tokens.txt", data_dir=f"{d}/espeak-ng-data"), num_threads=4))
    _tts[name] = sherpa_onnx.OfflineTts(cfg); return _tts[name]

def voice_line(i, who, text):
    raw = os.path.join(WORK, f"l{i}_raw.wav")
    ext = os.path.join(AUDIO_DIR, f"l{i}.wav") if AUDIO_DIR else ""
    if ext and os.path.exists(ext):
        raw = ext
    else:
        a = get_tts(VOICES[who]).generate(text, sid=0, speed=1.0)
        sf.write(raw, np.asarray(a.samples, np.float32), a.sample_rate)
    out = os.path.join(WORK, f"l{i}.wav")
    af = ("silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=1:stop_threshold=-45dB:stop_duration=0.25,"
          "highpass=f=70,equalizer=f=140:t=h:w=120:g=2.5,equalizer=f=3500:t=q:w=1.2:g=1.5,"
          "acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2,aecho=0.8:0.55:35:0.10,"
          "loudnorm=I=-15:TP=-1.5:LRA=7")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", af, "-ar", str(SR), "-ac", "1", out], check=True)
    a, _ = sf.read(out, dtype="float32")
    return a

t = 0.5; lines = []
for i, ln in enumerate(SCRIPT):
    a = voice_line(i, ln["who"], ln["spoken"]); dur = len(a)/SR
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
open(os.path.join(HERE, "scene", "timeline.js"), "w").write("window.TIMELINE = " + tl + ";")
print("OK", round(TOTAL, 1), "s;", len(SCRIPT), "falas")
