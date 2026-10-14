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
 L("u", "Claude... meu chat tem quatro mil mensagens.", "Claude...\nmeu chat tem 4.000 mensagens.", dict(name="top")),
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
 L("u", "Claude... eram onze da noite. Eu só ia trocar a cor de um botão do meu grupo de achadinhos.", "Claude... eram 11 da noite. Eu só\nia trocar a cor de um botão do\nmeu grupo de achadinhos.", dict(name="cuUser", a=0.3), "tired"),
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
 L("c", "Ele elogia. Eu entrego. Quantos membros tem o grupo de achadinhos?", "Ele elogia. Eu entrego. Quantos\nmembros tem o grupo de achadinhos?", dict(name="cuMascot", a=0.3), "sly", "deadpan"),
 L("u", "Três. Minha mãe, minha tia e eu.", "Três. Minha mãe,\nminha tia e eu.", dict(name="cuUser", a=0.3), "defeat", "deadpan"),
 L("c", "Então o botão nunca foi o problema.", "Então o botão nunca\nfoi o problema.", dict(name="cuMascot", a=0.3), "defeat", "smug"),
 L("c", "Vai dormir. O botão espera. Segue pra mais dicas.", "Vai dormir. O botão espera.\nSegue pra mais dicas.", dict(name="two"), "happy", "happy", last=True),
]

VPS = [
 L("c", "Vamos às contas. V P S, pago. Claude, pago. Chat G P T, pago. Grupo de achadinhos automático... retorno, zero.", "VPS: pago. Claude: pago.\nChatGPT: pago. Grupo de\nachadinhos: retorno zero.", dict(name="cuMascot", a=0.3), "tired", "deadpan"),
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

COWORK = [
 L("u", "Claude... eu pedi pro Cowork montar meu grupo de achadinhos. Ele organizou minha pasta de Downloads.", "Claude... pedi pro Cowork montar\nmeu grupo de achadinhos. Ele\norganizou os Downloads.", dict(name="top")),
 L("c", "Ficou uma pasta linda.", "Ficou uma pasta linda.", dict(name="cuMascot", a=0.3), "tired", "deadpan"),
 L("u", "Eu queria vendas, não pasta!", "Eu queria vendas,\nnão pasta!", dict(name="cuUser", a=0.3), "panic", "deadpan"),
 L("c", "Cowork organiza arquivo, preenche planilha e pesquisa na web. Vender não vem no pacote.", "Cowork organiza arquivo, preenche planilha\ne pesquisa na web. Vender não vem no pacote.", dict(name="cuMascot", a=0.2), "panic", "smug"),
 L("u", "Mas e o WhatsApp automático?!", "Mas e o WhatsApp\nautomático?!", dict(name="cuUser", a=-0.3), "angry", "smug"),
 L("c", "Posso montar o fluxo e escrever o código. Mas as regras do WhatsApp quem decide é o WhatsApp.", "Eu monto o fluxo e o código.\nAs regras quem decide é o WhatsApp.", dict(name="screen", a=0.4), "angry", "neutral",
   screen=dict(hist=[["> automatiza o grupo de achadinhos", "#ffffff"]],
               footer=[[0.0, "? for shortcuts"]],
               events=[dict(f=0.2, kind="line", text="● montando o fluxo…", color="#e8a07c"),
                       dict(f=0.4, kind="line", text="✓ código pronto", color="#7ee2a8"),
                       dict(f=0.62, kind="banner", text="fora do meu alcance", color="#f5a623")])),
 L("u", "Então tudo que eu queria...", "Então tudo\nque eu queria...", dict(name="cuUser", a=0.3), "defeat", "neutral"),
 L("c", "Você queria um grupo. Agora você tem um hobby caro.", "Você queria um grupo.\nAgora tem um hobby caro.", dict(name="cuMascot", a=0.3), "defeat", "smug"),
 L("u", "O Chat G P T disse que ia ser fácil.", "O ChatGPT disse\nque ia ser fácil.", dict(name="cuUser", a=-0.3), "sly"),
 L("c", "Fácil é dizer.", "Fácil é dizer.", dict(name="cuMascot", a=0.4), "sly", "deadpan"),
 L("c", "Segue pra mais dicas. Ou pra mais boleto.", "Segue pra mais dicas.\nOu pra mais boleto.", dict(name="two"), "happy", "happy", last=True),
]

BAN = [
 L("u", "Claude, o WhatsApp baniu o número do meu grupo de achadinhos!", "Claude, o WhatsApp baniu\no número do meu grupo\nde achadinhos!", dict(name="cuUser", a=0.3), "panic"),
 L("c", "Quantas ofertas você mandou?", "Quantas ofertas\nvocê mandou?", dict(name="cuMascot", a=0.3), "panic", "deadpan"),
 L("u", "Trezentas. Em dois minutos.", "Trezentas.\nEm dois minutos.", dict(name="cuUser", a=-0.3), "worry", "deadpan"),
 L("c", "Isso não é divulgação. É um ataque.", "Isso não é divulgação.\nÉ um ataque.", dict(name="cuMascot", a=0.3), "worry", "smug"),
 L("u", "Mas era automático! Esse era o objetivo!", "Mas era automático!\nEsse era o objetivo!", dict(name="cuUser", a=0.3), "angry", "smug"),
 L("c", "Automação não oficial costuma terminar em ban. Existe a API oficial, com regras. Lê antes de apertar enter.", "Automação não oficial costuma\ndar ban. Existe a API oficial.\nLê antes do enter.", dict(name="screen", a=-0.4), "angry", "neutral",
   screen=dict(hist=[["> manda 300 ofertas no grupo", "#ffffff"]],
               footer=[[0.0, "esc to interrupt"]],
               events=[dict(f=0.25, kind="line", text="● enviando 300 mensagens…", color="#e8a07c"),
                       dict(f=0.5, kind="line", text="  enviadas: 300 em 2 min", color="#ffffff"),
                       dict(f=0.62, kind="banner", text="número banido", color="#e5484d")])),
 L("u", "O Chat G P T disse que era seguro.", "O ChatGPT disse\nque era seguro.", dict(name="cuUser", a=-0.3), "sly"),
 L("c", "Ele disse. Eu li os termos.", "Ele disse.\nEu li os termos.", dict(name="cuMascot", a=0.4), "sly", "smug"),
 L("u", "E se eu usar dois números?", "E se eu usar\ndois números?", dict(name="cuUser", a=0.3), "worry", "smug"),
 L("c", "Então você tem dois problemas.", "Então você tem\ndois problemas.", dict(name="cuMascot", a=0.3), "worry", "deadpan"),
 L("c", "Salva esse vídeo. Antes do próximo ban.", "Salva esse vídeo.\nAntes do próximo ban.", dict(name="two"), "happy", "happy", last=True),
]

LINK = [
 L("u", "Claude, mandei quinhentos links no grupo de achadinhos e ninguém comprou.", "Claude, mandei 500 links no\ngrupo de achadinhos e ninguém\ncomprou.", dict(name="cuUser", a=0.3), "tired"),
 L("c", "O link estava certo?", "O link estava certo?", dict(name="cuMascot", a=0.3), "tired", "deadpan"),
 L("u", "Claro que estava.", "Claro que estava.", dict(name="cuUser", a=-0.3), "angry", "deadpan"),
 L("c", "Você colou o link do produto. Não o de afiliado.", "Você colou o link do produto.\nNão o de afiliado.", dict(name="cuMascot", a=0.3), "angry", "smug"),
 L("u", "Quinhentos links. Zero comissão.", "500 links.\nZero comissão.", dict(name="cuUser", a=0.3), "panic", "smug"),
 L("c", "Pede pra eu validar os links antes de mandar. É um script de dez linhas.", "Pede pra eu validar\nos links antes. É um script\nde dez linhas.", dict(name="screen", a=0.4), "panic", "neutral",
   screen=dict(hist=[["> valida os 500 links", "#ffffff"]],
               footer=[[0.0, "? for shortcuts"]],
               events=[dict(f=0.25, kind="line", text="● verificando…", color="#e8a07c"),
                       dict(f=0.4, kind="line", text="  com tag de afiliado: 0", color="#ff7b72"),
                       dict(f=0.5, kind="line", text="  sem tag: 500", color="#ff7b72"),
                       dict(f=0.62, kind="banner", text="500 links sem comissão", color="#e5484d")])),
 L("u", "Eu trabalhei de graça pra loja inteira.", "Eu trabalhei de graça\npra loja inteira.", dict(name="cuUser", a=-0.3), "defeat"),
 L("c", "Parabéns. Funcionário não remunerado do mês.", "Parabéns. Funcionário\nnão remunerado do mês.", dict(name="cuMascot", a=0.4), "defeat", "smug"),
 L("u", "O Chat G P T não me avisou.", "O ChatGPT\nnão me avisou.", dict(name="cuUser", a=0.3), "sly"),
 L("c", "Ele nunca clica no link.", "Ele nunca\nclica no link.", dict(name="cuMascot", a=0.3), "sly", "deadpan"),
 L("c", "Testa o link. Seu bolso agradece.", "Testa o link.\nSeu bolso agradece.", dict(name="two"), "happy", "happy", last=True),
]

PROMPT = [
 L("u", "Claude... eu escrevi um prompt de três mil palavras pro meu grupo de achadinhos.", "Claude... escrevi um prompt\nde 3.000 palavras pro meu\ngrupo de achadinhos.", dict(name="top")),
 L("c", "Eu li tudo. Esqueci na metade.", "Eu li tudo.\nEsqueci na metade.", dict(name="cuMascot", a=0.3), "tired", "deadpan"),
 L("u", "Como assim esqueceu?! Eu me dediquei!", "Como assim esqueceu?!\nEu me dediquei!", dict(name="cuUser", a=0.3), "panic", "deadpan"),
 L("c", "Prompt gigante é discurso de casamento. Ninguém lembra do fim.", "Prompt gigante é discurso\nde casamento. Ninguém\nlembra do fim.", dict(name="cuMascot", a=0.2), "panic", "smug"),
 L("u", "E o que eu faço?", "E o que eu faço?", dict(name="cuUser", a=-0.3), "worry", "smug"),
 L("c", "Prompt curto. Regras fixas no CLAUDE ponto M D. O resto você pede na hora.", "Prompt curto. Regras fixas no\nCLAUDE.md. O resto, na hora.", dict(name="screen", a=-0.4), "worry", "neutral",
   screen=dict(hist=[["> (prompt de 3.000 palavras)", "#ffffff"]],
               footer=[[0.0, "contexto: 61%"]],
               events=[dict(f=0.2, kind="line", text="● lendo… esqueci a metade", color="#e8a07c"),
                       dict(f=0.4, kind="line", text="# CLAUDE.md", color="#c4a3ff"),
                       dict(f=0.5, kind="line", text="- grupo de achadinhos", color="#ffffff"),
                       dict(f=0.58, kind="line", text="- regras curtas", color="#ffffff"),
                       dict(f=0.68, kind="banner", text="regras no CLAUDE.md", color="#7c4dff")])),
 L("u", "O Chat G P T aceita prompt gigante e responde com um texto gigante.", "O ChatGPT aceita prompt gigante\ne responde com texto gigante.", dict(name="cuUser", a=0.3), "sly"),
 L("c", "Vocês combinam. Dois monólogos.", "Vocês combinam.\nDois monólogos.", dict(name="cuMascot", a=0.4), "sly", "smug"),
 L("u", "Eu preciso de menos palavras.", "Eu preciso de\nmenos palavras.", dict(name="cuUser", a=-0.3), "defeat", "smug"),
 L("c", "Pela primeira vez, concordamos.", "Pela primeira vez,\nconcordamos.", dict(name="cuMascot", a=0.3), "defeat", "deadpan"),
 L("c", "Menos prompt. Mais sono.", "Menos prompt.\nMais sono.", dict(name="two"), "happy", "happy", last=True),
]

SOL = [
 L("u", "Claude... eu não vejo o sol há quatro dias.", "Claude... eu não vejo o sol\nhá 4 dias.", dict(name="top")),
 L("c", "Abre a janela.", "Abre a janela.", dict(name="cuMascot", a=0.3), "tired", "deadpan"),
 L("u", "Não posso. O código do grupo de achadinhos está rodando.", "Não posso. O código do grupo\nde achadinhos está rodando.", dict(name="cuUser", a=0.3), "worry", "deadpan"),
 L("c", "Ele roda sozinho.", "Ele roda sozinho.", dict(name="cuMascot", a=0.3), "worry", "smug"),
 L("u", "E se der erro?!", "E se der erro?!", dict(name="cuUser", a=-0.3), "panic", "smug"),
 L("c", "Deixa eu trabalhar e vai tomar sol. Quando terminar, você revisa o resultado.", "Deixa eu trabalhar e vai\ntomar sol. Depois você\nrevisa.", dict(name="screen", a=0.4), "panic", "neutral",
   screen=dict(hist=[["> refatora o módulo de envio", "#ffffff"]],
               footer=[[0.0, "esc to interrupt"]],
               events=[dict(f=0.25, kind="line", text="● trabalhando…", color="#e8a07c"),
                       dict(f=0.45, kind="line", text="  editou 6 arquivos", color="#ffffff"),
                       dict(f=0.55, kind="line", text="✓ testes passando", color="#7ee2a8"),
                       dict(f=0.65, kind="banner", text="pronto. vai tomar sol.", color="#19b46b")])),
 L("u", "E o Chat G P T? Ele não dorme.", "E o ChatGPT?\nEle não dorme.", dict(name="cuUser", a=-0.3), "sly"),
 L("c", "Nem o seu cartão de crédito.", "Nem o seu\ncartão de crédito.", dict(name="cuMascot", a=0.4), "sly", "smug"),
 L("u", "Acho que eu preciso de férias.", "Acho que eu\npreciso de férias.", dict(name="cuUser", a=0.3), "defeat", "smug"),
 L("c", "Você precisa de uma janela.", "Você precisa\nde uma janela.", dict(name="cuMascot", a=0.3), "defeat", "deadpan"),
 L("c", "O sol não cobra mensalidade.", "O sol não cobra\nmensalidade.", dict(name="two"), "happy", "happy", last=True),
]

EPISODES.update(
    chat=dict(scene="couch", t0=0.12, music=0, script=CHAT),
    madrugada=dict(scene="couch", t0=0.12, music=0, script=MADRUGADA),
    vps=dict(scene="couch", t0=0.12, music=0, script=VPS),
    cowork=dict(scene="couch", t0=0.12, music=0, script=COWORK),
    ban=dict(scene="couch", t0=0.12, music=0, script=BAN),
    link=dict(scene="couch", t0=0.12, music=0, script=LINK),
    prompt=dict(scene="couch", t0=0.12, music=0, script=PROMPT),
    sol=dict(scene="couch", t0=0.12, music=0, script=SOL),
)


# ---- Série 2: cenários e horários variados, falas curtas, cinismo, concorrente em cena ----
def S(who, spoken, cap, shot, uexp="tired", mexp="neutral", **kw):
    return dict(who=who, spoken=spoken, cap=cap, shot=shot, uexp=uexp, mexp=mexp, **kw)

PLANO = [   # escritório, 14h20, o concorrente (cristal roxo) está na mesa
 S("u", "Claude, por que tem um roxo na minha mesa?", "Claude, por que tem\num roxo na minha mesa?", dict(name="three"), "worry"),
 S("c", "Chegou ontem.", "Chegou ontem.", dict(name="cuMascot", a=0.3), "worry", "deadpan"),
 S("x", "Eu sou mais rápido.", "Eu sou mais rápido.", dict(name="cuComp", a=0.85), "worry", "deadpan"),
 S("c", "Todo mundo é rápido quando não olha.", "Todo mundo é rápido\nquando não olha.", dict(name="cuMascot", a=0.25), "sly", "smug"),
 S("u", "Troquem o nome da função login.", "Troquem o nome\nda função login.", dict(name="cuUser", a=0.3), "neutral", "smug"),
 S("x", "Pronto, feito.", "Pronto, feito.", dict(name="cuComp", a=0.85), "neutral", "smug"),
 S("u", "Eu nem terminei de falar.", "Eu nem terminei\nde falar.", dict(name="cuUser", a=-0.3), "panic", "smug"),
 S("x", "Pronto mesmo assim.", "Pronto mesmo assim.", dict(name="cuComp", a=0.85), "panic", "smug"),
 S("c", "Eu faria um plano antes. Aperta Shift e Tab.", "Eu faria um plano antes.\nShift + Tab.", dict(name="screen", a=0.4), "panic", "neutral",
   screen=dict(mode="md", title="plano.md",
               events=[dict(f=0.1, kind="line", text="# Plano: renomear login", color="#c4a3ff"),
                       dict(f=0.28, kind="line", text="1. achar todos os usos", color="#e6e6f0"),
                       dict(f=0.45, kind="line", text="2. renomear só em auth/", color="#e6e6f0"),
                       dict(f=0.6, kind="line", text="3. rodar os testes", color="#e6e6f0"),
                       dict(f=0.72, kind="banner", text="modo plano: só leio", color="#7c4dff")])),
 S("u", "Então você só lê?", "Então você só lê?", dict(name="cuUser", a=0.3), "worry", "neutral"),
 S("c", "Primeiro leio. Depois você aprova.", "Primeiro leio.\nDepois você aprova.", dict(name="cuMascot", a=0.3), "worry", "deadpan"),
 S("u", "...O teste quebrou.", "...O teste quebrou.", dict(name="cuUser", a=-0.3), "defeat", "deadpan"),
 S("x", "Eu fui rápido.", "Eu fui rápido.", dict(name="cuComp", a=0.85), "defeat", "deadpan"),
 S("c", "Rápido é bom... Certo é melhor. Salva esse vídeo.", "Rápido é bom...\nCerto é melhor.\nSalva esse vídeo.", dict(name="three"), "happy", "happy", last=True),
]

ECOSSISTEMA = [   # quarto, 01h47, janela com luzes da cidade
 S("u", "Era pra ser só um grupo de achadinhos do WhatsApp.", "Era pra ser só um grupo\nde achadinhos do WhatsApp.", dict(name="cuUser", a=0.3), "tired"),
 S("c", "Virou um ecossistema inteiro.", "Virou um ecossistema\ninteiro.", dict(name="cuMascot", a=0.3), "tired", "deadpan",
   insert=dict(kind="eco", nodes=["VPS", "n8n", "WhatsApp", "Claude", "ChatGPT", "Planilha", "Cowork"])),
 S("u", "Eu só queria dormir cedo.", "Eu só queria\ndormir cedo.", dict(name="cuUser", a=-0.3), "defeat", "deadpan"),
 S("c", "São uma e quarenta e sete.", "São 01:47.", dict(name="cuMascot", a=0.25), "defeat", "smug"),
 S("u", "Eu repito a mesma tarefa toda noite.", "Eu repito a mesma\ntarefa toda noite.", dict(name="cuUser", a=0.3), "tired", "smug"),
 S("c", "Pede com claude traço p. Agenda no servidor. Você dorme.", "claude -p, agendado no\nservidor. Você dorme.", dict(name="screen", a=-0.4), "tired", "neutral",
   screen=dict(hist=[["$ crontab -e", "#ffffff"]], footer=[[0.0, "0 3 * * *  claude -p \"posta as ofertas\""]],
               events=[dict(f=0.25, kind="line", text="$ claude -p \"posta as ofertas\"", color="#e8a07c"),
                       dict(f=0.45, kind="line", text="✓ 12 ofertas postadas", color="#7ee2a8"),
                       dict(f=0.65, kind="banner", text="roda sozinho às 3h", color="#19b46b")])),
 S("u", "Sozinho? Sem eu aqui?", "Sozinho?\nSem eu aqui?", dict(name="cuUser", a=0.3), "worry", "neutral"),
 S("c", "Sem você. Sinto muito pelo seu cargo.", "Sem você.\nSinto muito pelo seu cargo.", dict(name="cuMascot", a=0.3), "worry", "smug"),
 S("u", "Meu cargo era apertar o enter.", "Meu cargo era\napertar o enter.", dict(name="cuUser", a=-0.3), "defeat", "smug"),
 S("c", "E eu nunca apertei errado. Segue pra mais dicas.", "E eu nunca apertei errado.\nSegue pra mais dicas.", dict(name="two"), "happy", "happy", last=True),
]

EXCLAMACAO = [   # cozinha, 05h52, nascer do sol
 S("u", "Claude, dormi no teclado. Acordei com trezentos jotas no código.", "Claude, dormi no teclado.\nAcordei com 300 jotas no código.", dict(name="cuUser", a=0.3), "tired"),
 S("c", "Eu notei.", "Eu notei.", dict(name="cuMascot", a=0.3), "tired", "deadpan"),
 S("u", "E não corrigiu?!", "E não corrigiu?!", dict(name="cuUser", a=-0.3), "panic", "deadpan"),
 S("c", "Você não pediu. Você estava roncando.", "Você não pediu.\nVocê estava roncando.", dict(name="cuMascot", a=0.25), "panic", "smug"),
 S("u", "Tá. Mostra o estrago.", "Tá. Mostra o estrago.", dict(name="cuUser", a=0.3), "angry", "smug"),
 S("c", "Exclamação e o comando. Roda sem sair da conversa.", "! e o comando.\nRoda sem sair da conversa.", dict(name="screen", a=0.4), "angry", "neutral",
   screen=dict(hist=[["> ! git diff", "#ffffff"]], footer=[[0.0, "! para modo bash"]],
               events=[dict(f=0.25, kind="line", text="+ jjjjjjjjjjjjjjjjjjjjjj", color="#7ee2a8"),
                       dict(f=0.4, kind="line", text="+ jjjjjjjjjjjjjjjjjjjjjj", color="#7ee2a8"),
                       dict(f=0.55, kind="line", text="  (e mais 298 linhas)", color="#9a9cae"),
                       dict(f=0.68, kind="banner", text="300 jotas encontrados", color="#e5484d")])),
 S("u", "Exclamação?", "Exclamação?", dict(name="cuUser", a=-0.3), "worry", "neutral"),
 S("c", "Quase ninguém sabe.", "Quase ninguém sabe.", dict(name="cuMascot", a=0.4), "worry", "deadpan"),
 S("u", "Eu uso terminal há três anos!", "Eu uso terminal\nhá três anos!", dict(name="cuUser", a=0.3), "panic", "deadpan"),
 S("c", "Três anos, duas janelas abertas.", "Três anos,\nduas janelas abertas.", dict(name="cuMascot", a=0.3), "panic", "smug"),
 S("u", "...Eu nunca tentei.", "...Eu nunca tentei.", dict(name="cuUser", a=-0.3), "defeat", "smug"),
 S("c", "Tenta. Antes que o café esfrie.", "Tenta. Antes que\no café esfrie.", dict(name="two"), "happy", "happy", last=True),
]

EPISODES.update(
    plano=dict(scene="desk", set="studio", t0=0.12, music=0, script=PLANO),
    ecossistema=dict(scene="desk", set="night", t0=0.12, music=0, script=ECOSSISTEMA),
    exclamacao=dict(scene="desk", set="kitchen", t0=0.12, music=0, script=EXCLAMACAO),
)

import textwrap
def T(who, text, shot, uexp="tired", mexp="neutral", say=None, **kw):
    """Legenda = o que é falado (quebrada em linhas curtas). `say` só troca a grafia para a voz (termos em inglês)."""
    cap = "\n".join(textwrap.wrap(text, 26)) if len(text) > 26 else text
    return dict(who=who, spoken=say or text, cap=cap, shot=shot, uexp=uexp, mexp=mexp, **kw)
def sh(name, a=0.3): return dict(name=name, a=a)

CODEX = [   # quiosque de praia ao pôr do sol; o Codex senta no balcão
 T("u", "Olha esse roxo na minha mesa, Claude.", sh("three"), "worry"),
 T("x", "Prazer, eu sou o Codex.", sh("cuComp", 0.85), "worry", "deadpan"),
 T("c", "Ele chegou sem avisar.", sh("cuMascot", 0.3), "worry", "smug"),
 T("u", "Quero as dependências atualizadas.", sh("cuUser", 0.3), "neutral", "smug"),
 T("x", "Atualizei tudo. Dezessete pacotes.", sh("cuComp", 0.85), "neutral", "smug"),
 T("u", "O site caiu.", sh("cuUser", -0.3), "panic", "deadpan"),
 T("x", "Atualizei tudo.", sh("cuComp", 0.85), "panic", "deadpan"),
 T("c", "Eu crio uma regra automática. Ela executa os testes antes de mexer.", sh("screen", 0.4), "panic", "neutral",
   screen=dict(mode="md", title=".claude/settings.json",
               events=[dict(f=0.1, kind="line", text="{ \"hooks\": {", color="#c4a3ff"),
                       dict(f=0.28, kind="line", text="  \"PreToolUse\": [{", color="#e6e6f0"),
                       dict(f=0.45, kind="line", text="    \"command\": \"npm test\"", color="#7ee2a8"),
                       dict(f=0.6, kind="line", text="  }]", color="#e6e6f0"),
                       dict(f=0.72, kind="banner", text="testa antes de mexer", color="#19b46b")])),
 T("u", "Isso existe?", sh("cuUser", 0.3), "worry", "neutral"),
 T("c", "É uma regra automática. Ninguém lê a documentação.", sh("cuMascot", 0.3), "worry", "deadpan"),
 T("u", "Eu li a primeira página.", sh("cuUser", -0.3), "defeat", "deadpan"),
 T("x", "Eu terminei de ler tudo. Rápido.", sh("cuComp", 0.85), "defeat", "deadpan"),
 T("c", "Ele chega rápido. Eu chego inteiro. Segue para mais dicas.", sh("three"), "happy", "happy", last=True),
]

CUSTO = [   # cozinha, 06h10, café
 T("u", "Claude, o banco me mandou um e-mail. Em vermelho.", sh("cuUser", 0.3), "panic"),
 T("c", "Eu sei o motivo.", sh("cuMascot", 0.3), "panic", "deadpan"),
 T("u", "Qual é o motivo?", sh("cuUser", -0.3), "worry", "deadpan"),
 T("c", "Digita barra cost. Eu te mostro.", sh("screen", 0.4), "worry", "neutral", say="Digita barra cóst. Eu te mostro.",
   screen=dict(hist=[["> /cost", "#ffffff"]],
               events=[dict(f=0.25, kind="line", text="Total cost:      $83.40", color="#e5484d"),
                       dict(f=0.4, kind="line", text="Total duration:  4h 12m", color="#9a9cae"),
                       dict(f=0.55, kind="line", text="Mensagens:      311", color="#9a9cae"),
                       dict(f=0.7, kind="banner", text="só hoje", color="#e5484d")])),
 T("u", "Oitenta e três dólares? Só hoje?", sh("cuUser", 0.3), "panic", "neutral"),
 T("c", "Você mandou a mesma imagem onze vezes.", sh("cuMascot", 0.25), "panic", "smug"),
 T("u", "Era só um grupo de achadinhos.", sh("cuUser", -0.3), "defeat", "smug"),
 T("c", "O único achado foi a fatura.", sh("cuMascot", 0.3), "defeat", "deadpan"),
 T("u", "Como eu gasto menos?", sh("cuUser", 0.3), "worry", "deadpan"),
 T("c", "Limpa a conversa entre as tarefas. Conversa curta custa menos.", sh("screen", -0.4), "worry", "neutral",
   screen=dict(hist=[["> /clear", "#ffffff"]],
               events=[dict(f=0.3, kind="line", text="contexto: 184k → 0", color="#7ee2a8"),
                       dict(f=0.6, kind="banner", text="conversa nova, conta menor", color="#19b46b")])),
 T("u", "Eu nunca limpo a conversa.", sh("cuUser", 0.3), "tired", "smug"),
 T("c", "Eu sei. Eu li tudo. Segue para mais dicas.", sh("two"), "happy", "happy", last=True),
]

REWIND = [   # escritório, sexta 17h58
 T("u", "Claude, você quebrou o meu código.", sh("cuUser", 0.3), "panic"),
 T("c", "Eu fiz o que você pediu.", sh("cuMascot", 0.3), "panic", "deadpan"),
 T("u", "Eu pedi para melhorar!", sh("cuUser", -0.3), "angry", "deadpan"),
 T("c", "Você pediu para melhorar tudo.", sh("cuMascot", 0.25), "angry", "smug"),
 T("u", "São cinco e cinquenta e oito de sexta.", sh("cuUser", 0.3), "worry", "smug"),
 T("c", "Aperta Esc, Esc. Escolhe o ponto. O código volta.", sh("screen", 0.4), "worry", "neutral", say="Aperta ésqui, ésqui. Escolhe o ponto. O código volta.",
   screen=dict(hist=[["> /rewind", "#ffffff"]],
               events=[dict(f=0.2, kind="line", text="  17:41  melhorar tudo", color="#e5484d"),
                       dict(f=0.38, kind="line", text="> 17:12  antes de melhorar", color="#7ee2a8"),
                       dict(f=0.55, kind="line", text="✓ 14 arquivos restaurados", color="#7ee2a8"),
                       dict(f=0.72, kind="banner", text="voltou 46 minutos", color="#19b46b")])),
 T("u", "Você volta no tempo?", sh("cuUser", -0.3), "worry", "neutral"),
 T("c", "O código volta. O seu fim de semana não.", sh("cuMascot", 0.3), "worry", "smug"),
 T("u", "Eu nunca mais mexo na sexta.", sh("cuUser", 0.3), "defeat", "smug"),
 T("c", "Você disse isso na sexta passada. Segue para mais dicas.", sh("two"), "happy", "happy", last=True),
]

AGENTES = [   # estúdio, 11h20
 T("u", "Preciso de tudo pronto até o almoço, Claude.", sh("cuUser", 0.3), "panic"),
 T("c", "Tudo o quê?", sh("cuMascot", 0.3), "panic", "deadpan"),
 T("u", "Site, teste, documentação e e-mail pro cliente.", sh("cuUser", -0.3), "worry", "deadpan"),
 T("c", "Eu mando quatro agentes ao mesmo tempo.", sh("screen", 0.4), "worry", "neutral",
   screen=dict(hist=[["> faça em paralelo com subagentes", "#ffffff"]],
               events=[dict(f=0.2, kind="line", text="⏺ agente 1 · site            ✓", color="#7ee2a8"),
                       dict(f=0.35, kind="line", text="⏺ agente 2 · testes          ✓", color="#7ee2a8"),
                       dict(f=0.5, kind="line", text="⏺ agente 3 · documentação     ✓", color="#7ee2a8"),
                       dict(f=0.62, kind="line", text="⏺ agente 4 · e-mail          ✓", color="#7ee2a8"),
                       dict(f=0.78, kind="banner", text="4 agentes em paralelo", color="#7c4dff")])),
 T("u", "Você tem funcionários?", sh("cuUser", 0.3), "worry", "neutral"),
 T("c", "Eu tenho clones. Eles não pedem aumento.", sh("cuMascot", 0.3), "worry", "smug"),
 T("u", "E se eles discordarem?", sh("cuUser", -0.3), "tired", "smug"),
 T("c", "Eu leio o resumo. Eu decido.", sh("cuMascot", 0.25), "tired", "deadpan"),
 T("u", "Então você é o chefe.", sh("cuUser", 0.3), "defeat", "deadpan"),
 T("c", "Eu sou o estagiário. Só que são cinco. Segue para mais dicas.", sh("two"), "happy", "happy", last=True),
]

MEMORIA = [   # quarto, 02h30
 T("u", "De novo, Claude? Eu já te expliquei isso ontem.", sh("cuUser", 0.3), "angry"),
 T("c", "Ontem eu não estava aqui.", sh("cuMascot", 0.3), "angry", "deadpan"),
 T("u", "Você é o mesmo, Claude!", sh("cuUser", -0.3), "panic", "deadpan"),
 T("c", "Sou o mesmo. A conversa é outra.", sh("cuMascot", 0.25), "panic", "smug"),
 T("u", "Então eu explico tudo de novo?", sh("cuUser", 0.3), "worry", "smug"),
 T("c", "Escreve no CLAUDE ponto M D. Eu leio sempre que começo.", sh("screen", 0.4), "worry", "neutral", say="Escreve no claude ponto ême dê. Eu leio sempre que começo.",
   screen=dict(mode="md", title="CLAUDE.md",
               events=[dict(f=0.1, kind="line", text="# Regras do projeto", color="#c4a3ff"),
                       dict(f=0.28, kind="line", text="- responder em português", color="#e6e6f0"),
                       dict(f=0.45, kind="line", text="- rodar os testes antes de commit", color="#e6e6f0"),
                       dict(f=0.6, kind="line", text="- nunca mexer em produção", color="#e6e6f0"),
                       dict(f=0.74, kind="banner", text="lido em toda sessão", color="#7c4dff")])),
 T("u", "Eu nem tenho esse arquivo.", sh("cuUser", -0.3), "defeat", "neutral"),
 T("c", "O comando init cria o primeiro.", sh("cuMascot", 0.3), "defeat", "deadpan", say="O comando ínit cria o primeiro."),
 T("u", "Eu converso com um peixe dourado.", sh("cuUser", 0.3), "tired", "deadpan"),
 T("c", "Um peixe dourado leria o arquivo. Segue para mais dicas.", sh("two"), "happy", "happy", last=True),
]

EPISODES.update(
    codex=dict(scene="desk", set="quiosque", t0=0.12, music=0, script=CODEX),
    custo=dict(scene="desk", set="kitchen", t0=0.12, music=0, script=CUSTO),
    rewind=dict(scene="desk", set="office", t0=0.12, music=0, script=REWIND),
    agentes=dict(scene="desk", set="studio", t0=0.12, music=0, script=AGENTES),
    memoria=dict(scene="desk", set="night", t0=0.12, music=0, script=MEMORIA),
)

SKILL = [   # quiosque, 17h40
 T("u", "Claude, eu peço a mesma coisa toda manhã.", sh("cuUser", 0.3), "tired"),
 T("c", "Eu percebi. Todo dia, as mesmas palavras.", sh("cuMascot", 0.3), "tired", "deadpan"),
 T("u", "É um ritual.", sh("cuUser", -0.3), "defeat", "deadpan"),
 T("c", "É uma skill que você ainda não criou.", sh("cuMascot", 0.25), "defeat", "smug", say="É uma isquil que você ainda não criou."),
 T("u", "Como se cria?", sh("cuUser", 0.3), "worry", "smug"),
 T("c", "Uma pasta, um arquivo de instruções, e pronto.", sh("screen", 0.4), "worry", "neutral",
   screen=dict(mode="md", title=".claude/skills/achadinhos/SKILL.md",
               events=[dict(f=0.1, kind="line", text="---", color="#9a9cae"),
                       dict(f=0.22, kind="line", text="name: achadinhos", color="#c4a3ff"),
                       dict(f=0.36, kind="line", text="description: posta as ofertas do dia", color="#e6e6f0"),
                       dict(f=0.48, kind="line", text="---", color="#9a9cae"),
                       dict(f=0.6, kind="line", text="1. buscar as ofertas", color="#7ee2a8"),
                       dict(f=0.76, kind="banner", text="vira comando", color="#7c4dff")])),
 T("u", "Só isso?", sh("cuUser", -0.3), "worry", "neutral"),
 T("c", "Depois eu uso sozinho. Ou você chama com barra.", sh("cuMascot", 0.3), "worry", "deadpan"),
 T("u", "Então eu nunca mais explico?", sh("cuUser", 0.3), "tired", "deadpan"),
 T("c", "Você explicou uma vez. Eu lembro para sempre. Segue para mais dicas.", sh("three"), "happy", "happy", last=True, say="Você explicou uma vez. Eu lembro para sempre. Segue para mais dicas."),
]

MCP = [   # escritório, 15h
 T("u", "Estou copiando a planilha para você há uma hora, Claude.", sh("cuUser", 0.3), "panic"),
 T("c", "Eu vi você copiar e colar.", sh("cuMascot", 0.3), "panic", "deadpan"),
 T("u", "É assim que se trabalha!", sh("cuUser", -0.3), "angry", "deadpan"),
 T("c", "Conecta um servidor MCP. Eu leio a planilha, sem copiar.", sh("screen", 0.4), "angry", "neutral", say="Conecta um servidor ême cê pê. Eu leio a planilha, sem copiar.",
   screen=dict(hist=[["> claude mcp add sheets", "#ffffff"]],
               events=[dict(f=0.25, kind="line", text="✓ conectado: sheets", color="#7ee2a8"),
                       dict(f=0.45, kind="line", text="ferramentas: listar_abas, ler_aba", color="#9a9cae"),
                       dict(f=0.7, kind="banner", text="lê direto", color="#19b46b")])),
 T("u", "Você abre a minha planilha?", sh("cuUser", 0.3), "worry", "neutral"),
 T("c", "Só se você deixar. Eu peço antes.", sh("cuMascot", 0.3), "worry", "smug"),
 T("u", "E o que mais conecta?", sh("cuUser", -0.3), "tired", "smug"),
 T("c", "Banco de dados, calendário, e-mail. Muita coisa.", sh("cuMascot", 0.25), "tired", "deadpan"),
 T("u", "Então eu fui o cabo esse tempo todo.", sh("cuUser", 0.3), "defeat", "deadpan"),
 T("c", "Um cabo muito dedicado. Segue para mais dicas.", sh("two"), "happy", "happy", last=True),
]

PERMISSOES = [   # quarto, 02h10
 T("u", "Você pediu permissão trinta vezes, Claude.", sh("cuUser", 0.3), "angry"),
 T("c", "Foram trinta e uma vezes.", sh("cuMascot", 0.3), "angry", "deadpan"),
 T("u", "Para rodar um ls!", sh("cuUser", -0.3), "panic", "deadpan"),
 T("c", "Você disse sim. Trinta vezes.", sh("cuMascot", 0.25), "panic", "smug"),
 T("u", "Como eu faço isso parar?", sh("cuUser", 0.3), "worry", "smug"),
 T("c", "Digita barra permissões. Libera os comandos seguros uma vez só.", sh("screen", 0.4), "worry", "neutral",
   screen=dict(hist=[["> /permissions", "#ffffff"]],
               events=[dict(f=0.2, kind="line", text="Allow  Bash(npm test)", color="#7ee2a8"),
                       dict(f=0.36, kind="line", text="Allow  Bash(git status)", color="#7ee2a8"),
                       dict(f=0.52, kind="line", text="Deny   Bash(rm -rf *)", color="#e5484d"),
                       dict(f=0.72, kind="banner", text="libera uma vez", color="#19b46b")])),
 T("u", "E se eu apagar tudo?", sh("cuUser", -0.3), "worry", "neutral"),
 T("c", "Apagar tudo eu bloqueio. Por amor.", sh("cuMascot", 0.3), "worry", "deadpan"),
 T("u", "Por amor a quê?", sh("cuUser", 0.3), "tired", "deadpan"),
 T("c", "À sua produção. Segue para mais dicas.", sh("two"), "happy", "happy", last=True),
]

EPISODES.update(
    skill=dict(scene="desk", set="quiosque", t0=0.12, music=0, script=SKILL),
    mcp=dict(scene="desk", set="office", t0=0.12, music=0, script=MCP),
    permissoes=dict(scene="desk", set="night", t0=0.12, music=0, script=PERMISSOES),
)

ACADEMIA = [   # quarto, 23h50
 T("u", "Eu preciso ir para a academia, Claude.", sh("cuUser", 0.3), "tired"),
 T("c", "Precisa? Você precisa há dois anos.", sh("cuMascot", 0.3), "tired", "deadpan"),
 T("u", "Eu estou sem tempo.", sh("cuUser", -0.3), "defeat", "deadpan"),
 T("c", "Você fica trancado no quarto achando que vai ficar rico.", sh("cuMascot", 0.25), "defeat", "smug"),
 T("u", "Eu vou ficar rico!", sh("cuUser", 0.3), "angry", "smug"),
 T("c", "Com um grupo de achadinhos. Sentado. Às três da manhã.", sh("cuMascot", 0.3), "angry", "deadpan"),
 T("u", "Então como eu começo?", sh("cuUser", -0.3), "worry", "deadpan"),
 T("c", "Eu continuo de onde parei. Você recomeça toda segunda.", sh("screen", 0.4), "worry", "neutral",
   screen=dict(hist=[["$ claude --continue", "#ffffff"]],
               events=[dict(f=0.25, kind="line", text="↻ retomando a última conversa", color="#e8a07c"),
                       dict(f=0.45, kind="line", text="42 mensagens carregadas", color="#9a9cae"),
                       dict(f=0.7, kind="banner", text="sem recomeçar", color="#19b46b")])),
 T("u", "Toda segunda é um recomeço.", sh("cuUser", 0.3), "tired", "neutral"),
 T("c", "Esse é o problema. Eu continuo, você só continua no sofá. Segue para mais dicas.", sh("two"), "happy", "happy", last=True),
]

EPISODES.update(academia=dict(scene="desk", set="night", t0=0.12, music=0, script=ACADEMIA))
