#!/bin/bash
# espera um episódio terminar (até ~9 min por chamada) e mostra o progresso
cd "$(dirname "$0")"; EP=$1
T=$(python3 -c "import json;print(int(json.loads(open('scene/$EP.timeline.js').read()[17:-1])['total']*24))")
for i in $(seq 1 54); do [ -f work/$EP/done ] && break; sleep 10; done
echo "$EP: $(ls work/$EP/frames 2>/dev/null | wc -l)/$T $( [ -f work/$EP/done ] && echo PRONTO)"
