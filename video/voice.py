"""Síntese de fala: Piper (sherpa-onnx) + micropausas na pontuação + timbre/entonação via Praat + acabamento (ffmpeg).
Parâmetros em PARAMS para poder comparar variações medindo a clareza (asr_eval.py)."""
import os, re, subprocess, tempfile
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
PIPER_DIR = os.environ.get("PIPER_DIR", os.path.join(HERE, "models"))
VOICES = {"u": "cadu", "c": "faber"}
SR = 44100

PARAMS = dict(
    speed=1.0,                                                     # velocidade do TTS (<1 = mais devagar)
    pauses={"…": .55, ".": .40, "!": .40, "?": .40, ":": .28, ";": .28, ",": .20},
    comma_min_words=0,                                             # só separa por vírgula se os dois lados tiverem >= N palavras (0 = sempre)
    dry=dict(pm=0.68, rf=0.30, df=1.0, fs=0.90),                   # pm: tom (mediana) | rf: variação de entonação | fs: formantes (<1 = voz maior)
    mock=dict(pm=0.78, rf=1.7, df=1.12, fs=0.90),
    echo=True, comp_ratio=3, phon=False,
)

# grafia fonética só para o TTS (a legenda e o roteiro continuam com o texto original)
PHON = [
    (r"\bV P S\b", "vê pê ésse"), (r"\bChat G P T\b", "chat gê pê tê"), (r"\bCLAUDE ponto M D\b", "claude ponto ême dê"),
    (r"\bSKILL ponto M D\b", "skill ponto ême dê"), (r"\bCowork\b", "cô-uórk"), (r"\bWhatsApp\b", "uótsapi"),
    (r"\bDownloads\b", "daunlôdis"), (r"\bPDFs\b", "pê dê éfes"), (r"\bControl V\b", "contról vê"),
    (r"\bShift Tab\b", "xifti tábi"), (r"\bclaude traço p\b", "claude traço pê"), (r"\bprompt\b", "prômpiti"),
    (r"\blog\b", "lógui"), (r"\bcompact\b", "compáct"), (r"\bAPI\b", "a pê í"), (r"\bban\b", "bã"),
]

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

def speak(who, text, P):
    if P["phon"]:
        for a, b in PHON: text = re.sub(a, b, text)
    tts = get_tts(VOICES[who]); chunks = []; sr = 22050
    for seg, pause in pieces(text, P):
        a = tts.generate(seg, sid=0, speed=P["speed"]); x = np.asarray(a.samples, np.float32); sr = a.sample_rate
        idx = np.where(np.abs(x) > 0.012)[0]
        if len(idx): x = x[max(0, idx[0]-int(.02*sr)): idx[-1]+int(.06*sr)]
        chunks.append(x); chunks.append(np.zeros(int(pause*sr), np.float32))
    if chunks and not np.any(chunks[-1]): chunks = chunks[:-1]
    return np.concatenate(chunks), sr

def shape(x, sr, tone, P):
    if tone == "norm": return x
    import parselmouth
    from parselmouth.praat import call
    q = P[tone]; snd = parselmouth.Sound(x.astype("float64"), sr)
    med = call(snd.to_pitch(), "Get quantile", 0, 0, 0.5, "Hertz")
    out = call(snd, "Change gender", 60, 300, q["fs"], med*q["pm"], q["rf"], q["df"])
    y = np.asarray(out.values[0], np.float32); return y / (np.abs(y).max() + 1e-9) * 0.9

def finish(raw_path, out_path, who, P):
    body = "equalizer=f=95:t=q:w=1.0:g=3.5," if who == "c" else ""
    echo = "aecho=0.8:0.55:35:0.10," if P["echo"] else ""
    af = ("silenceremove=start_periods=1:start_threshold=-45dB,highpass=f=60," + body +
          "equalizer=f=140:t=h:w=120:g=2.5,equalizer=f=3500:t=q:w=1.2:g=1.5,"
          f"acompressor=threshold=-20dB:ratio={P['comp_ratio']}:attack=5:release=80:makeup=2," + echo + "loudnorm=I=-15:TP=-1.5:LRA=7")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw_path, "-af", af, "-ar", str(SR), "-ac", "1", out_path], check=True)

def synth_line(who, text, tone, P=PARAMS, workdir=None):
    """Fala completa já processada (float32, SR=44100)."""
    workdir = workdir or tempfile.mkdtemp()
    x, sr = speak(who, text, P); x = shape(x, sr, tone, P)
    raw, out = os.path.join(workdir, "raw.wav"), os.path.join(workdir, "out.wav")
    sf.write(raw, x, sr); finish(raw, out, who, P)
    a, _ = sf.read(out, dtype="float32"); return a
