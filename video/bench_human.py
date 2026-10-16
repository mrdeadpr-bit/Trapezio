"""Compara a síntese atual com a 'humana' (mesma voz e tom): HNR, jitter, shimmer, variação de tom, clareza (Whisper)."""
import os, sys, numpy as np, parselmouth
from parselmouth.praat import call
import voice, asr_eval
voice.PIPER_DIR = os.environ["PIPER_DIR"]
TEXT = {"u": ["Eu preciso ir para a academia, Claude.", "Então como eu começo?", "Nossa, que rápido!", "Eu vou ficar rico!"],
        "c": ["Você fica trancado no quarto achando que vai ficar rico.", "Não tinha muito o que escrever.", "Eu não menti. Eu só falo a verdade.", "Feito."]}
def metrics(a):
    snd = parselmouth.Sound(a.astype("float64"), voice.SR)
    pit = snd.to_pitch(None, 60, 400); f = pit.selected_array["frequency"]; f = f[f > 0]
    hnr = call(snd.to_harmonicity_cc(), "Get mean", 0, 0)
    pp = call(snd, "To PointProcess (periodic, cc)", 60, 400)
    jit = call(pp, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3) * 100
    shi = call([snd, pp], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6) * 100
    sd = float(np.std(12 * np.log2(f / np.median(f)))) if len(f) > 5 else 0
    X = np.abs(np.fft.rfft(a)) ** 2; fr = np.fft.rfftfreq(len(a), 1 / voice.SR); hf = X[fr > 6000].sum() / X.sum() * 100
    return dict(hnr=hnr, jitter=jit, shimmer=shi, f0sd=sd, hf=hf)
for name, human in (("atual", False), ("humana", True)):
    voice.HUMAN = human; res = {}
    for who, txts in TEXT.items():
        for t in txts:
            for k in range(3):
                tone = "dry" if who == "c" else "norm"
                a = voice.synth_line(who, t, tone, voice.PARAMS, "/tmp"); m = metrics(a)
                m["sim"] = asr_eval.sim(t, asr_eval.transcribe(a, voice.SR)); 
                for key, v in m.items(): res.setdefault((who, key), []).append(v)
    print(name)
    for who in "uc": print("  ", who, {k: round(float(np.mean(res[(who, k)])), 2) for k in ("hnr", "jitter", "shimmer", "f0sd", "hf", "sim")})
