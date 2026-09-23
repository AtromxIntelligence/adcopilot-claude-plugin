#!/usr/bin/env python3
"""Per-case and per-skill delta of the with-skills run over the tools-only run.

Usage: delta.py WITH.json TOOLS_ONLY.json [--markdown] [--fail-below X]

Both files are `claude plugin eval --json` results for the same cases. A case
belongs to the skill its `tool_used: Skill` grader names (the skill that fired),
and is OWNED by the skill whose tag it carries (connect, measure, launch); the
setup-* cases are the setup command's and fire adcopilot-connect, so they count
towards "fired" but not "owned". The deletion rule in the spec reads on owned.
With --fail-below, exit 1 when any skill's owned delta is below X.
"""
import argparse
import json
import os
import re
import sys

TAG_TO_SKILL = {"connect": "adcopilot-connect", "measure": "adcopilot-measure", "launch": "adcopilot-launch"}


def case_tags(root, case_dir):
    """Tags from the case.yaml, read without a YAML library (tags: [a, b] on one line)."""
    path = os.path.join(root or "", case_dir, "case.yaml")
    try:
        with open(path) as f:
            for line in f:
                m = re.match(r"^tags:\s*\[(.*)\]\s*$", line)
                if m:
                    return [t.strip().strip("'\"") for t in m.group(1).split(",") if t.strip()]
    except OSError:
        pass
    return []


def load(path):
    with open(path) as f:
        d = json.load(f)
    root = d.get("suite", {}).get("root")
    cases = {}
    for c in d["cases"]:
        runs = c.get("arms", {}).get("with") or []
        fired = None
        for g in c.get("graders", []):
            cfg = g.get("config", {})
            if g.get("type") == "tool_used" and cfg.get("tool") == "Skill":
                m = re.search(r"adcopilot-(\w+)", cfg.get("input_match") or cfg.get("inputMatch") or "")
                if m and int(cfg.get("max", 10**9) or 10**9) > 0:
                    fired = "adcopilot-" + m.group(1)
        tags = case_tags(root, c.get("dir", ""))
        owner = next((TAG_TO_SKILL[t] for t in tags if t in TAG_TO_SKILL), None)
        if owner is None:
            prefix = c["name"].split("-", 1)[0]
            owner = TAG_TO_SKILL.get(prefix)
        cases[c["name"]] = {
            "score": c["aggregates"]["score"],
            "fired": fired,
            "owner": owner,
            "runs": len(runs),
            "errors": sum(1 for r in runs if r.get("error")),
            "cost": sum((r.get("costUsd") or 0) + (r.get("judgeCostUsd") or 0) for r in runs),
        }
    return d, cases


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("with_json")
    ap.add_argument("tools_only_json")
    ap.add_argument("--markdown", action="store_true")
    ap.add_argument("--fail-below", type=float, default=None)
    a = ap.parse_args()

    dw, W = load(a.with_json)
    dt, T = load(a.tools_only_json)
    names = [n for n in W if n in T]
    missing = sorted((set(W) | set(T)) - set(names))

    rows = []
    for n in names:
        rows.append((n, W[n]["owner"] or "-", W[n]["fired"] or "-", W[n]["score"], T[n]["score"], W[n]["score"] - T[n]["score"], W[n]["errors"] + T[n]["errors"]))

    print("## Skill delta over the tools-only arm")
    print()
    print(f"with-skills: {a.with_json} (judge {dw.get('suite', {}).get('judgeModel') or 'default'}, ${dw.get('costUsd', 0):.2f})")
    print(f"tools-only:  {a.tools_only_json} (judge {dt.get('suite', {}).get('judgeModel') or 'default'}, ${dt.get('costUsd', 0):.2f})")
    print()
    print("| Case | Owner | Fires | With skill | Tools only | Delta | Run errors |")
    print("|---|---|---|---|---|---|---|")
    for n, owner, fired, w, t, dl, err in rows:
        print(f"| {n} | {owner} | {fired} | {w:.3f} | {t:.3f} | {dl:+.3f} | {err} |")
    if missing:
        print()
        print("Cases present in only one result, not compared: " + ", ".join(missing))

    skills = sorted({r[1] for r in rows if r[1] != "-"} | {r[2] for r in rows if r[2] != "-"})
    print()
    print("| Skill | Owned cases | Owned delta (mean) | Min owned delta | Cases that fire it | Fired delta (mean) |")
    print("|---|---|---|---|---|---|")
    worst = {}
    for s in skills:
        owned = [r for r in rows if r[1] == s]
        fired = [r for r in rows if r[2] == s]
        om = sum(r[5] for r in owned) / len(owned) if owned else float("nan")
        omin = min((r[5] for r in owned), default=float("nan"))
        fm = sum(r[5] for r in fired) / len(fired) if fired else float("nan")
        worst[s] = om
        print(f"| {s} | {len(owned)} | {om:+.3f} | {omin:+.3f} | {len(fired)} | {fm:+.3f} |")

    print()
    print("A skill with no positive owned delta has not earned its place: the connector's own playbook and tool descriptions already carry what its cases measure.")

    if a.fail_below is not None:
        bad = [s for s, v in worst.items() if not (v >= a.fail_below)]
        if bad:
            print()
            print(f"FAIL: owned delta below {a.fail_below:+.3f} for: " + ", ".join(bad))
            sys.exit(1)


if __name__ == "__main__":
    main()
