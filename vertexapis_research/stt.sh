#!/bin/bash
# Basit ses kaydı + STT script
# Kullanım: ./stt.sh [süre_saniye]
# Süre verilmezse Enter'a basana kadar kayıt yapar

API_KEY="${VERTEX_API_KEY:-}"
AUDIO_FILE="/tmp/stt_record.wav"

DURATION="${1:-}"

if [ -z "$API_KEY" ]; then
    echo "ERROR: Set VERTEX_API_KEY before running this script"
    exit 1
fi

echo "🎤 Kayıt başlıyor..."
if [ -n "$DURATION" ]; then
    echo "   ${DURATION} saniye kayıt yapılacak"
    arecord -f S16_LE -r 16000 -c 1 -d "$DURATION" "$AUDIO_FILE" 2>/dev/null
else
    echo "   Durdurmak için Ctrl+C"
    arecord -f S16_LE -r 16000 -c 1 "$AUDIO_FILE" 2>/dev/null
fi

echo ""
FILESIZE=$(stat -c%s "$AUDIO_FILE")
DURATION_SEC=$(python3 -c "print(f'{($FILESIZE - 44) / (16000 * 2):.1f}')")
echo "📁 Kayıt: ${DURATION_SEC}s, ${FILESIZE} bytes"
echo ""
echo "📡 API'ye gönderiliyor..."

START=$(date +%s%N)

python3 -c "
import json, base64, subprocess, sys

with open('$AUDIO_FILE', 'rb') as f:
    audio = f.read()

# WAV header'ı atla (44 byte)
raw_pcm = audio[44:] if audio[:4] == b'RIFF' else audio
b64 = base64.b64encode(raw_pcm).decode()

body = json.dumps({
    'config': {
        'encoding': 'LINEAR16',
        'sampleRateHertz': 16000,
        'languageCode': 'tr-TR',
        'alternativeLanguageCodes': ['en-US'],
        'enableAutomaticPunctuation': True,
        'model': 'latest_long'
    },
    'audio': {'content': b64}
})

with open('/tmp/stt_req.json', 'w') as f:
    f.write(body)

r = subprocess.run([
    'curl', '-s', '--max-time', '30',
    '-H', 'x-api-key: $API_KEY',
    '-H', 'Content-Type: application/json',
    '-d', '@/tmp/stt_req.json',
    'https://speech.vertexapis.com/v1p1beta1/speech:recognize'
], capture_output=True, text=True)

d = json.loads(r.stdout)
results = d.get('results', [])
if results:
    for res in results:
        alt = res['alternatives'][0]
        print(f\"📝 {alt['transcript']}\")
        print(f\"   Confidence: {alt.get('confidence', 0):.1%}\")
        lang = res.get('languageCode', '?')
        print(f\"   Dil: {lang}\")
else:
    print('❌ Ses tanınamadı')
    print(f'   Response: {json.dumps(d)[:300]}')
"

END=$(date +%s%N)
ELAPSED=$(( (END - START) / 1000000 ))
echo ""
echo "⏱️  API yanıt süresi: ${ELAPSED}ms"
