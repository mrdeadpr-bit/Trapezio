"""Mede a clareza da fala: transcreve cada áudio com Whisper (offline) e compara com o roteiro.
uso: python3 asr_eval.py <episodio> [pasta_dos_wavs]   (precisa de ASR_DIR com sherpa-onnx-whisper-small)"""
import os, re, sys, json, difflib, unicodedata
import numpy as np, soundfile as sf, sherpa_onnx

ASR_DIR = os.environ.get("ASR_DIR", "models/sherpa-onnx-whisper-small")
_rec = None
def recognizer():
    global _rec
    if _rec is None:
        _rec = sherpa_onnx.OfflineRecognizer.from_whisper(
            encoder=f"{ASR_DIR}/small-encoder.int8.onnx", decoder=f"{ASR_DIR}/small-decoder.int8.onnx",
            tokens=f"{ASR_DIR}/small-tokens.txt", language="pt", task="transcribe", num_threads=4)
    return _rec

def transcribe(x, sr):
    s = recognizer().create_stream(); s.accept_waveform(sr, np.asarray(x, np.float32)); recognizer().decode_stream(s); return s.result.text.strip()

def _nums(t):
    try:
        from num2words import num2words
        t = re.sub(r"(\d+)[.](\d{3})", r"\1\2", t)
        return re.sub(r"\d+", lambda m: num2words(int(m.group()), lang="pt_BR"), t)
    except Exception: return t

def norm(t):
    t = unicodedata.normalize("NFD", _nums(t).lower()); t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = t.replace("quatorze", "catorze")
    return re.sub(r"[^a-z0-9 ]", " ", t).split()

def wer(ref, hyp):
    r, h = norm(ref), norm(hyp)
    if not r: return 0.0
    d = list(range(len(h)+1))
    for i, rw in enumerate(r, 1):
        prev, d[0] = d[0], i
        for j, hw in enumerate(h, 1):
            cur = min(d[j]+1, d[j-1]+1, prev + (rw != hw)); prev, d[j] = d[j], cur
    return d[-1] / len(r)

def sim(ref, hyp):   # parecença de caracteres sem espaços (tolera "V P S" vs "vps")
    return difflib.SequenceMatcher(None, "".join(norm(ref)), "".join(norm(hyp))).ratio()

if __name__ == "__main__":
    ep = sys.argv[1]; d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "work", ep)
    tl = json.loads(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scene", ep + ".timeline.js")).read()[17:-1])
    tot_w = tot_s = 0
    for i, l in enumerate(tl["lines"]):
        x, sr = sf.read(os.path.join(sys.argv[2] if len(sys.argv) > 2 else d, f"l{i}.wav"), dtype="float32")
        hyp = transcribe(x, sr); w, s = wer(l["spoken"], hyp), sim(l["spoken"], hyp); tot_w += w; tot_s += s
        print(f"{i:2d} {l['who']} WER={w:4.2f} sim={s:4.2f} | {l['spoken'][:46]!r} -> {hyp[:60]!r}")
    n = len(tl["lines"]); print(f"MÉDIA  WER={tot_w/n:.3f}  similaridade={tot_s/n:.3f}")
