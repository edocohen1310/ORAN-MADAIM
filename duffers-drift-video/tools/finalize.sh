#!/bin/bash
# Finish the HyperFrames render: loudness to -16 LUFS (two-pass loudnorm), a 1080p
# file small enough for GitHub (<100 MB) and a lighter 720p copy for phones.
# Usage: tools/finalize.sh [out/render-raw.mp4]
set -euo pipefail
cd "$(dirname "$0")/.."
IN=${1:-out/render-raw.mp4}

stats=$(ffmpeg -hide_banner -nostats -i "$IN" -map 0:a -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
get() { echo "$stats" | python3 -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
LN="loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true"

ffmpeg -hide_banner -v error -stats -y -i "$IN" -map 0:v -map 0:a \
  -c:v libx264 -preset medium -crf 24 -pix_fmt yuv420p -movflags +faststart \
  -af "$LN" -c:a aac -b:a 128k -ar 48000 out/duffers-drift.mp4

ffmpeg -hide_banner -v error -stats -y -i out/duffers-drift.mp4 -map 0:v -map 0:a \
  -vf scale=1280:720:flags=lanczos -c:v libx264 -preset medium -crf 26 -pix_fmt yuv420p -movflags +faststart \
  -c:a copy out/duffers-drift-720p.mp4

ls -la out/duffers-drift.mp4 out/duffers-drift-720p.mp4
