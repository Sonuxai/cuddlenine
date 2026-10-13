#!/bin/sh
# Idempotent preview start. Probe first; only boot what is down.
if curl -sf -o /dev/null --max-time 1 http://127.0.0.1:8080/; then
  exit 0
fi
cd /workspace
npm run dev >/tmp/vite-dev.log 2>&1 &
exit 0
