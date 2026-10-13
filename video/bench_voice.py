"""Compara variações do pipeline de voz: clareza (Whisper) e variação de tom (naturalidade).  uso: python3 bench_voice.py"""
import copy, json, os, sys, time
import numpy as np, soundfile as sf
import voice, asr_eval
from episodes import EPISODES

def f0var(x, sr):
    hop = int(0.03*sr); win = int(0.06*sr); f = []
    for i in range(0, len(x)-win, hop):
        s = x[i:i+win]
        if np.sqrt(np.mean(s**2)) < 0.02: continue
        s = s - s.mean(); ac = np.correlate(s, s, "full")[len(s)-1:]; lo, hi = int(sr/300), int(sr/60)
        k = lo + np.argmax(ac[lo:hi])
        if ac[k] > 0.4*ac[0]: f.append(sr/k)
    f = np.array(f); return (float(np.median(f)), float(np.std(np.log(f))*100)) if len(f) > 5 else (0, 0)

# amostra: falas do Claude (seco) e do boneco de vários episódios
LINES = []
for ep in ["chat", "madrugada", "vps", "cowork", "ban", "link", "prompt", "sol"]:
    sc = EPISODES[ep]["script"]; cs = [l for l in sc if l["who"] == "c" and not l.get("last")][:3]; us = [l for l in sc if l["who"] == "u"][:1]
    for l in cs + us: LINES.append((l["who"], l["spoken"], "dry" if l["who"] == "c" else "norm"))
    last = [l for l in sc if l.get("last")]
    if last and ep in ("chat", "vps"): LINES.append(("c", last[0]["spoken"], "mock"))

VARIANTS = {
 "A_atual":   dict(),
 "B_limpo":   dict(echo=False, comma_min_words=3, phon=True, dry=dict(pm=0.68, rf=0.55, df=1.0, fs=0.94), mock=dict(pm=0.78, rf=1.7, df=1.12, fs=0.94)),
 "C_B_lento": dict(echo=False, comma_min_words=3, phon=True, speed=0.93, dry=dict(pm=0.68, rf=0.55, df=1.0, fs=0.94), mock=dict(pm=0.78, rf=1.7, df=1.12, fs=0.94)),
 "D_natural": dict(echo=False, comma_min_words=3, phon=True, speed=0.95, comp_ratio=2, dry=dict(pm=0.70, rf=0.75, df=1.0, fs=0.95), mock=dict(pm=0.80, rf=1.7, df=1.12, fs=0.95)),
}
only = sys.argv[1:] or list(VARIANTS)
res = {}
for name in only:
    P = copy.deepcopy(voice.PARAMS); P.update(VARIANTS[name]); t0 = time.time()
    W, S, V, M = [], [], [], []
    for who, text, tone in LINES:
        a = voice.synth_line(who, text, tone, P)
        hyp = asr_eval.transcribe(a, voice.SR); W.append(asr_eval.wer(text, hyp)); S.append(asr_eval.sim(text, hyp))
        med, var = f0var(a, voice.SR)
        if tone == "dry": V.append(var); M.append(med)
    res[name] = dict(WER=round(float(np.mean(W)), 3), sim=round(float(np.mean(S)), 3), c_var_pct=round(float(np.mean(V)), 1), c_tom_hz=round(float(np.mean(M))), seg=round(time.time()-t0))
    print(name, res[name], flush=True)
json.dump(res, open("/tmp/bench_voice.json", "w"))
