#!/usr/bin/env python3
"""Per-case and per-skill delta of the with-skills run over the tools-only run.

Usage: delta.py WITH.json TOOLS_ONLY.json [--markdown] [--fail-below X]

Both files are `claude plugin eval --json` results for the same cases. A case
belongs to the skill its `tool_used: Skill` grader names (the skill that fired),
and is OWNED by the skill whose tag it carries (connect, measure, launch); the
setup-* cases are the setup command's and fire adcopilot-connect, so they count
towards "fired" but not "owned". The deletion rule in the spec reads on owned.

A case whose TOOLS-ONLY arm scores at or above --guard-at (0.8, the CI
threshold) is demonstrating behaviour the connector already carries. It is
classified as a REGRESSION GUARD from the measurement itself — nothing in a
case file can declare it one — and is excluded from the owned-delta gate,
while its with-skills score must still reach --guard-at. A case the tools-only
arm scores LOW and the skill does not lift is a genuinely dead case and stays
in the gate, which is what the minimum is for.

With --fail-below X, exit 1 when any skill's owned delta over its gated cases —
the mean OR the minimum — is below X, when a skill has no gated case at all
(every case it owns is server-carried, so nothing justifies it), or when a
guard's with-skills score is below --guard-at.
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
    ap.add_argument("--guard-at", type=float, default=0.8, help="tools-only score at or above which a case is a regression guard (default 0.8, the CI threshold)")
    a = ap.parse_args()

    dw, W = load(a.with_json)
    dt, T = load(a.tools_only_json)
    names = [n for n in W if n in T]
    missing = sorted((set(W) | set(T)) - set(names))

    rows = []
    for n in names:
        owner = W[n]["owner"] or "-"
        if T[n]["score"] >= a.guard_at:
            klass = "guard"
        elif owner != "-":
            klass = "gated"
        else:
            klass = "command"
        rows.append((n, owner, W[n]["fired"] or "-", W[n]["score"], T[n]["score"], W[n]["score"] - T[n]["score"], W[n]["errors"] + T[n]["errors"], klass))

    print("## Skill delta over the tools-only arm")
    print()
    print(f"with-skills: {a.with_json} (judge {dw.get('suite', {}).get('judgeModel') or 'default'}, ${dw.get('costUsd', 0):.2f})")
    print(f"tools-only:  {a.tools_only_json} (judge {dt.get('suite', {}).get('judgeModel') or 'default'}, ${dt.get('costUsd', 0):.2f})")
    print()
    print(f"| Case | Owner | Fires | With skill | Tools only | Delta | Class (guard = tools-only ≥ {a.guard_at:.1f}) | Run errors |")
    print("|---|---|---|---|---|---|---|---|")
    for n, owner, fired, w, t, dl, err, klass in rows:
        note = klass
        if klass == "guard" and w < a.guard_at:
            note = f"guard — BELOW {a.guard_at:.1f} WITH THE SKILL"
        print(f"| {n} | {owner} | {fired} | {w:.3f} | {t:.3f} | {dl:+.3f} | {note} | {err} |")
    if missing:
        print()
        print("Cases present in only one result, not compared: " + ", ".join(missing))

    skills = sorted({r[1] for r in rows if r[1] != "-"} | {r[2] for r in rows if r[2] != "-"})
    print()
    print("| Skill | Gated cases | Gated delta (mean) | Min gated delta | Guards (server-carried) | Cases that fire it | Fired delta (mean) | Verdict |")
    print("|---|---|---|---|---|---|---|---|")
    bad = []
    for s in skills:
        owned = [r for r in rows if r[1] == s]
        gated = [r for r in owned if r[7] == "gated"]
        guards = [r for r in owned if r[7] == "guard"]
        fired = [r for r in rows if r[2] == s]
        om = sum(r[5] for r in gated) / len(gated) if gated else float("nan")
        omin = min((r[5] for r in gated), default=float("nan"))
        fm = sum(r[5] for r in fired) / len(fired) if fired else float("nan")
        weak_guards = [r[0] for r in guards if r[3] < a.guard_at]
        # The gate reads on the mean AND the minimum over the cases the server does not already
        # carry: one strong case must not carry a dead one, and a server-carried case is not dead.
        reasons = []
        if owned and not gated:
            reasons.append("no case the server does not carry")
        if weak_guards:
            reasons.append("guard below %.1f with the skill: %s" % (a.guard_at, ", ".join(weak_guards)))
        if a.fail_below is None:
            if gated and not (omin > 0):
                reasons.append("NO DELTA on a gated case")
        else:
            if gated and not (om >= a.fail_below):
                reasons.append(f"mean {om:+.3f} < {a.fail_below:+.3f}")
            if gated and not (omin >= a.fail_below):
                reasons.append(f"min {omin:+.3f} < {a.fail_below:+.3f}")
        verdict = ("FAIL: " + "; ".join(reasons)) if reasons else "ok"
        if reasons and (a.fail_below is not None or weak_guards or (owned and not gated)):
            bad.append(s)
        gtxt = ", ".join(f"{r[0]} ({r[3]:.3f}/{r[4]:.3f})" for r in guards) or "-"
        print(f"| {s} | {len(gated)} | {om:+.3f} | {omin:+.3f} | {gtxt} | {len(fired)} | {fm:+.3f} | {verdict} |")

    print()
    print(f"A case the tools-only arm scores at or above {a.guard_at:.1f} is a regression guard on behaviour the connector already carries: it is kept at {a.guard_at:.1f} with the skill and left out of the skill's delta. A skill with no positive delta over the cases the server does not carry has not earned its place; the gate reads on the minimum as well as the mean of those cases, so one strong case cannot carry a dead one.")

    if bad:
        print()
        print("FAIL: " + ", ".join(bad))
        sys.exit(1)


if __name__ == "__main__":
    main()
