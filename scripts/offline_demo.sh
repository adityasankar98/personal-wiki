#!/usr/bin/env bash
# Offline demonstration: run with Wi-Fi OFF. Records proof of no network, device specs,
# then a fresh CLI process for every step: help, ingest, the four ask tests, search,
# chat mode checks, the ask-vs-chat separation check, and `wiki check`.
#
#   script -q evidence/offline/terminal.txt bash scripts/offline_demo.sh
set -u
cd "$(dirname "$0")/.."
step() { printf '\n\033[1m$ %s\033[0m\n' "$*"; "$@"; }

echo "=== Offline demo · $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "=== Network proof"
networksetup -getairportpower en0 2>/dev/null || true
if route -n get default >/dev/null 2>&1; then echo "default route: PRESENT"; else echo "default route: none (no network)"; fi
if curl -sS -m 5 -o /dev/null https://huggingface.co 2>/tmp/curl_err; then
  echo "ABORT: huggingface.co is reachable. Turn Wi-Fi off and rerun."; exit 1
else
  echo "curl https://huggingface.co -> FAILED as expected: $(head -1 /tmp/curl_err)"
fi

echo; echo "=== Device"
sw_vers | tr '\n' ' '; echo
echo "chip: $(sysctl -n machdep.cpu.brand_string) · cores: $(sysctl -n hw.ncpu) · unified memory: $(( $(sysctl -n hw.memsize) / 1073741824 )) GB"
echo "memory now: $(memory_pressure | tail -1)"
echo "free disk: $(df -h . | awk 'NR==2 {print $4}')"
echo "python: $(.venv/bin/python --version) · mlx-vlm $(.venv/bin/pip show mlx-vlm 2>/dev/null | awk '/^Version/ {print $2}')"

step ./wiki --help
step ./wiki ingest "vault/raw/Pac-Man DQN README.md"
step ./wiki eval --label offline
step ./wiki search "reward clipping" --save
step ./wiki search "workshop catering budget"

echo; echo "=== Chat mode checks (scripted input, fresh process)"
printf '%s\n' \
  "what can we do?" \
  "what can you help me with?" \
  "Draft a 3-step plan to study for my next class." \
  "make that shorter" \
  "/save study plan" \
  "By the way, my Pac-Man agent won a class prize." \
  "What learning rate did I use for the Pac-Man agent?" \
  "/notes reward clipping" \
  "/sources" \
  "/exit" | ./wiki chat --transcript evidence/offline/chat-mode-checks.md

echo; echo "=== Ask must ignore the chat-only claim (fresh process, no history)"
step ./wiki ask "Did my Pac-Man agent win a class prize?" --save
step ./wiki check
echo; echo "=== Offline demo finished · $(date '+%H:%M:%S')"
