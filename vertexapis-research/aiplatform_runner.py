#!/usr/bin/env python3
"""
Moduler aiplatform.vertexapis.com istemcisi.

Neden curl?
- Bu ortamda bazi Python HTTP denemeleri 403/kararsiz davrandigi icin
  istekler subprocess ile curl uzerinden atiliyor.

Ornekler:
  python3 aiplatform_runner.py list-models

  python3 aiplatform_runner.py text \
    --model gemini-3-pro-preview \
    --prompt "Kisa bir merhaba yaz" \
    --api-key "$VERTEX_API_KEY"

  python3 aiplatform_runner.py image \
    --model gemini-3.1-flash-image-preview \
    --prompt "Mat siyah bir kosu ayakkabisi, beyaz arka plan" \
    --aspect-ratio 1:1 \
    --ref ./urun1.png --ref ./urun2.png

  python3 aiplatform_runner.py predict-image \
    --model imagen-4.0-generate-001 \
    --prompt "Kirmizi elma, beyaz arka plan"

  python3 aiplatform_runner.py stt \
    --model gemini-2.5-pro \
    --audio ./ses.wav

  python3 aiplatform_runner.py try-on \
    --person ./person.png \
    --product ./shoe.png
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


DEFAULT_PROJECT = "vertex"
DEFAULT_OUTPUT_DIR = Path.home() / "awesome-cortexai" / "generated"
DEFAULT_TIMEOUT = 30


@dataclass(frozen=True)
class ModelSpec:
    model_id: str
    endpoint_type: str  # generateContent | predict
    default_location: str
    capabilities: List[str]


MODEL_REGISTRY: Dict[str, ModelSpec] = {
    # Text / multimodal
    "gemini-2.5-pro": ModelSpec("gemini-2.5-pro", "generateContent", "us-central1", ["text", "vision", "stt", "tools"]),
    "gemini-2.5-flash": ModelSpec("gemini-2.5-flash", "generateContent", "us-central1", ["text", "vision", "stt", "tools"]),
    "gemini-2.0-flash": ModelSpec("gemini-2.0-flash", "generateContent", "us-central1", ["text", "vision", "stt"]),
    "gemini-2.0-flash-lite": ModelSpec("gemini-2.0-flash-lite", "generateContent", "us-central1", ["text"]),
    "gemini-3-pro-preview": ModelSpec("gemini-3-pro-preview", "generateContent", "us", ["text", "vision", "stt", "tools"]),
    "gemini-3-flash-preview": ModelSpec("gemini-3-flash-preview", "generateContent", "us", ["text", "vision", "stt", "tools"]),
    "gemini-3.1-pro-preview": ModelSpec("gemini-3.1-pro-preview", "generateContent", "us", ["text", "vision", "stt", "tools"]),

    # Gemini image
    "gemini-3.1-flash-image-preview": ModelSpec("gemini-3.1-flash-image-preview", "generateContent", "us-central1", ["image_gen", "image_edit", "multi_image"]),
    "gemini-3-pro-image-preview": ModelSpec("gemini-3-pro-image-preview", "generateContent", "us", ["image_gen", "image_edit", "multi_image"]),
    "gemini-2.5-flash-image": ModelSpec("gemini-2.5-flash-image", "generateContent", "us", ["image_gen", "image_edit", "multi_image"]),
    "gemini-2.5-flash-image-preview": ModelSpec("gemini-2.5-flash-image-preview", "generateContent", "us", ["image_gen", "image_edit", "multi_image"]),
    "gemini-2.0-flash-preview-image-generation": ModelSpec("gemini-2.0-flash-preview-image-generation", "generateContent", "us", ["image_gen"]),

    # Imagen predict
    "imagen-4.0-generate-001": ModelSpec("imagen-4.0-generate-001", "predict", "us", ["image_gen"]),
    "imagen-4.0-fast-generate-001": ModelSpec("imagen-4.0-fast-generate-001", "predict", "us", ["image_gen"]),
    "imagen-4.0-ultra-generate-001": ModelSpec("imagen-4.0-ultra-generate-001", "predict", "us", ["image_gen"]),
    "imagen-3.0-generate-001": ModelSpec("imagen-3.0-generate-001", "predict", "us", ["image_gen"]),
    "imagen-3.0-generate-002": ModelSpec("imagen-3.0-generate-002", "predict", "us", ["image_gen"]),
    "imagen-3.0-fast-generate-001": ModelSpec("imagen-3.0-fast-generate-001", "predict", "us", ["image_gen"]),

    # E-commerce special
    "virtual-try-on-001": ModelSpec("virtual-try-on-001", "predict", "us", ["try_on"]),
}


def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def read_file_b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def guess_mime(path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    return mime or "application/octet-stream"


def call_curl_json(url: str, api_key: str, body: Dict[str, Any], timeout: int) -> Dict[str, Any]:
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
        json.dump(body, f, ensure_ascii=False)
        body_path = f.name

    try:
        cmd = [
            "curl",
            "-sS",
            "--max-time",
            str(timeout),
            "-X",
            "POST",
            url,
            "-H",
            f"x-api-key: {api_key}",
            "-H",
            "Content-Type: application/json",
            "-d",
            f"@{body_path}",
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        out = proc.stdout.strip()

        if not out:
            raise RuntimeError("Bos response alindi")

        if out.startswith("error code:"):
            raise RuntimeError(out)

        try:
            return json.loads(out)
        except json.JSONDecodeError as exc:
            snippet = out[:400]
            raise RuntimeError(f"JSON parse hatasi: {snippet}") from exc
    finally:
        try:
            os.remove(body_path)
        except OSError:
            pass


def build_generate_url(project: str, location: str, model: str) -> str:
    return (
        "https://aiplatform.vertexapis.com/v1/"
        f"projects/{project}/locations/{location}/publishers/google/models/{model}:generateContent"
    )


def build_predict_url(project: str, location: str, model: str) -> str:
    return (
        "https://aiplatform.vertexapis.com/v1/"
        f"projects/{project}/locations/{location}/publishers/google/models/{model}:predict"
    )


def save_inline_images(parts: List[Dict[str, Any]], out_dir: Path, prefix: str) -> List[Path]:
    out_paths: List[Path] = []
    out_dir.mkdir(parents=True, exist_ok=True)
    idx = 1
    for part in parts:
        inline = part.get("inlineData")
        if not inline:
            continue
        data_b64 = inline.get("data")
        if not data_b64:
            continue
        mime = inline.get("mimeType", "image/png")
        ext = "png"
        if "jpeg" in mime:
            ext = "jpg"
        elif "webp" in mime:
            ext = "webp"
        out_path = out_dir / f"{prefix}_{idx}.{ext}"
        out_path.write_bytes(base64.b64decode(data_b64))
        out_paths.append(out_path)
        idx += 1
    return out_paths


def print_error_response(resp: Dict[str, Any]) -> None:
    err = resp.get("error")
    if not err:
        return
    code = err.get("code")
    msg = err.get("message", "")
    eprint(f"API ERROR {code}: {msg}")


def cmd_list_models(_: argparse.Namespace) -> int:
    print("Model registry:")
    for name in sorted(MODEL_REGISTRY.keys()):
        spec = MODEL_REGISTRY[name]
        caps = ",".join(spec.capabilities)
        print(f"- {name} | {spec.endpoint_type} | loc={spec.default_location} | {caps}")
    return 0


def cmd_text(args: argparse.Namespace) -> int:
    spec = MODEL_REGISTRY[args.model]
    location = args.location or spec.default_location
    body: Dict[str, Any] = {
        "contents": [{"role": "user", "parts": [{"text": args.prompt}]}]
    }
    url = build_generate_url(args.project, location, args.model)
    resp = call_curl_json(url, args.api_key, body, args.timeout)

    if "error" in resp:
        print_error_response(resp)
        return 1

    parts = resp.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    text_parts = [p.get("text", "") for p in parts if "text" in p]
    print("\n".join([t for t in text_parts if t]))
    return 0


def cmd_image(args: argparse.Namespace) -> int:
    spec = MODEL_REGISTRY[args.model]
    location = args.location or spec.default_location
    model = args.model

    parts: List[Dict[str, Any]] = [{"text": args.prompt}]
    for ref in args.ref:
        ref_path = Path(ref)
        if not ref_path.exists():
            eprint(f"Referans dosyasi yok: {ref_path}")
            return 1
        parts.append(
            {
                "inlineData": {
                    "mimeType": guess_mime(ref_path),
                    "data": read_file_b64(ref_path),
                }
            }
        )

    body: Dict[str, Any] = {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }

    if args.aspect_ratio:
        body["generationConfig"]["imageConfig"] = {"aspectRatio": args.aspect_ratio}

    url = build_generate_url(args.project, location, model)
    resp = call_curl_json(url, args.api_key, body, args.timeout)
    if "error" in resp:
        print_error_response(resp)
        return 1

    candidate_parts = resp.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    ts = int(time.time())
    saved = save_inline_images(candidate_parts, Path(args.out_dir), f"{model}_{ts}")
    text_parts = [p.get("text", "") for p in candidate_parts if "text" in p]

    if text_parts:
        print("Model text output:")
        print("\n".join([t for t in text_parts if t]))

    if not saved:
        eprint("Image output bulunamadi.")
        return 1

    print("Kaydedilen dosyalar:")
    for p in saved:
        print(f"- {p}")
    return 0


def cmd_predict_image(args: argparse.Namespace) -> int:
    spec = MODEL_REGISTRY[args.model]
    location = args.location or spec.default_location
    body: Dict[str, Any] = {
        "instances": [{"prompt": args.prompt}],
        "parameters": {"sampleCount": args.sample_count, "addWatermark": False},
    }
    if args.aspect_ratio:
        body["parameters"]["aspectRatio"] = args.aspect_ratio

    url = build_predict_url(args.project, location, args.model)
    resp = call_curl_json(url, args.api_key, body, args.timeout)
    if "error" in resp:
        print_error_response(resp)
        return 1

    predictions = resp.get("predictions", [])
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = int(time.time())
    saved: List[Path] = []
    i = 1
    for pred in predictions:
        b64 = pred.get("bytesBase64Encoded")
        if not b64 and isinstance(pred.get("image"), dict):
            b64 = pred["image"].get("bytesBase64Encoded")
        if not b64:
            continue
        out_path = out_dir / f"{args.model}_{ts}_{i}.png"
        out_path.write_bytes(base64.b64decode(b64))
        saved.append(out_path)
        i += 1

    if not saved:
        eprint("Predict response icinde image bulunamadi.")
        return 1

    print("Kaydedilen dosyalar:")
    for p in saved:
        print(f"- {p}")
    return 0


def cmd_stt(args: argparse.Namespace) -> int:
    spec = MODEL_REGISTRY[args.model]
    location = args.location or spec.default_location
    audio_path = Path(args.audio)
    if not audio_path.exists():
        eprint(f"Ses dosyasi yok: {audio_path}")
        return 1

    prompt = args.prompt or "Bu ses kaydini kelimesi kelimesine transkribe et."
    body: Dict[str, Any] = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {
                        "inlineData": {
                            "mimeType": guess_mime(audio_path),
                            "data": read_file_b64(audio_path),
                        }
                    },
                ],
            }
        ]
    }
    url = build_generate_url(args.project, location, args.model)
    resp = call_curl_json(url, args.api_key, body, args.timeout)
    if "error" in resp:
        print_error_response(resp)
        return 1

    parts = resp.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    text = "\n".join([p.get("text", "") for p in parts if "text" in p]).strip()
    print(text)
    return 0


def cmd_try_on(args: argparse.Namespace) -> int:
    model = args.model
    spec = MODEL_REGISTRY[model]
    location = args.location or spec.default_location

    person = Path(args.person)
    product = Path(args.product)
    if not person.exists() or not product.exists():
        eprint("Person veya product dosyasi bulunamadi.")
        return 1

    body: Dict[str, Any] = {
        "instances": [
            {
                "personImage": {"image": {"bytesBase64Encoded": read_file_b64(person)}},
                "productImages": [{"image": {"bytesBase64Encoded": read_file_b64(product)}}],
            }
        ],
        "parameters": {
            "sampleCount": args.sample_count,
            "addWatermark": False,
        },
    }
    url = build_predict_url(args.project, location, model)
    resp = call_curl_json(url, args.api_key, body, args.timeout)
    if "error" in resp:
        print_error_response(resp)
        return 1

    predictions = resp.get("predictions", [])
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = int(time.time())
    saved: List[Path] = []
    for i, pred in enumerate(predictions, start=1):
        b64 = pred.get("bytesBase64Encoded")
        if not b64 and isinstance(pred.get("image"), dict):
            b64 = pred["image"].get("bytesBase64Encoded")
        if not b64:
            continue
        out_path = out_dir / f"tryon_{ts}_{i}.png"
        out_path.write_bytes(base64.b64decode(b64))
        saved.append(out_path)

    if not saved:
        eprint("Try-on response icinde image bulunamadi.")
        return 1

    print("Kaydedilen dosyalar:")
    for p in saved:
        print(f"- {p}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="aiplatform.vertexapis.com moduler calistirici")
    parser.add_argument("--api-key", default=os.getenv("VERTEX_API_KEY"), help="x-api-key veya VERTEX_API_KEY env")
    parser.add_argument("--project", default=DEFAULT_PROJECT, help="Project id (varsayilan: vertex)")
    parser.add_argument("--location", help="Model location override (us, us-central1, global)")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Curl timeout (s)")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUTPUT_DIR), help="Cikti klasoru")

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-models", help="Kayitli model listesini goster")

    p_text = sub.add_parser("text", help="Text generation")
    p_text.add_argument("--model", required=True, choices=sorted(MODEL_REGISTRY.keys()))
    p_text.add_argument("--prompt", required=True)

    p_img = sub.add_parser("image", help="Gemini image generation/edit")
    p_img.add_argument("--model", required=True, choices=sorted(MODEL_REGISTRY.keys()))
    p_img.add_argument("--prompt", required=True)
    p_img.add_argument("--aspect-ratio", help="Orn: 1:1, 16:9, 21:9")
    p_img.add_argument("--ref", action="append", default=[], help="Referans gorsel (tekrarli kullanilabilir)")

    p_pred = sub.add_parser("predict-image", help="Imagen predict image generation")
    p_pred.add_argument("--model", required=True, choices=sorted(MODEL_REGISTRY.keys()))
    p_pred.add_argument("--prompt", required=True)
    p_pred.add_argument("--sample-count", type=int, default=1)
    p_pred.add_argument("--aspect-ratio", help="Imagen aspect ratio (destekliyorsa)")

    p_stt = sub.add_parser("stt", help="Audio -> text transcription")
    p_stt.add_argument("--model", required=True, choices=sorted(MODEL_REGISTRY.keys()))
    p_stt.add_argument("--audio", required=True)
    p_stt.add_argument("--prompt", help="Transcription instruction")

    p_try = sub.add_parser("try-on", help="Virtual try-on")
    p_try.add_argument("--model", default="virtual-try-on-001", choices=sorted(MODEL_REGISTRY.keys()))
    p_try.add_argument("--person", required=True)
    p_try.add_argument("--product", required=True)
    p_try.add_argument("--sample-count", type=int, default=1)

    return parser


def validate_api_key(api_key: Optional[str]) -> None:
    if not api_key:
        eprint("API key yok. --api-key ver veya VERTEX_API_KEY set et.")
        sys.exit(2)


def validate_model_for_command(model: str, command: str) -> None:
    spec = MODEL_REGISTRY[model]
    if command in {"text", "stt", "image"} and spec.endpoint_type != "generateContent":
        eprint(f"{model} modeli {command} icin uygun degil (endpoint={spec.endpoint_type}).")
        sys.exit(2)
    if command in {"predict-image", "try-on"} and spec.endpoint_type != "predict":
        eprint(f"{model} modeli {command} icin uygun degil (endpoint={spec.endpoint_type}).")
        sys.exit(2)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list-models":
        return cmd_list_models(args)

    validate_api_key(args.api_key)

    if hasattr(args, "model"):
        validate_model_for_command(args.model, args.command)

    try:
        if args.command == "text":
            return cmd_text(args)
        if args.command == "image":
            return cmd_image(args)
        if args.command == "predict-image":
            return cmd_predict_image(args)
        if args.command == "stt":
            return cmd_stt(args)
        if args.command == "try-on":
            return cmd_try_on(args)
    except RuntimeError as exc:
        eprint(str(exc))
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
