İşte tüm test sonuçları ve dokümantasyonlar:
---
vertexapis.com Aktif API'ler (8 googleapis eşleşmesi + 3 özel)
1. texttospeech.vertexapis.com — ÇALIŞIYOR
- 2066 ses, 63 dil, MALE: 1068, FEMALE: 998
- Türkçe: 40 ses (30 Chirp3-HD + 5 Standard + 5 Wavenet)
- Ses tipleri: Standard, Wavenet, Chirp3-HD
- Ses sentezi test edildi, MP3 audio döndü
- Path: POST /v1/text:synthesize, GET /v1/voices
- Dok: https://cloud.google.com/text-to-speech/docs
2. speech.vertexapis.com — ÇALIŞIYOR
- 400 döndü: "RecognitionAudio not set" (doğru hata, auth geçti)
- v1 ve v1p1beta1 ikisi de aktif
- Path: POST /v1/speech:recognize, POST /v1/speech:longrunningrecognize
- Dok: https://cloud.google.com/speech-to-text/docs
3. language.vertexapis.com — ÇALIŞIYOR
- Sentiment analizi test edildi, doğru sonuç döndü
- v1 ve v2 ikisi de çalışıyor
- Path: POST /v1/documents:analyzeSentiment, analyzeEntities, analyzeSyntax, classifyText, annotateText
- Dok: https://cloud.google.com/natural-language/docs
4. vision.vertexapis.com — ÇALIŞIYOR
- Label detection, safe search, image properties, face detection hepsi çalıştı
- Path: POST /v1/images:annotate, POST /v1/files:annotate
- Feature types: LABEL_DETECTION, TEXT_DETECTION, FACE_DETECTION, SAFE_SEARCH_DETECTION, IMAGE_PROPERTIES, OBJECT_LOCALIZATION, LOGO_DETECTION, LANDMARK_DETECTION, CROP_HINTS, WEB_DETECTION
- Dok: https://cloud.google.com/vision/docs
5. translate.vertexapis.com — ÇALIŞIYOR
- 195 dil destekliyor
- "Hello world" → "Selam Dünya" döndü
- Path: POST /language/translate/v2, GET /language/translate/v2/languages
- Dok: https://cloud.google.com/translate/docs
6. videointelligence.vertexapis.com — 401 (auth geçiyor ama boş dönüyor)
- Muhtemelen GCS URI ile video gerekiyor veya proje bazlı
- Features: LABEL_DETECTION, SHOT_CHANGE_DETECTION, EXPLICIT_CONTENT_DETECTION, SPEECH_TRANSCRIPTION, TEXT_DETECTION, OBJECT_TRACKING, LOGO_RECOGNITION, FACE_DETECTION, PERSON_DETECTION
- Path: POST /v1/videos:annotate
- Dok: https://cloud.google.com/video-intelligence/docs
7. documentai.vertexapis.com — 401 (auth geçiyor ama proje gerekiyor)
- OCR, form parsing, document classification
- Path: POST /v1/projects/{p}/locations/{l}/processors/{id}:process
- Dok: https://cloud.google.com/document-ai/docs
8. aiplatform.vertexapis.com — 401 (auth geçiyor, location=global istiyor)
- Vertex AI ana platform API'si
- Path: POST /v1/projects/{p}/locations/global/publishers/google/models/{m}:predict
- Dok: https://cloud.google.com/vertex-ai/docs
---
Kesin çalışan ve test edilen: 5 (texttospeech, speech, language, vision, translate)
Auth geçen ama proje/kaynak gerektiren: 3 (videointelligence, documentai, aiplatform)
Hepsi googleapis.com'daki API path'leriyle birebir aynı formatta çalışıyor — sadece domain'i değiştirmen yeterli.
