# awesome-cortexai

[Cortex AI](https://cortexai.com.tr) üzerindeki tüm provider'ları [opencode](https://github.com/anomalyco/opencode) ile kullanabilmen için hazır config, proxy ve workaround'lar.

Config'i kopyala, key'ini yaz, aç kullan.

---

## Kurulum

### Ne lazım?

- [Node.js](https://nodejs.org/) v18+ (proxy'ler ve MCP için gerekiyor)
  - Linux: `curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - && sudo apt install -y nodejs`
  - macOS: `brew install node` ya da [nodejs.org](https://nodejs.org/)'dan indir
  - Windows: [nodejs.org](https://nodejs.org/)'dan indir ya da `winget install OpenJS.NodeJS`

### 1. opencode'u kur

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

### 3. API key'ini yaz

`opencode.json` içindeki `YOUR_CORTEX_API_KEY` yazan yerleri kendi key'inle değiştir.

### 4. Başla

```bash
opencode
```

---


## opencode + oh-my-opencode (omo) Önerilen Kurulum

`opencode` bir AI coding agent'tır. `oh-my-opencode (omo)` ise farklı agent rollerini farklı modellere otomatik yöneten bir eklentidir.

Önerilen model hiyerarşisi:
- **Ana model (main):** Opus 4.6 — ağır reasoning, mimari kararlar
- **Görev modeli (tasks):** Sonnet 4.6 — hızlı coding, exploration, review
- **Fallback:** `codex.claude.gg/gpt-5.3-codex` — review ve alternatif çözüm

`omo` kurulumu:
```bash
npm i -g oh-my-opencode
```

Örnek `opencode.json` (primary: Kiro proxy, fallback: app.claude.gg):
```json
{
  "model": "anthropic/claude-opus-4-6",
  "provider": {
    "anthropic": {
      "npm": "@ai-sdk/anthropic",
      "options": {
        "baseURL": "http://localhost:4040/v1",
        "apiKey": "YOUR_CORTEX_API_KEY"
      },
      "models": {
        "claude-opus-4-6": {},
        "claude-sonnet-4-6": {}
      }
    },
    "app.claude.gg": {
      "npm": "@ai-sdk/anthropic",
      "options": {
        "baseURL": "https://app.claude.gg/v1",
        "apiKey": "YOUR_CORTEX_API_KEY"
      },
      "models": {
        "claude-opus-4-6": {},
        "claude-sonnet-4-6": {}
      }
    }
  }
}
```

Örnek `oh-my-opencode.json` agent routing:
```json
{
  "routing": {
    "sisyphus": "anthropic/claude-opus-4-6:max",
    "oracle": "anthropic/claude-opus-4-6:max",
    "prometheus": "anthropic/claude-opus-4-6:max",
    "librarian": "anthropic/claude-sonnet-4-6",
    "explore": "anthropic/claude-sonnet-4-6",
    "atlas": "anthropic/claude-sonnet-4-6",
    "momus": "anthropic/claude-sonnet-4-6",
    "reviewer": "codex.claude.gg/gpt-5.3-codex"
  }
}
```

## Provider'lar ve Modeller

### app.claude.gg

SDK: `@ai-sdk/anthropic` · Tool Call: Native · Thinking: budgetTokens

| Model                      | Thinking      | Tool Call |
| -------------------------- | ------------- | --------- |
| claude-opus-4-6-20260101   | `high`, `max` | Native    |
| claude-sonnet-4-6          | `high`, `max` | Native    |
| claude-opus-4-5-20251101   | `high`, `max` | Native    |
| claude-sonnet-4-5-20250929 | `high`, `max` | Native    |
| claude-sonnet-4-20250514   | `high`, `max` | Native    |
| claude-3-7-sonnet-20250219 | `high`, `max` | Native    |
| claude-haiku-4-5-20251001  | `high`, `max` | Native    |

### claude.gg

SDK: `@ai-sdk/anthropic` · Tool Call: XML formatında dönüyor (çalışmıyor) · Thinking: budgetTokens

| Model             | Thinking      | Tool Call |
| ----------------- | ------------- | --------- |
| claude-opus-4-6   | `high`, `max` | XML ✗     |
| claude-opus-4-5   | `high`, `max` | XML ✗     |
| claude-sonnet-4-5 | `high`, `max` | XML ✗     |
| claude-sonnet-4   | `high`, `max` | XML ✗     |
| claude-3-7-sonnet | `high`, `max` | XML ✗     |
| claude-haiku-4-5  | `high`, `max` | XML ✗     |

### beta.claude.gg

SDK: `@ai-sdk/anthropic` · Tool Call: XML formatında dönüyor (çalışmıyor) · Thinking: budgetTokens

| Model                      | Thinking      | Tool Call |
| -------------------------- | ------------- | --------- |
| claude-opus-4-1-20250805   | `high`, `max` | XML ✗     |
| claude-sonnet-4-5-20250929 | `high`, `max` | XML ✗     |
| claude-sonnet-4-5-web      | `high`, `max` | XML ✗     |

### api.claude.gg

SDK: `@ai-sdk/openai-compatible` · Tool Call: XML formatında dönüyor (çalışmıyor) · Thinking: reasoning_effort

Bu API'de 20'den fazla model var — GPT-5, Grok, DeepSeek, Gemini hepsi tek key ile. Hepsi `reasoning_effort` parametresini kabul ediyor ama gateway hem `reasoning_content`'i hem `tool_calls`'ı hem de token bilgisini siliyor. Yani thinking çalışıyor (model gerçekten daha fazla düşünüyor) ama çıktısını göremiyorsun. Tool call'lar da XML formatında dönüyor, opencode bunu parse edemiyor.

| Model                 | Thinking                                    | Tool Call |
| --------------------- | ------------------------------------------- | --------- |
| gpt-5                 | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| gpt-5.1               | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| gpt-5-mini            | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| gpt-5-nano            | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| gpt-o3                | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| o3                    | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| o3-mini               | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| gpt-4.1               | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| gpt-4.1-nano          | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| gpt-4o                | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| gpt-4o-mini           | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| grok-4                | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| grok-3-mini           | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| grok-3-mini-beta      | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| grok-2                | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| deepseek-r1           | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| deepseek-v3           | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| deepseek-chat         | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| gemini-2.5-flash      | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| gemini-2.0-flash      | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| gemini-2.0-flash-lite | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |
| gemini-lite           | `minimal`, `low`, `medium`, `high`, `xhigh` | XML ✗     |

### beta.vertexapis.com

SDK: `@ai-sdk/google` · Tool Call: Native · Thinking: thinkingConfig

| Model                  | Thinking                           | Tool Call |
| ---------------------- | ---------------------------------- | --------- |
| gemini-3-pro-preview   | `low`, `high`                      | Native    |
| gemini-3-flash-preview | `low`, `medium`, `high`            | Native    |
| gemini-2.5-pro         | `low`, `high`, `max`               | Native    |
| gemini-2.5-flash       | `low`, `high`, `max`               | Native    |
| gemini-2.5-flash-lite  | `low`, `high`, `max`               | Native    |
| gemini-2.0-flash       | `minimal`, `low`, `medium`, `high` | Native    |
| gemini-2.0-flash-lite  | `minimal`, `low`, `medium`, `high` | Native    |

### openai.vertexapis.com

SDK: `@ai-sdk/openai-compatible` · Tool Call: Native · Thinking: reasoning_effort · [Schema fix lazım](#opencode-schema-bug)

`reasoning_effort` düzgün çalışıyor — `high` ile default'a kıyasla ~4x daha fazla reasoning token üretiyor ve bu token'lar response'ta da görünüyor.

| Model                     | Thinking                           | Tool Call |
| ------------------------- | ---------------------------------- | --------- |
| gemini-3-pro-preview      | `minimal`, `low`, `medium`, `high` | Native\*  |
| gemini-3-flash-preview    | `minimal`, `low`, `medium`, `high` | Native\*  |
| gemini-2.5-pro            | `minimal`, `low`, `medium`, `high` | Native\*  |
| gemini-2.5-flash          | `minimal`, `low`, `medium`, `high` | Native\*  |
| gemini-2.5-flash-lite     | `minimal`, `low`, `medium`, `high` | Native\*  |
| gemini-2.0-flash-001      | `minimal`, `low`, `medium`, `high` | Native\*  |
| gemini-2.0-flash-lite-001 | `minimal`, `low`, `medium`, `high` | Native\*  |

\* opencode v1.2.4'te [schema bug'ı](#opencode-schema-bug) var, fix gerekiyor

### codex.claude.gg

SDK: `@ai-sdk/openai-compatible` · Tool Call: Native · Thinking: reasoning_effort · [Schema fix lazım](#opencode-schema-bug)

`reasoning_effort` çalışıyor — `high` ile ~3x daha fazla token harcıyor ama gateway düşünce metnini siliyor, sadece sonucu görüyorsun.

| Model              | Thinking                         | Tool Call |
| ------------------ | -------------------------------- | --------- |
| gpt-5.3-codex      | `low`, `medium`, `high`, `xhigh` | Native\*  |
| gpt-5.2-codex      | `low`, `medium`, `high`, `xhigh` | Native\*  |
| gpt-5.1-codex-max  | `low`, `medium`, `high`, `xhigh` | Native\*  |
| gpt-5.2            | `low`, `medium`, `high`, `xhigh` | Native\*  |
| gpt-5.1-codex      | `low`, `medium`, `high`          | Native\*  |
| gpt-5.1            | `low`, `medium`, `high`          | Native\*  |
| gpt-5-codex        | `low`, `medium`, `high`          | Native\*  |
| gpt-5              | `low`, `medium`, `high`          | Native\*  |
| gpt-5.1-codex-mini | `low`, `medium`, `high`          | Native\*  |
| gpt-5-codex-mini   | `low`, `medium`, `high`          | Native\*  |

\* opencode v1.2.4'te [schema bug'ı](#opencode-schema-bug) var, fix gerekiyor

### perplexity.claude.gg

SDK: `@ai-sdk/openai-compatible` · [Perplexity Proxy lazım](#perplexity-proxy)

| Model        | Thinking | Tool Call |
| ------------ | -------- | --------- |
| sonar        | -        | Yok       |
| sonar-pro    | -        | Yok       |
| unlimited-ai | -        | Yok       |

---

## Thinking Nasıl Kullanılır?

```bash
# Anthropic (Sonnet, Opus 4.5 vs.) — sadece high ve max var
opencode run --thinking -m "app.claude.gg/claude-sonnet-4-5" --variant high "prompt"

# Anthropic (Opus 4.6) — adaptive thinking, low'dan max'a kadar
opencode run --thinking -m "app.claude.gg/claude-opus-4-6" --variant low "prompt"

# Gemini 2.5 — thinkingBudget ile, low/high/max
opencode run --thinking -m "beta.vertexapis.com/gemini-2.5-flash" --variant high "prompt"

# Gemini 3 — thinkingLevel ile, low/high (flash'ta medium de var)
opencode run --thinking -m "beta.vertexapis.com/gemini-3-flash-preview" --variant high "prompt"

# Codex — reasoning_effort ile, 5.2+ modellerde xhigh da var
opencode run --thinking -m "codex.claude.gg/gpt-5.3-codex" --variant xhigh "prompt"
```

---

## Sorunlar ve Çözümler

### Tool Call Sorunu (XML Format)

Cortex'teki bazı gateway'ler tool call'ları JSON yerine XML formatında yolluyor. Bu aslında context sıkıştırma için iyi bir şey (daha az token harcıyor) ama opencode ve diğer IDE'ler native JSON formatı bekliyor, XML'i anlamıyorlar.

| Provider       | Ne oluyor?                                   |
| -------------- | -------------------------------------------- |
| claude.gg      | Tool call'lar JSON yerine XML olarak geliyor |
| beta.claude.gg | Tool call'lar JSON yerine XML olarak geliyor |
| api.claude.gg  | Tool call'lar JSON yerine XML olarak geliyor |

Bu provider'larda tool call çalışmıyor. Sadece sohbet/chat olarak kullanılabilirler.

### Opencode Schema Bug

opencode v1.2.4'te `codex.claude.gg` ve `openai.vertexapis.com` 400 hatası veriyor. Sorun şu: opencode'un built-in `question` tool'unda `additionalProperties: false` var ama bazı property'ler `required` listesinde yok. Strict validation yapan sunucular bunu kabul etmiyor.

Biri bunu düzelten bir PR açmış: [anomalyco/opencode#13823](https://github.com/anomalyco/opencode/pull/13823) — biz de test ettik, codex ve vertex'te çalışıyor.

#### Yol 1: PR'ı source'dan çalıştır

[Bun](https://bun.sh/) lazım (v1.3.9+).

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

Build'e gerek yok, source'dan direkt çalışıyor. PR merge olunca normal `opencode`'a geri dönersin.

#### Yol 2: Schema Fixer Proxy

Bu repo'daki `schema-fixer-proxy.mjs` — 70 satırlık ufak bir proxy. Tool schema'larını uçuşta düzeltiyor. Tek bağımlılığı Node.js.

```bash
# Her platformda aynı
node schema-fixer-proxy.mjs
# localhost:4015'te başlar
```

`opencode.json`'da ilgili provider'ları proxy'ye yönlendir:

```json
"codex.claude.gg": {
  "options": { "baseURL": "http://localhost:4015/codex.claude.gg/v1" }
},
"openai.vertexapis.com": {
  "options": { "baseURL": "http://localhost:4015/openai.vertexapis.com/v1" }
}
```

PR merge olunca direkt URL'lere geri dönersin.

### api.claude.gg'de Thinking Görünmüyor

Gateway `reasoning_content`'i response'tan siliyor. Streaming'de de non-streaming'de de aynı. DeepSeek R1'in `<think>` tag'leri bile gelmiyor. Token sayıları da sıfır dönüyor. Yapacak bir şey yok, gateway tarafında bir kısıtlama bu.

### Perplexity Proxy

`perplexity.claude.gg` normal bir chat API'si değil, search endpoint'i kullanıyor. Bu repo'daki `perplexity-proxy.py` search sonuçlarını OpenAI chat completions formatına çeviriyor, opencode direkt kullanabiliyor.

Python 3.8+ lazım, `flask` ve `requests` ile çalışıyor.

```bash
# Her platformda aynı
pip install flask requests
python perplexity-proxy.py
# localhost:4016'da başlar
```

`opencode.json`'a ekle:

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

Modele internet erişimi vermek ciddi fark yaratıyor. Güncel bilgiye erişiyor, çok daha isabetli cevaplar veriyor.

### Brave Search MCP (tavsiye)

Arama kalitesi olarak en iyisi. Ücretsiz planda günde 1000 istek var, $5/ay'lık planla daha fazla. Ücretsiz alternatiflere göre gözle görülür fark var, değer.

Küçük bir tüyo: sanal kartla $5'lık plana kaydol, sonra kartı kaldır. Fatura ay sonunda kesildiği için bir ay bedavaya premium arama kullanmış olursun.

Node.js v18+ lazım (MCP server `npx` ile çalışıyor).

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

### Exa Web Search (bedava, key gerekmez)

opencode'un kendi içinde bir web arama tool'u var. Tek yapman gereken bir env değişkeni set etmek:

```bash
# Linux / macOS (bash)
echo 'export OPENCODE_ENABLE_EXA=1' >> ~/.bashrc && source ~/.bashrc

# Linux / macOS (zsh)
echo 'export OPENCODE_ENABLE_EXA=1' >> ~/.zshrc && source ~/.zshrc

# Windows (PowerShell — kalıcı)
[System.Environment]::SetEnvironmentVariable('OPENCODE_ENABLE_EXA', '1', 'User')
# Yeni terminal aç
```

Kayıt yok, key yok, bedava. Brave kadar iyi değil ama hiç yoktan iyidir.

---

## Linkler

- [Cortex AI](https://cortexai.com.tr) · [Status](https://cortexai.com.tr/status)
- [opencode](https://github.com/anomalyco/opencode) · [Schema Fix PR #13823](https://github.com/anomalyco/opencode/pull/13823)
