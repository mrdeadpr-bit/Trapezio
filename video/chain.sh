#!/bin/bash
cd "$(dirname "$0")"
export PLAYWRIGHT_PATH=/opt/node22/lib/node_modules/playwright EP=vps SCENE=couch
B=192; Q=$((B/4))
for i in 0 1 2 3; do a=$((i*Q)); b=$(((i+1)*Q)); [ $i -eq 3 ] && b=$B; node render.js $a $b > work/vps/fix_$i.log 2>&1 & done; wait
ffmpeg -y -loglevel error -framerate 24 -i work/vps/frames/f%05d.jpg -i work/vps/mix.wav -c:v libx264 -preset slow -crf 22 -maxrate 6M -bufsize 12M -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart vps.mp4 && touch work/vps/fixed
./queue.sh cowork ban link prompt sol
