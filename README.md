# awesome-cortexai

[Cortex AI](https://cortexai.com.tr) provider ayarları — [opencode](https://github.com/anomalyco/opencode) ile kullanım için.

Hazır config, proxy'ler ve bilinen sorunların çözümleri.

---

## Kurulum

### Gereksinimler

- [Node.js](https://nodejs.org/) v18+ (proxy'ler ve MCP için)
  - Linux: `curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - && sudo apt install -y nodejs`
  - macOS: `brew install node` veya [nodejs.org](https://nodejs.org/) adresinden indir
  - Windows: [nodejs.org](https://nodejs.org/) adresinden indir veya `winget install OpenJS.NodeJS`

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
mkdir -p ~/.config/opencode
cp opencode.json ~/.config/opencode/opencode.json

# Windows (PowerShell)
New-Item -ItemType Directory -Force "$env:APPDATA\opencode"
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

| Model | Thinking Varyantları | Tool Call |
|-------|---------------------|-----------|
| claude-opus-4-6-20260101 | `high`, `max` | Native |
| claude-opus-4-5-20251101 | `high`, `max` | Native |
| claude-sonnet-4-5-20250929 | `high`, `max` | Native |
| claude-sonnet-4-20250514 | `high`, `max` | Native |
| claude-3-7-sonnet-20250219 | `high`, `max` | Native |
| claude-haiku-4-5-20251001 | `high`, `max` | Native |

### claude.gg

SDK: `@ai-sdk/anthropic` · Tool Call: [Proxy gerekli](#tool-call-proxy) · Thinking: budgetTokens

| Model | Thinking Varyantları | Tool Call |
|-------|---------------------|-----------|
| claude-opus-4-6 | `high`, `max` | Proxy |
| claude-opus-4-5 | `high`, `max` | Proxy |
| claude-sonnet-4-5 | `high`, `max` | Proxy |
| claude-sonnet-4 | `high`, `max` | Proxy |
| claude-3-7-sonnet | `high`, `max` | Proxy |
| claude-haiku-4-5 | `high`, `max` | Proxy |

### beta.claude.gg

SDK: `@ai-sdk/anthropic` · Tool Call: [Proxy gerekli](#tool-call-proxy) · Thinking: budgetTokens

| Model | Thinking Varyantları | Tool Call |
|-------|---------------------|-----------|
| claude-opus-4-1-20250805 | `high`, `max` | Proxy |
| claude-sonnet-4-5-20250929 | `high`, `max` | Proxy |
| claude-sonnet-4-5-web | `high`, `max` | Proxy |

### api.claude.gg

SDK: `@ai-sdk/openai-compatible` · Tool Call: [Proxy gerekli](#tool-call-proxy) · Thinking: reasoning_effort (gateway strip ediyor)

Tüm modeller `reasoning_effort` parametresini kabul ediyor (`minimal` `low` `medium` `high` `xhigh`). Model daha fazla düşünüyor ama gateway `reasoning_content`'i, `reasoning_tokens`'ı ve `tool_calls`'ı strip ediyor. Tool call için [xml-toolcall-proxy](#tool-call-proxy) gerekli.

| Model | Thinking Varyantları | Tool Call |
|-------|---------------------|-----------|
| gpt-5 | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| gpt-5.1 | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| gpt-5-mini | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| gpt-5-nano | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| gpt-o3 | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| o3 | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| o3-mini | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| gpt-4.1 | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| gpt-4.1-nano | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| gpt-4o | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| gpt-4o-mini | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| grok-4 | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| grok-3-mini | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| grok-3-mini-beta | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| grok-2 | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| deepseek-r1 | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| deepseek-v3 | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| deepseek-chat | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| gemini-2.5-flash | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| gemini-2.0-flash | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| gemini-2.0-flash-lite | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |
| gemini-lite | `minimal`, `low`, `medium`, `high`, `xhigh` | Proxy |

### beta.vertexapis.com

SDK: `@ai-sdk/google` · Tool Call: Native · Thinking: thinkingConfig

| Model | Thinking Varyantları | Tool Call |
|-------|---------------------|-----------|
| gemini-3-pro-preview | `low`, `high` | Native |
| gemini-3-flash-preview | `low`, `medium`, `high` | Native |
| gemini-2.5-pro | `low`, `high`, `max` | Native |
| gemini-2.5-flash | `low`, `high`, `max` | Native |
| gemini-2.5-flash-lite | `low`, `high`, `max` | Native |
| gemini-2.0-flash | `minimal`, `low`, `medium`, `high` | Native |
| gemini-2.0-flash-lite | `minimal`, `low`, `medium`, `high` | Native |

### openai.vertexapis.com

SDK: `@ai-sdk/openai-compatible` · Tool Call: Native · Thinking: reasoning_effort
[Schema fix gerekli](#opencode-schema-bug)

`reasoning_effort` çalışıyor — `high` ile default'a göre ~4x daha fazla reasoning token üretiyor.

| Model | Thinking Varyantları | Tool Call |
|-------|---------------------|-----------|
| gemini-3-pro-preview | `minimal`, `low`, `medium`, `high` | Native* |
| gemini-3-flash-preview | `minimal`, `low`, `medium`, `high` | Native* |
| gemini-2.5-pro | `minimal`, `low`, `medium`, `high` | Native* |
| gemini-2.5-flash | `minimal`, `low`, `medium`, `high` | Native* |
| gemini-2.5-flash-lite | `minimal`, `low`, `medium`, `high` | Native* |
| gemini-2.0-flash-001 | `minimal`, `low`, `medium`, `high` | Native* |
| gemini-2.0-flash-lite-001 | `minimal`, `low`, `medium`, `high` | Native* |

\* [Schema fix](#opencode-schema-bug) gerekli

### codex.claude.gg

SDK: `@ai-sdk/openai-compatible` · Tool Call: Native · Thinking: reasoning_effort
[Schema fix gerekli](#opencode-schema-bug)

`reasoning_effort` çalışıyor — model daha fazla düşünüyor (`high` ile ~3x daha fazla token) ama gateway `reasoning_content`'i strip ediyor.

| Model | Thinking Varyantları | Tool Call |
|-------|---------------------|-----------|
| gpt-5.3-codex | `low`, `medium`, `high`, `xhigh` | Native* |
| gpt-5.2-codex | `low`, `medium`, `high`, `xhigh` | Native* |
| gpt-5.1-codex-max | `low`, `medium`, `high`, `xhigh` | Native* |
| gpt-5.2 | `low`, `medium`, `high`, `xhigh` | Native* |
| gpt-5.1-codex | `low`, `medium`, `high` | Native* |
| gpt-5.1 | `low`, `medium`, `high` | Native* |
| gpt-5-codex | `low`, `medium`, `high` | Native* |
| gpt-5 | `low`, `medium`, `high` | Native* |
| gpt-5.1-codex-mini | `low`, `medium`, `high` | Native* |
| gpt-5-codex-mini | `low`, `medium`, `high` | Native* |

\* [Schema fix](#opencode-schema-bug) gerekli

### perplexity.claude.gg

SDK: `@ai-sdk/openai-compatible` · [Perplexity Proxy gerekli](#perplexity-proxy)

| Model | Thinking Varyantları | Tool Call |
|-------|---------------------|-----------|
| sonar | - | Yok |
| sonar-pro | - | Yok |
| unlimited-ai | - | Yok |

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

---

## Bilinen Sorunlar ve Çözümleri

### Tool Call Proxy

Bazı Cortex gateway'leri tool call'ları JSON yerine XML formatında gönderiyor — bu context sıkıştırma için daha az token kullanıyor ama opencode ve diğer IDE'ler native JSON tool call formatı bekliyor. [xml-toolcall-proxy](https://github.com/sametakofficial/xml-toolcall-proxy) bu XML tool call'ları native JSON formatına çeviriyor.

Proxy [@minpeter/ai-sdk-tool-call-middleware](https://github.com/minpeter/ai-sdk-tool-call-middleware) kullanarak XML tool call'ları parse edip native `tool_use` (Anthropic) veya `tool_calls` (OpenAI) formatına dönüştürüyor. Streaming destekli — text anında iletiliyor.

Ek özellikler:
- Dynamic upstream routing — URL'ye domain'i yaz, proxy otomatik yönlendirir
- Anthropic ↔ OpenAI format dönüşümü
- Extended thinking passthrough

| Provider | Sorun | Proxy çözüyor mu? |
|----------|-------|-------------------|
| claude.gg | Gateway `tools` array'ini request'ten siliyor | Evet |
| beta.claude.gg | Gateway `tools` array'ini request'ten siliyor | Evet |
| api.claude.gg | Gateway `tool_calls`'ı response'tan siliyor | Evet (5 model test edildi) |

#### Kurulum

```bash
git clone https://github.com/sametakofficial/xml-toolcall-proxy.git
cd xml-toolcall-proxy
cp .env.example .env   # API key'ini düzenle
npm install
node proxy.mjs          # localhost:4012'de başlar
```

Etkilenen provider'ları `opencode.json`'da proxy'ye yönlendir:

```json
"claude.gg": {
  "options": { "baseURL": "http://localhost:4012/claude.gg/v1" }
},
"api.claude.gg": {
  "options": { "baseURL": "http://localhost:4012/api.claude.gg/v1" }
}
```

Detaylı bilgi için [xml-toolcall-proxy repo](https://github.com/sametakofficial/xml-toolcall-proxy)'suna bak.

### Opencode Schema Bug

`codex.claude.gg` ve `openai.vertexapis.com` opencode v1.2.4'te 400 hatası veriyor. Sebebi: built-in `question` tool schema'sında `additionalProperties: false` var ama tüm property'ler `required`'da listelenmiyor. Strict validator'lar bunu reddediyor.

Bunu düzelten açık bir PR var: [anomalyco/opencode#13823](https://github.com/anomalyco/opencode/pull/13823) — codex ve vertex ile test edildi, çalışıyor.

#### Seçenek 1: PR'ı source'dan çalıştır

[Bun](https://bun.sh/) gerekli (v1.3.9+).

```bash
# Linux / macOS
curl -fsSL https://bun.sh/install | bash

# Windows (PowerShell)
irm bun.sh/install.ps1 | iex
```

Sonra:

```bash
gh pr checkout 13823 --repo anomalyco/opencode
bun install
cd packages/opencode
bun run --conditions=browser ./src/index.ts
```

Build gerekmez, source'dan direkt çalışır. PR merge olunca normal `opencode` komutuna geri dönebilirsin.

#### Seçenek 2: Schema Fixer Proxy

Repo'daki `schema-fixer-proxy.mjs` — ~70 satırlık minimal proxy, tool schema'larını anında düzeltiyor. Sadece Node.js gerekli, başka bağımlılık yok.

```bash
# Linux / macOS / Windows (hepsinde aynı)
node schema-fixer-proxy.mjs
# localhost:4015'te başlar
```

Etkilenen provider'ları proxy'ye yönlendir:

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

Gateway `reasoning_content`'i response'tan siliyor. Streaming ve non-streaming test edildi, DeepSeek R1 `<think>` tag'leri de yok. Token bilgisi de strip ediliyor. Çözüm yok — gateway seviyesinde kısıtlama.

### Perplexity Proxy

`perplexity.claude.gg` standart chat completions API'si yerine search endpoint kullanıyor. Repo'daki `perplexity-proxy.py` bu search API'sini OpenAI Chat Completions formatına çeviriyor — opencode direkt kullanabiliyor.

Python 3.8+ ve `flask`, `requests` gerekli.

```bash
# Linux / macOS
pip install flask requests
python perplexity-proxy.py

# Windows
pip install flask requests
python perplexity-proxy.py

# localhost:4016'da başlar
```

`opencode.json`'da:

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

En iyi arama kalitesi. Ücretsiz plan günde 1000 istek, $5/ay plan ile daha fazla. Arama sonuçları ücretsiz alternatiflere göre fark edilir derecede daha iyi.

İpucu: sanal kartla $5'lık plana kaydol, sonra kartı kaldır. Fatura ay sonunda kesildiği için bir ay ücretsiz premium arama kullanmış olursun.

Node.js v18+ gerekli (MCP server `npx` ile çalışıyor).

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
