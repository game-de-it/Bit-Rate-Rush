#!/bin/sh
# plumOS-Bubble 実機へ転送して実行する。
#   ./deploy_bubble.sh              転送のみ
#   ./deploy_bubble.sh run          転送してゲーム起動 (FE を止めて実行、終了後 FE 復帰)
#   ./deploy_bubble.sh bench stress 転送して負荷計測 (stress|run) → 結果を表示
set -eu
HOST="${BUBBLE_HOST:-192.168.10.101}"
: "${SSHPASS:?SSHPASS=<password> を環境変数で指定してください}"
export SSHPASS
REMOTE=/storage/user/Roms/pyxel/Bit-Rate-Rush
SSH="sshpass -e ssh -o StrictHostKeyChecking=no root@$HOST"
SCP="sshpass -e scp -o StrictHostKeyChecking=no"
HERE="$(cd "$(dirname "$0")" && pwd)"

find "$HERE" -name __pycache__ -type d -prune -exec rm -rf {} +
$SSH "mkdir -p $REMOTE"
$SCP -r "$HERE"/*.py "$HERE"/assets "$HERE"/core "$HERE"/data "$HERE"/entities "$HERE"/scenes "$HERE"/systems "$HERE"/ui "root@$HOST:$REMOTE/"
echo "copied to $HOST:$REMOTE"

case "${1:-}" in
  run)
    $SSH "sh /storage/plumos/bin/plumos-portmaster-frontend-control acquire; \
          sh /storage/plumos/bin/plumos-pyxel-bubble-launch $REMOTE/main.py; \
          sh /storage/plumos/bin/plumos-portmaster-frontend-control release"
    ;;
  bench)
    MODE="${2:-stress}"; SEC="${3:-40}"
    $SSH "sh /storage/plumos/bin/plumos-portmaster-frontend-control acquire; \
          echo '=== bench $MODE' >> /storage/plumos/logs/pyxel/runtime.log; \
          sh /storage/plumos/bin/plumos-pyxel-bubble-launch $REMOTE/bench.py $MODE $SEC; \
          sh /storage/plumos/bin/plumos-portmaster-frontend-control release; \
          grep '\[bench\]' /storage/plumos/logs/pyxel/runtime.log | tail -n 20"
    ;;
esac
