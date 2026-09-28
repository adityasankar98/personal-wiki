#!/usr/bin/env bash
# Waits until the internet is unreachable, then records the offline demo.
# Start it while online, turn Wi-Fi off, wait for DONE, turn Wi-Fi back on.
cd "$(dirname "$0")/.."
mkdir -p evidence/offline
echo "Waiting for the network to go down... turn Wi-Fi OFF now."
while curl -s -m 3 -o /dev/null https://huggingface.co; do sleep 2; done
echo "Network is down. Starting the recorded offline demo (about 3 minutes)..."
sleep 3
script -q evidence/offline/terminal.txt bash scripts/offline_demo.sh
echo
echo "=================================================================="
echo " DONE. Take a screenshot now (Wi-Fi icon + this terminal visible),"
echo " then turn Wi-Fi back ON and tell Claude 'done'."
echo "=================================================================="
