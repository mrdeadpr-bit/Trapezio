# Especificação completa da série (versão atual)

Tudo abaixo vem do código real em `video/`. Valores entre parênteses são os do código.

## 0. Como é feito: sem API, tudo local

- **Não uso API de voz nem de vídeo.** Nenhum ElevenLabs, OpenAI TTS ou Creative Claw (ele nunca foi usado nos vídeos entregues).
- **Voz:** modelos neurais **Piper pt-BR** (`faber`, `cadu`; `jeff` só em testes), rodando offline pelo **sherpa-onnx** (Python). Depois eu processo o timbre com **Praat** (`praat-parselmouth`) e acabo com **ffmpeg** e **numpy**.
- **Imagem:** **three.js r160** (`npm i three@0.160.0`) numa página HTML (`scene/desk.html`), renderizada quadro a quadro em **Chromium headless via Playwright** (`render.js`). O ffmpeg junta os quadros JPEG com o áudio.
- **Checagem de fala:** **Whisper-small** offline (sherpa-onnx) transcreve cada tentativa de voz e escolho a melhor.
- **Quem faz tudo:** eu, escrevendo e rodando código na sessão. O "prompt" do fim do arquivo é o que reproduz isso.
- Não dá para eu ouvir o áudio. Só confiro por transcrição, medição de tom e quadros.

### Instalação
`./setup.sh` (npm: three, playwright+chromium; pip: `sherpa-onnx soundfile numpy praat-parselmouth`; modelos em `models/`: `vits-piper-pt_BR-{faber,cadu,jeff}-medium` e `sherpa-onnx-whisper-small`, baixados das releases públicas do sherpa-onnx). Também precisa de ffmpeg.

## 1. Vozes (configuração exata)

### 1.1 Boneco (u) = Piper `cadu`, sem processamento de timbre
- `generate(speed=1.0, sid=0)`, tom "norm" (sem Praat).
- Acabamento (ffmpeg): `silenceremove=start_periods=1:start_threshold=-45dB, highpass=60, equalizer f=140 (high-shelf 120 Hz, +2.5 dB), equalizer f=3500 (q, w=1.2, +1.5 dB), acompressor threshold=-20dB ratio=3 attack=5 release=80 makeup=2, aecho=0.8:0.55:35:0.10, loudnorm I=-15 TP=-1.5 LRA=7`.

### 1.2 Claude (c) = Piper `faber` + Praat (mesma voz do Ep. 4 e do Ep. 7)
- `generate(speed=1.0)`.
- Praat "Change gender" (faixa de tom 60–300 Hz; se falhar tenta 50–500 e 75–600):
  - **seca (padrão):** `pm=0.68` (mediana do tom × 0,68), `rf=0.30` (faixa de entonação × 0,30, achatada), `df=1.0`, `fs=0.90` (formantes × 0,90).
  - **deboche (última fala `last=True`):** `pm=0.78`, `rf=1.7`, `df=1.12`, `fs=0.90`.
  - A mediana do tom vem de `to_pitch` com quantil 0,5. Resultado medido: ~96–100 Hz.
- Acabamento: o mesmo do boneco, mais `equalizer f=95 (q, w=1.0, +3.5 dB)` antes do EQ de 140 Hz.
- Não há diferença de código entre o Ep. 4 e o Ep. 7 (conferido no git). Eu medi: tom ~99 Hz e velocidade ~17 caracteres/s nos dois.

### 1.3 Codex (x) = Piper `cadu` deslocado para voz feminina
- `generate(speed=1.0)`; Praat "fem": `pm=1.85`, `rf=1.15`, `df=1.0`, `fs=1.2` (tom medido ~210–230 Hz).
- Usa o `PARAMS` novo: fonética `PHON` ativa (Codex→"Códex"), vírgula só separa se os dois lados tiverem ≥3 palavras, corte de silêncio com limiar 0,004 e margens 0,06/0,09 s.
- Acabamento (`finish`): `highpass=60, equalizer 140 high-shelf +2.5, equalizer 3500 +1.5, acompressor ratio=2 attack=5 release=80 makeup=2, alimiter limit=0.95`, depois normalização por RMS (alvo 0,16; `tanh`; ×0,95).
- Não é uma voz feminina "nativa": o Piper pt-BR só tem vozes masculinas. Kokoro (`pf_dora`) existia como opção (`X_KOKORO=1`), mas soou com sotaque americano e foi descartada.

### 1.4 Micropausas (iguais para todos)
Pontuação → pausa depois do trecho: `…` 0,55 s; `.` `!` `?` 0,40 s; `:` `;` 0,28 s; `,` 0,20 s. Cada trecho é sintetizado separado e os silêncios são inseridos. Para boneco/Claude toda vírgula vira pausa; no Codex só se os dois lados tiverem ≥3 palavras. Limiar de corte de silêncio de cada trecho: 0,012 (margens 0,02 s e 0,06 s) para boneco/Claude.

### 1.5 Escolha da melhor tentativa (`BEST_OF=10`)
O Piper tem aleatoriedade. Para cada fala gero até 10 tentativas, transcrevo com Whisper-small e pontuo `0,5 × similaridade de caracteres + 0,5 × (1 − WER)`. Paro cedo se ≥0,97. Fico com a melhor. Falas abaixo de ~0,90 eu reescrevo.

### 1.6 Regras de texto para a voz
- **A legenda é exatamente o texto falado.** O helper `T(who, texto, shot, ...)` quebra a legenda sozinho (26 caracteres por linha).
- `say=` troca só a grafia para a voz (termos em inglês): "skill"→"isquil", "MCP"→"ême cê pê", "Esc"→"ésqui".
- "Claude" no começo da fala sai abafado na voz do boneco: coloco no fim ("..., Claude.").
- Evito termos que o TTS lê mal ("gancho", "rm -rf", "Esc"...).

### 1.7 Timing
`t0=0.12 s` antes da primeira fala; intervalo de 0,22 s entre falas; total = fim da última fala + 1 s. A amplitude de cada quadro (24 fps, RMS) controla a boca e o corpo na cena. Trocar só áudio sem re-renderizar: variável `FIT` (JSON com `[início, fim]` por fala; usa `atempo`).

## 2. Mixagem e música (`make_audio.py`)
- **Mono da fala/efeitos:** `voz×0,9 + ambiente×0,010 + cliques×0,55 + whoosh×0,07`.
- **Ambiente:** ruído gaussiano suavizado (média móvel de 220 amostras ×0,9).
- **Teclado:** cada fala com tela tem 9 cliques/s (ruído diferenciado, decaimento 7 ms, ×0,30, aleatório 0,6–1,0); a cada banner um sino (660+990 Hz, decaimento rápido, ×0,10).
- **Whoosh:** ruído filtrado (18 amostras) com envelope sen², 0,22 s, ×0,55, 0,12 s antes de cada fala.
- **Música padrão (a mesma em todos):** 72 BPM, compasso de 4 tempos. Acordes por compasso (raiz grave + 4 notas): Am-ish (55 Hz; 220, 261,63, 329,63, 392), F (43,65; 174,61, 220, 261,63, 329,63), C (65,41; 196, 261,63, 329,63, 392), G (49; 196, 246,94, 293,66, 392); `META.music=0` começa pelo primeiro.
  - Pad: 4 notas × 2 osciladores desafinados (×0,997/×1,003) com 3 harmônicos, amplitude 0,022, ataque/liberação 0,9 s, panorama estéreo.
  - Baixo: seno + 2º harmônico, 0,20, decaimento lento.
  - Teclas: padrão [0,2,1,3,2,1,3,2] em colcheias, uma oitava acima, decaimento 3,2, 0,045.
  - Filtro `lowpass=3200`, `aecho=0.8:0.65:70|140:0.22|0.12`, RMS final 0,032, fade-in 0,8 s, fade-out 1,6 s.
  - Ducking: a música cai 30% quando alguém fala (envelope de 0,2 s).
  - Mix final normalizado para 0,92 de pico, fade-out de 0,8 s.

## 3. Imagem (`scene/desk.html`)

### 3.1 Renderização
- 1080×1920, 24 fps, `WebGLRenderer` sem antialias, pixelRatio 1, sombras PCFSoft, **sem tone mapping**.
- Pós-processamento: `RenderPass → BokehPass → UnrealBloomPass(força por cenário, raio 0,6, limiar 0,85) → OutputPass → FXAA`. Bokeh: foco = distância da câmera ao alvo, `aperture = ap/dist×0,3`, `maxblur 0,011`.
- Câmera `PerspectiveCamera(fov 36 padrão)`, perto 0,1, longe 100.
- **Estabilidade:** posições calculadas uma vez a partir de pontos fixos (`REST`); só há aproximação linear (dolly) dentro de cada fala. Nada de balanço, nada de seguir peças animadas.
- Partículas flutuantes: 56 cubos 0,07 (36 no escritório), emissivos, movimento senoidal lento, desfocados.
- Cor sólida em tudo (`vari=0`): sem ruído nem degradê nos objetos.

### 3.2 Boneco (grupo `user`, posição −1,1/1,5/0,2, rotação −0,38 rad)
- Corpo: torso 0,85×1,45×1,4 moletom `#356f73` (barra `#2a5a5e`, 0,88×0,24×1,42); cordões brancos; capuz; jeans `#20263a`; tênis brancos.
- Cabeça 1,1 cubo, rosto em textura de pixel 16×16 (pele `#f3d3bd`, sombra `#e6b99f`, sobrancelha `#2b1d18`, olheira `#c79fb0`); sem barba.
- **Cabelo:** geometria sólida de uma cor só (`#08080a`, emissivo `#17171c`): casquete, nuca, laterais e franja irregular em 16 colunas.
- Braços: 2 grupos (braço 0,36×1,0×0,36 inclinado 0,45 rad, antebraço 1,0×0,32×0,32, mão como filha do antebraço, para não piscar). Coxas, canelas e braços em planos que não se sobrepõem (evita z-fighting).
- Notebook no colo: base prateada, tela `#0f1017` desenhada em canvas 2048×1536 (terminal ou markdown), dobradiça −0,22 rad.
- **Expressões (`uexp`)**: tired (sobrancelha worry, olhos meio fechados), worry (+suor), panic (sobrancelha alta, olhos arregalados, boca "o", suor), angry, defeat (olhos fechados, boca triste), sly, happy (sorriso + blush), neutral. Boca abre pela amplitude do áudio (0–3 px). Pisca a cada 3,4 s (0,12 s).
- Animação: cabeça sobe/desce 0,012, torso respira 1%, braços digitam (seno de 20 rad/s) quando há tela, pânico treme a cabeça levemente.

### 3.3 Claude (mascote)
- Corpo 1,45×1,35×2,1 laranja `#e8744c` (emissivo 0,2), 4 pernas 0,36×0,7×0,36 `#f08a60`, 2 braços 0,3×0,6×0,3. Rosto 24×16 em pixel: olhos `#17101a` 2×4 (5 se grande), sem boca (só um traço `#c9603a`). Piscada a cada 3,9 s.
- **Expressões (`mexp`)**: neutral; deadpan (pálpebra 2 px); smug (pálpebra 1 px); happy (olhos "^ ^"). Na última fala levanta o braço e acena.
- Quica 0,06 ao falar; pernas se mexem ao falar.

### 3.4 Codex (só quando há `who="x"` ou plano `cuComp`)
- Nuvem lisa: 1 lóbulo central (esfera r1,5 achatada em x×0,52) + 7 lóbulos (r0,92, x×0,46) em anel de raio 1,38; 72×48 segmentos; degradê vertex-color azul `#1f4dff` → violeta `#7b4dff` → lavanda `#f0b8ff` na diagonal; `MeshStandard` rugosidade 0,38, emissivo `#2a2f9a` 0,32.
- `>_` branco (canvas 320×240, traço 34 px, pontas redondas), plano 2,3×1,72, que olha para a câmera e fica na frente da nuvem (distância 2,55 do centro). Luz de ponto roxa `#8a5cff` (3,0).
- Posição (6,0/2,38/0), rotação π+0,72; flutua com seno; fala = quica.

### 3.5 Planos de câmera (`shot`)
- `cuUser(a)`: 4,5→4,0 do rosto, fov 36, a = ±0,3.
- `cuMascot(a)`: 5,8→5,2, a = 0,25–0,3.
- `cuComp`: 14,5→13,5, rotação 0,3 em relação à frente do Codex.
- `screen(a)`: tela do notebook, fov 28, 4,3→3,8, corpo do boneco escondido.
- `three`: (2,9→2,7 / 4,4 / 21→20) olhando (2,9/3,2/0), fov 48. `two`: (1,4→1,2 / 3,8 / 12→11), fov 48.

### 3.6 Legenda e telas
- Legenda DOM: Inter/DejaVu Sans 600, 56 px, branca com sombra, posição 600 px do topo (1330 px nos planos de tela, 150 px nos inserts). Máx. 3 linhas de ~26 caracteres.
- Tela de terminal: barra de título, "✻ Claude Code", histórico, caixa de entrada, banner diagonal colorido (texto ≤ ~18 caracteres, animado) com eventos por fração da fala (`f`). Modo `md`: arquivo com título e linhas em negrito.
- Inserts: celular de WhatsApp (520×980) e diagrama "ecossistema" (SVG).

### 3.7 Cenários (`set`) e iluminação
| set | hora | fundo | luz principal | bloom |
|---|---|---|---|---|
| night | 02h | `#0a0e26`, janela com bokeh de cidade, sofá roxo, luzinhas, estante, abajur | lua `#9fb4ff` 0,9 + lâmpada `#ffb067` 3,2 + preenchimentos | 0,38 |
| office | tarde | `#a9cdf2` (céu azul), mesa branca, monitor, sofá cinza, plantas | sol `#fff1dc` 1,3 | 0,05 |
| kitchen | 06h | `#f2c6a0`, janela de nascer do sol, geladeira, bancada, cafeteira | sol `#ffa860` 1,1 + lâmpada | 0,12 |
| studio | noite | `#120c2a`, neon roxo/azul, monitor com ícones | lua `#a39bff` + pontos rosa e azul | 0,42 |
| quiosque | 17h40 | céu/mar/sol em canvas, areia, palhoça, postes, luzinhas, balcão, palmeiras, prancha, coco | sol `#ff9a58` 1,6 + ponto quente | 0,28 |

## 4. Episódios feitos
Série "divã" (cena `couch`, antiga): chat, madrugada, vps, cowork, ban, link, prompt, sol. Série 2 (cena `desk`): plano, ecossistema, exclamacao, codex, custo, rewind, agentes, memoria, skill, mcp, permissoes, academia.
Dicas já usadas (não repetir): Esc Esc, Shift+Tab/plano, `!`, `claude -p`, `/cost`, `/clear`, `/rewind`, subagentes, CLAUDE.md e `/init`, hooks, skills, MCP, `/permissions`, `--continue`, Ctrl+V.

## 5. Comandos
```
./setup.sh
EP=<ep> PIPER_DIR=models ASR_DIR=models/sherpa-onnx-whisper-small BEST_OF=10 python3 make_audio.py
EP=<ep> SCENE=desk PLAYWRIGHT_PATH=$(npm root)/playwright node render.js 60,150,330   # quadros de teste (vírgula obrigatória)
PLAYWRIGHT_PATH=$(npm root)/playwright ./queue.sh <ep>      # render completo, 4 processos (~20–30 min por episódio)
```

## 6. Prompt para colar

```
Você vai produzir vídeos verticais (1080x1920, 24 fps, 25–35 s) de um boneco "voxel / Minecraft" conversando com o mascote Claude, em humor seco, estilo kadugrowth.
Tudo local, sem APIs: three.js + Chromium/Playwright, Piper pt-BR (sherpa-onnx), Praat, Whisper-small e ffmpeg. Use o repositório video/ (leia ESPECIFICACAO_COMPLETA.md, episodes.py, voice.py, make_audio.py, scene/desk.html, render.js, queue.sh).

PERSONAGENS: o boneco (pele branca, sem barba, moletom verde-azulado, olheiras, cansado) quer enriquecer com um grupo automático de achadinhos no WhatsApp e se enrola. O Claude (mascote laranja de blocos, sem boca, inexpressivo, cínico) o chama pelo nome, nunca de "Doutor". O Codex (nuvem roxa lisa com >_) aparece só quando o tema pedir.

ROTEIRO: 10 a 12 falas curtíssimas, gancho nos 2 primeiros segundos, deboche, callbacks, uma dica NOVA e real do Claude Code por episódio (nunca repita as de ESPECIFICACAO_COMPLETA, seção 4), aplicada a um dilema do cotidiano (academia, dinheiro, sono). Última fala do Claude em tom de deboche e "Segue para mais dicas". Legenda = texto falado (use T() e say=).

ÁUDIO: boneco = Piper cadu sem processamento; Claude = Piper faber com Praat pm 0,68 rf 0,30 fs 0,90 (deboche final pm 0,78 rf 1,7 df 1,12); Codex = cadu com Praat pm 1,85 rf 1,15 fs 1,2; micropausas por pontuação; BEST_OF=10 com Whisper; música sintética padrão e a mesma em todos.

IMAGEM: câmera estável, cores sólidas, bokeh/bloom baixo, cenário e horário diferentes a cada episódio.

PROCESSO: roteiro em episodes.py → make_audio.py → quadros de teste → queue.sh → conferir contact sheet → enviar o MP4, commit e push. Mantenha a sessão ativa durante o render. Não abra PR.
```
