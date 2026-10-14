# Prompt para reproduzir a série no Claude Desktop

## Requisitos (nenhum plugin/skill é obrigatório)

Tudo roda com código local. O que o Claude Desktop precisa ter:

- **Claude Code no Desktop** (aba Code) ou **Cowork**, com acesso a shell e a uma pasta de trabalho. É o que permite rodar comandos, renderizar e salvar o MP4.
- Programas no computador: Node 20+, Python 3.10+, ffmpeg, Chromium (vem com o Playwright).
- Pacotes: `npm i three@0.160.0 playwright`; `pip install sherpa-onnx soundfile numpy praat-parselmouth`.
- Modelos de voz (download único): Piper pt-BR `faber`, `cadu`, `jeff` (medium, formato sherpa-onnx `vits-piper-pt_BR-*`) e Whisper-small do sherpa-onnx (só para checar a clareza da fala).
- Repositório: `mrdeadpr-bit/trapezio`, pasta `video/`, branch `claude/amazing-volta-bnn5yd`. Já contém cena, vozes, roteiros e scripts de render.

Não precisa de: Creative Claw, ElevenLabs, nem skills de vídeo/imagem. O Creative Claw falhou ao conectar nesta sessão e gasta créditos. Só use com a sua autorização.
Skills úteis, mas opcionais: nenhuma. Os roteiros ficam em `episodes.py`.

## Prompt

```
Você vai produzir vídeos verticais de Instagram (1080x1920, 24 fps, 25 a 40 s) em 3D "voxel / Minecraft" com humor seco.
Faça tudo sozinho: roteiro, voz, música, animação, legenda, render e edição. Repositório: video/ (leia episodes.py, voice.py, make_audio.py, scene/desk.html, render.js, queue.sh).

PERSONAGENS
- Humano: pele branca, sem barba, moletom verde-azulado escuro, olheiras, cansado. Quer só um grupo automático de "achadinhos" no WhatsApp e se enrolou: tokens, madrugadas, chats gigantes, VPS, assinaturas, sem receita.
- Claude: mascote laranja em blocos, sem boca, inexpressivo, cínico, voz grave e seca. Nunca é "Doutor". Chama-se "Claude".
- Concorrente (opcional): Codex, nuvem roxa lisa com ">_" branco (não quadriculada), voz feminina delicada sem sotaque. Mostre onde ele falha e onde é melhor que o Claude.

ESTILO (referência: vídeos do kadugrowth)
- Falas curtíssimas, deboche e cinismo, callbacks entre episódios.
- Gancho nos 2 primeiros segundos.
- Dicas REAIS do Claude Code/Cowork ditas de passagem (Esc Esc, /rewind, /cost, /clear, CLAUDE.md e /init, hooks, subagentes, Shift+Tab, claude -p).
- Fala final do Claude em tom de deboche e "Segue para mais dicas".
- Um episódio deve ter a frase "era pra ser só um grupo de achadinhos do WhatsApp, virou um ecossistema".
- Cada episódio tem cenário e horário diferentes: noite, cozinha de manhã, escritório, estúdio, quiosque ao pôr do sol.
- Mostre close do notebook com terminal ou markdown sendo digitado.

IMAGEM
- Câmera estável. Só dolly linear, sem tremor, e nunca dirigida por nó animado. Posições de repouso fixas.
- Cores sólidas, sem degradê nos itens. O cabelo é de uma cor só.
- Efeitos: Bokeh, Bloom e FXAA, com bloom baixo.
- Legenda no máximo 3 linhas de ~26 caracteres.
- A LEGENDA É EXATAMENTE O TEXTO FALADO (use o helper T() de episodes.py). Só troque a grafia para a voz em termos em inglês, com `say=`.

ÁUDIO
- Voz do humano = Piper "cadu" sem processamento. Voz do Claude = Piper "faber" com Praat (pm .68, rf .30, fs .90) e cadeia ffmpeg original do Ep. 7. Deboche final com pm .78, rf 1.7, df 1.12.
- Codex = "cadu" com Praat fem (pm 1.85, rf 1.15, fs 1.2).
- Micropausas na pontuação: "…" .55; ". ! ?" .40; ": ;" .28; "," .20.
- Sem loudnorm. Normalize por RMS. Escolha o melhor de N takes por transcrição com Whisper (BEST_OF=10) e reescreva falas que o TTS lê mal.
- Música: o mesmo pad sintético contínuo em todos os episódios, mais teclado, whoosh e ambiente.

PROCESSO
1. Escreva o roteiro em episodes.py (use T e sh).
2. `EP=<ep> PIPER_DIR=... ASR_DIR=... BEST_OF=10 python3 make_audio.py` (gera work/<ep>/mix.wav e scene/<ep>.timeline.js).
3. Confira 2 a 3 quadros com `node render.js f1,f2,f3` (precisa de vírgula na lista).
4. `./queue.sh <ep>...` (4 processos de render, ~0,5 fps). Monte uma contact sheet com ffmpeg tile e confira legenda, tela e cenário.
5. Envie cada MP4 pronto (<30 MB), faça commit e push na branch designada. Não abra PR.
Mantenha a sessão ativa durante o render e espere em laços de no máximo 10 min.

ENTREGA: um MP4 por episódio e um resumo curto do que foi feito e das limitações (não dá para ouvir o áudio, só checar por transcrição).
```

## Armadilhas já resolvidas

- `pkill -f` mata o seu próprio shell. Use `pgrep` e `kill` por PID.
- Render com 1 quadro só precisa de vírgula: `node render.js 60,61`.
- Quando mudar só a fala 0, use `FIT=<json de [início,fim]>` para trocar o áudio sem re-renderizar tudo.
