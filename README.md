# awesome-cortexai

[Cortex AI](https://cortexai.com.tr) provider ayarları — [opencode](https://github.com/anomalyco/opencode) ile kullanım için.

Hazır config, proxy'ler ve bilinen sorunların çözümleri.

---

## Kurulum

### 1. opencode kur

```bash
# Linux / macOS
curl -fsSL https://opencode.ai/install | bash

# Windows (PowerShell)
irm https://opencode.ai/install.ps1 | iex
```

### 2. Config'i kopyala

```bash
# Linux / macOS
cp opencode.json ~/.config/opencode/opencode.json

# Windows (PowerShell)
Copy-Item opencode.json "$env:APPDATA\opencode\opencode.json"
```

### 3. API key'ini ayarla

`opencode.json` içindeki `YOUR_CORTEX_API_KEY` kısımlarını kendi Cortex API key'inle değiştir.

### 4. Çalıştır

```bash
opencode
```

---

## Provider ve Model Listesi

### app.claude.gg

SDK: `@ai-sdk/anthropic` · Tool Call: Native · Thinking: budgetTokens

| Model | Thinking Varyantları |
|-------|---------------------|
| claude-opus-4-6-20260101 | `high`, `max` |
| claude-opus-4-5-20251101 | `high`, `max` |
| claude-sonnet-4-5-20250929 | `high`, `max` |
| claude-sonnet-4-20250514 | `high`, `max` |
| claude-3-7-sonnet-20250219 | `high`, `max` |
| claude-haiku-4-5-20251001 | `high`, `max` |

### claude.gg

SDK: `@ai-sdk/anthropic` · Tool Call: [Proxy gerekli](#tool-call-proxy) · Thinking: budgetTokens

| Model | Thinking Varyantları |
|-------|---------------------|
| claude-opus-4-6 | `high`, `max` |
| claude-opus-4-5 | `high`, `max` |
| claude-sonnet-4-5 | `high`, `max` |
| claude-sonnet-4 | `high`, `max` |
| claude-3-7-sonnet | `high`, `max` |
| claude-haiku-4-5 | `high`, `max` |

### beta.claude.gg

SDK: `@ai-sdk/anthropic` · Tool Call: [Proxy gerekli](#tool-call-proxy) · Thinking: budgetTokens

| Model | Thinking Varyantları |
|-------|---------------------|
| claude-opus-4-1-20250805 | `high`, `max` |
| claude-sonnet-4-5-20250929 | `high`, `max` |
| claude-sonnet-4-5-web | `high`, `max` |

### api.claude.gg

SDK: `@ai-sdk/openai-compatible` · Tool Call: [Proxy gerekli](#tool-call-proxy) · Thinking: Gateway strip ediyor

| Model | Thinking Varyantları |
|-------|---------------------|
| gpt-5 | `low`, `medium`, `high` |
| gpt-5.1 | `low`, `medium`, `high` |
| gpt-5-mini | `minimal`, `low`, `medium`, `high` |
| gpt-5-nano | `minimal`, `low`, `medium`, `high` |
| gpt-o3 | `low`, `medium`, `high` |
| o3 | `low`, `medium`, `high` |
| o3-mini | `minimal`, `low`, `medium`, `high` |
| gpt-4.1 | - |
| gpt-4.1-nano | - |
| gpt-4o | - |
| gpt-4o-mini | - |
| grok-4 | - |
| grok-3-mini | - |
| grok-3-mini-beta | - |
| grok-2 | - |
| deepseek-r1 | - |
| deepseek-v3 | - |
| deepseek-chat | - |
| gemini-2.5-flash | - |
| gemini-2.5-pro | - |
| gemini-3-pro | - |
| gemini-2.0-flash | - |
| gemini-2.0-flash-lite | - |
| gemini-lite | - |
| gemini | - |

### beta.vertexapis.com

SDK: `@ai-sdk/google` · Tool Call: Native · Thinking: thinkingConfig

| Model | Thinking Varyantları |
|-------|---------------------|
| gemini-3-pro-preview | `low`, `high` |
| gemini-3-flash-preview | `low`, `medium`, `high` |
| gemini-2.5-pro | `low`, `high`, `max` |
| gemini-2.5-flash | `low`, `high`, `max` |
| gemini-2.5-flash-lite | `low`, `high`, `max` |
| gemini-2.0-flash | `minimal`, `low`, `medium`, `high` |
| gemini-2.0-flash-lite | `minimal`, `low`, `medium`, `high` |

### openai.vertexapis.com

SDK: `@ai-sdk/openai-compatible` · Tool Call: Native · Thinking: reasoning_effort
[Schema fix gerekli](#opencode-schema-bug)

| Model | Thinking Varyantları |
|-------|---------------------|
| gemini-3-pro-preview | `minimal`, `low`, `medium`, `high` |
| gemini-3-flash-preview | `minimal`, `low`, `medium`, `high` |
| gemini-2.5-pro | `minimal`, `low`, `medium`, `high` |
| gemini-2.5-flash | `minimal`, `low`, `medium`, `high` |
| gemini-2.5-flash-lite | `minimal`, `low`, `medium`, `high` |
| gemini-2.0-flash-001 | `minimal`, `low`, `medium`, `high` |
| gemini-2.0-flash-lite-001 | `minimal`, `low`, `medium`, `high` |

### codex.claude.gg

SDK: `@ai-sdk/openai-compatible` · Tool Call: Native · Thinking: reasoning_effort
[Schema fix gerekli](#opencode-schema-bug)

| Model | Thinking Varyantları |
|-------|---------------------|
| gpt-5.3-codex | `low`, `medium`, `high`, `xhigh` |
| gpt-5.2-codex | `low`, `medium`, `high`, `xhigh` |
| gpt-5.1-codex-max | `low`, `medium`, `high`, `xhigh` |
| gpt-5.2 | `low`, `medium`, `high`, `xhigh` |
| gpt-5.1-codex | `low`, `medium`, `high` |
| gpt-5.1 | `low`, `medium`, `high` |
| gpt-5-codex | `low`, `medium`, `high` |
| gpt-5 | `low`, `medium`, `high` |
| gpt-5.1-codex-mini | `low`, `medium`, `high` |
| gpt-5-codex-mini | `low`, `medium`, `high` |

### perplexity.claude.gg

SDK: `@ai-sdk/openai-compatible` · [Perplexity Proxy gerekli](#perplexity-proxy)

| Model | Thinking Varyantları |
|-------|---------------------|
| sonar | - |
| sonar-pro | - |
| unlimited-ai | - |

---

## Thinking Kullanımı

```bash
# Anthropic (Sonnet, Opus 4.5 vs.) — high, max
opencode run --thinking -m "app.claude.gg/claude-sonnet-4-5" --variant high "prompt"

# Anthropic (Opus 4.6) — low, medium, high, max
opencode run --thinking -m "app.claude.gg/claude-opus-4-6" --variant low "prompt"

# Gemini 2.5 — low, high, max
opencode run --thinking -m "beta.vertexapis.com/gemini-2.5-flash" --variant high "prompt"

# Gemini 3 — low, high (flash'ta ek olarak medium)
opencode run --thinking -m "beta.vertexapis.com/gemini-3-flash-preview" --variant high "prompt"

# Codex — low, medium, high (5.2+ modellerde xhigh)
opencode run --thinking -m "codex.claude.gg/gpt-5.3-codex" --variant xhigh "prompt"
```

Codex modelleri `reasoning_effort` parametresini kabul ediyor — model gerçekten daha fazla düşünüyor (`high` ile ~3x daha fazla token) ama gateway `reasoning_content`'i strip ediyor, düşünce metni response'ta görünmüyor.

openai.vertexapis.com Gemini modelleri `reasoning_effort` destekliyor ve çalışıyor — `high` ile default'a göre ~4x daha fazla reasoning token üretiyor.

---

## Bilinen Sorunlar ve Çözümleri

### Tool Call Proxy

Bazı Cortex gateway'leri tool call'ları request veya response'tan siliyor. [xml-toolcall-proxy](https://github.com/sametakofficial/xml-toolcall-proxy) bunu çözüyor — tool'ları system prompt'a XML olarak inject ediyor, model XML tool call yazıyor, proxy bunu native formata çeviriyor.

| Provider | Sorun | Proxy çözüyor mu? |
|----------|-------|-------------------|
| claude.gg | Gateway `tools` array'ini request'ten siliyor | Evet |
| beta.claude.gg | Gateway `tools` array'ini request'ten siliyor | Evet |
| api.claude.gg | Gateway `tool_calls`'ı response'tan siliyor | Evet (5 model test edildi) |

Kullanmak için provider'ın baseURL'sini proxy'ye yönlendir:

```json
"claude.gg": {
  "options": {
    "baseURL": "http://localhost:4012/claude.gg/v1"
  }
}
```

Kurulum için [xml-toolcall-proxy repo](https://github.com/sametakofficial/xml-toolcall-proxy)'suna bak.

### Opencode Schema Bug

`codex.claude.gg` ve `openai.vertexapis.com` opencode v1.2.4'te 400 hatası veriyor. Sebebi: built-in `question` tool schema'sında `additionalProperties: false` var ama tüm property'ler `required`'da listelenmiyor. Strict validator'lar bunu reddediyor.

Bunu düzelten açık bir PR var: [anomalyco/opencode#13823](https://github.com/anomalyco/opencode/pull/13823) — codex ve vertex ile test edildi, çalışıyor.

**Seçenek 1: PR'ı source'dan kullan**

```bash
gh pr checkout 13823 --repo anomalyco/opencode
bun install
cd packages/opencode
bun run --conditions=browser ./src/index.ts
```

**Seçenek 2: Schema Fixer Proxy**

Repo'daki `schema-fixer-proxy.mjs` — ~70 satırlık minimal proxy, tool schema'larını anında düzeltiyor. Bağımlılık yok.

```bash
node schema-fixer-proxy.mjs  # localhost:4015'te başlar
```

```json
"codex.claude.gg": {
  "options": { "baseURL": "http://localhost:4015/codex.claude.gg/v1" }
},
"openai.vertexapis.com": {
  "options": { "baseURL": "http://localhost:4015/openai.vertexapis.com/v1" }
}
```

PR merge olunca direkt URL'lere geri dönebilirsin.

### api.claude.gg Thinking Strip

Gateway `reasoning_content`'i response'tan siliyor. Streaming ve non-streaming test edildi, DeepSeek R1 `<think>` tag'leri de yok. Çözüm yok — gateway seviyesinde kısıtlama.

### Perplexity Proxy

`perplexity.claude.gg` farklı bir API formatı kullanıyor (search endpoint). Repo'daki `perplexity-proxy.py` bunu OpenAI Chat Completions formatına çeviriyor.

```bash
pip install flask requests
python perplexity-proxy.py  # localhost:4016'da başlar
```

```json
"perplexity.claude.gg": {
  "npm": "@ai-sdk/openai-compatible",
  "options": {
    "baseURL": "http://localhost:4016/v1",
    "apiKey": "YOUR_CORTEX_API_KEY"
  },
  "models": {
    "sonar": { "tool_call": false },
    "sonar-pro": { "tool_call": false },
    "unlimited-ai": { "tool_call": false }
  }
}
```

---

## Web Arama

Web arama ciddi fark yaratıyor — model gerçek zamanlı internet bağlamı kazanıyor ve çok daha iyi cevaplar veriyor.

### Brave Search MCP (önerilen)

En iyi arama kalitesi. Ücretsiz plan günde 1000 istek, $5/ay plan ile daha fazla. Gerçekten değer — arama sonuçları ücretsiz alternatiflere göre fark edilir derecede daha iyi.

İpucu: sanal kartla $5'lık plana kaydol, sonra kartı kaldır. Fatura ay sonunda kesildiği için bir ay ücretsiz premium arama kullanmış olursun.

1. [brave.com/search/api](https://brave.com/search/api/) adresinden API key al
2. `opencode.json`'a ekle:

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

### Exa Web Search (ücretsiz, API key gerekmez)

opencode'un built-in web arama tool'u var. Tek bir env değişkeni export et:

```bash
# Linux / macOS (bash)
echo 'export OPENCODE_ENABLE_EXA=1' >> ~/.bashrc && source ~/.bashrc

# Linux / macOS (zsh)
echo 'export OPENCODE_ENABLE_EXA=1' >> ~/.zshrc && source ~/.zshrc

# Windows (PowerShell — kalıcı)
[System.Environment]::SetEnvironmentVariable('OPENCODE_ENABLE_EXA', '1', 'User')
# Yeni terminal aç
```

Kayıt yok, API key yok. Brave kadar iyi değil ama hesap açmak istemiyorsan işini görür.

---

## Linkler

- [Cortex AI](https://cortexai.com.tr) · [Status](https://cortexai.com.tr/status)
- [opencode](https://github.com/anomalyco/opencode) · [Schema Fix PR #13823](https://github.com/anomalyco/opencode/pull/13823)
- [xml-toolcall-proxy](https://github.com/sametakofficial/xml-toolcall-proxy)
