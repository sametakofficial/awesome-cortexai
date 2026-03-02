# Vertex Generator - Quick Reference Cheat Sheet

## Setup (One Time)

```bash
# Install dependencies
pip3 install requests

# Set API key
export VERTEX_API_KEY="sk-your-api-key-here"

# Or add to ~/.bashrc for persistence
echo 'export VERTEX_API_KEY="sk-your-key"' >> ~/.bashrc
source ~/.bashrc
```

## Quick Commands

### Images (Fast - 5-15 seconds)

```bash
# Simplest - Gemini API
python3 vertex_generator.py image "your prompt here"

# Beta Fast (Flash model)
python3 vertex_generator.py image "your prompt" --api beta

# Beta Quality (Pro model)
python3 vertex_generator.py image "your prompt" --api beta --model pro

# With aspect ratio
python3 vertex_generator.py image "your prompt" --api beta --aspect-ratio 16:9
```

### Videos (Slow - 30-120 seconds)

```bash
# Basic video
python3 vertex_generator.py video "your prompt"

# Short video (5 seconds)
python3 vertex_generator.py video "your prompt" --duration 5

# With audio
python3 vertex_generator.py video "your prompt" --audio

# Fast test (720p)
python3 vertex_generator.py video "your prompt" --resolution 720p --duration 5
```

## Common Use Cases

### Social Media Images

```bash
# Instagram post (1:1)
python3 vertex_generator.py image "product photo" --api beta --aspect-ratio 1:1

# Instagram story (9:16)
python3 vertex_generator.py image "portrait" --api beta --aspect-ratio 9:16

# YouTube thumbnail (16:9)
python3 vertex_generator.py image "thumbnail design" --api beta --aspect-ratio 16:9

# Twitter header (21:9)
python3 vertex_generator.py image "banner design" --api beta --aspect-ratio 21:9
```

### Video Content

```bash
# Short clip for social (5s)
python3 vertex_generator.py video "dynamic intro" --duration 5 --audio

# B-roll footage (8s)
python3 vertex_generator.py video "nature scene" --duration 8 --resolution 1080p

# Quick test (720p, 3s)
python3 vertex_generator.py video "test animation" --duration 3 --resolution 720p
```

## API Selection Guide

| Need | Use This Command |
|------|------------------|
| Quick image test | `--api gemini` |
| High quality image | `--api beta --model pro` |
| Fast image batch | `--api beta --model flash` |
| Any video | `--api gemini` (only option) |

## Rate Limits

```
gemini.vertexapis.com:  50/hour,  500/day  (image + video)
beta.vertexapis.com:    N/A,      3500/day (image only)
```

**Tips:**
- Use Beta for high-volume images (3500/day)
- Use Gemini for videos (only option, 500/day)
- Space requests by 2-5 seconds

## Output Location

```bash
# All files saved to:
~/vertex_outputs/

# List generated files:
ls -lth ~/vertex_outputs/

# Open latest image:
xdg-open ~/vertex_outputs/$(ls -t ~/vertex_outputs/*.png | head -1)

# Open latest video:
mpv ~/vertex_outputs/$(ls -t ~/vertex_outputs/*.mp4 | head -1)
```

## Troubleshooting One-Liners

```bash
# Check if API key is set
echo $VERTEX_API_KEY

# Test network connectivity
curl -I https://gemini.vertexapis.com/health

# Check rate limit status (gemini only)
curl -H "Authorization: Bearer $VERTEX_API_KEY" \
  https://gemini.vertexapis.com/key/status

# View recent errors
python3 vertex_generator.py image "test" --api gemini 2>&1 | grep -i error

# Check Python version
python3 --version

# Verify requests module
python3 -c "import requests; print(requests.__version__)"
```

## Batch Generation

```bash
# Generate multiple images
for prompt in "cat" "dog" "bird"; do
    python3 vertex_generator.py image "$prompt in space" --api beta
    sleep 2
done

# From file
while read prompt; do
    python3 vertex_generator.py image "$prompt" --api beta
    sleep 3
done < prompts.txt
```

## Integration (Python)

```python
from vertex_generator import VertexGenerator
import os

gen = VertexGenerator(os.getenv("VERTEX_API_KEY"))

# Generate image
img = gen.generate_image_gemini("a cat")

# Generate video
vid = gen.generate_video_gemini("ocean waves", duration_seconds=5)
```

## Performance Tips

1. **Testing:** Use `--api beta --model flash` (fastest)
2. **Production:** Use `--api beta --model pro` (best quality)
3. **Videos:** Use `--resolution 720p --duration 5` for testing
4. **Rate limits:** Beta API has 7x higher limit than Gemini

## Common Errors & Fixes

| Error | Fix |
|-------|-----|
| "No API key" | `export VERTEX_API_KEY="sk-..."` |
| "Video only supported on gemini" | Add `--api gemini` |
| Rate limit | Wait or use different API |
| Timeout | Video takes 30-120s, be patient |

## Aliases (Optional)

Add to `~/.bashrc`:

```bash
# Quick aliases
alias vimg='python3 ~/awesome-cortexai/vertexapis-research/vertex_generator.py image'
alias vvid='python3 ~/awesome-cortexai/vertexapis-research/vertex_generator.py video'
alias vout='cd ~/vertex_outputs && ls -lth'

# Usage after sourcing bashrc:
# vimg "a cat in space"
# vvid "ocean waves" --duration 5
# vout
```

## Quick Test

Run all tests:
```bash
cd ~/awesome-cortexai/vertexapis-research
./test_generator.sh
```

## File Size Estimates

| Type | Resolution | Duration | Size |
|------|------------|----------|------|
| Image (PNG) | N/A | N/A | 1-5 MB |
| Video (720p) | 720p | 5s | 2-5 MB |
| Video (1080p) | 1080p | 5s | 5-10 MB |
| Video (1080p) | 1080p | 10s | 10-20 MB |

## Pro Tips

1. **Always test with 720p first** for videos
2. **Use Beta Flash for rapid iteration** on images
3. **Use Beta Pro for final images** when quality matters
4. **Add --seed** for reproducible results
5. **Space requests 2-5 seconds** to respect rate limits
6. **Check output folder** after generation: `~/vertex_outputs/`

## Getting Help

```bash
# Full help
python3 vertex_generator.py --help

# Examples
python3 vertex_generator.py --help | grep -A 20 Examples
```

---

**Need more info?** Check `GENERATOR_README.md` for complete documentation.
