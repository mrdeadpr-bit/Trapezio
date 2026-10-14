#!/bin/bash
cd /home/user/Trapezio/video
for ep in "$@"; do EP=$ep PIPER_DIR=/tmp/claude-0/-home-user-Trapezio/7ccc3705-e889-550f-a19f-47fc4ee2c724/scratchpad/piper ASR_DIR=/tmp/claude-0/-home-user-Trapezio/7ccc3705-e889-550f-a19f-47fc4ee2c724/scratchpad/asr/sherpa-onnx-whisper-small BEST_OF=10 python3 make_audio.py 2>&1 | grep "fala\|OK\|Error\|Trace" | grep -v sherpa > work/$ep/audio.log; touch work/$ep/audio.done; done
