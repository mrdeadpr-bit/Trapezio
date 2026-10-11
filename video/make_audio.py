"""Gera voz neural (Kokoro), trilha, cliques de teclado e o timeline.json que a cena 3D consome."""
import json, os, sys, wave
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

HERE = os.path.dirname(os.path.abspath(__file__))
KOKORO_DIR = os.environ.get("KOKORO_DIR", os.path.join(HERE, "models"))
WORK = os.path.join(HERE, "work"); os.makedirs(WORK, exist_ok=True)
SR, FPS, GAP = 24000, 30, 0.40

# who: u = você (voz masculina), c = Claude (voz feminina)
# screen: o que aparece no notebook enquanto o Claude explica; f = fração do trecho de tela (0..1)
SCRIPT = [
 dict(who="u", spoken="Claude, eu uso você só pra conversar. Será que eu tô aproveitando direito?",
      cap="Claude, eu uso você só pra conversar.\nTô aproveitando direito?"),
 dict(who="c", spoken="Nem perto! Primeiro: aperta Shift mais Tab pra alternar entre os modos. Tem até o modo plano, que pensa antes de mexer no código.",
      cap="Shift + Tab alterna os modos.\nTem o modo plano!", badge="Shift + Tab",
      screen=dict(footer=[[0.0, "? for shortcuts"], [0.12, "⏵⏵ accept edits on  (shift+tab to cycle)"], [0.32, "⏸ plan mode on  (shift+tab to cycle)"]],
                  events=[dict(f=0.45, kind="type", f1=0.88, text="refatora a tela de login"),
                          dict(f=0.92, kind="line", text="● Plano: 1) separar form 2) validar", color="#e8a07c")])),
 dict(who="u", spoken="E se eu quiser desfazer o que você fez?", cap="E se eu quiser desfazer\no que você fez?"),
 dict(who="c", spoken="Aperta Esc duas vezes. Eu volto no tempo, e restauro o código também.",
      cap="Esc + Esc\nvolta no tempo!", badge="Esc  Esc",
      screen=dict(hist=[["> refatora a tela de login", "#ffffff"], ["✓ editou login.tsx  (+42 -8)", "#7ee2a8"]],
                  footer=[[0.0, "esc to interrupt"], [0.3, "Esc again to rewind"]],
                  events=[dict(f=0.45, kind="line", text="╭─ Rewind ─────────────────────╮", color="#e8a07c"),
                          dict(f=0.5, kind="line", text="│ ▸ Restaurar código + conversa │", color="#ffffff"),
                          dict(f=0.6, kind="line", text="│   Restaurar só a conversa     │", color="#9a9aa6"),
                          dict(f=0.65, kind="line", text="│   Restaurar só o código       │", color="#9a9aa6"),
                          dict(f=0.7, kind="line", text="╰───────────────────────────────╯", color="#e8a07c")])),
 dict(who="u", spoken="E os comandos?", cap="E os comandos?"),
 dict(who="c", spoken="Digita barra pra ver todos. E o barra init cria o CLAUDE ponto M D, que é a memória do seu projeto.",
      cap="/ lista tudo. /init cria o\nCLAUDE.md, a memória do projeto.", badge="/init",
      screen=dict(footer=[[0.0, "/ for commands"]],
                  events=[dict(f=0.15, kind="type", f1=0.5, text="/init"),
                          dict(f=0.55, kind="line", text="● Analisando o projeto…", color="#e8a07c"),
                          dict(f=0.8, kind="line", text="✓ CLAUDE.md criado", color="#7ee2a8")])),
 dict(who="u", spoken="E o que são skills?", cap="E o que são skills?"),
 dict(who="c", spoken="São pacotes de instruções que eu carrego sozinho quando a tarefa pede. Cria uma pasta, escreve um SKILL ponto M D, e pronto!",
      cap="Skills = pacotes de instruções.\nUma pasta + SKILL.md e pronto!", badge="SKILL.md",
      screen=dict(footer=[[0.0, "? for shortcuts"]],
                  events=[dict(f=0.1, kind="type", f1=0.55, text="cria .claude/skills/revisar/SKILL.md"),
                          dict(f=0.6, kind="line", text="---", color="#9a9aa6"),
                          dict(f=0.68, kind="line", text="name: revisar", color="#e8a07c"),
                          dict(f=0.76, kind="line", text="description: revisa o código antes do PR", color="#e8a07c"),
                          dict(f=0.84, kind="line", text="---", color="#9a9aa6"),
                          dict(f=0.92, kind="line", text="✓ skill criada", color="#7ee2a8")])),
 dict(who="u", spoken="Mais alguma dica?", cap="Mais alguma dica?"),
 dict(who="c", spoken="Barra compact quando a conversa encher. E arroba mais o nome do arquivo, pra me apontar direto o que importa.",
      cap="/compact quando encher.\n@arquivo aponta o que importa.", badge="/compact  @arquivo",
      screen=dict(footer=[[0.0, "contexto: 92%"], [0.45, "contexto: 18%"]],
                  events=[dict(f=0.08, kind="type", f1=0.35, text="/compact"),
                          dict(f=0.4, kind="line", text="✓ conversa resumida", color="#7ee2a8"),
                          dict(f=0.5, kind="type", f1=0.92, text="@src/login.tsx corrige o bug")])),
 dict(who="u", spoken="Valeu! Agora eu sei usar de verdade!", cap="Valeu! Agora eu sei\nusar de verdade!", final_u=True),
 dict(who="c", spoken="Segue pra mais dicas!", cap="Segue pra mais dicas!", final=True),
]
VOICES = {"u": ("pm_alex", 1.0), "c": ("pf_dora", 1.0)}

k = Kokoro(os.path.join(KOKORO_DIR, "kokoro.onnx"), os.path.join(KOKORO_DIR, "voices.bin"))
def tts(who, text):
    v, sp = VOICES[who]
    s, sr = k.create(text, voice=v, speed=sp, lang="pt-br")
    s = np.asarray(s, np.float32)
    if sr != SR:  # reamostra simples
        x = np.linspace(0, len(s)-1, int(len(s)*SR/sr)); s = np.interp(x, np.arange(len(s)), s).astype(np.float32)
    # corta silêncio das pontas e normaliza
    idx = np.where(np.abs(s) > 0.01)[0]
    if len(idx): s = s[max(0, idx[0]-int(.03*SR)): idx[-1]+int(.12*SR)]
    return s / (np.abs(s).max()+1e-6) * 0.85

t = 0.7; lines = []
for i, ln in enumerate(SCRIPT):
    a = tts(ln["who"], ln["spoken"]); dur = len(a)/SR
    ln.update(start=round(t, 3), end=round(t+dur, 3)); lines.append(a)
    # envelope de amplitude por frame (boca)
    n = int(dur*FPS)+2; amp = []
    for f in range(n):
        seg = a[int(f/FPS*SR): int((f+1)/FPS*SR)]
        amp.append(round(float(np.sqrt(np.mean(seg**2))) if len(seg) else 0.0, 4))
    ln["amp"] = amp
    if "screen" in ln:
        cut = min(1.4, 0.32*dur)
        ln["screen"]["cut"] = round(t+cut, 3); ln["screen"]["seg"] = round(dur-cut+GAP*0.6, 3)
    t += dur + GAP
TOTAL = t + 1.2
N = int(TOTAL*SR)

voice = np.zeros(N, np.float32)
for ln, a in zip(SCRIPT, lines):
    s0 = int(ln["start"]*SR); voice[s0:s0+len(a)] += a

# trilha suave
def tone(f, dur, vol):
    x = np.arange(int(dur*SR))/SR
    w = np.sin(2*np.pi*f*x) + 0.25*np.sin(4*np.pi*f*x)
    return (w*np.minimum(1, x/0.01)*np.exp(-x*3.0)*vol).astype(np.float32)
music = np.zeros(N, np.float32)
chords = [[261.6,329.6,392.0],[220.0,261.6,329.6],[174.6,220.0,261.6],[196.0,246.9,293.7]]
tt, kk = 0.0, 0
while tt < TOTAL-0.5:
    ch = chords[int(tt//4.8) % 4]; f = ch[kk % 3]*(2 if kk % 6 >= 3 else 1)
    n_ = tone(f, 0.9, 0.035); a_ = int(tt*SR); b_ = min(N, a_+len(n_)); music[a_:b_] += n_[:b_-a_]
    if kk % 8 == 0:
        n_ = tone(ch[0]/2, 1.6, 0.05); b_ = min(N, a_+len(n_)); music[a_:b_] += n_[:b_-a_]
    tt += 0.30; kk += 1
env = np.convolve(np.abs(voice), np.ones(int(.15*SR))/int(.15*SR), mode="same")
music *= 1 - 0.7*np.clip(env*10, 0, 1)

# cliques de teclado nas frases com tela
rng = np.random.default_rng(7)
clicks = np.zeros(N, np.float32)
def click():
    n_ = int(0.03*SR); x = rng.standard_normal(n_).astype(np.float32)
    x = np.diff(x, prepend=0); return x*np.exp(-np.arange(n_)/(0.006*SR))*0.22
for ln in SCRIPT:
    sc = ln.get("screen")
    if not sc: continue
    for ev in sc["events"]:
        if ev["kind"] != "type": continue
        t0, t1 = sc["cut"]+ev["f"]*sc["seg"], sc["cut"]+ev["f1"]*sc["seg"]
        for ci in range(len(ev["text"])):
            ct = t0 + (t1-t0)*ci/len(ev["text"]) + rng.uniform(-0.01, 0.01)
            c = click(); a_ = int(ct*SR); clicks[a_:a_+len(c)] += c[:N-a_]*rng.uniform(.6, 1)
# "pop" quando o balão muda
pops = np.zeros(N, np.float32)
for ln in SCRIPT:
    n_ = tone(880, 0.10, 0.05); a_ = int((ln["start"]-0.05)*SR); pops[a_:a_+len(n_)] += n_[:N-a_]

mix = voice + music + clicks*1.0 + pops
f_ = int(.8*SR); mix[-f_:] *= np.linspace(1, 0, f_)
mix = np.clip(mix/np.abs(mix).max()*0.92, -1, 1)
sf.write(os.path.join(WORK, "mix.wav"), mix, SR)

tl = json.dumps(dict(total=round(TOTAL, 3), fps=FPS, lines=SCRIPT), ensure_ascii=False)
open(os.path.join(HERE, "scene", "timeline.js"), "w").write("window.TIMELINE = " + tl + ";")
print("OK", round(TOTAL, 1), "s;", len(SCRIPT), "falas")
