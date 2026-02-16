#!/usr/bin/env python3
"""Perplexity Search → OpenAI Chat Completions proxy."""

import json
import time
import os
import requests
from flask import Flask, request, Response, jsonify

CORTEX_BASE = "https://perplexity.claude.gg/v1/search"
API_KEY = os.environ.get("PERPLEXITY_PROXY_KEY", "sk-0f2246e77aa642cfafd6c4b0dd5fe14d")
PORT = int(os.environ.get("PERPLEXITY_PROXY_PORT", "4016"))

app = Flask(__name__)


def extract_query(messages):
    for m in reversed(messages):
        if m.get("role") == "user":
            return m["content"]
    return messages[-1]["content"] if messages else ""


def format_results(results, query):
    if not results:
        return f'No search results found for: "{query}"'
    lines = [f'Here are the search results for: "{query}"\n']
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r.get('title', '')}")
        lines.append(f"    URL: {r.get('url', '')}")
        lines.append(f"    {r.get('snippet', '')}")
        if r.get("date"):
            lines.append(f"    Date: {r['date']}")
        lines.append("")
    return "\n".join(lines).strip()


def make_response_json(content, model):
    return {
        "id": f"chatcmpl-{int(time.time() * 1000)}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }


@app.route("/v1/models", methods=["GET"])
@app.route("/models", methods=["GET"])
def models():
    return jsonify(
        {
            "object": "list",
            "data": [
                {
                    "id": "sonar",
                    "object": "model",
                    "created": 1700000000,
                    "owned_by": "perplexity",
                },
                {
                    "id": "sonar-pro",
                    "object": "model",
                    "created": 1700000000,
                    "owned_by": "perplexity",
                },
                {
                    "id": "unlimited-ai",
                    "object": "model",
                    "created": 1700000000,
                    "owned_by": "perplexity",
                },
            ],
        }
    )


@app.route("/v1/chat/completions", methods=["POST"])
@app.route("/chat/completions", methods=["POST"])
def chat_completions():
    body = request.get_json(force=True)
    query = extract_query(body.get("messages", []))
    model = body.get("model", "sonar")
    is_stream = body.get("stream", False)

    # Cortex search
    try:
        res = requests.post(
            CORTEX_BASE,
            json={"query": query, "max_results": 10},
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}",
            },
            timeout=30,
        )
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        return jsonify({"error": f"Cortex search error: {e}"}), 502

    content = format_results(data.get("results", []), query)

    if is_stream:
        cid = f"chatcmpl-{int(time.time() * 1000)}"

        def generate():
            chunk = {
                "id": cid,
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": model,
                "choices": [
                    {
                        "index": 0,
                        "delta": {"role": "assistant", "content": content},
                        "finish_reason": None,
                    }
                ],
            }
            yield f"data: {json.dumps(chunk)}\n\n"
            done = {
                "id": cid,
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": model,
                "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
            }
            yield f"data: {json.dumps(done)}\n\n"
            yield "data: [DONE]\n\n"

        return Response(
            generate(),
            mimetype="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
        )

    return jsonify(make_response_json(content, model))


@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "proxy": "perplexity-search-to-chat"})


if __name__ == "__main__":
    print(f"Perplexity proxy running on http://127.0.0.1:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False)
