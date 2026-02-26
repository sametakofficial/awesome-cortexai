# Google Gemini - aiplatform.vertexapis.com Komutları

API Key: `sk-0f2246e77aa642cfafd6c4b0dd5fe14d`
Base URL: `https://aiplatform.vertexapis.com/v1/models`

---

# TTS (Text-to-Speech)

## 1. Pro Non-Streaming (EN İYİ KALİTE)

```bash
curl -s --max-time 60 -H "x-api-key:sk-0f2246e77aa642cfafd6c4b0dd5fe14d" -H "Content-Type: application/json" \
  "https://aiplatform.vertexapis.com/v1/models/gemini-2.5-pro-tts:generateContent" \
  -d '{"contents":[{"role":"user","parts":[{"text":"METNİ BURAYA YAZ"}]}],"generationConfig":{"responseModalities":["AUDIO"],"speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":"Kore"}}}}}' \
  | python3 -c "import json,sys,base64,struct;d=json.load(sys.stdin);pcm=base64.b64decode(d['candidates'][0]['content']['parts'][0]['inlineData']['data']);sr=24000;ds=len(pcm);hdr=struct.pack('<4sI4s4sIHHIIHH4sI',b'RIFF',36+ds,b'WAVE',b'fmt ',16,1,1,sr,sr*2,2,16,b'data',ds);open('/tmp/kore_pro.wav','wb').write(hdr+pcm);print(f'OK {ds/(sr*2):.1f}s')" \
  && mpv /tmp/kore_pro.wav
```

## 2. Pro Streaming (UYARI: TTS kalitesi non-streaming'den düşük)

```bash
curl -s --max-time 60 -N -H "x-api-key:sk-0f2246e77aa642cfafd6c4b0dd5fe14d" -H "Content-Type: application/json" \
  "https://aiplatform.vertexapis.com/v1/models/gemini-2.5-pro-tts:streamGenerateContent" \
  -d '{"contents":[{"role":"user","parts":[{"text":"METNİ BURAYA YAZ"}]}],"generationConfig":{"responseModalities":["AUDIO"],"speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":"Kore"}}}}}' \
  | python3 -c "
import json,sys,base64,struct
pcm=b''
for chunk in json.load(sys.stdin):
    if 'candidates' in chunk:
        for p in chunk['candidates'][0]['content']['parts']:
            if 'inlineData' in p:
                pcm+=base64.b64decode(p['inlineData']['data'])
sr=24000;ds=len(pcm);hdr=struct.pack('<4sI4s4sIHHIIHH4sI',b'RIFF',36+ds,b'WAVE',b'fmt ',16,1,1,sr,sr*2,2,16,b'data',ds)
open('/tmp/kore_pro_stream.wav','wb').write(hdr+pcm);print(f'OK {ds/(sr*2):.1f}s')" \
  && mpv /tmp/kore_pro_stream.wav
```

## 3. Flash Non-Streaming

```bash
curl -s --max-time 60 -H "x-api-key:sk-0f2246e77aa642cfafd6c4b0dd5fe14d" -H "Content-Type: application/json" \
  "https://aiplatform.vertexapis.com/v1/models/gemini-2.5-flash-tts:generateContent" \
  -d '{"contents":[{"role":"user","parts":[{"text":"METNİ BURAYA YAZ"}]}],"generationConfig":{"responseModalities":["AUDIO"],"speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":"Kore"}}}}}' \
  | python3 -c "import json,sys,base64,struct;d=json.load(sys.stdin);pcm=base64.b64decode(d['candidates'][0]['content']['parts'][0]['inlineData']['data']);sr=24000;ds=len(pcm);hdr=struct.pack('<4sI4s4sIHHIIHH4sI',b'RIFF',36+ds,b'WAVE',b'fmt ',16,1,1,sr,sr*2,2,16,b'data',ds);open('/tmp/kore_flash.wav','wb').write(hdr+pcm);print(f'OK {ds/(sr*2):.1f}s')" \
  && mpv /tmp/kore_flash.wav
```

## 4. Flash Streaming

```bash
curl -s --max-time 60 -N -H "x-api-key:sk-0f2246e77aa642cfafd6c4b0dd5fe14d" -H "Content-Type: application/json" \
  "https://aiplatform.vertexapis.com/v1/models/gemini-2.5-flash-tts:streamGenerateContent" \
  -d '{"contents":[{"role":"user","parts":[{"text":"METNİ BURAYA YAZ"}]}],"generationConfig":{"responseModalities":["AUDIO"],"speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":"Kore"}}}}}' \
  | python3 -c "
import json,sys,base64,struct
pcm=b''
for chunk in json.load(sys.stdin):
    if 'candidates' in chunk:
        for p in chunk['candidates'][0]['content']['parts']:
            if 'inlineData' in p:
                pcm+=base64.b64decode(p['inlineData']['data'])
sr=24000;ds=len(pcm);hdr=struct.pack('<4sI4s4sIHHIIHH4sI',b'RIFF',36+ds,b'WAVE',b'fmt ',16,1,1,sr,sr*2,2,16,b'data',ds)
open('/tmp/kore_flash_stream.wav','wb').write(hdr+pcm);print(f'OK {ds/(sr*2):.1f}s')" \
  && mpv /tmp/kore_flash_stream.wav
```

## TTS Kalite Sıralaması

1. **Pro Non-Streaming** — En iyi duygu, tonlama, nefes. Yavaş ama değer.
2. **Flash Non-Streaming** — Pro'ya yakın, daha hızlı.
3. **Pro Streaming** — Kalite düşüyor, Flash non-streaming'den bile kötü olabiliyor.
4. **Flash Streaming** — En hızlı ama en düz.

## TTS Prompt Tüyoları

- `BÜYÜK HARF` = bağırma
- `...` = duraklama/nefes
- `değilmişşşş` = uzatma
- `!` = enerji
- `?` = ton değişimi
- `psst...` küçük harf = fısıltı
- `ben... ben dayanamıyorum...` = hıçkırık/ağlama
- Sayıları yazıyla yaz: `iki yüz kırk yedi bin`

## TTS Sesler (30 adet)

| Kadın | Erkek |
|-------|-------|
| Achernar, Aoede, Autonoe | Achird, Algenib, Algieba |
| Callirrhoe, Despina, Erinome | Alnilam, Charon, Enceladus |
| Gacrux, **Kore**, Laomedeia | Fenrir, Iapetus, Orus |
| Leda, Pulcherrima, Sulafat | Puck, Rasalgethi, Sadachbia |
| Vindemiatrix, Zephyr | Sadaltager, Schedar, Umbriel, Zubenelgenubi |

---

# STT (Speech-to-Text)

## 1. Gemini Pro STT - Streaming (EN İYİ KALİTE + EN HIZLI)

Ses kaydı al ve Gemini Pro ile transkribe et:

```bash
# 1. Kayıt al (Ctrl+C ile durdur)
arecord -f S16_LE -r 16000 -c 1 /tmp/rec.wav

# 2. MP3'e çevir (küçük boyut)
ffmpeg -y -i /tmp/rec.wav -ar 16000 -ac 1 -b:a 64k /tmp/rec.mp3

# 3. Gemini Pro streaming STT
python3 -c "
import json,base64
with open('/tmp/rec.mp3','rb') as f: audio=f.read()
body={'contents':[{'role':'user','parts':[
    {'inlineData':{'mimeType':'audio/mp3','data':base64.b64encode(audio).decode()}},
    {'text':'Bu ses kaydını kelimesi kelimesine transkribe et. İngilizce kelimeler varsa İngilizce yaz, Türkçe kelimeler varsa Türkçe yaz. Sadece transkripti yaz.'}
]}]}
with open('/tmp/stt_body.json','w') as f: json.dump(body,f)
" && \
curl -s --max-time 30 -N -H "x-api-key:sk-0f2246e77aa642cfafd6c4b0dd5fe14d" -H "Content-Type: application/json" \
  -d @/tmp/stt_body.json \
  "https://aiplatform.vertexapis.com/v1/models/gemini-2.5-pro:streamGenerateContent" \
  | python3 -c "
import json,sys
for chunk in json.load(sys.stdin):
    if 'candidates' in chunk:
        for p in chunk['candidates'][0].get('content',{}).get('parts',[]):
            if 'text' in p: print(p['text'],end='',flush=True)
print()
"
```

## 2. Gemini Pro STT - Non-Streaming

```bash
python3 -c "
import json,base64
with open('/tmp/rec.mp3','rb') as f: audio=f.read()
body={'contents':[{'role':'user','parts':[
    {'inlineData':{'mimeType':'audio/mp3','data':base64.b64encode(audio).decode()}},
    {'text':'Bu ses kaydını kelimesi kelimesine transkribe et. İngilizce kelimeler varsa İngilizce yaz, Türkçe kelimeler varsa Türkçe yaz. Sadece transkripti yaz.'}
]}]}
with open('/tmp/stt_body.json','w') as f: json.dump(body,f)
" && \
curl -s --max-time 30 -H "x-api-key:sk-0f2246e77aa642cfafd6c4b0dd5fe14d" -H "Content-Type: application/json" \
  -d @/tmp/stt_body.json \
  "https://aiplatform.vertexapis.com/v1/models/gemini-2.5-pro:generateContent" \
  | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(d['candidates'][0]['content']['parts'][0]['text'])
"
```

## 3. Gemini Flash STT (daha ucuz, biraz daha yavaş)

```bash
# Aynı body, sadece model değişiyor
curl -s --max-time 30 -H "x-api-key:sk-0f2246e77aa642cfafd6c4b0dd5fe14d" -H "Content-Type: application/json" \
  -d @/tmp/stt_body.json \
  "https://aiplatform.vertexapis.com/v1/models/gemini-2.5-flash:generateContent" \
  | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(d['candidates'][0]['content']['parts'][0]['text'])
"
```

## STT Kalite Sıralaması

1. **Gemini 2.5 Pro streaming** — En iyi + en hızlı (2.9s, "QR detection system", "finder pattern")
2. **Gemini 2.5 Pro non-streaming** — Aynı kalite, daha yavaş (5.3s)
3. **Gemini 2.5 Flash** — İyi ama yavaş (20s)
4. **Google Speech API v1** — Karışık dilde berbat ("QR detechtım", "final patronlara")

## STT Notlar

- Gemini Pro karışık TR+EN konuşmayı mükemmel anlıyor
- Google Speech API karışık dilde çöp, sadece Türkçe'de idare eder
- Gemini token bazlı faturalanıyor (~800 token/20s ses), Speech API saniye bazlı
- MP3 formatı gönder, WAV çok büyük oluyor

---

# Karşılaştırma Komutları

```bash
# TTS: 4'ünü arka arkaya dinle
mpv /tmp/kore_pro.wav /tmp/kore_pro_stream.wav /tmp/kore_flash.wav /tmp/kore_flash_stream.wav
```

---

# Gemini 3 Ailesi (locations/us)

**ÖNEMLİ:** Gemini 3 modelleri `locations/us-central1` değil `locations/us` kullanıyor!

Base URL: `https://aiplatform.vertexapis.com/v1/projects/vertex/locations/us/publishers/google/models/`

## Çalışan Modeller

| Model | Durum |
|-------|-------|
| `gemini-3-pro-preview` | ✅ Çalışıyor |
| `gemini-3-flash-preview` | ✅ Çalışıyor |
| `gemini-3.1-pro-preview` | ✅ Çalışıyor |
| `gemini-3.1-flash-preview` | ❌ 404 |

## Gemini 3 Pro - Text Generation

```bash
curl -s --max-time 30 -H "x-api-key:sk-0f2246e77aa642cfafd6c4b0dd5fe14d" -H "Content-Type: application/json" \
  "https://aiplatform.vertexapis.com/v1/projects/vertex/locations/us/publishers/google/models/gemini-3-pro-preview:generateContent" \
  -d '{"contents": [{"role": "user", "parts": [{"text": "Merhaba!"}]}]}' \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['candidates'][0]['content']['parts'][0]['text'])"
```

## Gemini 3 Pro - Streaming (alt=sse ÇALIŞMIYOR, JSON array formatı kullan)

```bash
curl -s --max-time 30 -H "x-api-key:sk-0f2246e77aa642cfafd6c4b0dd5fe14d" -H "Content-Type: application/json" \
  "https://aiplatform.vertexapis.com/v1/projects/vertex/locations/us/publishers/google/models/gemini-3-pro-preview:streamGenerateContent" \
  -d '{"contents": [{"role": "user", "parts": [{"text": "Merhaba!"}]}]}' \
  | python3 -c "
import json,sys
for chunk in json.load(sys.stdin):
    if 'candidates' in chunk:
        for p in chunk['candidates'][0].get('content',{}).get('parts',[]):
            if 'text' in p: print(p['text'],end='',flush=True)
print()
"
```

## Gemini 3 Pro - STT (Ses Girişi)

```bash
# MP3 veya WAV ses dosyasını gönder
python3 -c "
import json,base64
with open('/tmp/rec.mp3','rb') as f: audio=f.read()
body={'contents':[{'role':'user','parts':[
    {'inlineData':{'mimeType':'audio/mp3','data':base64.b64encode(audio).decode()}},
    {'text':'Bu ses kaydını kelimesi kelimesine transkribe et.'}
]}]}
with open('/tmp/stt_body.json','w') as f: json.dump(body,f)
" && \
curl -s --max-time 30 -H "x-api-key:sk-0f2246e77aa642cfafd6c4b0dd5fe14d" -H "Content-Type: application/json" \
  -d @/tmp/stt_body.json \
  "https://aiplatform.vertexapis.com/v1/projects/vertex/locations/us/publishers/google/models/gemini-3-pro-preview:generateContent" \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['candidates'][0]['content']['parts'][0]['text'])"
```

## Gemini 3 Pro - TTS (KİLİTLİ)

```bash
# ÇALIŞMIYOR: "You are not allowlisted to request audio output"
# Pro, Flash, 3.1 Pro hepsinde aynı hata
# Yetenek var ama vertexapis.com proxy'sinde allowlist kısıtı
curl -s --max-time 30 -H "x-api-key:sk-0f2246e77aa642cfafd6c4b0dd5fe14d" -H "Content-Type: application/json" \
  "https://aiplatform.vertexapis.com/v1/projects/vertex/locations/us/publishers/google/models/gemini-3-pro-preview:generateContent" \
  -d '{"contents": [{"role": "user", "parts": [{"text": "Merhaba"}]}], "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Kore"}}}}}' \
  | python3 -m json.tool
```

## Gemini 3 Pro - Function Calling

```bash
curl -s --max-time 30 -H "x-api-key:sk-0f2246e77aa642cfafd6c4b0dd5fe14d" -H "Content-Type: application/json" \
  "https://aiplatform.vertexapis.com/v1/projects/vertex/locations/us/publishers/google/models/gemini-3-pro-preview:generateContent" \
  -d '{"contents": [{"role": "user", "parts": [{"text": "Weather in London?"}]}], "tools": [{"functionDeclarations": [{"name": "get_weather", "description": "Get weather", "parameters": {"type": "OBJECT", "properties": {"city": {"type": "STRING"}}}}]}]}' \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print(json.dumps(d['candidates'][0]['content']['parts'][0].get('functionCall',{}),indent=2))"
```

## Gemini 3 Pro - Code Execution

```bash
curl -s --max-time 30 -H "x-api-key:sk-0f2246e77aa642cfafd6c4b0dd5fe14d" -H "Content-Type: application/json" \
  "https://aiplatform.vertexapis.com/v1/projects/vertex/locations/us/publishers/google/models/gemini-3-pro-preview:generateContent" \
  -d '{"contents": [{"role": "user", "parts": [{"text": "What is 2+2? Use code."}]}], "tools": [{"codeExecution": {}}]}' \
  | python3 -c "
import json,sys
d=json.load(sys.stdin)
for p in d['candidates'][0]['content']['parts']:
    if 'executableCode' in p: print('CODE:', p['executableCode']['code'])
    if 'codeExecutionResult' in p: print('RESULT:', p['codeExecutionResult']['output'])
    if 'text' in p: print('TEXT:', p['text'])
"
```

## Gemini 3 Pro - JSON Mode

```bash
curl -s --max-time 30 -H "x-api-key:sk-0f2246e77aa642cfafd6c4b0dd5fe14d" -H "Content-Type: application/json" \
  "https://aiplatform.vertexapis.com/v1/projects/vertex/locations/us/publishers/google/models/gemini-3-pro-preview:generateContent" \
  -d '{"contents": [{"role": "user", "parts": [{"text": "List 3 Turkish cities with population"}]}], "generationConfig": {"responseMimeType": "application/json"}}' \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['candidates'][0]['content']['parts'][0]['text'])"
```

## Gemini 3 Pro - Google Search Grounding

```bash
curl -s --max-time 30 -H "x-api-key:sk-0f2246e77aa642cfafd6c4b0dd5fe14d" -H "Content-Type: application/json" \
  "https://aiplatform.vertexapis.com/v1/projects/vertex/locations/us/publishers/google/models/gemini-3-pro-preview:generateContent" \
  -d '{"contents": [{"role": "user", "parts": [{"text": "Bugün Türkiyede gündem ne?"}]}], "tools": [{"googleSearch": {}}]}' \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['candidates'][0]['content']['parts'][0]['text'][:500])"
```

## Gemini 3 Pro - Vision

```bash
# Resim base64 olarak gönderilir
B64=$(base64 -w0 resim.png)
curl -s --max-time 30 -H "x-api-key:sk-0f2246e77aa642cfafd6c4b0dd5fe14d" -H "Content-Type: application/json" \
  "https://aiplatform.vertexapis.com/v1/projects/vertex/locations/us/publishers/google/models/gemini-3-pro-preview:generateContent" \
  -d "{\"contents\": [{\"role\": \"user\", \"parts\": [{\"text\": \"Bu resimde ne var?\"}, {\"inlineData\": {\"mimeType\": \"image/png\", \"data\": \"$B64\"}}]}]}" \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['candidates'][0]['content']['parts'][0]['text'])"
```

## Gemini 3 Pro - System Instruction

```bash
curl -s --max-time 30 -H "x-api-key:sk-0f2246e77aa642cfafd6c4b0dd5fe14d" -H "Content-Type: application/json" \
  "https://aiplatform.vertexapis.com/v1/projects/vertex/locations/us/publishers/google/models/gemini-3-pro-preview:generateContent" \
  -d '{"systemInstruction": {"parts": [{"text": "Sen bir korsan gibi konuş"}]}, "contents": [{"role": "user", "parts": [{"text": "Merhaba!"}]}]}' \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['candidates'][0]['content']['parts'][0]['text'])"
```

## Gemini 3 Yetenek Özeti

| Yetenek | 3 Pro | 3 Flash | 3.1 Pro |
|---------|-------|---------|---------|
| Text Generation | ✅ | ✅ | ✅ |
| Streaming (JSON array) | ✅ | ✅ | ✅ |
| Streaming (SSE) | ❌ HTML | ❌ HTML | ❌ HTML |
| Vision | ✅ | ✅ | ✅ |
| STT (ses girişi) | ✅ | ✅ | ✅ |
| TTS (ses çıkışı) | ❌ allowlist | ❌ allowlist | ❌ allowlist |
| Function Calling | ✅ | ✅ | ✅ |
| Code Execution | ✅ | ✅ | ✅ |
| JSON Mode | ✅ | ✅ | ✅ (test edilmedi ama kesin var) |
| Google Search | ✅ | ✅ (test edilmedi ama kesin var) | ✅ (test edilmedi ama kesin var) |
| System Instruction | ✅ (2.5 Pro'da test edildi) | ✅ (kesin var) | ✅ (kesin var) |
| Thinking/Reasoning | ✅ (292 token) | ✅ | ✅ (592 token) |

## Gemini 3 vs 2.5 Farkları

- Gemini 3 `locations/us` istiyor, 2.5 `locations/us-central1`
- Gemini 3 streaming'de `alt=sse` çalışmıyor, JSON array formatı kullanılmalı
- Gemini 3 TTS allowlist kısıtı var (2.5-pro-tts/flash-tts'de yok)
- Gemini 3.1 Pro daha fazla thinking token kullanıyor (592 vs 292)
