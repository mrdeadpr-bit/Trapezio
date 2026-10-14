#!/bin/bash
# Prepara tudo para rodar a série em um computador novo (Claude Desktop/Code).  uso: ./setup.sh   (dentro de video/)
set -e
cd "$(dirname "$0")"
npm install --no-audit --no-fund                       # three@0.160.0 (package.json)
npm install --no-audit --no-fund playwright && npx playwright install chromium
pip install sherpa-onnx soundfile numpy praat-parselmouth
mkdir -p models && cd models
B=https://github.com/k2-fsa/sherpa-onnx/releases/download
for v in faber cadu jeff; do curl -L $B/tts-models/vits-piper-pt_BR-$v-medium.tar.bz2 | tar xj; done
curl -L $B/asr-models/sherpa-onnx-whisper-small.tar.bz2 | tar xj
echo "pronto. Use: PIPER_DIR=$PWD ASR_DIR=$PWD/sherpa-onnx-whisper-small  PLAYWRIGHT_PATH=\$(npm root)/playwright"
