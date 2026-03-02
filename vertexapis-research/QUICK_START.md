# 🚀 Quick Start Guide

## 1️⃣ Setup (30 seconds)

```bash
# Set API key
export VERTEX_API_KEY="sk-your-api-key-here"

# Or add to ~/.bashrc permanently
echo 'export VERTEX_API_KEY="sk-your-key"' >> ~/.bashrc
source ~/.bashrc
```

## 2️⃣ Your First Image (10 seconds)

```bash
python3 vertex_media_generator.py image "a cat in space"
```

## 3️⃣ Your First Video (90 seconds)

```bash
python3 vertex_media_generator.py video "ocean waves" -d 5 -r 720p
```

## 📋 Common Commands

```bash
# List providers
python3 vertex_media_generator.py list

# Image - Gemini (simple)
python3 vertex_media_generator.py image "your prompt" -p gemini

# Image - Beta Flash (fast, 3500/day)
python3 vertex_media_generator.py image "your prompt" -p beta

# Image - Beta Pro (quality)
python3 vertex_media_generator.py image "your prompt" -p beta --model pro

# Video - Gemini only
python3 vertex_media_generator.py video "your prompt" -p gemini

# Quick test
./quick_test.sh
```

## 📊 Provider Choice

| Need | Command |
|------|---------|
| Quick image test | `-p gemini` |
| High-volume images | `-p beta` (3500/day) |
| Best image quality | `-p beta --model pro` |
| Any video | `-p gemini` (only option) |

## 📁 Output

All files: `~/vertex_outputs/`

```bash
# List files
ls -lth ~/vertex_outputs/

# Open latest
xdg-open ~/vertex_outputs/$(ls -t ~/vertex_outputs/ | head -1)
```

## 🎯 Best Practices

1. **Test with 720p first** for videos
2. **Use Beta for images** (7x higher limit)
3. **Space requests 2-5 seconds** apart
4. **Be patient with videos** (30-120s)

## 🛠️ Troubleshooting

```bash
# No API key?
export VERTEX_API_KEY="sk-your-key"

# Video not working?
# Only Gemini supports video:
python3 vertex_media_generator.py video "test" -p gemini

# Want higher quality?
# Use Beta Pro model:
python3 vertex_media_generator.py image "test" -p beta --model pro
```

## 📖 More Info

- Detailed usage: `USAGE.md`
- Research report: `vertex-apis-comprehensive-report.html`
- Main README: `README.md`

---

**Simple. Modular. Powerful.**
