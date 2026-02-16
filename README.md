# awesome-cortexai

[Cortex AI](https://cortexai.com.tr) provider ayarları — [opencode](https://github.com/anomalyco/opencode) ile kullanım için.

## Hızlı Başlangıç

```bash
curl -fsSL https://opencode.ai/install | bash
cp opencode.json ~/.config/opencode/opencode.json
# YOUR_CORTEX_API_KEY kısmını kendi key'inle değiştir
opencode
```

## Provider'lar

| Provider | SDK | Thinking | Tool Call | Not |
|----------|-----|----------|-----------|-----|
| **app.claude.gg** | `@ai-sdk/anthropic` | budgetTokens | Native | Tam destek, tüm Claude modelleri |
| **beta.vertexapis.com** | `@ai-sdk/google` | thinkingConfig | Native | Tam destek, Gemini modelleri |
| **claude.gg** | `@ai-sdk/anthropic` | budgetTokens | [Proxy](#tool-call-proxy) | Gateway tool'ları request'ten siliyor |
| **beta.claude.gg** | `@ai-sdk/anthropic` | budgetTokens | [Proxy](#tool-call-proxy) | Gateway tool'ları request'ten siliyor |
| **api.claude.gg** | `@ai-sdk/openai-compatible` | Yok (strip) | [Proxy](#tool-call-proxy) | GPT-5, Grok-4, DeepSeek, Gemini vs. Gateway tool_calls + reasoning strip |
| **codex.claude.gg** | `@ai-sdk/openai-compatible` | reasoning_effort* | Native | [Schema fix](#opencode-schema-bug) gerekli |
| **openai.vertexapis.com** | `@ai-sdk/openai-compatible` | reasoning_effort | Native | [Schema fix](#opencode-schema-bug) gerekli |

## Thinking

```bash
# Anthropic modelleri
opencode run --thinking -m "app.claude.gg/claude-sonnet-4-5" --variant high "prompt"

# Gemini modelleri
opencode run --thinking -m "beta.vertexapis.com/gemini-2.5-flash" --variant high "prompt"
```

Varyantlar: `low`, `default`, `high`, `max`

Codex modelleri `reasoning_effort` varyantlarını destekliyor (`low`/`medium`/`high`, 5.2+ modellerde `xhigh`). Parametre kabul ediliyor ama reasoning token'ları response'ta görünmüyor — gateway strip ediyor.

openai.vertexapis.com Gemini modelleri `reasoning_effort` destekliyor ve çalışıyor — `high` ile default'a göre ~4x daha fazla reasoning token üretiyor.

## Tool Call Proxy

Bazı Cortex gateway'leri tool call'ları request veya response'tan siliyor. Bunu [xml-toolcall-proxy](https://github.com/sametakofficial/xml-toolcall-proxy) ile çözdük — tool'ları system prompt'a XML olarak inject ediyor, model XML tool call yazıyor, proxy bunu native formata çeviriyor.

Etkilenen provider'lar:

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

## Opencode Schema Bug

`codex.claude.gg` ve `openai.vertexapis.com` opencode v1.2.4'te 400 hatası veriyor. Sebebi: built-in `question` tool schema'sında `additionalProperties: false` var ama tüm property'ler `required`'da listelenmiyor. Strict validator'lar bunu reddediyor.

Bunu düzelten açık bir PR var: [anomalyco/opencode#13823](https://github.com/anomalyco/opencode/pull/13823) — codex ve vertex ile test edildi, çalışıyor.

### Seçenek 1: PR'ı source'dan kullan

```bash
gh pr checkout 13823 --repo anomalyco/opencode
bun install
cd packages/opencode
bun run --conditions=browser ./src/index.ts  # build gerekmez, source'dan çalışır
```

### Seçenek 2: Schema Fixer Proxy

Source'dan çalıştırmak istemiyorsan repo'daki `schema-fixer-proxy.mjs`'yi kullan. ~70 satırlık minimal bir proxy — tool schema'larını anında düzeltiyor. Bağımlılık yok.

```bash
node schema-fixer-proxy.mjs  # localhost:4015'te başlar
```

Etkilenen provider'ları `opencode.json`'da proxy'ye yönlendir:

```json
"codex.claude.gg": {
  "options": {
    "baseURL": "http://localhost:4015/codex.claude.gg/v1"
  }
},
"openai.vertexapis.com": {
  "options": {
    "baseURL": "http://localhost:4015/openai.vertexapis.com/v1"
  }
}
```

Herhangi bir strict OpenAI-uyumlu endpoint ile çalışır. PR merge olunca direkt URL'lere geri dönebilirsin.

## Web Arama

Web arama ciddi fark yaratıyor — model gerçek zamanlı internet bağlamı kazanıyor ve çok daha iyi cevaplar veriyor. İki seçenek:

### Brave Search MCP (önerilen)

En iyi arama kalitesi. Ücretsiz plan günde 1000 istek veriyor, $5/ay plan ile daha fazla. Gerçekten değer — arama sonuçları ücretsiz alternatiflere göre fark edilir derecede daha iyi.

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
# bash
echo 'export OPENCODE_ENABLE_EXA=1' >> ~/.bashrc && source ~/.bashrc

# zsh
echo 'export OPENCODE_ENABLE_EXA=1' >> ~/.zshrc && source ~/.zshrc
```

Kayıt yok, API key yok. Brave kadar iyi değil ama hesap açmak istemiyorsan işini görür.

## Bilinen Limitler

- **api.claude.gg thinking** — gateway `reasoning_content`'i strip ediyor, çözüm yok
- **perplexity.claude.gg** — farklı format, opencode ile uyumsuz

## Linkler

- [Cortex AI](https://cortexai.com.tr) · [Status](https://cortexai.com.tr/status)
- [opencode](https://github.com/anomalyco/opencode) · [PR #13823](https://github.com/anomalyco/opencode/pull/13823)
- [xml-toolcall-proxy](https://github.com/sametakofficial/xml-toolcall-proxy)
- [Detaylı test raporu](rapor.html)
