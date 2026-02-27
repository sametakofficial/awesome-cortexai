#!/bin/bash
# Replicate MCP wrapper - starts proxy then MCP
# Proxy routes: predictions -> Gate AI, metadata -> Replicate

DIR="$(cd "$(dirname "$0")" && pwd)"

export GATEAI_API_TOKEN="${GATEAI_API_TOKEN:-}"
export REPLICATE_API_TOKEN="${REPLICATE_API_TOKEN:-}"
PROXY_PORT="${PROXY_PORT:-9877}"

# Start proxy in background
node "$DIR/proxy.js" &
PROXY_PID=$!
sleep 1

# Cleanup on exit
cleanup() {
  kill $PROXY_PID 2>/dev/null
  wait $PROXY_PID 2>/dev/null
}
trap cleanup EXIT INT TERM

# Run MCP with proxy as base URL
export REPLICATE_BASE_URL="http://127.0.0.1:${PROXY_PORT}/v1"
export REPLICATE_API_TOKEN="proxy-handled"
npx -y replicate-mcp "$@"
