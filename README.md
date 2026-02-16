# awesome-cortexai

[Cortex AI](https://cortexai.com.tr) provider configs for [opencode](https://github.com/anomalyco/opencode).

## Quick Start

```bash
curl -fsSL https://opencode.ai/install | bash
cp opencode.json ~/.config/opencode/opencode.json
# Replace YOUR_CORTEX_API_KEY with your key
opencode
```

## Providers

| Provider | SDK | Thinking | Tool Call | Notes |
|----------|-----|----------|-----------|-------|
| **app.claude.gg** | `@ai-sdk/anthropic` | budgetTokens | Native | Full support, all Claude models |
| **beta.vertexapis.com** | `@ai-sdk/google` | thinkingConfig | Native | Full support, Gemini models |
| **claude.gg** | `@ai-sdk/anthropic` | budgetTokens | [Proxy](#tool-call-proxy) | Gateway strips tools from request |
| **beta.claude.gg** | `@ai-sdk/anthropic` | budgetTokens | [Proxy](#tool-call-proxy) | Gateway strips tools from request |
| **api.claude.gg** | `@ai-sdk/openai-compatible` | No (stripped) | [Proxy](#tool-call-proxy) | GPT-5, Grok-4, DeepSeek, Gemini etc. Gateway strips tool_calls + reasoning |
| **codex.claude.gg** | `@ai-sdk/openai-compatible` | - | Native | Requires [schema fix](#opencode-schema-bug) |
| **openai.vertexapis.com** | `@ai-sdk/openai-compatible` | - | Native | Requires [schema fix](#opencode-schema-bug) |

## Thinking

```bash
# Anthropic models
opencode run --thinking -m "app.claude.gg/claude-sonnet-4-5" --variant high "prompt"

# Gemini models
opencode run --thinking -m "beta.vertexapis.com/gemini-2.5-flash" --variant high "prompt"
```

Variants: `low`, `default`, `high`, `max`

## Tool Call Proxy

Some Cortex gateways strip tool calls from requests or responses. We solved this using [xml-toolcall-proxy](https://github.com/sametakofficial/xml-toolcall-proxy) — it moves tools into the system prompt as XML, the model responds with XML tool calls, and the proxy converts them back to native format.

Affected providers and what the proxy fixes:

| Provider | Problem | Proxy fixes it? |
|----------|---------|-----------------|
| claude.gg | Gateway removes `tools` array from request | Yes |
| beta.claude.gg | Gateway removes `tools` array from request | Yes |
| api.claude.gg | Gateway removes `tool_calls` from response | Yes (5 models tested) |

To use the proxy, point the provider's baseURL through it:

```json
"claude.gg": {
  "options": {
    "baseURL": "http://localhost:4012/claude.gg/v1"
  }
}
```

See the [xml-toolcall-proxy repo](https://github.com/sametakofficial/xml-toolcall-proxy) for setup instructions.

## Opencode Schema Bug

`codex.claude.gg` and `openai.vertexapis.com` return 400 on opencode v1.2.4 because the built-in `question` tool schema has `additionalProperties: false` but doesn't list all properties in `required`. Strict validators reject this.

We fixed it and opened a PR: [anomalyco/opencode#13738](https://github.com/anomalyco/opencode/pull/13738)

To use the fix now:

```bash
git clone -b fix/sanitize-tool-schemas https://github.com/sametakofficial/opencode.git
cd opencode && bun install
cd packages/opencode
bun run --conditions=browser ./src/index.ts  # runs from source, no build needed
```

## Web Search

Web search makes a huge difference — the model gets real-time internet context and gives much better answers. Two options:

### Brave Search MCP (recommended)

Best search quality. Free tier gives 1000 requests/day, or grab the $5/mo plan for more. Honestly worth it — the search results are noticeably better than free alternatives.

Tip: sign up with a virtual card for the $5 plan, then remove the card. Billing is end of month so you get a free month of premium search.

1. Get an API key at [brave.com/search/api](https://brave.com/search/api/)
2. Add to your `opencode.json`:

```json
"mcp": {
  "brave-search": {
    "command": "npx",
    "args": ["-y", "@anthropic-ai/brave-search-mcp"],
    "env": {
      "BRAVE_API_KEY": "YOUR_BRAVE_API_KEY"
    }
  }
}
```

### Exa Web Search (free, no API key)

opencode has a built-in web search tool. Just export one env variable:

```bash
# bash
echo 'export OPENCODE_ENABLE_EXA=1' >> ~/.bashrc && source ~/.bashrc

# zsh
echo 'export OPENCODE_ENABLE_EXA=1' >> ~/.zshrc && source ~/.zshrc
```

No signup, no API key. Not as good as Brave but works fine if you don't want to deal with accounts.

## Known Limits

- **api.claude.gg thinking** — gateway strips `reasoning_content`, no workaround
- **perplexity.claude.gg** — different format, incompatible with opencode

## Links

- [Cortex AI](https://cortexai.com.tr) · [Status](https://cortexai.com.tr/status)
- [opencode](https://github.com/anomalyco/opencode) · [PR #13738](https://github.com/anomalyco/opencode/pull/13738)
- [xml-toolcall-proxy](https://github.com/sametakofficial/xml-toolcall-proxy)
- [Detailed test report](rapor.html)
