#!/bin/bash
# VOLVER ATRÁS — deshace el play: revierte su commit en GitHub y Vercel vuelve a la landing anterior (~1 min).
#   bash tools/volver-atras.sh <commit que imprimió dar-play.sh>
# Igual que el play: trabaja en una copia temporal, nunca en la carpeta web-panama-LIVE.
set -euo pipefail

C="${1:?Falta el commit del play (lo imprimió dar-play.sh al final)}"
NUEVA="$(cd "$(dirname "$0")/.." && pwd)"
LIVE="$(cd "${PLAY_LIVE_DIR:-$NUEVA/../web-panama-LIVE}" && pwd)"   # PLAY_LIVE_DIR solo para ensayos

git -C "$LIVE" fetch -q origin
TMP="$(mktemp -d)/landing"
limpiar() { cd "$NUEVA"; git -C "$LIVE" worktree remove --force "$TMP" >/dev/null 2>&1 || rm -rf "$TMP"; git -C "$LIVE" worktree prune >/dev/null 2>&1 || true; }
trap limpiar EXIT
git -C "$LIVE" worktree add -q --detach "$TMP" origin/main
cd "$TMP"
git revert --no-edit "$C"
git push -q origin HEAD:main
cd "$NUEVA"
if [ "$(git -C "$LIVE" symbolic-ref --short HEAD 2>/dev/null || true)" = "main" ]; then
  git -C "$LIVE" merge -q --ff-only origin/main 2>/dev/null || echo "(la carpeta web-panama-LIVE quedó atrás de GitHub: hacer git pull cuando toque)"
fi
echo "Revertido en GitHub. Vercel vuelve a la landing anterior en ~1 min."
