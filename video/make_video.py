import subprocess, wave, os, math, textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(OUT, "work"); os.makedirs(WORK, exist_ok=True)
W, H, FPS = 1080, 1920, 30
SR = 22050

# (quem, texto falado, texto da legenda, destaque opcional)
SCRIPT = [
 ("u", "Claude, eu uso você só pra conversar. Tô aproveitando direito?", "Claude, eu uso você só pra conversar.\nTô aproveitando direito?", None),
 ("c", "Nem perto! Primeiro: aperte Shift Tab pra alternar entre os modos. Tem até o modo plano, que pensa antes de mexer.", "Primeiro: Shift + Tab\nalterna os modos. Tem o modo plano!", "Shift + Tab"),
 ("u", "E se eu quiser desfazer o que você fez?", "E se eu quiser desfazer\no que você fez?", None),
 ("c", "Aperte Esc duas vezes. Eu volto no tempo.", "Esc + Esc\nvolta no tempo!", "Esc  Esc"),
 ("u", "E os comandos?", "E os comandos?", None),
 ("c", "Barra mostra todos. E barra init cria o CLAUDE ponto MD, a memória do seu projeto.", "/  lista tudo.\n/init cria o CLAUDE.md,\na memória do projeto.", "/init"),
 ("u", "E o que são skills?", "E o que são skills?", None),
 ("c", "Pacotes de instruções que eu carrego sozinho quando a tarefa pede. Crie uma pasta, escreva o SKILL ponto MD, e pronto!", "Skills = pacotes de instruções.\nUma pasta + SKILL.md e pronto!", "SKILL.md"),
 ("u", "Mais alguma dica?", "Mais alguma dica?", None),
 ("c", "Barra compact quando a conversa encher. E arroba arquivo pra me apontar direto o arquivo certo.", "/compact quando encher.\n@arquivo aponta o arquivo certo.", "/compact  @arquivo"),
 ("u", "Valeu! Agora eu sei usar!", "Valeu! Agora eu sei usar!", None),
 ("c", "Segue pra mais dicas!", "Segue pra mais dicas!", None),
]
GAP = 0.45
VOICE = {"u": ("mb-br3", 165, 62), "c": ("mb-br1", 150, 38)}

# ---------- 1) voz ----------
def synth(i, who, text):
    v, s, p = VOICE[who]
    path = os.path.join(WORK, f"l{i}.wav")
    subprocess.run(["espeak-ng", "-v", v, "-s", str(s), "-p", str(p), "-w", path, text], check=True)
    # padroniza para 22050 mono
    out = os.path.join(WORK, f"l{i}_n.wav")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",path,"-ar",str(SR),"-ac","1",
                    "-af","highpass=f=90,acompressor=threshold=-18dB:ratio=3,volume=1.6", out], check=True)
    with wave.open(out) as w:
        d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)/32768
    return d

lines = [synth(i, w, t) for i, (w, t, _, _) in enumerate(SCRIPT)]
T0 = 0.6  # silêncio inicial
starts, t = [], T0
for d in lines:
    starts.append(t); t += len(d)/SR + GAP
TOTAL = t + 0.9
N = int(TOTAL*SR)

# ---------- 2) trilha + mix ----------
voice = np.zeros(N, np.float32)
for s, d in zip(starts, lines):
    a = int(s*SR); voice[a:a+len(d)] += d

def tone(f, dur, vol, kind="sine"):
    x = np.arange(int(dur*SR))/SR
    w = np.sin(2*np.pi*f*x) + 0.3*np.sin(4*np.pi*f*x)
    env = np.minimum(1, x/0.01) * np.exp(-x*3.2)
    return (w*env*vol).astype(np.float32)

music = np.zeros(N, np.float32)
chords = [[261.6,329.6,392.0],[220.0,261.6,329.6],[174.6,220.0,261.6],[196.0,246.9,293.7]]
step = 0.30; k = 0; tt = 0.0
while tt < TOTAL-0.5:
    ch = chords[int(tt//4.8) % 4]
    f = ch[k % 3] * (2 if k % 6 >= 3 else 1)
    n = tone(f, 0.9, 0.045)
    a = int(tt*SR); b = min(N, a+len(n)); music[a:b] += n[:b-a]
    if k % 8 == 0:
        n = tone(ch[0]/2, 1.6, 0.07); b = min(N, a+len(n)); music[a:b] += n[:b-a]
    tt += step; k += 1
# ducking: música baixa quando alguém fala
env = np.abs(voice); win = int(0.15*SR)
env = np.convolve(env, np.ones(win)/win, mode="same")
duck = 1 - 0.65*np.clip(env*12, 0, 1)
music *= duck
# "pop" quando o balão aparece
pops = np.zeros(N, np.float32)
for s in starts:
    n = tone(880, 0.12, 0.10); a = int((s-0.08)*SR); pops[a:a+len(n)] += n[:N-a]
mix = voice + music + pops
fade = int(0.8*SR); mix[-fade:] *= np.linspace(1, 0, fade)
mix = np.clip(mix/ max(1e-6, np.abs(mix).max()) * 0.92, -1, 1)
wav_path = os.path.join(WORK, "mix.wav")
with wave.open(wav_path, "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix*32767).astype(np.int16).tobytes())

# envelope de amplitude por frame p/ animar a boca
def amp_at(i, tsec):
    d = lines[i]; a = int((tsec-starts[i])*SR)
    if a < 0 or a >= len(d): return 0.0
    seg = d[a:a+int(SR/FPS)]
    return float(np.sqrt(np.mean(seg**2))) if len(seg) else 0.0

# ---------- 3) desenho ----------
def font(sz, bold=True):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p, sz)
F_CAP, F_NAME, F_HI, F_TITLE = font(44), font(40), font(70), font(64)
INK = (34, 34, 38); BG1 = (253, 246, 236); BG2 = (247, 226, 205); ORANGE = (217, 119, 87)

def bg():
    img = Image.new("RGB", (W, H), BG1); d = ImageDraw.Draw(img)
    for y in range(H):
        t = y/H; d.line([(0,y),(W,y)], fill=tuple(int(BG1[j]*(1-t)+BG2[j]*t) for j in range(3)))
    d.rectangle([0, 1500, W, H], fill=(236, 205, 175))
    d.line([(0,1500),(W,1500)], fill=INK, width=5)
    return img

BASE = bg()

def stick(d, cx, base_y, talk, tt, wave_arm=False):
    # boneco palito
    bob = int(6*math.sin(tt*6)) if talk else 0
    hy = base_y-330+bob
    d.ellipse([cx-60, hy-60, cx+60, hy+60], fill=(255,255,255), outline=INK, width=8)
    # olhos + boca
    d.ellipse([cx-24, hy-14, cx-12, hy-2], fill=INK); d.ellipse([cx+12, hy-14, cx+24, hy-2], fill=INK)
    if talk > 0.02:
        r = int(6+min(16, talk*120)); d.ellipse([cx-r, hy+16, cx+r, hy+16+r*1.2], fill=INK)
    else:
        d.arc([cx-20, hy+6, cx+20, hy+34], 20, 160, fill=INK, width=6)
    d.line([cx, hy+60, cx, base_y-120+bob], fill=INK, width=9)           # corpo
    sh = hy+110
    ang = math.sin(tt*8)*0.5 if wave_arm else 0.1
    d.line([cx, sh, cx-80, sh+90], fill=INK, width=9)
    d.line([cx, sh, cx+90*math.cos(ang), sh+90*math.sin(ang)-60*wave_arm], fill=INK, width=9)
    d.line([cx, base_y-120+bob, cx-60, base_y], fill=INK, width=9)       # pernas
    d.line([cx, base_y-120+bob, cx+60, base_y], fill=INK, width=9)

def mascot(d, cx, base_y, talk, tt, happy=False):
    # mascote laranja estilo pixel, com bracinhos e perninhas
    s = 36; bob = int(8*math.sin(tt*5)) if talk else int(3*math.sin(tt*2))
    x0 = cx - 5*s; y0 = base_y - 11*s + bob
    body = [(1,0,9,5),(0,2,10,4)]  # corpo + braços laterais
    d.rectangle([x0+1*s, y0+0*s, x0+9*s, y0+6*s], fill=ORANGE, outline=INK, width=6)
    d.rectangle([x0-1*s, y0+2*s, x0+1*s, y0+4*s], fill=ORANGE, outline=INK, width=6)
    d.rectangle([x0+9*s, y0+2*s, x0+11*s, y0+4*s], fill=ORANGE, outline=INK, width=6)
    for lx in (2, 4, 6, 8):
        d.rectangle([x0+lx*s, y0+6*s, x0+(lx+0.6)*s, y0+8.6*s], fill=ORANGE, outline=INK, width=5)
    # olhos
    ey = y0+2*s
    if happy:
        d.arc([x0+2.5*s, ey-6, x0+3.7*s, ey+14], 200, 340, fill=INK, width=7)
        d.arc([x0+6.3*s, ey-6, x0+7.5*s, ey+14], 200, 340, fill=INK, width=7)
    else:
        d.rectangle([x0+3*s, ey, x0+3.6*s, ey+1.2*s], fill=INK)
        d.rectangle([x0+6.4*s, ey, x0+7*s, ey+1.2*s], fill=INK)
    if talk > 0.02:
        r = int(8+min(20, talk*150))
        d.ellipse([x0+5*s-r, y0+4.2*s, x0+5*s+r, y0+4.2*s+r*1.1], fill=INK)
    else:
        d.line([x0+4.3*s, y0+4.5*s, x0+5.7*s, y0+4.5*s], fill=INK, width=6)

def center_text(d, text, f, cx, y, fill=INK, spacing=14):
    bb = d.multiline_textbbox((0,0), text, font=f, spacing=spacing, align="center")
    d.multiline_text((cx-(bb[2]-bb[0])/2, y), text, font=f, fill=fill, spacing=spacing, align="center")
    return bb[3]-bb[1]

def bubble(d, who, text, scale):
    box_w, pad = 980, 44
    f = F_CAP
    bb = d.multiline_textbbox((0,0), text, font=f, spacing=14, align="center")
    th = bb[3]-bb[1]; bh = th+2*pad
    bx0, by0 = (W-box_w)//2, 520
    hh = int(bh*scale); cy = by0 + bh/2
    x0,x1,y0,y1 = bx0, bx0+box_w, cy-hh/2, cy+hh/2
    fillc = (255,255,255) if who=="u" else (255,236,222)
    d.rounded_rectangle([x0,y0,x1,y1], radius=44, fill=fillc, outline=INK, width=7)
    tail_x = 300 if who=="u" else 780
    d.polygon([(tail_x-30,y1-3),(tail_x+30,y1-3),(tail_x+(-10 if who=="u" else 10),y1+70)], fill=fillc, outline=INK)
    d.line([(tail_x-26,y1-1),(tail_x+26,y1-1)], fill=fillc, width=9)
    if scale > 0.9:
        d.multiline_text((x0+(box_w-(bb[2]-bb[0]))/2, y0+pad-bb[1]), text, font=f, fill=INK, spacing=14, align="center")

def key_card(d, text, prog):
    if not text: return
    s = min(1, prog*4)
    bb = d.textbbox((0,0), text, font=F_HI)
    w = (bb[2]-bb[0])+110; h = 130
    cx, cy = W//2, 1000
    w2, h2 = w*s, h*s
    d.rounded_rectangle([cx-w2/2, cy-h2/2+8, cx+w2/2, cy+h2/2+8], radius=26, fill=INK)
    d.rounded_rectangle([cx-w2/2, cy-h2/2, cx+w2/2, cy+h2/2], radius=26, fill=(255,255,255), outline=INK, width=7)
    if s > .95: d.text((cx-(bb[2]-bb[0])/2, cy-(bb[3]-bb[1])/2-bb[1]), text, font=F_HI, fill=ORANGE)

# ---------- 4) renderiza frames ----------
frames_dir = os.path.join(WORK, "frames")
os.makedirs(frames_dir, exist_ok=True)
for f in os.listdir(frames_dir): os.remove(os.path.join(frames_dir, f))
nf = int(TOTAL*FPS)
ends = [s+len(d)/SR for s, d in zip(starts, lines)]
for fi in range(nf):
    ts = fi/FPS
    img = BASE.copy(); d = ImageDraw.Draw(img)
    # título
    center_text(d, "Claude Code na prática", F_TITLE, W//2, 150, fill=INK)
    d.rounded_rectangle([W//2-150, 240, W//2+150, 252], radius=6, fill=ORANGE)
    cur = None
    for i in range(len(SCRIPT)):
        if starts[i]-0.08 <= ts < ends[i]+GAP*0.8: cur = i
    ut = ct = 0.0
    if cur is not None:
        a = amp_at(cur, ts)
        if SCRIPT[cur][0] == "u": ut = a
        else: ct = a
    last = ts > ends[-1]
    stick(d, 270, 1480, ut, ts, wave_arm=(cur is not None and SCRIPT[cur][0]=="u" and ut>0.02) or last)
    mascot(d, 790, 1480, ct, ts, happy=last)
    d.text((270-d.textlength("VOCÊ", font=F_NAME)/2, 1530), "VOCÊ", font=F_NAME, fill=INK)
    d.text((800-d.textlength("CLAUDE", font=F_NAME)/2, 1530), "CLAUDE", font=F_NAME, fill=INK)
    if cur is not None:
        who, _, cap, hi = SCRIPT[cur]
        prog = (ts-(starts[cur]-0.08))
        bubble(d, who, cap, min(1, 0.6+prog*5))
        if hi and who == "c": key_card(d, hi, prog)
    # barra de progresso
    d.rectangle([0, H-14, int(W*ts/TOTAL), H], fill=ORANGE)
    img.save(os.path.join(frames_dir, f"f{fi:05d}.png"))

# ---------- 5) monta mp4 ----------
out = os.path.join(OUT, "claude_code_dicas.mp4")
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",os.path.join(frames_dir,"f%05d.png"),
                "-i",wav_path,"-c:v","libx264","-pix_fmt","yuv420p","-crf","18","-c:a","aac","-b:a","160k",
                "-shortest","-movflags","+faststart", out], check=True)
print("OK", out, f"{TOTAL:.1f}s")
