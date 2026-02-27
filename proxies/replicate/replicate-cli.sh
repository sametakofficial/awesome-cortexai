#!/bin/bash
# Replicate CLI - metadata from Replicate, predictions from Gate AI
# Requires: GATEAI_API_TOKEN and REPLICATE_API_TOKEN env vars
GATEAI_TOKEN="${GATEAI_API_TOKEN:-}"
REPLICATE_TOKEN="${REPLICATE_API_TOKEN:-}"
GATE="https://api.gateai.app/v1"
REPL="https://api.replicate.com/v1"

case "$1" in
  search)
    curl -s -X QUERY -H "Authorization: Bearer $REPLICATE_TOKEN" -H "Content-Type: text/plain" -d "$2" "$REPL/models" | python3 -c "
import sys,json
d=json.load(sys.stdin)
for r in d.get('results',[]):
    print(f\"{r['owner']}/{r['name']} | {r.get('description','')[:120]} | runs:{r.get('run_count',0)}\")
" 2>/dev/null
    ;;
  info)
    curl -s -H "Authorization: Bearer $REPLICATE_TOKEN" "$REPL/models/$2" 2>/dev/null
    ;;
  schema)
    curl -s -H "Authorization: Bearer $REPLICATE_TOKEN" "$REPL/models/$2" | python3 -c "
import sys,json
d=json.load(sys.stdin)
v=d.get('latest_version',{})
s=v.get('openapi_schema',{}).get('components',{}).get('schemas',{}).get('Input',{}).get('properties',{})
print(f\"Model: {d['owner']}/{d['name']}\")
print(f\"Description: {d.get('description','')}\")
print(f\"Runs: {d.get('run_count',0)}\")
print('Input schema:')
for k,v in s.items():
    t=v.get('type','')
    desc=v.get('description','')[:80]
    default=v.get('default','')
    print(f'  {k} ({t}): {desc} [default: {default}]')
" 2>/dev/null
    ;;
  run)
    MODEL="$2"
    INPUT="$3"
    curl -s -X POST -H "Authorization: Bearer $GATEAI_TOKEN" -H "Content-Type: application/json" \
      -d "{\"input\":$INPUT}" "$GATE/models/$MODEL/predictions" 2>/dev/null
    ;;
  status)
    curl -s -H "Authorization: Bearer $GATEAI_TOKEN" "$GATE/predictions/$2" 2>/dev/null
    ;;
  poll)
    ID="$2"
    for i in $(seq 1 30); do
      R=$(curl -s -H "Authorization: Bearer $GATEAI_TOKEN" "$GATE/predictions/$ID" 2>/dev/null)
      S=$(echo "$R" | python3 -c "import sys,json;print(json.load(sys.stdin).get('status',''))" 2>/dev/null)
      if [ "$S" = "succeeded" ] || [ "$S" = "failed" ] || [ "$S" = "canceled" ]; then
        echo "$R"
        exit 0
      fi
      sleep 2
    done
    echo "$R"
    ;;
  account)
    curl -s -H "Authorization: Bearer $REPLICATE_TOKEN" "$REPL/account" 2>/dev/null
    ;;
  collections)
    curl -s -H "Authorization: Bearer $REPLICATE_TOKEN" "$REPL/collections" 2>/dev/null
    ;;
  collection)
    curl -s -H "Authorization: Bearer $REPLICATE_TOKEN" "$REPL/collections/$2" 2>/dev/null
    ;;
  *)
    echo "Usage: replicate <command> [args]"
    echo ""
    echo "Metadata (Replicate - free):"
    echo "  search <query>        Search models"
    echo "  info <owner/model>    Get model details (JSON)"
    echo "  schema <owner/model>  Get model input schema (readable)"
    echo "  account               Account info"
    echo "  collections           List collections"
    echo "  collection <slug>     Get collection details"
    echo ""
    echo "Predictions (Gate AI - paid):"
    echo "  run <owner/model> '{\"key\":\"val\"}'   Create prediction"
    echo "  status <prediction-id>               Check prediction status"
    echo "  poll <prediction-id>                 Poll until complete"
    ;;
esac
