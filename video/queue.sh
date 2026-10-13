#!/bin/bash
# Renderiza uma lista de episódios em sequência; cria work/<ep>/done ao terminar cada um.   uso: ./queue.sh ep1 ep2 ...
cd "$(dirname "$0")"
for ep in "$@"; do
  rm -f work/$ep/done; ./run_ep.sh $ep couch > work/$ep/run.log 2>&1
  [ -f $ep.mp4 ] && touch work/$ep/done
done
