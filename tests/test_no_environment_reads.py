"""Nothing in the plugin reads the installer's environment, and nothing in it is
a long run of base64.

The plugin directory held 0.2.17 for review under its rule "Uses a credential
from the user's machine". Its pre-submission checklist says not to read a
credential that is already set in the user's environment and send it to a
server, "even in a README example", or to remove every part that reads one; and
to commit readable source instead of anything the security scan cannot read,
because code it cannot read is held for a reviewer. The plugin folder is the
repository root, so `.github/`, `tests/` and `evals/` ship in it and the scan
reads them as it reads the skills.

What the review found, each fixed in 0.2.18 and held here:

- a workflow that read two variables the CI runner sets, next to a container
  run;
- a test that handed its subprocess the whole environment of the machine it
  ran on;
- a README step that pointed Claude Code at a profile folder under the home
  directory, which is where a login lives;
- a Cursor install link whose connector configuration was base64.

So no file in the plugin, other than an image, may read a variable of the
machine it runs on, with one deliberate exception: `evals/ablation/tools-only.sh`
reads its own settings (`ABLATION_*`), the scratch directory (`TMPDIR`) and its
own script variables, each named below. Nor may one hold a run of 80 or more
base64 characters, or the base64 of a JSON object, which is what the Cursor link
carried.

The patterns are spelled in pieces so that this file does not hold what it
forbids: the scan reads `tests/` too, and the guard is one of the plugin's own
files, so it is held to its own rule.

The rule covers every file the plugin ships bar the images. Nothing in the eval
tool snapshots (`_tools.json`) or the mocks trips the base64 rule, so it was not
narrowed to the folders a customer reads.

Run with `python3 -m unittest discover -s tests -v` from the repository root
(stdlib only; CI runs it in checks.yml).
"""

import base64
import json
import os
import re
import sys
import unittest
from urllib.parse import quote

# The helpers sit beside this file; the path is set so this file also runs
# on its own (`python3 tests/test_no_environment_reads.py`).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from structure_helpers import read  # noqa: E402
from test_plugin_size import IMAGE_OR_FONT, plugin_files  # noqa: E402


def spelled(*pieces):
    return re.compile("".join(pieces))


# (what it is, pattern). Each pattern is written in two or more pieces, none of
# which is the forbidden text on its own.
FORBIDDEN = [
    ("a variable the GitHub runner sets",
     spelled(r"\bGIT", "HUB_[A-Z0-9_]+")),
    ("a variable the GitHub runner sets",
     spelled(r"\bRUN", "NER_[A-Z0-9_]+")),
    ("the home directory's variable",
     spelled(r"\$\{?HO", r"ME\b")),
    ("a read of the process environment (Python)",
     spelled(r"\benv", r"iron\b")),
    ("a read of the process environment (any language)",
     spelled(r"\bget", r"env\b")),
    ("a read of the process environment (Node)",
     spelled(r"\bprocess\.", "env\\b")),
    ("a read of the process environment (Deno)",
     spelled(r"\bDeno\.", "env\\b")),
    ("the command that prints the environment",
     spelled(r"\bprint", r"env\b")),
    ("a workflow secret",
     spelled(r"\$\{\{\s*sec", r"rets\.")),
]


# A run of base64 characters, in each of the two alphabets (they are never mixed
# in one string, which is also what keeps a URL path, with its slashes and
# hyphens, from reading as base64). The standard alphabet takes the
# percent-encoded forms of the three characters a link carries it with
# (padding, slash, plus), and the run is measured in characters as written, so
# the percent-encoded padding counts as three each.
B64_RUNS = (
    re.compile(r"(?:[A-Za-z0-9+/]|%3[Dd]|%2[FfBb])+={0,2}"),
    re.compile(r"[A-Za-z0-9_-]+={0,2}"),
)
B64_MIN_CHARS = 80

# base64 of a JSON object always opens with these three characters: this is
# what the Cursor link's configuration was, and it is shorter than the run above
# for a small object, so it is caught on its own.
B64_JSON = re.compile(r"ey" + r"J[A-Za-z0-9+/_-]{16,}")


# `evals/ablation/tools-only.sh`, the one script that reads settings from the
# environment on purpose. Every name it reads is listed, and a new one is a
# deliberate edit here. None is a credential.
ABLATION_SCRIPT = "evals/ablation/tools-only.sh"
ABLATION_SETTINGS = {
    "ABLATION_CONCURRENCY",
    "ABLATION_FAIL_BELOW",
    "ABLATION_JUDGE_MODEL",
    "ABLATION_MAX_COST_USD",
    "ABLATION_OUT",
    "ABLATION_WITH_JSON",
    "ABLATION_WORKDIR",
}
# The scratch directory its temporary copy is made in, and the shell's own
# record of where the script is.
ABLATION_SHELL = {"TMPDIR", "BASH_SOURCE"}
# The script's own variables: set by the script, read by the script.
ABLATION_OWN = {
    "CLEAN", "COPY", "DELTA_ARGS", "EVAL_ARGS", "FAIL_BELOW", "JOBS", "JUDGE",
    "MAX_COST", "OUT", "ROOT", "STAMP", "VERSION", "WITH_JSON", "WORK",
    "fm", "marker", "skill", "status",
}
CREDENTIAL_WORDS = re.compile(r"TOKEN|KEY|SECRET|PASSWORD|PASSWD|CREDENTIAL|AUTH",
                              re.I)


def text_files():
    """(name, text) for every plugin file bar the images and fonts. A file
    that is not UTF-8 text is reported by the caller as one nothing can read."""
    for name, _size in plugin_files():
        if os.path.splitext(name)[1].lower() in IMAGE_OR_FONT:
            continue
        try:
            yield name, read(name)
        except UnicodeDecodeError:
            yield name, None


def forbidden_reads(text):
    """(line number, what it is, the text matched) for each forbidden read in
    `text`."""
    found = []
    for number, line in enumerate(text.splitlines(), 1):
        for what, pattern in FORBIDDEN:
            m = pattern.search(line)
            if m:
                found.append((number, what, m.group(0)))
    return found


def looks_like_base64(run):
    """Base64 of anything real has capitals, small letters and digits in it by
    the time it is 80 characters long. A slug of lower-case words does not."""
    return (re.search(r"[A-Z]", run) is not None
            and re.search(r"[a-z]", run) is not None
            and re.search(r"[0-9]", run) is not None)


def base64_runs(text):
    """(line number, the run, trimmed) for each long base64 run, and each
    base64 JSON object, in `text`."""
    found = []
    for number, line in enumerate(text.splitlines(), 1):
        for pattern in B64_RUNS:
            for m in pattern.finditer(line):
                run = m.group(0)
                if len(run) >= B64_MIN_CHARS and looks_like_base64(run):
                    found.append((number, run[:40] + "..."))
        for m in B64_JSON.finditer(line):
            found.append((number, m.group(0)[:40] + "..."))
    return found


def cursor_link_as_it_was():
    """The install link 0.2.17 carried, rebuilt from its parts: the connector's
    configuration as base64 in a link, which is what the directory could not
    read. Built here so that this file does not hold it."""
    config = json.dumps({"type": "http", "url": "https://mcp.adcopilot.cloud/mcp"},
                        separators=(",", ":"))
    encoded = quote(base64.b64encode(config.encode()).decode(), safe="")
    return "https://cursor.com/en/install-mcp?name=adcopilot&config=" + encoded


class NoEnvironmentReads(unittest.TestCase):

    def test_no_file_reads_a_variable_of_the_machine_it_runs_on(self):
        problems = []
        for name, text in text_files():
            if text is None:
                problems.append("%s is not UTF-8 text, so nothing can read it" % name)
                continue
            for number, what, matched in forbidden_reads(text):
                problems.append("%s:%d has %s: %s" % (name, number, what, matched))
        self.assertEqual(problems, [],
                         "the plugin directory holds a plugin that reads a "
                         "credential from the user's machine; remove these:\n"
                         + "\n".join(problems))

    def test_no_file_holds_a_long_run_of_base64(self):
        problems = []
        for name, text in text_files():
            if text is None:
                continue  # reported by the test above
            for number, run in base64_runs(text):
                problems.append("%s:%d has %s" % (name, number, run))
        self.assertEqual(problems, [],
                         "the plugin directory holds code the security scan "
                         "cannot read for a reviewer; write it out:\n"
                         + "\n".join(problems))

    def test_the_ablation_script_reads_only_its_own_variables(self):
        script = read(ABLATION_SCRIPT)
        names = set(re.findall(r"\$\{?([A-Za-z_][A-Za-z0-9_]*)", script))
        allowed = ABLATION_SETTINGS | ABLATION_SHELL | ABLATION_OWN
        self.assertEqual(sorted(names - allowed), [],
                         "%s reads a variable that is not named in this file; "
                         "name it here if it is the script's own, and make sure "
                         "it is not a credential" % ABLATION_SCRIPT)
        # The settings the script's header documents are the settings it reads.
        for setting in sorted(ABLATION_SETTINGS):
            with self.subTest(setting=setting):
                self.assertIn(setting, names)
        # None of what it may read is a credential.
        for name in sorted(ABLATION_SETTINGS | ABLATION_SHELL | ABLATION_OWN):
            with self.subTest(name=name):
                self.assertIsNone(CREDENTIAL_WORDS.search(name), name)

    def test_the_leak_check_mounts_the_checkout_by_its_directory_and_still_fails(self):
        """0.2.18: the workflow no longer names a runner variable. It mounts the
        step's working directory, which is the checkout, and writes its log to a
        temporary file; it fails on a leak, on an error line, and on a scan that
        read no commit, as it did."""
        workflow = read(".github/workflows/leak-check.yml")
        for part in ('-v "$PWD:/repo:ro" -w /repo "$IMAGE"',
                     'log="$(mktemp)"',
                     "--exit-code 1",
                     'if [ "$rc" -ne 0 ]; then',
                     "if grep -q 'ERR' \"$log\"; then",
                     "if ! grep -Eq '[1-9][0-9]* commits scanned' \"$log\"; then"):
            with self.subTest(part=part):
                self.assertIn(part, workflow)

    def test_the_guard_finds_what_it_is_for(self):
        # Each forbidden read, written out from its parts.
        runner = "$" + "GITHUB" + "_WORKSPACE:/repo"
        temp = "log=\"$" + "RUNNER" + "_TEMP/x.log\""
        home = "mkdir -p \"$" + "HOME" + "/.x\""
        python_read = "os." + "env" + "iron"
        python_get = "os." + "get" + "env('X')"
        node_read = "process." + "env" + ".X"
        secret = "${{ " + "sec" + "rets.X }}"
        for sample in (runner, temp, home, python_read, python_get, node_read,
                       secret):
            with self.subTest(sample=sample):
                self.assertTrue(forbidden_reads(sample), sample)
        # The words near them that are fine.
        for sample in ("ABLATION_OUT", "the user's environment variable",
                       "$" + "HOME" + "WORK", "CI_RUNNER", "environment"):
            with self.subTest(sample=sample):
                self.assertEqual(forbidden_reads(sample), [], sample)

    def test_the_guard_finds_the_cursor_link_it_replaced(self):
        link = cursor_link_as_it_was()
        self.assertIn("config=" + "ey" + "J", link)
        self.assertEqual(len(link.split("config=")[1]), B64_MIN_CHARS)
        found = base64_runs("   [Add AdCopilot to Cursor](%s)" % link)
        # The run and the base64 JSON object both fire on it.
        self.assertEqual(len(found), 2, found)
        # Text that is not base64: a digest, a long URL path and a long slug,
        # which hold slashes and hyphens, and a sentence.
        for sample in ("sha256:" + "ab" * 32,
                       "https://developers.example.com/documentation/ads-commerce/"
                       "ads-ai-connectors/ads-mcp-server/ads-mcp-server-overview",
                       "a-slug-of-words-" * 6,
                       "The connector is at https://mcp.adcopilot.cloud/mcp and "
                       "needs no key."):
            with self.subTest(sample=sample):
                self.assertEqual(base64_runs(sample), [], sample)

    def test_this_file_is_held_to_its_own_rule(self):
        name = "tests/test_no_environment_reads.py"
        self.assertEqual(forbidden_reads(read(name)), [])
        self.assertEqual(base64_runs(read(name)), [])


if __name__ == "__main__":
    unittest.main()
