#!/bin/bash
cd /home/user/Me-editing/viral-short
B=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
rm -rf /tmp/claude-0/vbundle; npx remotion bundle src/index.ts --out-dir=/tmp/claude-0/vbundle --log=error >/dev/null 2>&1
mkdir -p out/final
for id in tvgoat2 tvsign; do
  npx remotion render /tmp/claude-0/vbundle Guess-$id out/raw_$id.mp4 --concurrency=4 --browser-executable=$B --log=error || { echo "RENDERFAIL $id"; continue; }
  J=$(ffmpeg -hide_banner -i out/raw_$id.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
  g(){ echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
  ffmpeg -v error -y -i out/raw_$id.mp4 -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true" -ar 48000 -c:a aac -b:a 192k -map_metadata -1 out/final/$id.mp4
  rm out/raw_$id.mp4; echo "DONE $id"; bash /home/user/Me-editing/.work/qc.sh out/final/$id.mp4
done
echo ALLDONE
