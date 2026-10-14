"""Síntese de fala: Piper (sherpa-onnx) + micropausas na pontuação + timbre/entonação via Praat + acabamento (ffmpeg).
Parâmetros em PARAMS para poder comparar variações medindo a clareza (asr_eval.py)."""
import os, re, subprocess, tempfile
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
PIPER_DIR = os.environ.get("PIPER_DIR", os.path.join(HERE, "models"))
VOICES = {"u": "cadu", "c": "faber", "x": "jeff"}                  # vozes Piper (boneco usa cadu)
KOKORO_DIR = os.environ.get("KOKORO_DIR", os.path.join(HERE, "models"))
KOKORO = {"u": "pm_santa", "c": "pm_alex", "x": "pf_dora"}           # os três em Kokoro (bem mais natural que o Piper), cada um com um timbre
if os.environ.get("HUMAN_PIPER") == "1": KOKORO.pop("u")                  # HUMAN_PIPER=1 volta a voz antiga do boneco (Piper/cadu)
USE_KOKORO = os.environ.get("USE_KOKORO", "0") == "1"      # Kokoro ficou com timbre "monstro" ao baixar o tom; padrão voltou ao Piper (vozes aprovadas)
SR = 44100

LEGACY = os.environ.get("LEGACY", "1") == "1"                  # voz do Ep. 7 (prompt): boneco = cadu, Claude = faber grave (processamento original); só o Codex (x) usa voz feminina
PARAMS = dict(
    speed=1.04,                                                    # velocidade do TTS (>1 = mais rápido)
    pauses={"…": .55, ".": .40, "!": .40, "?": .40, ":": .28, ";": .28, ",": .20},
    comma_min_words=3,                                             # só separa por vírgula se os dois lados tiverem >= N palavras
    dry=dict(pm=0.78, rf=1.0, df=1.0, fs=1.0),                     # pm: tom (mediana) | rf: variação de entonação (1.0 = natural, sem achatar) | fs: formantes (1.0 = timbre original)
    mock=dict(pm=0.86, rf=1.5, df=1.08, fs=1.0),
    echo=False, comp_ratio=2, phon=True,
    kspeed=1.05, kspeed_mock=0.92,                                 # velocidade do Kokoro (normal / deboche)
    kpitch=dict(u=1.0, c=0.78, x=1.0, c_mock=0.80),                      # razão de tom via Rubber Band (<1 = mais grave); timbre acompanha o tom
)

LPARAMS = dict(PARAMS, speed=1.0, comma_min_words=1, thr=0.012, pad0=0.02, pad1=0.06,
               dry=dict(pm=0.68, rf=0.30, df=1.0, fs=0.90), mock=dict(pm=0.78, rf=1.7, df=1.12, fs=0.90), phon=False)
def use_k(who): return who in KOKORO and (USE_KOKORO or who == "x")

# grafia fonética só para o TTS (a legenda e o roteiro continuam com o texto original)
PHON = [
    (r"\bV P S\b", "vê pê ésse"), (r"\bChat G P T\b", "chat gê pê tê"), (r"\bCLAUDE ponto M D\b", "claude ponto ême dê"),
    (r"\bSKILL ponto M D\b", "skill ponto ême dê"), (r"\bCowork\b", "cô-uórk"), (r"\bWhatsApp\b", "uótsapi"),
    (r"\bDownloads\b", "daunlôdis"), (r"\bPDFs\b", "pê dê éfes"), (r"\bControl V\b", "contról vê"),
    (r"\bShift Tab\b", "xifti tábi"), (r"\bclaude traço p\b", "claude traço pê"), (r"\bprompt\b", "prômpiti"),
    (r"\blog\b", "lógui"), (r"\bcompact\b", "compáct"), (r"\bAPI\b", "a pê í"), (r"\bban\b", "bã"), (r"\bCodex\b", "Códex"),
]

_kok = None
def get_kokoro():
    global _kok
    if _kok is None:
        from kokoro_onnx import Kokoro
        _kok = Kokoro(os.path.join(KOKORO_DIR, "kokoro.onnx"), os.path.join(KOKORO_DIR, "voices.bin"))
    return _kok

def rubber(x, sr, ratio):
    """Muda o tom com Rubber Band (formantes deslocados junto: soa como uma voz realmente mais grave)."""
    d = tempfile.mkdtemp(); a, b = os.path.join(d, "a.wav"), os.path.join(d, "b.wav"); sf.write(a, x, sr)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a, "-af", f"rubberband=pitch={ratio}:formant=shifted:pitchq=quality:transients=smooth", "-ar", str(sr), b], check=True)
    y, _ = sf.read(b, dtype="float32"); return y

_tts = {}
def get_tts(name):
    if name in _tts: return _tts[name]
    import sherpa_onnx
    d = os.path.join(PIPER_DIR, f"vits-piper-pt_BR-{name}-medium")
    cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(
        model=f"{d}/pt_BR-{name}-medium.onnx", tokens=f"{d}/tokens.txt", data_dir=f"{d}/espeak-ng-data"), num_threads=4))
    _tts[name] = sherpa_onnx.OfflineTts(cfg); return _tts[name]

def pieces(text, P):
    """[(trecho, pausa_depois)]: separa em . ! ? … : ; sempre, e em vírgula só se os dois lados forem longos o bastante."""
    text = text.replace("...", "…")
    raw = []
    for m in re.finditer(r"([^.!?…:;,]+)([.!?…:;,]*)", text):
        seg, punct = m.group(1).strip(), m.group(2)
        if seg: raw.append([seg, punct])
    out = []
    for i, (seg, punct) in enumerate(raw):
        if out and out[-1][2] == "," and P["comma_min_words"]:         # decide se a vírgula anterior vira pausa de verdade
            prev = out[-1]
            if len(prev[0].split()) < P["comma_min_words"] or len(seg.split()) < P["comma_min_words"]:
                prev[0] = prev[0] + ", " + seg; prev[2] = punct; continue
        out.append([seg, punct[0] if punct else "", punct[0] if punct else ""])
    res = []
    for seg, p0, punct in out:
        pause = P["pauses"].get(punct, 0.0) if punct else 0.0
        res.append((seg + (p0 if p0 else ""), pause))
    return res

def speak(who, text, P, tone="norm"):
    if P["phon"]:
        for a, b in PHON: text = re.sub(a, b, text)
    uk = use_k(who); chunks = []; sr = 24000 if uk else 22050
    tts = None if uk else get_tts(VOICES[who])
    for seg, pause in pieces(text, P):
        if uk:
            x, sr = get_kokoro().create(seg, voice=KOKORO[who], speed=(P["kspeed_mock"] if tone == "mock" else P["kspeed"]), lang="pt-br"); x = np.asarray(x, np.float32)
            idx = np.where(np.abs(x) > 0.004)[0]
            if len(idx): x = x[max(0, idx[0]-int(.06*sr)): idx[-1]+int(.09*sr)]
            chunks.append(x); chunks.append(np.zeros(int(pause*sr), np.float32)); continue
        a = tts.generate(seg, sid=0, speed=(1.0 if who == "x" else P["speed"])); x = np.asarray(a.samples, np.float32); sr = a.sample_rate
        idx = np.where(np.abs(x) > P.get("thr", 0.004))[0]
        if len(idx): x = x[max(0, idx[0]-int(P.get("pad0", .06)*sr)): idx[-1]+int(P.get("pad1", .09)*sr)]
        chunks.append(x); chunks.append(np.zeros(int(pause*sr), np.float32))
    if chunks and not np.any(chunks[-1]): chunks = chunks[:-1]
    return np.concatenate(chunks), sr

def shape(x, sr, tone, P, who="u"):
    if use_k(who):
        r = P["kpitch"].get(who + "_mock") if tone == "mock" and (who + "_mock") in P["kpitch"] else P["kpitch"][who]
        return rubber(x, sr, r) if abs(r - 1.0) > 0.01 else x
    if tone == "norm": return x
    import parselmouth
    from parselmouth.praat import call
    q = P[tone]; snd = parselmouth.Sound(x.astype("float64"), sr)
    for lo, hi in ((60, 300), (50, 500), (75, 600)):                     # se o Praat não achar o tom, tenta outra faixa
        try:
            med = call(snd.to_pitch(None, lo, hi), "Get quantile", 0, 0, 0.5, "Hertz")
            out = call(snd, "Change gender", lo, hi, q["fs"], med*q["pm"], q["rf"], q["df"])
            y = np.asarray(out.values[0], np.float32); return y / (np.abs(y).max() + 1e-9) * 0.9
        except Exception:
            continue
    r = q["pm"]                                                           # último recurso: baixa o tom por reamostragem
    idx = np.arange(0, len(x) - 1, r); y = np.interp(idx, np.arange(len(x)), x).astype(np.float32)
    return y / (np.abs(y).max() + 1e-9) * 0.9

def finish(raw_path, out_path, who, P):
    body = "equalizer=f=100:t=q:w=1.0:g=1.5," if (who == "c" and not USE_KOKORO) else ""
    echo = "aecho=0.8:0.55:35:0.10," if P["echo"] else ""
    af = ("highpass=f=60," + body + "equalizer=f=140:t=h:w=120:g=2.5,equalizer=f=3500:t=q:w=1.2:g=1.5,"
          f"acompressor=threshold=-20dB:ratio={P['comp_ratio']}:attack=5:release=80:makeup=2," + echo + "alimiter=limit=0.95")
    tmp = out_path + ".tmp.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw_path, "-af", af, "-ar", str(SR), "-ac", "1", tmp], check=True)
    a, _ = sf.read(tmp, dtype="float32"); os.remove(tmp)
    v = a[np.abs(a) > 0.02]; rms = float(np.sqrt(np.mean(v**2))) if len(v) else 0.1       # volume por RMS da parte falada (igual em todas as falas)
    a = np.tanh(a * (0.16 / max(rms, 1e-4)) * 1.0) * 0.95
    sf.write(out_path, a.astype(np.float32), SR)

def finish_legacy(raw, out, who):
    body = "equalizer=f=95:t=q:w=1.0:g=3.5," if who == "c" else ""
    af = ("silenceremove=start_periods=1:start_threshold=-45dB,highpass=f=60," + body + "equalizer=f=140:t=h:w=120:g=2.5,equalizer=f=3500:t=q:w=1.2:g=1.5,"
          "acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2,aecho=0.8:0.55:35:0.10,loudnorm=I=-15:TP=-1.5:LRA=7")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", af, "-ar", str(SR), "-ac", "1", out], check=True)

def synth_line(who, text, tone, P=PARAMS, workdir=None):
    """Fala completa já processada (float32, SR=44100)."""
    workdir = workdir or tempfile.mkdtemp()
    if LEGACY and who in ("u", "c"):                                  # voz do Ep. 7
        x, sr = speak(who, text, LPARAMS, tone); x = shape(x, sr, tone, LPARAMS, who)
        raw, out = os.path.join(workdir, "raw.wav"), os.path.join(workdir, "out.wav")
        sf.write(raw, x, sr); finish_legacy(raw, out, who)
        a, _ = sf.read(out, dtype="float32"); return a
    x, sr = speak(who, text, P, tone); x = shape(x, sr, tone, P, who)
    raw, out = os.path.join(workdir, "raw.wav"), os.path.join(workdir, "out.wav")
    sf.write(raw, x, sr); finish(raw, out, who, P)
    a, _ = sf.read(out, dtype="float32"); return a
