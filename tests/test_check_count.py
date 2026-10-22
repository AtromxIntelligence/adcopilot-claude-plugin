"""The audit's check count, the same on every surface of this repo.

AdCopilot's audit catalogue is 70 checks, each listed (AdCopilot v2.44, its
decisions D221 and D225), and AdCopilot's own repo holds every count it
states to that number with one test (`tests/test_check_count_agreement.py`
there). This is the same check for the plugin, because the plugin's text is
read by the model as AdCopilot's word: a skill, the agent, a command, the
README or an eval mock that says 73 or 74 checks (or "seventy-three") after
v2.44 is a stale claim the model repeats to a customer.

It reads every tracked text file but this folder's (the tests quote stale
phrases to ban them) and fails on a count of the checks above 70 ("73
checks", "the 74-check audit", "of the 73 checks", "seventy-three") and on a
mock's `checks_total` that is not 70. A count of 70 or under is left alone:
it may be a run's own ("53 of the 59 checks that apply", "15 checks not
evaluated"). The README's release notes are history and keep the counts they
were written with (a paragraph that opens with a version in bold, "**0.2.12
(…", is not read), and the lines in `ALLOWED` quote an old count on purpose,
each with its reason.

Run with `python3 -m unittest discover -s tests -v` from the repository root.
"""

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_SIZE = 70

# "70 checks", "70-check", "of the 70 checks", "14 of the 70 checks" (its
# second number is the registry's). Never "check-in".
DIGITS = re.compile(r"\b(?:\d{1,2} of the )?(\d{2})[ -]checks?\b(?!-in)")
WORDS = re.compile(
    r"\b(sixty|seventy)(?:-(one|two|three|four|five|six|seven|eight|nine))?"
    r"(?=[ -]checks?\b(?!-in)|\b(?![ -]\w))", re.I)
TOTAL = re.compile(r"checks_total\\?\"?\s*:\s*(\d+)")
_TENS = {"sixty": 60, "seventy": 70}
_ONES = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
         "seven": 7, "eight": 8, "nine": 9}
# A release note: history, kept as written.
RELEASE_NOTE = re.compile(r"^\*\*\d+\.\d+\.\d+ \(")
# (file, words on the line): an old count quoted on purpose, and why.
ALLOWED = {
    # The grader's own comment on what 0.2.11 said, to explain its regex.
    ("evals/review-account-day-named-searches/case.yaml",
     "0.2.11 said \"73% of its 73 checks\""),
}


# The eval tool snapshots (`evals/**/mocks/adcopilot/_tools.json`): each is
# the server's served text at the revision its descriptions stamp ("Tools
# revision: 0066a60e." and so on), and plugin issue #5 holds that they are
# refreshed whole, from the server, by a generator, never edited by hand. A 74
# changed to 70 under a 0066a60e stamp would be a snapshot of no server, so
# they keep the count they were taken with until that refresh (0.2.15), and
# this scan leaves them out. Only a stamped snapshot is left out
# (test_only_stamped_snapshots_are_skipped).
SNAPSHOT = "/mocks/adcopilot/_tools.json"


def _snapshot(name):
    return name.endswith(SNAPSHOT)


def _tracked():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                         text=True, check=True).stdout.split()
    for name in out:
        if name.startswith("tests/") or name in ("LICENSE",):
            continue
        if _snapshot(name):
            continue
        path = ROOT / name
        try:
            yield name, path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError):
            continue


def _counts(text):
    """(number, the words) for every count of the checks in `text`."""
    for m in DIGITS.finditer(text):
        yield int(m.group(1)), m.group(0)
    for m in WORDS.finditer(text):
        n = _TENS[m.group(1).lower()] + _ONES.get((m.group(2) or "").lower(), 0)
        yield n, m.group(0)
    for m in TOTAL.finditer(text):
        yield int(m.group(1)), m.group(0)


class CheckCount(unittest.TestCase):
    def test_no_count_of_the_checks_is_above_seventy(self):
        stale, seen = [], 0
        for name, text in _tracked():
            for i, line in enumerate(text.split("\n"), 1):
                if name == "README.md" and RELEASE_NOTE.match(line):
                    continue
                if any(name == f and w in line for f, w in ALLOWED):
                    continue
                for n, words in _counts(line):
                    seen += 1
                    total = "checks_total" in words
                    if (total and n != REGISTRY_SIZE) or n > REGISTRY_SIZE:
                        stale.append(f"{name}:{i}: {words!r}")
        self.assertEqual(stale, [], "a check count above 70:\n"
                         + "\n".join(stale))
        # The scan reads something: the skills and the mocks state it.
        self.assertGreaterEqual(seen, 10)

    def test_the_scan_catches_a_stale_count(self):
        for text, n in (("attempts all 73 checks", 73),
                        ("the 74-check audit", 74),
                        ("three of the seventy-three.", 73),
                        ("of the seventy checks", 70),
                        ('"checks_total": 73', 73),
                        ('\\"checks_total\\":74', 74),
                        ("14 of the 73 checks", 73)):
            self.assertIn(n, [c for c, _ in _counts(text)], text)
        self.assertEqual(list(_counts("74 check-in runs")), [])
        self.assertEqual(list(_counts("seventy-three people")), [])

    def test_every_allowed_line_is_still_there(self):
        found = set()
        for name, text in _tracked():
            for f, w in ALLOWED:
                if name == f and w in text:
                    found.add((f, w))
        self.assertEqual(found, ALLOWED)

    def test_only_stamped_snapshots_are_skipped(self):
        out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                             text=True, check=True).stdout.split()
        skipped = [n for n in out if _snapshot(n)]
        self.assertGreater(len(skipped), 0)
        for name in skipped:
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(snapshot=name):
                self.assertRegex(text, r"Tools revision: [0-9a-f]{8}\.")

    def test_the_release_notes_are_skipped_only_as_release_notes(self):
        self.assertTrue(RELEASE_NOTE.match("**0.2.12 (2026-10-17, aligned"))
        self.assertFalse(RELEASE_NOTE.match("Deep attempts all seventy"))

    def test_the_json_mocks_state_seventy(self):
        """Each eval mock of a `full_audit` result carries the count it
        grades on; they all say 70."""
        found = 0
        for name, text in _tracked():
            if name.endswith("full_audit.md"):
                for n, _w in _counts(text):
                    if "checks_total" in _w:
                        found += 1
                        self.assertEqual(n, REGISTRY_SIZE, name)
        self.assertGreater(found, 0)


if __name__ == "__main__":
    unittest.main()
