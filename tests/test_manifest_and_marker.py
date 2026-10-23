"""The manifest, the plugin marker, the README's release note and the commands.

One of the structural test files that `tests/test_structure.py` was split
into in 0.2.15. At 273 KB that file was over the plugin directory's 256 KiB
limit for a file that is not an image or a font. The tests moved verbatim, by
topic (same classes, same names, same assertions), and the helpers they share
live in `structure_helpers.py`; `tests/test_plugin_size.py` keeps any file
from growing past the limit again.

Run with `python3 -m unittest discover -s tests -v` from the repository root
(stdlib only; CI runs it in checks.yml).

What it pins, and why each one is here:
- The manifest is 0.2.4 and every command the README lists exists.
- The plugin marker says its version (#696): every interactive
  `get_org_context` call passes `source: "claude-plugin/<version>"` with
  the manifest's own version, so a release bump that misses one copy
  fails here; no bare `"claude-plugin"` is left; the version is the
  X.Y.Z the server reads; and every eval grader that checks the marker
  fails the bare value and passes the versioned one.

- The release bump's other halves: the README carries a note for the
  manifest's version that says the release checklist comes before the tag,
  and every release note names its own marker; no compiled cache is tracked
  (a `.pyc` names the path it was compiled from).
- The docs skill answers a question about AdCopilot from the one
  `get_org_context` call (0.2.12), and the measure skill's description names
  both of its routes.
- The commands and skills carry no sales or banned wording, and the README's
  "What it will not do" lists only what is enforced or qualified.
"""

import os
import sys
import json
import re
import subprocess
import unittest

# The helpers sit beside this file; the path is set so this file also runs
# on its own (`python3 tests/test_manifest_and_marker.py`).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from structure_helpers import (  # noqa: E402
    BANNED,
    BARE_MARKER,
    COMMANDS,
    NO_SKILLS,
    ROOT,
    SCHEDULED_SOURCE_RULE,
    VERSIONED_COMMANDS,
    flat,
    frontmatter,
    manifest_version,
    plugin_marker,
    read,
    section,
)


# 0.2.12: the docs skill answers a question about AdCopilot from the one
# get_org_context call. On 2026-10-14 "walk me through what it can do" got a
# capability list, an unasked performance review (the server's next_step had
# handed the account to adcopilot-review), a second list in another grouping
# and three closing questions.
DOCS_ROUTING = ("Make no Google Ads, Analytics, Search Console or Tag Manager "
                "read for it, and start no other AdCopilot skill.")


class Commands(unittest.TestCase):

    def test_each_command_exists_with_frontmatter(self):
        for name in COMMANDS:
            with self.subTest(command=name):
                fm = frontmatter(read("commands/%s.md" % name))
                self.assertRegex(fm, r"(?m)^name: %s$" % name)
                self.assertRegex(fm, r"(?m)^description: \S")

    def test_interactive_reads_carry_the_plugin_marker(self):
        """A skill or agent that calls `get_org_context` stamps plugin use.

        The skills and agents are globbed from disk, not listed, because the
        0.2.5 review found three new components omitting the marker while this
        test passed — it only looked at four commands, so "all 49 tests pass"
        was no evidence for the thing it was quoted as proving. Without the
        marker the server never stamps `orgs.plugin_first_seen_at`, and the
        customer keeps being asked to install what they already use.

        Commands are the four that read directly; the rest legitimately
        delegate to a skill (`commands/launch.md` only names the tool while
        `adcopilot-launch` makes the call), and a test that cannot tell a
        delegation from a read would fail on prose.

        `adcopilot-daily` carries both: its run is unattended, so it passes
        `source: "claude-scheduled"`, and from 0.2.14 (#22) its set-up and the reply
        after a run, with a person here, pass the versioned marker.
        """
        for name in ("audit", "daily", "weekly", "negatives"):
            with self.subTest(command=name):
                self.assertIn(plugin_marker(), read("commands/%s.md" % name))

        readers = ["skills/%s/SKILL.md" % d
                   for d in sorted(os.listdir(os.path.join(ROOT, "skills")))]
        agents_dir = os.path.join(ROOT, "agents")
        if os.path.isdir(agents_dir):
            readers += ["agents/%s" % f for f in sorted(os.listdir(agents_dir))
                        if f.endswith(".md")]
        checked = 0
        for rel in readers:
            text = read(rel)
            if "get_org_context" not in text:
                continue
            checked += 1
            with self.subTest(surface=rel):
                markers = ([plugin_marker()] + (['source: "claude-scheduled"']
                                                if "adcopilot-daily" in rel
                                                else []))
                for marker in markers:
                    self.assertIn(
                        marker, text,
                        "%s calls get_org_context without %s" % (rel, marker))
        self.assertGreaterEqual(checked, 7, "expected every reading skill and "
                                            "agent to be checked, saw %d" % checked)

    def test_daily_runs_the_four_reads(self):
        text = read("commands/daily.md")
        for read_ in ("budget_pacing", "analyze_search_terms", "days: 7",
                      "change_event", "ad_group_ad"):
            with self.subTest(read=read_):
                self.assertIn(read_, text)

    def test_daily_hands_a_scheduled_run_to_the_skill(self):
        # Someone may save "/adcopilot:daily" itself as the scheduled task.
        text = read("commands/daily.md")
        self.assertIn("started by a schedule", text)
        self.assertIn("`adcopilot-daily` skill's run", text)

    def test_readme_lists_every_command(self):
        readme = read("README.md")
        for name in COMMANDS:
            with self.subTest(command=name):
                self.assertIn("`/adcopilot:%s`" % name, readme)
        self.assertIn("adcopilot-daily", readme)


class Readme(unittest.TestCase):

    def test_will_not_do_lists_only_what_is_enforced_or_qualified(self):
        # "What it will not do" is the server's limits and the approval
        # prompt's. A scheduled run's read-only instructions are neither, so
        # they are described where the schedule is, with what keeps them.
        will_not = section(read("README.md"), "## What it will not do") or ""
        self.assertNotIn("scheduled run", will_not)

    def test_the_schedule_section_says_what_keeps_a_run_to_reads(self):
        # Since D186 (AdCopilot `scheduled_guard.py`) the server refuses every
        # write tool on a connection in a scheduled run, AdCopilot's own notes
        # aside; it knows the run only from its first call. The 0.2.14 review:
        # "Nothing on AdCopilot's side stops a change" was no longer true.
        morning = " ".join((section(read("README.md"),
                                    "### Every morning, without asking") or "").split())
        self.assertNotIn("It changes nothing", morning)
        self.assertNotIn("Nothing on AdCopilot's side stops a change", morning)
        self.assertIn("AdCopilot holds a scheduled run to reads as well: once a "
                      "run's first call is `get_org_context` with "
                      "`source: \"claude-scheduled\"`, AdCopilot refuses every "
                      "tool that changes Google Ads", morning)
        self.assertIn("a run that skips it or sends another source is not held",
                      morning)
        self.assertIn("**Automatically approve**", morning)
        self.assertIn("**Blocked**", morning)

    def test_each_release_note_names_its_own_marker(self):
        # The 0.2.14 review: #24's version bump rewrote the 0.2.13 note's
        # "moves to `claude-plugin/0.2.13`" to 0.2.14. A release note is
        # history: the marker it says the files move to is its own version.
        notes = 0
        for line in read("README.md").splitlines():
            m = re.match(r"\*\*(\d+\.\d+\.\d+) \(", line)
            if not m:
                continue
            notes += 1
            for moved in re.findall(r"moves to `claude-plugin/([^`]+)`", line):
                with self.subTest(note=m.group(1)):
                    self.assertEqual(moved, m.group(1))
        self.assertGreaterEqual(notes, 5)

    def test_no_claim_the_recipe_is_already_everywhere(self):
        readme = read("README.md")
        self.assertNotIn("same text", readme)
        self.assertNotIn("emails and docs give", readme)

    def test_the_emailed_check_in_is_the_morning_check_only_when_on(self):
        morning = section(read("README.md"), "### Every morning, without asking") or ""
        self.assertIn("emailed daily check-in, when it is on,", morning)

    def test_the_release_profile_is_never_a_temporary_config_dir(self):
        """The release checklist said to start Claude Code with
        `CLAUDE_CONFIG_DIR=$(mktemp -d)`. A session that cannot write its MCP
        refresh lock under its config dir replays a spent refresh token, and
        AdCopilot signs a reused one out (2026-10-07). The checklist now warns
        against it and gives a directory that persists."""
        releasing = section(read("README.md"), "## Releasing") or ""
        self.assertTrue(releasing, "the README has no Releasing section")
        self.assertNotRegex(releasing, r"CLAUDE_CONFIG_DIR=\$\(mktemp")
        self.assertIn("Never point `CLAUDE_CONFIG_DIR` at a temporary "
                      "directory", releasing)
        self.assertIn('CLAUDE_CONFIG_DIR="$HOME/.claude-adcopilot-release"',
                      releasing)


class Copy(unittest.TestCase):

    def test_the_delete_claim_names_its_one_exception(self):
        """Wherever the plugin says it does not delete, it names the exception.

        This sentence has now been wrong in four places across two review
        rounds — the docs skill, the review skill, the auditor, the manifest
        description — and each time it was corrected where the reviewer pointed
        and left standing in the file beside it. README.md was the fourth, and
        the only one a customer reads unprompted. A negative keyword IS deleted,
        by three tools that each describe themselves as the inverse of their
        add, so an unqualified "never deletes" is false everywhere it appears."""
        import re
        files = ["README.md", ".claude-plugin/plugin.json"]
        files += ["skills/%s/SKILL.md" % d
                  for d in sorted(os.listdir(os.path.join(ROOT, "skills")))]
        agents_dir = os.path.join(ROOT, "agents")
        if os.path.isdir(agents_dir):
            files += ["agents/%s" % f for f in sorted(os.listdir(agents_dir))
                      if f.endswith(".md")]
        # a sentence asserting no deletion, without "negative" within 220 chars
        # Only the GENERAL claim. "the asset tools refuse a remove" is a true,
        # narrow statement about one tool family and needs no exception; what
        # must never stand unqualified is a blanket "it does not delete".
        claim = re.compile(
            r"(never delet\w*|cannot delet\w*|does not delet\w*|"
            r"nothing is (?:ever )?deleted|Delete anything)", re.I)
        for rel in files:
            text = read(rel)
            for m in claim.finditer(text):
                window = text[m.start():m.start() + 400]
                with self.subTest(file=rel, claim=m.group(0)):
                    self.assertRegex(
                        window, r"(?i)negativ",
                        "%s says %r without naming the negative-keyword "
                        "exception within the next 400 characters"
                        % (rel, m.group(0)))

    def test_readme_lists_every_skill_and_agent_that_ships(self):
        """The README's count and its list both come from what is on disk.

        "Four skills" survived a branch that shipped six, and then "Six skills"
        survived one that shipped seven — twice, because the count was prose.
        A component nobody documents is a component nobody finds."""
        words = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five",
                 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"}
        readme = read("README.md")

        skills = sorted(os.listdir(os.path.join(ROOT, "skills")))
        self.assertIn("%s skills, which Claude draws on" % words[len(skills)],
                      readme,
                      "the README's skill count does not match the %d skills on "
                      "disk: %s" % (len(skills), skills))
        for name in skills:
            with self.subTest(skill=name):
                self.assertIn("**%s**" % name, readme)

        agents_dir = os.path.join(ROOT, "agents")
        if os.path.isdir(agents_dir):
            agents = sorted(f[:-3] for f in os.listdir(agents_dir)
                            if f.endswith(".md"))
            for name in agents:
                with self.subTest(agent=name):
                    self.assertIn("**%s**" % name, readme)

    def test_no_banned_words_anywhere_the_model_reads(self):
        files = ["README.md"] + ["commands/%s" % f for f in os.listdir(os.path.join(ROOT, "commands"))]
        files += ["skills/%s/SKILL.md" % d for d in os.listdir(os.path.join(ROOT, "skills"))]
        agents_dir = os.path.join(ROOT, "agents")
        if os.path.isdir(agents_dir):
            files += ["agents/%s" % f for f in os.listdir(agents_dir)
                      if f.endswith(".md")]
        for rel in files:
            with self.subTest(file=rel):
                self.assertIsNone(BANNED.search(read(rel)))


class PluginVersionMarker(unittest.TestCase):
    """#696: the plugin says which version it is on the marker itself.

    The marker without a version can come from any plugin release, 0.1.0
    included, so the server can only hand a turn to the skills every release
    ships. With `source: "claude-plugin/<version>"` it can tell an install
    that has `adcopilot-review` from one that does not, and route the counted
    account's review to it. A skill cannot read the manifest at run time —
    claude.ai has no shell and SKILL.md no templating — so the version is a
    literal in every file, and these tests are what keep the copies equal to
    `.claude-plugin/plugin.json`: a release bump that misses one fails here.
    The server reads the version only as X.Y.Z, and treats anything else as
    no version, which is safe but silent."""

    MARKER_VALUE = re.compile(r'"claude-plugin/([^"\s]*)"')
    # The README may write the marker with a placeholder, `<version>`; a
    # literal there is a version and is held to the manifest like the rest.
    README_MARKER_VALUE = re.compile(r'"claude-plugin/(\d[^"\s]*)"')

    def model_read(self):
        files = ["skills/%s/SKILL.md" % d
                 for d in sorted(os.listdir(os.path.join(ROOT, "skills")))]
        files += ["commands/%s" % f
                  for f in sorted(os.listdir(os.path.join(ROOT, "commands")))]
        agents_dir = os.path.join(ROOT, "agents")
        if os.path.isdir(agents_dir):
            files += ["agents/%s" % f for f in sorted(os.listdir(agents_dir))
                      if f.endswith(".md")]
        return files

    def test_the_manifest_version_is_what_the_server_reads(self):
        # situations.plugin_version reads ^\d+\.\d+\.\d+$ only; a "-rc1" or
        # a "+build" would be read as no version.
        self.assertRegex(manifest_version(), r"^\d+\.\d+\.\d+$")

    def test_every_marker_names_the_manifest_version(self):
        seen = 0
        for rel in self.model_read() + ["README.md"]:
            values = (self.README_MARKER_VALUE if rel == "README.md"
                      else self.MARKER_VALUE)
            for m in values.finditer(read(rel)):
                seen += 1
                with self.subTest(file=rel, value=m.group(0)):
                    self.assertEqual(
                        m.group(1), manifest_version(),
                        "%s marks plugin use as %s but the manifest is %s — move "
                        "every copy with the bump" % (rel, m.group(0), manifest_version()))
        # 14 in 0.2.14: one in each marked file (#22's second review). Connect's
        # and launch's later steps say "the `source` the first rule gives",
        # "the same `source`" and "the `source` given under Arriving mid-arc",
        # so a scheduled run meets the literal only beside its exception.
        self.assertGreaterEqual(seen, 14, "expected the 14 marker sites, saw %d" % seen)

    def test_no_bare_marker_is_left(self):
        # Outside the four commands' no-skills exception, nowhere.
        for rel in self.model_read():
            with self.subTest(file=rel):
                text = flat(rel)
                if rel in VERSIONED_COMMANDS:
                    self.assertEqual(text.count(NO_SKILLS), 1)
                    text = text.replace(NO_SKILLS, "")
                self.assertNotIn(BARE_MARKER, text,
                                 "%s still passes the marker without the version" % rel)

    def test_every_marked_file_says_to_keep_the_version(self):
        # The server's own `source` description names the bare value and says
        # any other value is ignored; a model left to itself may "correct"
        # the suffix away. One sentence per file, the same in each.
        keep = ("Send `source` exactly as written, the version included: it "
                "tells AdCopilot which of this plugin's steps are installed here.")
        for rel in self.model_read():
            text = read(rel)
            if plugin_marker() not in text:
                continue
            with self.subTest(file=rel):
                self.assertEqual(" ".join(text.split()).count(keep), 1)

    def test_a_routed_turn_keeps_the_request_it_was_given(self):
        # The server picks the skill from the account's situation, not from
        # which command called (situations.plugin_skill), so /weekly on an
        # account whose results are not counted is told the measurement
        # steps cover the turn. Every marked file does its own request first
        # and keeps the limit next_step adds. One sentence, the same in each.
        guard = ("When the answer's `plugin.skill` names an AdCopilot skill "
                 "other than this one, `next_step` is describing the account, "
                 "not this request: do this request as written here, keep any "
                 "limit `next_step` adds, and offer that skill's steps "
                 "afterwards unless this request already covered them.")
        marked = 0
        for rel in self.model_read():
            text = read(rel)
            if plugin_marker() not in text:
                continue
            marked += 1
            with self.subTest(file=rel):
                flat_text = " ".join(text.split())
                if rel == DocsAnswersFromTheOneCall.DOCS:
                    # 0.2.12: the docs skill does not offer that skill's steps
                    # afterwards; it follows none of them on this turn and
                    # ends on one offer of its own (DocsAnswersFromTheOneCall).
                    self.assertEqual(flat_text.count(guard), 0)
                    self.assertEqual(flat_text.count(DOCS_ROUTING), 1)
                else:
                    self.assertEqual(flat_text.count(guard), 1)
        # 13 from 0.2.13: adcopilot-daily's set-up and its reply after a run
        # send the versioned marker too (#22); 14 from 0.2.14:
        # adcopilot-fix-checks (#24).
        self.assertEqual(marked, 14)

    def test_the_marker_graders_need_the_version(self):
        """Each case's marks-plugin-use grader counts the calls it fails on, so
        its pattern must match a call without the versioned marker and must
        not match one with it, wherever `source` sits in the input."""
        def input_match(case):
            text = read("evals/%s/case.yaml" % case)
            start = text.find("  - name: marks-plugin-use\n")
            if start < 0:
                return None
            end = text.find("\n  - name: ", start + 1)
            block = text[start:end if end > 0 else len(text)]
            m = re.search(r"^\s+input_match: '((?:[^']|'')*)'\s*$", block, re.M)
            self.assertIsNotNone(m, "%s/marks-plugin-use has no input_match" % case)
            return re.compile(m.group(1).replace("''", "'"))

        v = manifest_version()
        counted = ['{}', '{"source":"claude-plugin"}', '{"source": "claude-plugin"}',
                   '{"source":"claude-plugin/"}', '{"source":"claude-plugin/latest"}',
                   '{"source":"chatgpt"}', '{"tools":["full_audit"]}', 'not json']
        passed = ['{"source":"claude-plugin/%s"}' % v,
                  '{"source": "claude-plugin/%s"}' % v,
                  '{"tools":["full_audit","budget_pacing"],"source":"claude-plugin/%s"}' % v]
        graded = 0
        for case in sorted(os.listdir(os.path.join(ROOT, "evals"))):
            if not os.path.isfile(os.path.join(ROOT, "evals", case, "case.yaml")):
                continue
            pattern = input_match(case)
            if pattern is None:
                continue
            graded += 1
            for call in counted:
                with self.subTest(case=case, call=call):
                    self.assertRegex(call, pattern)
            for call in passed:
                with self.subTest(case=case, call=call):
                    self.assertNotRegex(call, pattern)
        self.assertGreaterEqual(graded, 19)

    def test_the_ablation_stub_carries_the_marker(self):
        # Otherwise the tools-only arm fails the marker on every case and each
        # skill's delta is the marker's weight, not what its body teaches.
        script = read("evals/ablation/tools-only.sh")
        self.assertIn('source: \\"claude-plugin/$VERSION\\"', script)
        self.assertIn(".claude-plugin/plugin.json", script)
        self.assertIn("*/adcopilot-daily/SKILL.md) ;;", script)

    def test_the_ablation_stub_says_what_a_scheduled_run_sends(self):
        # PR #22, second review: the stub kept the plugin marker but dropped
        # the scheduled-run sentence that is now part of the same marker text,
        # so review-scheduled-unmarked failed its baseline by construction and
        # the review skill's delta measured the forced marker. The script's
        # own stub loop runs here on a copy of the skills.
        import shutil
        import tempfile
        bash = shutil.which("bash")
        if bash is None:
            self.skipTest("no bash")
        script = read("evals/ablation/tools-only.sh")
        loop = re.search(r'(?ms)^for skill in "\$COPY"/skills/\*/SKILL\.md; do$.*?^done$',
                         script)
        self.assertIsNotNone(loop, "the stub loop is not where it was")
        with tempfile.TemporaryDirectory() as work:
            shutil.copytree(os.path.join(ROOT, "skills"), os.path.join(work, "skills"))
            done = subprocess.run(
                [bash, "-c", "set -euo pipefail\n" + loop.group(0)],
                env=dict(os.environ, COPY=work, VERSION=manifest_version()),
                capture_output=True, text=True)
            self.assertEqual(done.returncode, 0, done.stderr)
            stubs = {name: open(os.path.join(work, "skills", name, "SKILL.md"),
                                encoding="utf-8").read()
                     for name in os.listdir(os.path.join(work, "skills"))}
        for name, stub in sorted(stubs.items()):
            body = " ".join(stub.split("\n---\n", 1)[1].split())
            with self.subTest(skill=name):
                if name == "adcopilot-daily":
                    self.assertNotIn("source", body)
                    continue
                self.assertIn(plugin_marker(), body)
                self.assertEqual(body.count(SCHEDULED_SOURCE_RULE), 1)
                self.assertGreater(body.find(SCHEDULED_SOURCE_RULE),
                                   body.find(plugin_marker()))
        self.assertNotIn("expected to fail there",
                         read("evals/review-scheduled-unmarked/case.yaml"))


class Manifest(unittest.TestCase):

    def test_version(self):
        """The manifest's version, checked against the newest tag rather than a
        literal.

        It was `"0.2.4"` written out, which makes every release a two-sided
        edit: leave the manifest alone and checks.yml's "Manifest version is
        not behind the latest tag" step fails once the tag exists; bump it and
        this assertion fails instead. Neither branch could be tagged green.
        Derived from `git tag` the way that CI step derives it, the manifest may
        equal the newest tag or be ahead of it (an unreleased bump), and never
        behind."""
        manifest = json.loads(read(".claude-plugin/plugin.json"))["version"]
        tags = subprocess.run(["git", "tag", "--sort=-v:refname"],
                              cwd=ROOT, capture_output=True, text=True).stdout.split()
        newest = next((x[1:] for x in tags if x.startswith("v")), None)
        if newest is None:
            self.skipTest("no version tags yet")
        def parts(v):
            return tuple(int(n) for n in v.split("."))
        self.assertGreaterEqual(
            parts(manifest), parts(newest),
            "the manifest (%s) is behind the newest tag (v%s) — bump "
            ".claude-plugin/plugin.json before tagging" % (manifest, newest))

    def test_no_compiled_python_is_tracked(self):
        """0.2.13's first push committed tests/__pycache__/*.pyc, compiled by
        the builder's own test run: a plugin install copies the repository,
        so it would have shipped to every user, and the file recorded the
        local scratch path it was compiled in. Nothing compiled is tracked,
        and .gitignore keeps the next one out."""
        listed = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT,
                                capture_output=True, text=True)
        if listed.returncode != 0:
            self.skipTest("not a git checkout")
        tracked = [p for p in listed.stdout.split("\0")
                   if "__pycache__/" in p or p.endswith((".pyc", ".pyo"))]
        self.assertEqual(tracked, [])
        ignore = read(".gitignore").splitlines()
        for rule in ("__pycache__/", "*.pyc"):
            with self.subTest(rule=rule):
                self.assertIn(rule, ignore)


class DocsAnswersFromTheOneCall(unittest.TestCase):
    """0.2.12: a question about AdCopilot itself is answered from the one
    `get_org_context` call. The server hands a running, counted account to
    `adcopilot-review` on every plugin call, the docs skill's included, so the
    docs skill follows none of the account's steps on its own turn, keeps only
    a limit `next_step` names, answers once as one list, and ends on exactly
    one question offering one read. Approval keeps its condition wherever it
    comes up."""

    DOCS = "skills/adcopilot-docs/SKILL.md"

    def text(self):
        return flat(self.DOCS)

    def test_it_reads_nothing_and_starts_no_other_skill(self):
        text = self.text()
        self.assertEqual(text.count(DOCS_ROUTING), 1)
        self.assertIn("A question about AdCopilot itself is answered from that "
                      "one call, plus the documentation site where this file "
                      "says so.", text)

    def test_it_follows_none_of_the_accounts_steps_on_this_turn(self):
        text = self.text()
        # v2.41 alignment (#829): the playbook's section is "[PLUGIN] The
        # installed skill" and no longer says the skill owns the turn; it and
        # next_step answer a question first and offer the steps after.
        self.assertIn("The answer's `next_step`, `playbook` (its sections on the "
                      "installed skill and on a returning customer included), "
                      "`cross_reads` and `question_map` describe the account, "
                      "not this question: do not follow them on this turn, not "
                      "even their offer of a skill's steps.", text)
        self.assertNotIn("owns the turn", text)
        self.assertIn("Keep from them only a limit `next_step` names", text)

    def test_the_capabilities_answer_is_one_list(self):
        can = " ".join((section(read(self.DOCS), "## What AdCopilot can do") or "").split())
        self.assertIn("Answer it once, as one list, in this order:", can)
        order = ["what is connected and what each lets them do",
                 "what connecting each of the others would unlock",
                 "the routines installed here",
                 "what AdCopilot may change, with its condition",
                 "the plan's look-ups"]
        at = [can.find(piece) for piece in order]
        self.assertNotIn(-1, at, dict(zip(order, at)))
        self.assertEqual(at, sorted(at))
        self.assertIn("never a second list in another grouping, and never come "
                      "back later in the same reply to answer it again", can)

    def test_one_fact_may_be_the_reason_for_the_offer(self):
        can = " ".join((section(read(self.DOCS), "## What AdCopilot can do") or "").split())
        self.assertIn("One fact from `get_org_context`'s 30-day summary", can)
        # v2.41 alignment (#821): `last_30d` names its window whenever it
        # was read (`context_probe._apply`, `start_date` and `end_date`).
        self.assertIn("with the dates it names, `start_date` to `end_date`", can)
        self.assertNotIn("when `last_30d` carries them", can)

    def test_it_ends_on_exactly_one_question(self):
        nxt = " ".join((section(read(self.DOCS), "## What is next") or "").split())
        self.assertIn("end the reply with exactly one question", nxt)
        self.assertIn("Not a fix, not a change, and not a second offer.", nxt)

    def test_approval_keeps_its_condition_wherever_it_comes_up(self):
        allowed = " ".join((section(read(self.DOCS),
                                    "## What AdCopilot is allowed to change") or "").split())
        self.assertIn("That holds wherever approval comes up", allowed)
        self.assertIn("a heading, a parenthesis, a list item", allowed)


class MeasureDescription(unittest.TestCase):
    """0.2.12: the measure skill's description named only the Analytics route,
    and a reply said conversion tracking "needs Analytics and Tag Manager
    connected". Its body has always had two routes.

    Fix round 1: the first 0.2.12 description said the direct route "needs
    neither Analytics nor Tag Manager", but the body puts that route's
    Google Ads conversion tag "on the same trigger as step 3", a Tag Manager
    trigger, and walks no other way onto the site. The description promises
    only what the body walks: no Analytics, and the tag through Tag
    Manager."""

    MEASURE = "skills/adcopilot-measure/SKILL.md"

    def desc(self):
        fm = frontmatter(read(self.MEASURE))
        return re.search(r"^description: (.+)$", fm, re.M).group(1)

    def test_it_names_both_routes(self):
        desc = self.desc()
        self.assertIn("through Analytics", desc)
        self.assertIn("directly in Google Ads", desc)
        self.assertLessEqual(len(desc), 1024)

    def test_the_direct_route_is_described_as_the_body_walks_it(self):
        desc = self.desc()
        direct = desc[desc.index("directly in Google Ads"):]
        self.assertIn("needs no Analytics", direct)
        self.assertIn("through Tag Manager", direct)
        body = read(self.MEASURE).split("\n---\n", 1)[1]
        self.assertIn("on the same trigger as step 3", body)
        # A route without Tag Manager may be promised only once the body
        # walks putting the tag on the site some other way.
        if not re.search(r"without Tag Manager", body):
            self.assertNotRegex(desc, r"(?:nor|no|without) Tag Manager")


class ReleaseNoteAndMarker(unittest.TestCase):
    """The bump's other halves: the README carries a note for the manifest's
    version that says the release checklist comes before the tag, and no file
    under skills, commands or agents, whatever its type, names another
    version on the marker."""

    def test_the_readme_has_a_note_for_this_version(self):
        notes = section(read("README.md"), "## AdCopilot version") or ""
        start = notes.find("**%s (" % manifest_version())
        self.assertGreaterEqual(start, 0, "no README note for %s" % manifest_version())
        note = " ".join(notes[start:].split("\n\n", 1)[0].split())
        self.assertIn("must be run before this version is tagged", note)

    def test_every_marker_anywhere_names_the_manifest_version(self):
        seen = 0
        for sub in ("skills", "commands", "agents"):
            for dirpath, _dirs, names in os.walk(os.path.join(ROOT, sub)):
                for name in names:
                    rel = os.path.relpath(os.path.join(dirpath, name), ROOT)
                    for m in re.finditer(r"claude-plugin/(\d+\.\d+\.\d+)", read(rel)):
                        seen += 1
                        with self.subTest(file=rel):
                            self.assertEqual(m.group(1), manifest_version())
        # 14 at 0.2.14: one in each marked file, adcopilot-daily and
        # adcopilot-fix-checks among them
        # (connect had three and launch two until #22's second review).
        self.assertGreaterEqual(seen, 14)


class NoCompiledCaches(unittest.TestCase):
    """A compiled cache is a build product of a local run, not plugin text:
    a `.pyc` names the path it was compiled from, so committing one publishes
    that machine's directory names in a public repository (review of
    AdCopilot #919, PR #23). `.gitignore` keeps them out, and nothing
    tracked may be one."""

    def test_gitignore_ignores_python_caches(self):
        lines = read(".gitignore").splitlines()
        self.assertIn("__pycache__/", lines)
        self.assertIn("*.py[cod]", lines)

    def test_no_tracked_file_is_a_compiled_cache(self):
        listed = subprocess.run(["git", "ls-files"], cwd=ROOT,
                                capture_output=True, text=True)
        if listed.returncode != 0:
            self.skipTest("not a git checkout")
        cached = [path for path in listed.stdout.splitlines()
                  if "__pycache__/" in path
                  or path.endswith((".pyc", ".pyo", ".pyd"))]
        self.assertEqual(cached, [])


if __name__ == "__main__":
    unittest.main()
