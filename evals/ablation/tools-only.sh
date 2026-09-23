#!/usr/bin/env bash
# The tools-only ablation: what does each SKILL add over the connector alone?
#
# `claude plugin eval --ablation with-without` removes the WHOLE plugin, and the
# plugin is what registers the connector, so its without-arm has no tools at all
# and its delta measures "skill and tools versus neither" — an empty SKILL.md
# would score the same. The honest comparison keeps the connector and drops only
# the skill: this script copies the plugin, keeps .mcp.json, evals/ and every
# mock, reduces each skill to its frontmatter plus one sentence (so the Skill
# tool still fires and the case stays comparable), runs the same suite against
# both copies with --ablation none, and prints the per-case and per-skill delta.
# A skill whose cases show no delta over this arm has not earned its place.
#
# Usage:  evals/ablation/tools-only.sh [extra claude plugin eval args, e.g. --case 'measure-*']
# Env:    ABLATION_OUT           where the two JSON results and the table go
#                                (default evals/results/ablation-<timestamp>/, gitignored)
#         ABLATION_WITH_JSON     reuse this --json result for the with-skills arm instead of running it
#         ABLATION_JUDGE_MODEL   judge for llm graders (default sonnet; CI uses the same)
#         ABLATION_CONCURRENCY   -j for claude plugin eval (default 3)
#         ABLATION_MAX_COST_USD  --max-cost-usd per arm (default 15)
#         ABLATION_WORKDIR       where the tools-only copy is built (default: a temp dir, removed afterwards)
#         ABLATION_FAIL_BELOW    exit 1 if any skill's delta over its own cases is below this (default: report only)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STAMP="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
OUT="${ABLATION_OUT:-$ROOT/evals/results/ablation-$STAMP}"
JUDGE="${ABLATION_JUDGE_MODEL:-sonnet}"
JOBS="${ABLATION_CONCURRENCY:-3}"
MAX_COST="${ABLATION_MAX_COST_USD:-15}"
WITH_JSON="${ABLATION_WITH_JSON:-}"
FAIL_BELOW="${ABLATION_FAIL_BELOW:-}"

if [ -n "${ABLATION_WORKDIR:-}" ]; then
  WORK="$ABLATION_WORKDIR"; CLEAN=0
else
  WORK="$(mktemp -d "${TMPDIR:-/tmp}/adcopilot-tools-only.XXXXXX")"; CLEAN=1
fi
COPY="$WORK/plugin"
mkdir -p "$OUT" "$COPY"

command -v claude >/dev/null || { echo "claude is not on PATH" >&2; exit 1; }
command -v python3 >/dev/null || { echo "python3 is not on PATH" >&2; exit 1; }

# 1. The tools-only copy: everything the plugin ships except the skill bodies.
rsync -a --exclude .git --exclude 'evals/results' "$ROOT/" "$COPY/"
for skill in "$COPY"/skills/*/SKILL.md; do
  fm="$(awk 'NR==1 && $0=="---"{print; inside=1; next} inside{print; if($0=="---") exit}' "$skill")"
  if [ -z "$fm" ]; then echo "no frontmatter in $skill" >&2; exit 1; fi
  { printf '%s\n\n' "$fm"; printf 'Help the customer with this through the AdCopilot connector.\n'; } > "$skill"
done
echo "tools-only copy at $COPY; stubbed skills:"
for skill in "$COPY"/skills/*/SKILL.md; do echo "  $(basename "$(dirname "$skill")"): $(wc -l < "$skill") lines"; done

EVAL_ARGS=(--ablation none --trust-plugin --no-publish --threshold 0 --judge-model "$JUDGE" -j "$JOBS" --max-cost-usd "$MAX_COST")

# 2. The tools-only arm. Exit 2 (cost ceiling / rejected credential) is fatal; exit 1 cannot
#    happen on a threshold of 0 unless a case failed to load, which is also fatal.
echo "== tools-only arm"
claude plugin eval "$COPY" "${EVAL_ARGS[@]}" --json "$OUT/tools-only.json" "$@"

# 3. The with-skills arm, unless a result was handed in.
if [ -n "$WITH_JSON" ]; then
  cp "$WITH_JSON" "$OUT/with-skills.json"
else
  echo "== with-skills arm"
  claude plugin eval "$ROOT" "${EVAL_ARGS[@]}" --json "$OUT/with-skills.json" "$@"
fi

# 4. The delta.
DELTA_ARGS=(--markdown)
[ -n "$FAIL_BELOW" ] && DELTA_ARGS+=(--fail-below "$FAIL_BELOW")
python3 "$ROOT/evals/ablation/delta.py" "$OUT/with-skills.json" "$OUT/tools-only.json" "${DELTA_ARGS[@]}" | tee "$OUT/delta.md"
status=$?
echo "results in $OUT"
[ "$CLEAN" = 1 ] && rm -rf "$WORK"
exit $status
