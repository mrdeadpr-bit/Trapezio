#!/bin/bash
# Renderiza uma lista de episódios em sequência; cria work/<ep>/done ao terminar cada um.   uso: ./queue.sh ep1 ep2 ...
cd "$(dirname "$0")"
for ep in "$@"; do
  rm -f work/$ep/done; SC=$(python3 -c "from episodes import EPISODES; print(EPISODES['$ep']['scene'])"); ./run_ep.sh $ep $SC > work/$ep/run.log 2>&1
  [ -f $ep.mp4 ] && touch work/$ep/done
done
