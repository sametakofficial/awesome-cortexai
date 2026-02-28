# VertexAPIs Arastirma Raporu

Tarih: 2026-02-28

Bu dokuman, `vertexapis.com` uzerinde yaptigimiz kapsamli testlerin ozetini ve teknik bulgularini icerir.
Odak nokta: `aiplatform.vertexapis.com` (Vertex AI publisher models proxy) ve gorsel/video/ses yetenekleri.

## 1) Mimari ve Proxy Eslesmesi

- `aiplatform.vertexapis.com`, pratikte Google Vertex AI publisher endpoints'lerinin proxy'si gibi davraniyor.
- Eslesen endpoint yapisi:
  - Proxy: `https://aiplatform.vertexapis.com/v1/projects/.../locations/.../publishers/google/models/...:generateContent`
  - Orijinal: `https://{location}-aiplatform.googleapis.com/v1/projects/.../locations/.../publishers/google/models/...:generateContent`
- Birebir parity yok: region, allowlist, org policy, gateway farklari nedeniyle bazi model/ozellikler kisitli olabiliyor.

## 2) Kesfedilen Subdomainler

Aktif ve test edilen ana domainler:

- `aiplatform.vertexapis.com`
- `texttospeech.vertexapis.com`
- `speech.vertexapis.com`
- `language.vertexapis.com`
- `vision.vertexapis.com`
- `translate.vertexapis.com`
- `videointelligence.vertexapis.com`
- `documentai.vertexapis.com`

## 3) Gemini Ailesi (Text/Tool/Audio/Vision)

### 3.1 Region Notu (kritik)

- Gemini 2.x/2.5 text modelleri agirlikla `locations/us-central1` uzerinde stabil.
- Gemini 3 preview text modelleri icin `locations/us` ile daha iyi sonuc alindi.

### 3.2 Calisan model seti (text/agentik)

- `gemini-2.5-pro`
- `gemini-2.5-flash`
- `gemini-2.0-flash`
- `gemini-2.0-flash-lite`
- `gemini-3-pro-preview`
- `gemini-3-flash-preview`
- `gemini-3.1-pro-preview`

### 3.3 Test edilen calisan yetenekler

- Text generation: calisiyor
- Vision (inline image): calisiyor
- Function calling: calisiyor
- Code execution: calisiyor
- JSON mode (`responseMimeType: application/json`): calisiyor
- Grounding (`googleSearch` tool): calisiyor
- STT (audio input ile transcription): calisiyor
- Streaming: calisiyor (bu proxylendirmede SSE yerine JSON chunk davranisi daha stabil)

### 3.4 TTS durumu (Gemini 3/3.1)

- Hata: `You are not allowlisted to request audio output`
- Yorum: Yetenek modelde var ama tenant/proje tarafinda allowlist/policy kilidi var.
- `v1`/`v1beta1`, `AUDIO`/`TEXT+AUDIO`, farkli body varyantlari denendi; sonuc degismedi.

## 4) STT ve Streaming Bulgulari

- STT hem 2.5 hem 3/3.1 tarafinda calisti.
- Streaming endpoint tarafinda bu proxyde en stabil desen: `streamGenerateContent` + JSON chunk parse.
- `alt=sse` bazi kombinasyonlarda HTML/kararsiz dondu.

Not: Latency testleri ag, model yuk ve gateway durumuna gore degiskenlik gosterdi.

## 5) Gorsel Modellerde Son Durum (Canli Dogrulama)

Asagidaki modellerde canli image output alindi:

- `gemini-3.1-flash-image-preview` (`:generateContent`)
- `gemini-3-pro-image-preview` (`:generateContent`)
- `gemini-2.5-flash-image` (`:generateContent`)
- `gemini-2.5-flash-image-preview` (`:generateContent`)
- `gemini-2.0-flash-preview-image-generation` (`:generateContent`)
- `imagen-4.0-generate-001` (`:predict`)
- `imagen-4.0-fast-generate-001` (`:predict`)
- `imagen-4.0-ultra-generate-001` (`:predict`)
- `imagen-3.0-generate-001` (`:predict`)
- `imagen-3.0-generate-002` (`:predict`)
- `imagen-3.0-fast-generate-001` (`:predict`)
- `virtual-try-on-001` (`:predict`)

### 5.1 Docs'ta var ama ortamda kisitli/erisilemeyenler

- `imagen-product-recontext-preview-06-30`: model referansi var, bu projede `unavailable` dondu.
- `imagen-4.0-upscale-preview`: 504/unstable.
- `imagen-upscale-001` ve bazi upscale varyantlari: 404.

### 5.2 Calismayan image alias denemeleri

- `gemini-3-flash-image-preview`: 404
- `gemini-3.1-pro-image-preview`: 404
- `gemini-2.5-pro-image*`: 404

### 5.3 Onemli ayirim (image output)

Asagidaki text modellerinde `responseModalities=["IMAGE"]` denemesi image output vermedi:

- `gemini-3-pro-preview`
- `gemini-3.1-pro-preview`
- `gemini-3-flash-preview`
- `gemini-2.5-pro`

Hata tipi: `Multi-modal output is not supported.`

Sonuc: Image output icin dogru model ailesi `*-image*` modelleri.

## 6) Video (Veo) Durumu

Dokumantasyondaki bircok Veo ID'si denendi (preview/fast/001 varyantlari).

Ortak sonuc:

- Cogu modelde `Organization Policy constraint constraints/vertexai.allowedModels` hatasi.
- Bazilarinda 404 (model varyanti bu tenant/proxyde yok).

Yorum: Video modeli teknik olarak mevcut olsa da bu ortamda policy nedeniyle kullanilamiyor.

## 7) Aspect Ratio / Cozunurluk Testi (Gemini 3.1 Flash Image)

Kaynak: docs + canli API testi.

### 7.1 Dokumantasyon

- `generationConfig.imageConfig.aspectRatio` alani destekleniyor.
- Not edilen destekli oranlar: `1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9`

### 7.2 Canli test sonucu

- `aspectRatio=1:1` -> 1024x1024
- `aspectRatio=16:9` -> 1376x768
- `aspectRatio=21:9` -> 1584x672
- `aspectRatio=8:1` -> 1408x768 (istenen oran uygulanmadi, fallback benzeri)

### 7.3 512px sorusu

Su alanlar denendi ve reddedildi:

- `outputResolution`
- `size`
- `width` / `height`

Hata: `Unknown name ... at generation_config.image_config`

Sonuc: Bu modelde dogrudan `512x512` zorlamak icin resmi bir alan gorunmedi; model bucket bazli cozunurluk donuyor.

## 8) Urun Egitimi / LoRA / Fine-tune Durumu

- Bu calisan image endpointlerinde dogrudan "urun LoRA egitimi" akisi bulunmadi.
- Pratikte calisan yol: inference tabanli referansli uretim/edit.
- E-ticaret odakli ozel endpointlerden:
  - `virtual-try-on-001` calisiyor.
  - `imagen-product-recontext-preview-06-30` bu projede gated/unavailable.

## 9) Uretilen Ornek Ciktilar (lokal)

Calisma boyunca olusan onemli gorseller:

- `awesome-cortexai/g31_product_gen_1.png`
- `awesome-cortexai/g31_product_edit_1.png`
- `awesome-cortexai/g31_multi_to_single_1.png`
- `awesome-cortexai/g3pro_image_edit_1.png`
- `awesome-cortexai/imagen4_generate_1.png`
- `awesome-cortexai/virtual_tryon_1.png`
- `awesome-cortexai/aspect_tests/config_1_1.png`
- `awesome-cortexai/aspect_tests/config_16_9.png`
- `awesome-cortexai/aspect_tests/config_21_9.png`
- `awesome-cortexai/aspect_tests/config_8_1.png`

## 10) Operasyonel Notlar

- Bu ortamda isteklerde `curl` daha stabil davrandi.
- Header kullanimi: `x-api-key`.
- Uzun isteklerde timeout ve edge kararsizliklari gorulebildi.
- Bazi isteklerde 1033/504 gibi edge/proxy kaynakli gecici hatalar gozlemlendi.

---

## Kisa Sonuc

- `aiplatform.vertexapis.com` kullanisli bir Vertex AI proxy'si gibi calisiyor.
- Gemini image + Imagen + try-on tarafinda beklenenden fazla model calisiyor.
- Video (Veo) policy ile bloklu.
- Gemini 3 TTS allowlist kilidine takiliyor.
- 3.1 Flash Image'da `512px` zorlamak ve `8:1` almak pratikte desteklenmiyor (su anki schema/behavior ile).
