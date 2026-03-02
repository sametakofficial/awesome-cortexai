#!/usr/bin/env python3
import base64
import json
import os
import struct
import subprocess
import tempfile
import time
import zlib
from pathlib import Path


API_KEY = os.getenv("VERTEX_API_KEY")
URL = (
    "https://aiplatform.vertexapis.com/v1/projects/vertex/locations/us-central1/"
    "publishers/google/models/gemini-3-pro-image-preview:generateContent"
)
OUT_DIR = Path("/home/samet/awesome-cortexai/generated/pro_image_param_tests")
OUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_MD = Path(
    "/home/samet/awesome-cortexai/vertexapis-research/endpoints2/"
    "gemini-3-pro-image-supported-params-test.md"
)


def tiny_png_b64() -> str:
    width, height = 4, 4
    raw = b""
    for _ in range(height):
        raw += b"\x00" + (b"\xff\x00\x00" * width)

    def chunk(ctype: bytes, data: bytes) -> bytes:
        c = ctype + data
        return (
            struct.pack(">I", len(data))
            + c
            + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")
    return base64.b64encode(png).decode("ascii")


def parse_image_dims(data: bytes):
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        w, h = struct.unpack(">II", data[16:24])
        return w, h, "png"
    if data.startswith(b"\xff\xd8"):
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in [
                0xC0,
                0xC1,
                0xC2,
                0xC3,
                0xC5,
                0xC6,
                0xC7,
                0xC9,
                0xCA,
                0xCB,
                0xCD,
                0xCE,
                0xCF,
            ]:
                h = struct.unpack(">H", data[i + 5 : i + 7])[0]
                w = struct.unpack(">H", data[i + 7 : i + 9])[0]
                return w, h, "jpeg"
            if marker in [0xD8, 0xD9]:
                i += 2
                continue
            if i + 4 > len(data):
                break
            seg = struct.unpack(">H", data[i + 2 : i + 4])[0]
            i += 2 + seg
    return None, None, "unknown"


def call_api(body: dict, timeout_sec: int = 35):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(body, f, ensure_ascii=False)
        temp_path = f.name
    try:
        cmd = [
            "curl",
            "-sS",
            "--max-time",
            str(timeout_sec),
            "-w",
            "\nHTTP:%{http_code}\n",
            "-X",
            "POST",
            URL,
            "-H",
            f"x-api-key: {API_KEY}",
            "-H",
            "Content-Type: application/json",
            "-d",
            f"@{temp_path}",
        ]
        p = subprocess.run(cmd, capture_output=True, text=True)
        out = p.stdout
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass

    if "\nHTTP:" in out:
        raw, tail = out.rsplit("\nHTTP:", 1)
        http = tail.strip().splitlines()[0]
    else:
        raw, http = out, "000"

    raw = raw.strip()
    if not raw:
        return http, {"error": "EMPTY_RESPONSE"}
    if raw.startswith("error code:"):
        return http, {"error": raw}
    try:
        return http, json.loads(raw)
    except json.JSONDecodeError:
        return http, {"error": "NON_JSON", "raw": raw[:300]}


def run_case(name: str, body: dict):
    http, data = call_api(body)
    rec = {
        "test": name,
        "http": http,
        "ok": False,
        "error": None,
        "image_count": 0,
        "dims": [],
        "mimes": [],
        "text": None,
        "files": [],
    }

    if "error" in data and not data.get("candidates"):
        if isinstance(data.get("error"), dict):
            rec["error"] = f"{data['error'].get('code')} {data['error'].get('message', '')[:180]}"
        else:
            rec["error"] = str(data.get("error"))[:220]
        return rec

    if isinstance(data.get("error"), dict):
        rec["error"] = f"{data['error'].get('code')} {data['error'].get('message', '')[:180]}"
        return rec

    rec["ok"] = True
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    texts = [p.get("text", "") for p in parts if "text" in p]
    if texts:
        rec["text"] = " ".join([t.strip() for t in texts if t.strip()])[:200]

    i = 1
    ts = int(time.time())
    for p in parts:
        inline = p.get("inlineData")
        if not inline:
            continue
        b64 = inline.get("data")
        if not b64:
            continue
        blob = base64.b64decode(b64)
        w, h, fmt = parse_image_dims(blob)
        ext = "png" if fmt == "png" else "jpg" if fmt == "jpeg" else "bin"
        out = OUT_DIR / f"{name}_{ts}_{i}.{ext}"
        out.write_bytes(blob)
        rec["image_count"] += 1
        rec["dims"].append(f"{w}x{h}" if w and h else "unknown")
        rec["mimes"].append(inline.get("mimeType", "?"))
        rec["files"].append(str(out))
        i += 1

    return rec


def main():
    if not API_KEY:
        raise SystemExit("Set VERTEX_API_KEY before running this script")

    ref_b64 = tiny_png_b64()
    prompt = "Generate a photorealistic red apple product image on pure white background, no text."

    cases = [
        (
            "baseline",
            {
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
            },
        ),
        (
            "aspect_1_1",
            {
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {
                    "responseModalities": ["TEXT", "IMAGE"],
                    "imageConfig": {"aspectRatio": "1:1"},
                },
            },
        ),
        (
            "aspect_16_9",
            {
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {
                    "responseModalities": ["TEXT", "IMAGE"],
                    "imageConfig": {"aspectRatio": "16:9"},
                },
            },
        ),
        (
            "aspect_21_9",
            {
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {
                    "responseModalities": ["TEXT", "IMAGE"],
                    "imageConfig": {"aspectRatio": "21:9"},
                },
            },
        ),
        (
            "imageSize_4K",
            {
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {
                    "responseModalities": ["TEXT", "IMAGE"],
                    "imageConfig": {"aspectRatio": "16:9", "imageSize": "4K"},
                },
            },
        ),
        (
            "imageSize_2K",
            {
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {
                    "responseModalities": ["TEXT", "IMAGE"],
                    "imageConfig": {"aspectRatio": "16:9", "imageSize": "2K"},
                },
            },
        ),
        (
            "output_png",
            {
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {
                    "responseModalities": ["TEXT", "IMAGE"],
                    "imageConfig": {
                        "aspectRatio": "1:1",
                        "imageOutputOptions": {"mimeType": "image/png"},
                    },
                },
            },
        ),
        (
            "output_jpeg",
            {
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {
                    "responseModalities": ["TEXT", "IMAGE"],
                    "imageConfig": {
                        "aspectRatio": "1:1",
                        "imageOutputOptions": {"mimeType": "image/jpeg"},
                    },
                },
            },
        ),
        (
            "person_generation_allow",
            {
                "contents": [{"role": "user", "parts": [{"text": "Generate a portrait photo of a smiling person."}]}],
                "generationConfig": {
                    "responseModalities": ["TEXT", "IMAGE"],
                    "imageConfig": {"aspectRatio": "1:1", "personGeneration": "allow_all"},
                },
            },
        ),
        (
            "safety_settings",
            {
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
                "safetySettings": [
                    {
                        "method": "PROBABILITY",
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                    }
                ],
            },
        ),
        (
            "edit_inline_ref",
            {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"inlineData": {"mimeType": "image/png", "data": ref_b64}},
                            {"text": "Convert this image to black-and-white cartoon style."},
                        ],
                    }
                ],
                "generationConfig": {
                    "responseModalities": ["TEXT", "IMAGE"],
                    "imageConfig": {"aspectRatio": "1:1"},
                },
            },
        ),
    ]

    results = [run_case(name, body) for name, body in cases]

    lines = []
    lines.append("# Gemini 3 Pro Image - Dokumantasyon Bazli Parametre Testi")
    lines.append("")
    lines.append("- Endpoint: `aiplatform.vertexapis.com`")
    lines.append("- Model: `gemini-3-pro-image-preview`")
    lines.append("- Location: `us-central1`")
    lines.append("- Kapsam: docs'ta gecen image parametreleri + 4K denemesi")
    lines.append("")
    lines.append("| Test | HTTP | Durum | Gorsel | Boyut | MIME | Not |")
    lines.append("|---|---:|---|---:|---|---|---|")
    for r in results:
        status = "✅" if r["ok"] else "❌"
        dims = ", ".join(r["dims"]) if r["dims"] else "-"
        mimes = ", ".join(r["mimes"]) if r["mimes"] else "-"
        note = (r["error"] or r["text"] or "-").replace("|", "\\|")[:180]
        lines.append(
            f"| `{r['test']}` | {r['http']} | {status} | {r['image_count']} | {dims} | {mimes} | {note} |"
        )

    lines.append("")
    lines.append("## Kaydedilen Dosyalar")
    for r in results:
        for f in r["files"]:
            lines.append(f"- `{f}`")

    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written: {REPORT_MD}")
    for r in results:
        print(r["test"], r["http"], "OK" if r["ok"] else "ERR", r["dims"], r["error"])


if __name__ == "__main__":
    main()
