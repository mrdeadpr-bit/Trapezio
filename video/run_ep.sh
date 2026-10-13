#!/bin/bash
# Renderiza um episódio e monta o MP4.   uso: ./run_ep.sh <episodio> [cena]
# pré-requisitos: make_audio.py já rodou com EP=<episodio> (gera work/<ep>/mix.wav e scene/<ep>.timeline.js)
EP=$1; SCENE=${2:-couch}; cd "$(dirname "$0")"
export EP SCENE PLAYWRIGHT_PATH=${PLAYWRIGHT_PATH:-/opt/node22/lib/node_modules/playwright}
N=$(python3 -c "import json;print(int(json.loads(open('scene/$EP.timeline.js').read()[17:-1])['total']*24))")
[ -z "$RESUME" ] && rm -rf work/$EP/frames
for i in 0 1 2 3; do a=$((i*N/4)); b=$(((i+1)*N/4)); node render.js $a $b > work/$EP/r$i.log 2>&1 & done
wait
ffmpeg -y -loglevel error -framerate 24 -i work/$EP/frames/f%05d.jpg -i work/$EP/mix.wav -c:v libx264 -preset slow -crf 22 -maxrate 6M -bufsize 12M -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart $EP.mp4
echo "frames: $(ls work/$EP/frames | wc -l)/$N"; ls -la $EP.mp4
