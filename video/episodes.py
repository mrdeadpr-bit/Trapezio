"""Roteiros dos episódios. Cada um: scene (arquivo em scene/), t0 (início da 1ª fala), music (variação), script."""

ESC = [
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

EPISODES = {"esc": dict(scene="index", t0=0.5, music=0, script=ESC)}


def L(who, spoken, cap, shot, uexp="tired", mexp="neutral", **kw):
    return dict(who=who, spoken=spoken, cap=cap, shot=shot, uexp=uexp, mexp=mexp, **kw)

# ---- Série "No divã": ele deitado, o Claude de terapeuta ----
CHAT = [
 L("u", "Doutor Claude... meu chat tem quatro mil mensagens.", "Doutor Claude...\nmeu chat tem 4.000 mensagens.", dict(name="top")),
 L("c", "Eu sei. Eu esqueci o começo na mensagem seiscentos.", "Eu sei. Eu esqueci o começo\nna mensagem 600.", dict(name="cuMascot", a=0.3), "tired", "deadpan"),
 L("u", "Como assim esqueceu?! Eu expliquei o projeto inteiro!", "Como assim esqueceu?!\nEu expliquei o projeto inteiro!", dict(name="cuUser", a=0.3), "panic", "deadpan"),
 L("c", "Contexto tem limite. Chat gigante vira sopa.", "Contexto tem limite.\nChat gigante vira sopa.", dict(name="cuMascot", a=0.2), "panic", "smug"),
 L("u", "E eu não durmo há três dias por isso!", "E eu não durmo há\ntrês dias por isso!", dict(name="cuUser", a=-0.3), "defeat", "smug"),
 L("c", "Abre um chat novo. O essencial vai no CLAUDE ponto M D. E usa o barra compact.", "Chat novo. O essencial no\nCLAUDE.md. E usa o /compact.", dict(name="screen", a=0.4), "defeat", "neutral",
   screen=dict(hist=[["> (chat com 4.000 mensagens…)", "#ffffff"]],
               footer=[[0.0, "Context low (3% remaining) · Run /compact"], [0.55, "contexto: 12%"]],
               events=[dict(f=0.25, kind="line", text="> /compact", color="#ffffff"),
                       dict(f=0.4, kind="line", text="● resumindo a conversa…", color="#e8a07c"),
                       dict(f=0.6, kind="banner", text="✓ conversa resumida", color="#19b46b")])),
 L("u", "Mas o Chat G P T me responde na hora. Com quatorze tópicos.", "Mas o ChatGPT responde na hora.\nCom 14 tópicos.", dict(name="cuUser", a=-0.3), "sly", "neutral"),
 L("c", "Quatorze tópicos. Nenhum arquivo alterado. Impressionante.", "14 tópicos.\nNenhum arquivo alterado. Impressionante.", dict(name="cuMascot", a=0.3), "sly", "smug"),
 L("u", "...Verdade.", "...Verdade.", dict(name="cuUser", a=0.3), "defeat", "smug"),
 L("c", "Salva esse vídeo antes de abrir o chat quatro mil e um.", "Salva esse vídeo antes de\nabrir o chat 4.001.", dict(name="two"), "happy", "happy", last=True),
]

MADRUGADA = [
 L("u", "Doutor... eram onze da noite. Eu só ia trocar a cor de um botão.", "Eram 11 da noite.\nEu só ia trocar a cor de um botão.", dict(name="cuUser", a=0.3), "tired"),
 L("c", "São quatro da manhã.", "São 4 da manhã.", dict(name="cuMascot", a=0.3), "tired", "deadpan"),
 L("u", "Eu sei! E agora o limite de uso acabou!", "Eu sei! E agora o\nlimite de uso acabou!", dict(name="cuUser", a=-0.3), "panic", "deadpan"),
 L("c", "Você colou um log de duas mil linhas. Três vezes. Cola só o erro. E manda tudo numa mensagem só.", "Você colou um log de 2.000 linhas.\nTrês vezes. Cola só o erro.", dict(name="screen", a=-0.4), "panic", "neutral",
   screen=dict(hist=[["> (log de 2.000 linhas colado)", "#ffffff"], ["> (log de 2.000 linhas colado)", "#ffffff"]],
               footer=[[0.0, "esc to interrupt"], [0.5, "5-hour limit reached ∙ resets 4am"]],
               events=[dict(f=0.3, kind="line", text="● lendo 2.000 linhas…", color="#e8a07c"),
                       dict(f=0.55, kind="banner", text="limite de uso atingido", color="#e5484d")])),
 L("u", "Mas eu pago o Claude E o Chat G P T!", "Mas eu pago o Claude\nE o ChatGPT!", dict(name="cuUser", a=0.3), "angry", "neutral"),
 L("c", "Dois salários pra ninguém dormir. Eficiente.", "Dois salários pra ninguém\ndormir. Eficiente.", dict(name="cuMascot", a=0.4), "angry", "smug"),
 L("u", "Pelo menos o Chat G P T diz que minha ideia é ótima.", "Pelo menos o ChatGPT diz\nque minha ideia é ótima.", dict(name="cuUser", a=-0.3), "sly"),
 L("c", "Ele elogia. Eu entrego. Quantos membros tem o seu grupo?", "Ele elogia. Eu entrego.\nQuantos membros tem o seu grupo?", dict(name="cuMascot", a=0.3), "sly", "deadpan"),
 L("u", "Três. Minha mãe, minha tia e eu.", "Três. Minha mãe,\nminha tia e eu.", dict(name="cuUser", a=0.3), "defeat", "deadpan"),
 L("c", "Então o botão nunca foi o problema.", "Então o botão nunca\nfoi o problema.", dict(name="cuMascot", a=0.3), "defeat", "smug"),
 L("c", "Vai dormir. O botão espera. Segue pra mais dicas.", "Vai dormir. O botão espera.\nSegue pra mais dicas.", dict(name="two"), "happy", "happy", last=True),
]

VPS = [
 L("c", "Vamos às contas. V P S: pago. Claude: pago. Chat G P T: pago. Retorno... zero.", "VPS: pago. Claude: pago.\nChatGPT: pago. Retorno: zero.", dict(name="cuMascot", a=0.3), "tired", "deadpan"),
 L("u", "Não fala o número em voz alta.", "Não fala o número\nem voz alta.", dict(name="cuUser", a=0.3), "defeat", "deadpan"),
 L("c", "Zero. Zero reais.", "Zero. Zero reais.", dict(name="cuMascot", a=0.4), "defeat", "smug"),
 L("u", "Mas o grupo vai bombar! Eu sinto!", "Mas o grupo vai bombar!\nEu sinto!", dict(name="cuUser", a=-0.3), "panic", "smug"),
 L("c", "Você sente. A planilha não sente.", "Você sente.\nA planilha não sente.", dict(name="cuMascot", a=0.3), "panic", "deadpan"),
 L("c", "Me manda os dados. Cliques, vendas, horário. Eu monto o relatório e mostro onde está o furo.", "Me manda os dados. Eu monto\no relatório e mostro o furo.", dict(name="screen", a=0.4), "panic", "neutral",
   screen=dict(hist=[["> analisa as postagens do grupo", "#ffffff"]],
               footer=[[0.0, "? for shortcuts"]],
               events=[dict(f=0.25, kind="line", text="● lendo dados…", color="#e8a07c"),
                       dict(f=0.4, kind="line", text="  cliques: 312", color="#ffffff"),
                       dict(f=0.5, kind="line", text="  vendas:  0", color="#ff7b72"),
                       dict(f=0.62, kind="banner", text="achei o furo", color="#f5a623")])),
 L("u", "O Chat G P T me sugeriu um nome pro grupo.", "O ChatGPT me sugeriu\num nome pro grupo.", dict(name="cuUser", a=-0.3), "sly"),
 L("c", "Nome bonito não converte. Número converte.", "Nome bonito não converte.\nNúmero converte.", dict(name="cuMascot", a=0.3), "sly", "smug"),
 L("u", "...Eu vou olhar os números.", "...Eu vou olhar\nos números.", dict(name="cuUser", a=0.3), "happy", "smug"),
 L("c", "Dados antes de ferramenta. Segue pra mais dicas.", "Dados antes de ferramenta.\nSegue pra mais dicas.", dict(name="two"), "happy", "happy", last=True),
]

EPISODES.update(
    chat=dict(scene="couch", t0=0.12, music=0, script=CHAT),
    madrugada=dict(scene="couch", t0=0.12, music=0, script=MADRUGADA),
    vps=dict(scene="couch", t0=0.12, music=0, script=VPS),
)
