#!/usr/bin/env python3
"""
Cortex AI + opencode provider test suite.
Her provider'dan tüm modelleri otomatik algılayıp paralel test eder.

Kullanım: python3 test_providers.py
"""

import json, subprocess, socket, time, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

CONFIG = Path.home() / ".config" / "opencode" / "opencode.json"
SKIP = ["perplexity.claude.gg", "kiro-gateway-4040", "kiro-gateway-8080"]
TIMEOUT = 60
WORKERS = 1  # opencode session lock var, paralel çalışmıyor

G = "\033[92m"; R = "\033[91m"; Y = "\033[93m"; C = "\033[96m"; B = "\033[1m"; X = "\033[0m"


def port_ok(port):
    try:
        s = socket.create_connection(("127.0.0.1", port), timeout=2); s.close(); return True
    except:
        return False


def oc_run(model, prompt, thinking=False, variant=None):
    cmd = ["opencode", "run", "--format", "json", "-m", model]
    if thinking: cmd.append("--thinking")
    if variant: cmd.extend(["--variant", variant])
    cmd.append(prompt)

    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT, cwd=str(Path.home()))
        out = (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return {"ok": False, "err": f"TIMEOUT {TIMEOUT}s"}
    except Exception as e:
        return {"ok": False, "err": str(e)[:80]}

    text = ""; tool = False; reasoning = 0; err = None

    for line in out.strip().split("\n"):
        line = line.strip()
        if not line: continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue

        t = d.get("type", "")
        p = d.get("part", {})

        if t == "text":
            text = p.get("text", "")[:80]
        elif t == "tool_call":
            tool = True
        elif t == "step_finish":
            reasoning = p.get("tokens", {}).get("reasoning", 0)
        elif t == "error":
            msg = p.get("message") or p.get("error") or ""
            if isinstance(msg, str) and msg:
                err = msg[:80]

    if err:
        return {"ok": False, "err": err}
    if not text and not tool:
        return {"ok": False, "err": "boş response"}
    return {"ok": True, "text": text, "tool": tool, "reasoning": reasoning}


def main():
    cfg = json.load(open(CONFIG))

    print(f"\n{B}{C}{'═'*70}\n  PROXY KONTROL\n{'═'*70}{X}")
    for name, port in [("xml-toolcall-proxy", 4012), ("schema-fixer-proxy", 4015), ("perplexity-proxy", 4016)]:
        s = f"{G}✓{X}" if port_ok(port) else f"{R}✗{X}"
        print(f"  {s} {name} (:{port})")

    # Tüm modelleri topla
    all_models = []
    for pname, pd in cfg["provider"].items():
        if pname in SKIP: continue
        for mid, m in pd.get("models", {}).items():
            variants = list(m.get("variants", {}).keys())
            all_models.append({
                "p": pname, "m": mid, "full": f"{pname}/{mid}",
                "tc": m.get("tool_call", False),
                "v": variants,
                "hi": variants[-1] if variants else None,
            })

    print(f"\n{B}{C}{'═'*70}\n  {len(all_models)} MODEL BULUNDU\n{'═'*70}{X}")

    # Her provider'dan en hafif modeli seç (hızlı test)
    # Tercih sırası: haiku > sonnet > flash > mini > nano > ilk model
    prefer = ["haiku", "nano", "mini", "lite", "2.5-flash", "flash", "sonnet", "chat", "gpt-5"]
    seen = set()
    test_models = []
    for p_name in dict.fromkeys(m["p"] for m in all_models):
        if p_name in seen: continue
        seen.add(p_name)
        p_models = [m for m in all_models if m["p"] == p_name]
        picked = p_models[0]
        for pref in prefer:
            match = [m for m in p_models if pref in m["m"].lower()]
            if match:
                picked = match[0]
                break
        test_models.append(picked)

    tasks = []
    for t in test_models:
        tasks.append(("basic", t))
        if t["tc"]:
            tasks.append(("tool", t))
        if t["hi"]:
            tasks.append(("think_on", t))
            tasks.append(("think_off", t))

    print(f"\n{B}{C}{'═'*70}\n  {len(tasks)} TEST — {len(test_models)} provider, {WORKERS} paralel\n{'═'*70}{X}")

    results = {}

    def do(task):
        kind, t = task
        f = t["full"]
        if kind == "basic":
            return t["p"], t["m"], kind, oc_run(f, "What is 2+2? Just the number.")
        elif kind == "tool":
            return t["p"], t["m"], kind, oc_run(f, "List files in the current directory. Use your file listing tool.")
        elif kind == "think_on":
            return t["p"], t["m"], kind, oc_run(f, "What is 15*17?", thinking=True, variant=t["hi"])
        elif kind == "think_off":
            return t["p"], t["m"], kind, oc_run(f, "What is 2+2?")

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = {pool.submit(do, t): t for t in tasks}
        for fut in as_completed(futs):
            try:
                prov, mid, kind, res = fut.result()
                key = f"{prov}/{mid}"
                if key not in results: results[key] = {}
                results[key][kind] = res

                if res["ok"]:
                    detail = ""
                    if kind == "tool":
                        detail = f"{G}tool_call{X}" if res["tool"] else f"{Y}text only{X}"
                    elif kind == "think_on":
                        detail = f"reasoning={res['reasoning']}"
                    else:
                        detail = res["text"][:30]
                    print(f"  {G}✓{X} {kind:10s} {key:45s} {detail}")
                else:
                    print(f"  {R}✗{X} {kind:10s} {key:45s} {res['err'][:40]}")
            except Exception as e:
                print(f"  {R}✗ EXCEPTION: {e}{X}")

    # Sonuç tablosu
    print(f"\n{B}{C}{'═'*70}\n  SONUÇ TABLOSU\n{'═'*70}{X}")
    print(f"\n  {'Provider/Model':<45s} {'Basic':>6s} {'Tool':>6s} {'ThinkOn':>8s} {'ThinkOff':>9s} {'R.Tok':>6s}")
    print(f"  {'─'*45} {'─'*6} {'─'*6} {'─'*8} {'─'*9} {'─'*6}")

    ok_count = 0; fail_count = 0; warn_count = 0

    for t in test_models:
        key = f"{t['p']}/{t['m']}"
        r = results.get(key, {})

        def s(k):
            if k not in r: return f"{'—':>6s}"
            return f"{G}{'✓':>6s}{X}" if r[k]["ok"] else f"{R}{'✗':>6s}{X}"

        def tc():
            if "tool" not in r: return f"{'—':>6s}"
            res = r["tool"]
            if not res["ok"]: return f"{R}{'✗':>6s}{X}"
            if res["tool"]: return f"{G}{'✓':>6s}{X}"
            return f"{Y}{'~':>6s}{X}"

        def rt():
            if "think_on" not in r: return f"{'—':>6s}"
            if not r["think_on"]["ok"]: return f"{R}{'✗':>6s}{X}"
            return f"{r['think_on']['reasoning']:>6d}"

        # Count
        for k, v in r.items():
            if v["ok"]:
                if k == "tool" and not v.get("tool"): warn_count += 1
                else: ok_count += 1
            else:
                fail_count += 1

        print(f"  {key:<45s} {s('basic')} {tc()} {s('think_on')} {s('think_off')} {rt()}")

    print(f"\n  {G}Geçti: {ok_count}{X} | {Y}Uyarı: {warn_count}{X} | {R}Başarısız: {fail_count}{X}")

    # Hatalar
    errors = []
    for key, r in results.items():
        for k, v in r.items():
            if not v["ok"]:
                errors.append((key, k, v["err"]))
    if errors:
        print(f"\n{B}{R}  Hatalar:{X}")
        for key, k, e in errors:
            print(f"    {key} [{k}]: {e}")

    print()


if __name__ == "__main__":
    main()
