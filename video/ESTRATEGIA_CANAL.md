# Estratégia do canal "O problema é o prompt" (recálculo)

Ponto de partida: 13 seguidores em 4 dias, 6 vídeos, ~5 mil views no total, e os 2 últimos com ~200 views cada.
Eu não vejo suas métricas. Tudo abaixo é hipótese a testar, não verdade. A seção 9 diz o que preciso de você.

## 1. O que os números provavelmente dizem
- 5 mil views em 6 vídeos mostra que o algoritmo testou o conteúdo em grupos pequenos. Alguns vídeos passaram do teste inicial e outros não.
- 200 views em 2 vídeos seguidos é o padrão de "foi entregue a poucos e não segurou". Pode ser o tema, o gancho ou a retenção. Instagram também oscila sem motivo claro, então não tire conclusão com só 2 vídeos.
- Só dá para decidir com os dados de cada Reel: **retenção nos primeiros 3 s, tempo médio assistido, compartilhamentos e salvamentos por view**. É isso que o Instagram usa para distribuir.

## 2. Por que acho que os últimos vídeos travaram (hipóteses, em ordem de probabilidade)
1. **Sem promessa clara nos 2 primeiros segundos.** Piada de abertura abstrata ("Claude, a IA não entende o que eu peço") não diz ao espectador de TI o que ele ganha em ficar.
2. **Humor interno.** A piada do nome do perfil e a persona de diretor de cinema só funcionam para quem já conhece o canal. O público novo não tem o contexto.
3. **Dica fraca ou invisível.** Em vários episódios a dica aparece no meio, sem demonstração de antes e depois. Ninguém salva ou envia um vídeo sem "isso resolve um problema meu".
4. **Duração e ritmo.** 30–38 s com falas lentas e muitos closes parados. A retenção cai antes da dica.
5. **Voz sintética e boneco.** Posso estar errado, porque não ouço o áudio. Se a voz soa artificial, o público de TI desconfia. Isso é um risco, não um fato.
6. **Falta de série e de motivo para seguir.** Cada vídeo é avulso. Ninguém sabe o que vai receber no próximo.

## 3. Nova linha editorial: uma promessa só
**"Prompts que funcionam, explicados por um sênior cético."** O nome do canal já diz isso. Tudo passa a girar em torno de um antes e depois mostrado na tela:
- O boneco (júnior, cansado) manda um prompt ruim.
- O Claude (sênior cético, seco) mostra o resultado ruim na tela e explica por que veio ruim.
- Ele reescreve o prompt. O resultado melhora, e o espectador pode copiar e salvar.

Isso cria três coisas que o algoritmo premia: **salvar** (prompt pronto), **enviar** (a dor reconhecida: "isso é o meu chefe") e **comentar** ("quero o prompt").

## 4. Fórmula de cada vídeo (20 a 25 s)
| tempo | o quê |
|---|---|
| 0–2 s | Gancho com **dor ou prova**, em texto grande no primeiro quadro e falado. Ex.: "Esse prompt custou R$ 40 e não resolveu nada." |
| 2–10 s | O erro: prompt ruim, resultado ruim, **mostrado na tela e legível**. |
| 10–18 s | O conserto: prompt bom **escrito na tela**, resultado bom. O Claude diz em voz clara o que mudou. |
| 18–22 s | Fecho cético e engraçado, que fecha o laço do gancho. |
| 22–25 s | "Comenta PROMPT que eu te mando o texto pronto" (gera comentário) e "segue o perfil". |

Regras:
- Uma ideia por vídeo. Cortar tudo o que não serve ao antes e depois.
- Sem piada interna. Quem nunca viu o canal deve entender em 2 s.
- A dica tem de ser **verdadeira e verificável**. Se eu não tiver certeza de um comando, não entra.
- Tela em português, com o comando literal só quando ele precisa existir assim.
- Cortes mais rápidos: ninguém fica mais de 2 s no mesmo enquadramento sem mudar de zoom ou de elemento.

## 5. Cinco séries (rodízio)
- **A. Prompt de júnior x prompt de sênior** (60% do conteúdo). A série principal.
- **B. Quanto custou** (tokens e reais). O brasileiro é sensível a preço, e é o gancho mais forte que já tivemos ("não gasta token").
- **C. Mito ou verdade (IA para dev).** O Claude cético: "mostra o teste". Debate sem ataque a pessoas.
- **D. Dores de TI.** "Funciona na minha máquina", "deploy na sexta", "reunião que podia ser e-mail", "vaga júnior pedindo 5 anos". Resolve com 1 dica real.
- **E. Reação a Reels.** Usa o celular com os reels (já feito), mas só para desmontar um mito com prova, nunca como piada solta.

## 6. Doze roteiros (gancho, dica, fecho)
1. **Bug sem pista** (A). Gancho: "Arruma o bug." → "Qual bug?". Dica: contexto + erro + limite + prova. Fecho: "Um chute com ponto final custa o mesmo que um pedido bom."
2. **Funciona na minha máquina** (D). Dica: pedir ao Claude um **teste que falha** antes de corrigir. Fecho: "Se não reproduz, não é bug, é lenda."
3. **A IA inventou a biblioteca** (C). Dica: mandar "se não tiver certeza, diga que não sabe" e pedir o **arquivo e a linha** da resposta. Fecho: "Confia, mas roda."
4. **Contexto gigante** (B). Dica: `/compact` com instrução ("foque nos testes") para resumir a conversa. Mostrar o antes e depois em reais.
5. **Qual modelo usar** (B). Dica: `/model` para trocar de modelo conforme a tarefa. Fecho: "Não precisa do mais caro para renomear variável."
6. **Mencione o arquivo** (A). Dica: `@arquivo` para apontar o arquivo exato em vez de descrever. Fecho: "Eu não adivinho o seu projeto."
7. **Sexta 17h58** (D). Dica: pedir um plano antes de mexer (modo plano, Shift+Tab) e revisar. Fecho: "Quem aprova o diff na sexta jura que leu."
8. **Vaga júnior pedindo 5 anos** (D, tom irônico, sem atacar ninguém). Dica: usar o Claude para treinar entrevista técnica com critério ("aja como entrevistador, nota de 0 a 10 e justifique").
9. **PR de 3000 linhas** (A). Dica: pedir resumo do PR por arquivo e **os 3 riscos**. Fecho: "Mil e quinhentas linhas é formatação."
10. **"A IA vai acabar com o meu emprego"** (E/C). Claude cético: o que ela faz bem, o que não faz, e a diferença para quem escreve bom prompt. Sem alarme e sem promessa vazia.
11. **Retomar de onde parou** (A/B). Dica: `claude --resume` para escolher uma conversa anterior. Fecho com o gancho de academia, agora com valor.
12. **O prompt perfeito não existe** (C). Dica: pedir que o Claude **liste as suposições** antes de executar. Fecho: "Quem não declara suposição, herda a minha."

## 7. Três roteiros prontos (para aprovar antes de produzir)

**Roteiro 1: "Arruma o bug" (A)**
- Texto na tela, 1º quadro: "PROMPT DE JÚNIOR x PROMPT DE SÊNIOR"
- u: "Claude, arruma o bug." *(tela: o prompt)*
- c: "Qual bug?"
- u: "O que está dando erro."
- c: "Isso é um chute com ponto final." *(tela: resposta com 4 hipóteses vagas)*
- c: "Quatro hipóteses. Zero certezas. Você pagou por isso."
- c: "Agora o prompt de sênior." *(tela grande, linha a linha: "Erro: TypeError em pagamento.js, linha 42." / "Esperado: total em centavos." / "Rode: npm test." / "Não mexa em outros arquivos. Mostre o diff.")*
- c: "Erro, esperado, prova e limite. Quatro linhas." *(tela: diff de 2 linhas, testes passando)*
- u: "Era só isso?"
- c: "Salva esse vídeo. Comenta PROMPT que eu mando o texto. Segue a gente."

**Roteiro 2: "Funciona na minha máquina" (D)**
- Gancho: u: "Na minha máquina funciona." / c: "Na sua máquina tudo funciona, inclusive o que está quebrado."
- Dica: "Antes de corrigir, peça um teste que falha." *(tela: prompt "Escreva um teste que reproduza este erro. Só depois corrija.")*
- Resultado: teste vermelho → correção → teste verde.
- Fecho: "Se não reproduz, não é bug. É lenda."

**Roteiro 3: "A IA inventou a biblioteca" (C)**
- Gancho: u: "Claude, essa biblioteca não existe." / c: "Existe. Na minha cabeça."
- Dica: "Se não tiver certeza, diga que não sabe. Cite o arquivo e a linha."
- Resultado: o Claude responde "Não tenho certeza. Confirme na documentação."
- Fecho: "Confia, mas roda."

## 8. Plano de 14 dias (teste, não aposta)
- **Dias 1–2:** analisar os 6 vídeos (seção 9). Não postar nada até decidir.
- **Dias 3–14:** 1 vídeo por dia, 20–25 s, da série A, B e D em rodízio.
- **Testes:** mesmo roteiro com 2 ganchos diferentes em dias diferentes. Trocar um elemento por vez.
- **Capa e primeiro quadro:** texto grande com a promessa. O perfil fixa o melhor Reel e uma bio de uma linha ("Prompts que funcionam, para quem é de TI").
- **Comentários:** responder todos e transformar perguntas em roteiro (vira o próximo episódio).
- **Critério de decisão:** manter o formato que tiver melhor retenção de 3 s e mais salvamentos/envios por view. Cortar o resto.
- **Sem comprar seguidor ou seguir/deixar de seguir em massa.**

## 9. O que preciso de você
1. As métricas dos 6 Reels: views, **% que passou dos 3 s**, tempo médio assistido, curtidas, comentários, compartilhamentos, salvamentos.
2. Quais foram os 2 últimos e quais os 2 melhores.
3. Se a voz dos vídeos recebeu comentário (positivo ou negativo).
4. Seu objetivo: seguidores, clientes, afiliados do grupo de achadinhos ou autoridade em IA? Isso muda o fecho.
5. Quanto tempo por dia você tem para postar e responder comentários.

## 10. Limites honestos
- Não existe fórmula que garanta alcance. Posso aumentar a chance de retenção e de envio, mas não prometer números.
- A voz sintética e o visual são decisões suas. Se os dados mostrarem que a voz atrapalha, o caminho é testar uma voz melhor (por exemplo, a sua própria, gravada). Só faço isso com a sua autorização, e serviços externos de voz custam créditos.
- Não ouço o áudio. Se algo soar estranho, só você percebe.
