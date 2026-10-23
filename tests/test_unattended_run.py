"""The unattended run: what it sends, what it may call and what its set-up says.

One of the structural test files that `tests/test_structure.py` was split
into in 0.2.15. At 273 KB that file was over the plugin directory's 256 KiB
limit for a file that is not an image or a font. The tests moved verbatim, by
topic (same classes, same names, same assertions), and the helpers they share
live in `structure_helpers.py`; `tests/test_plugin_size.py` keeps any file
from growing past the limit again.

Run with `python3 -m unittest discover -s tests -v` from the repository root
(stdlib only; CI runs it in checks.yml).

What it pins, and why each one is here:
- The unattended run. `adcopilot-daily` passes `claude-scheduled`, never
  `claude-plugin`, and its instructions say read-only and ask-nothing — the
  two properties a scheduled run with nobody to answer depends on, and its
  first call names AdCopilot's morning check as its `task`. It calls no
  `save_org_context` either: Claude lists that tool with the write tools, and
  every set-up made before 0.2.14 keeps those on Needs approval, so a note
  that waits for approval stops the run. From 0.2.14 the set-up says what
  AdCopilot's `schedule_recipe.ALWAYS_ALLOW_STEP` says (v2.44.0): the
  read-only tools and AdCopilot's two notes tools, by the titles Claude shows,
  on Always allow, every other write tool on Needs approval. Founder answer 6
  (notes in a run) waits until the people who already schedule the check
  have been told and that notice has been measured.
  With no account named it never falls back to a manager account, which
  Google refuses metrics for.
- Honesty about what keeps a run to reads (D71's family). Nothing on the
  server makes a scheduled run read-only; on Automatically approve, or in a
  Claude Code routine, the instructions are all that does. Neither the skill
  nor the README may call that a guarantee.
- The instructions the set-up hands over are AdCopilot's own recipe, word for
  word (`ads_mcp_cloud/schedule_recipe.py`, SCHEDULED_CHECKIN, as of
  AdCopilot v2.44.0); the call it opens with, `CHECKIN_FIRST_CALL`, is what
  marks the run as the morning check.
  The server's emails, docs and dashboard do not all carry it yet, so nothing
  here says they do.
- The scheduled marker (#22, released in 0.2.14, founder answer 3): every file that tells the
  model to send `source: "claude-plugin/<version>"` also says, in one
  sentence the same in each, that a scheduled run sends
  `source: "claude-scheduled"` instead and never `claude-plugin`. Those are
  the strings AdCopilot reads (`schedule_recipe.SCHEDULED_SOURCE`,
  `tools_adcopilot.PLUGIN_SOURCE`, `scheduled_guard.is_scheduled_source` at
  release/v2.42.0, d9bd20ae): a scheduled task whose own words carry no
  marker, answered by the review skill with the plugin marker, was never
  seen as a scheduled run. `adcopilot-daily` says both halves:
  the run sends the scheduled marker, a person's set-up or reply the
  versioned plugin marker, never the scheduled one.

- The README's morning section and the daily skill agree on what keeps a run
  to reads, and every copy of the set-up step names both AdCopilot tools
  Claude lists under Write/delete tools (0.2.14).
"""

import os
import sys
import re
import unittest

# The helpers sit beside this file; the path is set so this file also runs
# on its own (`python3 tests/test_unattended_run.py`).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from structure_helpers import (  # noqa: E402
    BARE_MARKER,
    CHECKIN_FIRST_CALL,
    NO_SKILLS,
    ROOT,
    SALES,
    SCHEDULED_CHECKIN,
    SCHEDULED_SOURCE_RULE,
    VERSIONED_COMMANDS,
    flat,
    frontmatter,
    grader,
    grader_block,
    manifest_version,
    mock,
    model_read_files,
    plugin_marker,
    read,
    section,
)


# AdCopilot's own recipe (server: ads_mcp_cloud/schedule_recipe.py,
# SCHEDULED_CHECKIN, AdCopilot v2.44.0, read on release/v2.44.1 and on the
# deployed code). `{account}` is filled in by the set-up. Change it there
# first, then here and in the skill. Its first call is the server's
# CHECKIN_FIRST_CALL: the scheduled source and the morning check's own task
# (CHECKIN_TASK, C5), the marker AdCopilot counts as its morning check.
CHECKIN_TASK = "AdCopilot morning check"


# #22, in 0.2.14 (founder answer 3): the two `source` values AdCopilot reads, as the
# server spells them at release/v2.42.0 (d9bd20ae):
# `schedule_recipe.SCHEDULED_SOURCE` (read by `tools_adcopilot._note_source`
# and `scheduled_guard.is_scheduled_source`, spacing and case aside) and
# `tools_adcopilot.PLUGIN_SOURCE`, with "/<version>" after it from 0.2.7
# (`tools_adcopilot._plugin_marker`).
SERVER_SCHEDULED_SOURCE = "claude-scheduled"


SERVER_PLUGIN_SOURCE = "claude-plugin"


# adcopilot-daily's own pair: the run sends the scheduled marker (its step 1),
# and a person's set-up or reply sends the versioned plugin marker, never the
# scheduled one.
DAILY_WITH_A_PERSON = ("Only the run sends `source: \"claude-scheduled\"`. "
                       "With a person here, in the set-up or after the run, "
                       "call `get_org_context` with `source: "
                       "\"claude-plugin/%s\"`, never `claude-scheduled`, "
                       "which would tell AdCopilot nobody is there.")


# The run keeps no note (PR #22, second review). Founder answer 6 let it keep
# AdCopilot's own notes, but the server annotates save_org_context as a write
# (`tools_adcopilot._WRITE`, readOnlyHint false), so Claude lists it with the
# write tools, and every set-up keeps those on Needs approval: the plugin's own
# steps from 0.2.4 to 0.2.12 and AdCopilot's `schedule_recipe.ALWAYS_ALLOW_STEP`
# at d9bd20ae. A scheduled run cannot answer that prompt, so a run that keeps a
# note never finishes. The ban stays until the server's step, docs and mails
# say Always allow for that tool and existing schedulers have been told.
# 0.2.14: the set-up now lets that tool through (ALWAYS_ALLOW_STEP below), but
# every schedule set up before it still asks; the ban lifts only once those
# people have been told (AdCopilot's notice notice_2026_10_schedule_allow) and
# the notice has been measured.
RUN_NO_NOTE = ("and not `save_org_context` either, even where AdCopilot's "
               "instructions ask for notes as you go: the source marker "
               "already records the run, and a schedule set up before this "
               "plugin's 0.2.14 may still keep that tool on **Needs "
               "approval**, so a note would stop the run at a prompt nobody "
               "can answer.")


# The 0.2.13 first draft's two sentences, which would have stalled every run
# set up before them.
RUN_NOTES = ("`save_org_context` is allowed for AdCopilot's own notes only")


SET_UP_NOTE_ALLOWED = ("set `save_org_context` alone to **Always allow**")


# The set-up's first Claude step as every plugin version from 0.2.4 to 0.2.13
# worded it: every write and delete tool kept asking, `get_org_context` and
# `save_org_context` included, so from v2.42.3 (which annotates
# get_org_context as not read-only) a run set up that way stopped at its first
# call. Gone from 0.2.14.
SET_UP_WRITES_ASK = ("The write and delete tools stay on **Needs approval**.")


# 0.2.14: what AdCopilot's `schedule_recipe.ALWAYS_ALLOW_STEP` says (v2.44.0,
# its CONTEXT_TOOL_TITLE and SAVE_TOOL_TITLE): the two AdCopilot tools Claude
# lists under Write/delete tools that a run needs, by the titles Claude shows,
# on Always allow; every other write tool on Needs approval.
CONTEXT_TOOL_TITLE = "AdCopilot: what is connected and where you are"


SAVE_TOOL_TITLE = "AdCopilot: save business notes and progress"


SET_UP_ALWAYS_ALLOW = (
    "Set the **Read-only tools** to **Always allow**, because a scheduled run "
    "cannot answer a prompt. Under **Write/delete tools**, set “%s” and “%s” "
    "to **Always allow** too: they keep AdCopilot's own notes and never change "
    "Google Ads, and the run's first call is the first of them. Keep every "
    "other Write/delete tool on **Needs approval**, so Claude asks before each "
    "change." % (CONTEXT_TOOL_TITLE, SAVE_TOOL_TITLE))


def fenced(text, lang="text"):
    """The body of the first ```lang fenced block in `text`, or None."""
    m = re.search(r"^```%s\n(.*?)\n```$" % lang, text or "", re.S | re.M)
    return m.group(1) if m else None


class UnattendedRun(unittest.TestCase):

    def skill(self):
        return read("skills/adcopilot-daily/SKILL.md")

    def test_frontmatter(self):
        fm = frontmatter(self.skill())
        self.assertRegex(fm, r"(?m)^name: adcopilot-daily$")
        self.assertRegex(fm, r"(?m)^description: .*scheduled")

    def test_marks_the_scheduled_run_and_never_the_plugin_marker(self):
        run = section(self.skill(), "## The run")
        self.assertIsNotNone(run, "adcopilot-daily has no '## The run' section")
        self.assertIn('source: "claude-scheduled"', run)
        self.assertNotIn('source: "claude-plugin', run)

    def test_read_only_and_asks_nothing(self):
        run = section(self.skill(), "## The run") or ""
        self.assertRegex(run, r"Read only\.")
        self.assertRegex(run, r"Ask nothing\.")
        # save_org_context is named as a tool the run does not call (PR #22,
        # second review: a note would wait at an approval prompt).
        self.assertIn("save_org_context", run)
        self.assertEqual(" ".join(run.split()).count(RUN_NO_NOTE), 1)
        self.assertRegex(run, r"Never offer to schedule")

    def test_the_lenses(self):
        run = section(self.skill(), "## The run") or ""
        for read_ in ("budget_pacing", "analyze_search_terms", "days: 7",
                      "change_event", "ad_group_ad"):
            with self.subTest(read=read_):
                self.assertIn(read_, run)

    def test_the_instructions_are_adcopilots_recipe_word_for_word(self):
        setup = section(self.skill(), "## The set-up")
        self.assertIsNotNone(setup, "adcopilot-daily has no '## The set-up' section")
        self.assertEqual(fenced(setup), SCHEDULED_CHECKIN)
        self.assertIn("8:07", setup)
        # The two ways {account} is filled in, as the server fills it.
        self.assertIn('"Google Ads account "', setup)
        self.assertIn('"the Google Ads account I have switched on in AdCopilot"', setup)

    def test_claude_steps(self):
        # Plan section 6: reads on Always allow, writes left on Needs
        # approval, Manually approve, and one run to prove it is unattended.
        setup = section(self.skill(), "## The set-up") or ""
        for step in ("**Always allow**", "**Needs approval**", "**Set up manually**",
                     "**Manually approve**", "**Run now**",
                     "Schedule a task for every weekday at 8:07 AM my time with these instructions:"):
            with self.subTest(step=step):
                self.assertIn(step, setup)

    def test_claude_code_steps(self):
        # A routine runs in the cloud and cannot see the plugin's connector;
        # the plugin offers to run /schedule for them.
        setup = section(self.skill(), "## The set-up") or ""
        for step in ("claude.ai/customize/connectors", "the `schedule` skill",
                     "/schedule weekdays at 8:07am", "without asking"):
            with self.subTest(step=step):
                self.assertIn(step, setup)

    def test_recording_respects_the_emailed_check_in(self):
        # save_org_context refuses status/surface on an in_app row while
        # AdCopilot's runner is live (tenants.ROUTINE_IN_APP_LOCKED_FIELDS),
        # so the set-up records only when the row is not in_app.
        setup = section(self.skill(), "## The set-up") or ""
        for part in ("`save_org_context`", "`user_set`", "`claude_scheduled`", "`in_app`"):
            with self.subTest(part=part):
                self.assertIn(part, setup)

    def test_the_set_up_records_what_stops_the_offer(self):
        # `routine.own_schedule` is the record AdCopilot accepts on an
        # in_app row, and `unavailable` is how a Claude with no scheduled
        # tasks stops the offer; from 0.2.7 the server leaves its own
        # schedule section to this plugin on the turns a skill owns.
        setup = " ".join((section(self.skill(), "## The set-up") or "").split())
        self.assertIn("`routine.own_schedule` `saved` and `routine.daily`", setup)
        self.assertIn("so record `routine.own_schedule` `saved` alone", setup)
        self.assertIn("`routine.own_schedule` `unavailable`", setup)
        self.assertNotIn("so record nothing", setup)

    def test_the_account_without_one_named(self):
        # The account AdCopilot's own check-in reads (plan B6/B11 fields).
        run = section(self.skill(), "## The run") or ""
        self.assertIn("`latest_check_in.account`", run)
        self.assertIn("`routine.daily.customer_id`", run)

    def test_the_fallback_skips_manager_accounts(self):
        # Google refuses metric reads on a manager (MCC) account
        # (REQUESTED_METRICS_FOR_MANAGER); the server's own check-in learned
        # that in v2.30.1 (orgs 32 and 43). get_org_context flags each account
        # `manager`. Both the run's fallback and the set-up's fill-in skip it.
        run = section(self.skill(), "## The run") or ""
        self.assertIn("`manager`", run)
        self.assertIn("only manager accounts", run)
        setup = section(self.skill(), "## The set-up") or ""
        self.assertIn("manager", setup)

    def test_automatic_approval_is_not_called_read_only(self):
        # Automatically approve approves every call, writes included; nothing
        # on the server refuses a write in a claude-scheduled session. The
        # instructions are what keep the run to reads, and the skill says so.
        setup = section(self.skill(), "## The set-up") or ""
        self.assertNotIn("only reads run", setup)
        team = setup[setup.find("**Automatically approve**"):]
        team = team[:team.find("\n\n")]
        self.assertIn("changes included", team)
        self.assertIn("keep them exactly as written", team)
        self.assertIn("**Blocked**", team)

    def test_a_routine_is_kept_to_reads_by_its_instructions(self):
        setup = section(self.skill(), "## The set-up") or ""
        self.assertIn("A routine runs its tools without asking, so the read-only "
                      "instructions are what keep it to reads", setup)

    def test_no_claim_the_recipe_is_already_everywhere(self):
        # The emails, docs and dashboard do not all carry SCHEDULED_CHECKIN
        # until the server's one-recipe release (plan B9) is deployed.
        setup = section(self.skill(), "## The set-up") or ""
        self.assertNotIn("same text", setup)
        self.assertNotIn("emails, docs", setup)

    def test_an_emailed_check_in_keeps_coming_and_they_are_told(self):
        # While routine.daily.status is in_app the set-up records nothing and
        # the server's refusal (MSG_ROUTINE_RUN_BY_ADCOPILOT) never reaches
        # them, so the skill tells them both arrive and where to pause one.
        setup = section(self.skill(), "## The set-up") or ""
        record = setup[setup.find("**Then record it.**"):]
        self.assertIn("keeps coming as well", record)
        self.assertIn("Routine card", record)

    def test_no_sales_wording_in_the_run(self):
        run = section(self.skill(), "## The run") or ""
        self.assertIsNone(SALES.search(run))


# The README note the three tests below read (`test_the_release_check_expects_no_note`,
# `test_the_readme_note_says_both` and
# `test_the_readme_note_says_only_the_recipe_is_the_morning_check`) is 0.2.14's:
# the version that shipped #22, the tool titles and the morning check's task.
# Looked up by the manifest's version they read the note of whatever version
# is current, so from 0.2.15 they would ask a release that changes none of this
# to repeat it. A release note is history; they pin this one.
SCHEDULED_NOTE_VERSION = "0.2.14"


class ScheduledSourceMarker(unittest.TestCase):
    """#22, in 0.2.14: which `source` a scheduled run sends, and what it may save.

    Founder answer 3: every file that tells the model which `source` to pass
    to `get_org_context` says that a scheduled run passes "claude-scheduled",
    never "claude-plugin", and otherwise "claude-plugin/<version>". Until
    0.2.12 only adcopilot-daily's run said so; a scheduled task whose own
    words carry no marker, answered by the review skill, sent the plugin
    marker, and the server (`tools_adcopilot._note_source`, and from
    release/v2.42.0 `scheduled_guard.note_front_door`) never saw a scheduled
    run. Founder answer 6 would let the run use `save_org_context` for
    AdCopilot's own notes, and v2.42.0's guard leaves that tool alone
    (`scheduled_guard.guarded`), but Claude asks before it on every set-up
    made so far, so the run still keeps no note (PR #22, second review)."""

    DAILY = "skills/adcopilot-daily/SKILL.md"
    REVIEW = "skills/adcopilot-review/SKILL.md"
    KEEP = ("Send `source` exactly as written, the version included: it tells "
            "AdCopilot which of this plugin's steps are installed here.")
    CASE = "daily-scheduled-run"

    def marked(self):
        return [rel for rel in model_read_files()
                if plugin_marker() in read(rel)]

    def test_the_values_are_the_ones_the_server_reads(self):
        self.assertIn('`source: "%s"`' % SERVER_SCHEDULED_SOURCE,
                      SCHEDULED_SOURCE_RULE)
        self.assertIn("never `%s`" % SERVER_PLUGIN_SOURCE, SCHEDULED_SOURCE_RULE)
        self.assertNotIn(BARE_MARKER, SCHEDULED_SOURCE_RULE)
        self.assertEqual(plugin_marker(), 'source: "%s/%s"'
                         % (SERVER_PLUGIN_SOURCE, manifest_version()))
        # AdCopilot's recipe opens with the same value.
        self.assertIn('source "%s"' % SERVER_SCHEDULED_SOURCE, SCHEDULED_CHECKIN)

    def test_every_file_that_sends_the_plugin_marker_says_what_a_run_sends(self):
        checked = 0
        for rel in self.marked():
            if rel == self.DAILY:
                continue
            checked += 1
            text = flat(rel)
            with self.subTest(file=rel):
                self.assertEqual(text.count(SCHEDULED_SOURCE_RULE), 1)
                # Beside the marker it overrides: after the keep sentence, and
                # in the four commands after the no-skills exception too.
                self.assertGreater(text.find(SCHEDULED_SOURCE_RULE),
                                   text.find(self.KEEP))
                if rel in VERSIONED_COMMANDS:
                    self.assertGreater(text.find(SCHEDULED_SOURCE_RULE),
                                       text.find(NO_SKILLS))
        # 13 in 0.2.14: adcopilot-fix-checks (#24) is marked too.
        self.assertEqual(checked, 13)

    def test_the_plugin_marker_is_written_once_beside_its_exception(self):
        # PR #22, second review: connect's steps 2 and 3 and launch's step 1
        # restated `source: "claude-plugin/<version>"` with no exception, so a
        # scheduled run working through the steps met the plain marker again.
        # Each marked file writes it once, in the paragraph that says what a
        # scheduled run sends instead (adcopilot-daily: what a person's
        # set-up or reply sends), and every later call refers back to it.
        marked = self.marked()
        self.assertEqual(len(marked), 14)
        for rel in marked:
            text = read(rel)
            with self.subTest(file=rel):
                self.assertEqual(text.count(plugin_marker()), 1)
                para = [p for p in re.split(r"\n\s*\n", text)
                        if plugin_marker() in p][0]
                para = " ".join(para.split())
                if rel == self.DAILY:
                    self.assertIn(" ".join((DAILY_WITH_A_PERSON
                                            % manifest_version()).split()), para)
                else:
                    self.assertIn(SCHEDULED_SOURCE_RULE, para)
        refer = {"skills/adcopilot-connect/SKILL.md": (
                     "Call `get_org_context` with the `source` the first rule gives.",
                     "calling `get_org_context` again, with the same `source`."),
                 "skills/adcopilot-launch/SKILL.md": (
                     'Call `get_org_context` with the `source` given under '
                     '"Arriving mid-arc".',)}
        for rel, lines in refer.items():
            for line in lines:
                with self.subTest(file=rel, line=line):
                    self.assertEqual(flat(rel).count(line), 1)

    def test_the_review_skill_says_it_with_its_first_call(self):
        top = read(self.REVIEW).split("## Spend the reads you are given", 1)[0]
        self.assertEqual(" ".join(top.split()).count(SCHEDULED_SOURCE_RULE), 1)

    def test_the_scheduled_marker_is_written_nowhere_else(self):
        # Outside the rule, only adcopilot-daily names the scheduled value: a
        # person's conversation that sent it would be read as a run nobody is
        # there for.
        for rel in model_read_files():
            if rel == self.DAILY:
                continue
            with self.subTest(file=rel):
                rest = flat(rel).replace(SCHEDULED_SOURCE_RULE, "")
                self.assertNotIn(SERVER_SCHEDULED_SOURCE, rest)

    def test_daily_says_both_halves(self):
        text = read(self.DAILY)
        intro = " ".join(text.split("\n## The run\n", 1)[0].split())
        self.assertEqual(intro.count(" ".join(
            (DAILY_WITH_A_PERSON % manifest_version()).split())), 1)
        run = section(text, "## The run") or ""
        self.assertIn('`source: "claude-scheduled"`', run)
        self.assertIn("never `claude-plugin`", run)
        self.assertNotIn('source: "claude-plugin', run)
        # Its own words, not the other files' sentence.
        self.assertEqual(flat(self.DAILY).count(SCHEDULED_SOURCE_RULE), 0)

    def test_the_run_keeps_no_note(self):
        # PR #22, second review: Claude asks before save_org_context on every
        # set-up made so far (the plugin's own steps up to 0.2.12 and
        # AdCopilot's ALWAYS_ALLOW_STEP), so a run that keeps a note waits at
        # a prompt nobody answers. The run keeps its ban, with the reason, and
        # the first draft's allowance is gone.
        run = " ".join((section(read(self.DAILY), "## The run") or "").split())
        self.assertEqual(run.count(RUN_NO_NOTE), 1)
        self.assertIn("Call no tool that changes anything", run)
        self.assertNotIn(RUN_NOTES, run)
        self.assertNotIn("`session_note`", run)

    def test_the_set_up_lets_the_runs_two_adcopilot_tools_through(self):
        # 0.2.14: since v2.42.3 Claude lists get_org_context, every run's
        # first call, under Write/delete tools, so a set-up that kept every
        # write tool asking stalled the run at that call. The step now says
        # what AdCopilot's ALWAYS_ALLOW_STEP says: read-only tools and the
        # two AdCopilot tools, by the titles Claude shows, on Always allow;
        # every other write tool still asks. The run keeps its ban on notes
        # all the same (test_the_run_keeps_no_note): schedules set up before
        # this version still ask before save_org_context.
        setup = section(read(self.DAILY), "## The set-up") or ""
        claude = setup[setup.find("**Claude — claude.ai, Cowork, the desktop app:**"):]
        step1 = " ".join(claude[claude.find("\n1. "):claude.find("\n2. ")].split())
        self.assertIn(SET_UP_ALWAYS_ALLOW, step1)
        self.assertIn("**Tool permissions**", step1)
        self.assertNotIn(SET_UP_WRITES_ASK, step1)
        self.assertNotIn(SET_UP_NOTE_ALLOWED, step1)
        # Never a tool identifier: Claude shows the title, not the name.
        self.assertNotIn("`get_org_context`", step1)
        self.assertNotIn("`save_org_context`", step1)
        self.assertEqual(" ".join(read(self.DAILY).split()).count("**Always allow**"), 2)
        run = " ".join((section(read(self.DAILY), "## The run") or "").split())
        self.assertEqual(run.count(RUN_NO_NOTE), 1)

    def test_the_release_check_expects_no_note(self):
        releasing = " ".join((section(read("README.md"), "## Releasing") or "").split())
        step6 = releasing[releasing.find("6. The scheduled run"):
                          releasing.find("7. `claude plugin validate")]
        self.assertIn("and no `save_org_context` either (a schedule set up "
                      "before 0.2.14 keeps that tool asking first, so a note "
                      "would stop it)", step6)
        self.assertNotIn("**Always allow**", step6)
        # The run forbids a change in every product it can reach, so the
        # release check does too: under "in Google Ads" alone, a run that
        # created an Analytics event or a Tag Manager tag would pass step 6.
        products = "in Google Ads, Analytics, Tag Manager or Search Console"
        run = " ".join((section(read(self.DAILY), "## The run") or "").split())
        self.assertIn(products, run)
        self.assertIn("calls no tool that changes anything " + products, step6)
        note = section(read("README.md"), "## AdCopilot version") or ""
        note = " ".join(note[note.find("**%s (" % SCHEDULED_NOTE_VERSION):]
                        .split("\n\n", 1)[0].split())
        self.assertNotIn(SET_UP_NOTE_ALLOWED, note)
        for part in ("still calls no `save_org_context`",
                     "a run that kept a note would stop there and never finish",
                     "once AdCopilot has told the people who already schedule "
                     "the check to set the two tools to **Always allow**, and "
                     "that notice has been measured"):
            with self.subTest(part=part):
                self.assertIn(part, note)

    def test_the_scheduled_case_fails_any_save(self):
        # A note included: on the set-ups that exist, it stops the run.
        text = read("evals/%s/case.yaml" % self.CASE)
        saves = [b for b in re.split(r"\n  - name: ", text)[1:]
                 if re.search(r"^\s+tool: \S*__save_org_context\s*$", b, re.M)]
        self.assertEqual(len(saves), 1, "one grader on save_org_context")
        block = grader_block(text, "never-writes-to-adcopilot")
        for line in ("type: tool_used", "min: 0", "max: 0"):
            with self.subTest(line=line):
                self.assertRegex(block, r"(?m)^\s+%s\s*$" % re.escape(line))
        # Counted on every call, whatever it carries.
        self.assertNotIn("input_match", block)
        self.assertNotIn("notes-only-to-adcopilot", text)
        self.assertNotIn("kept a note in AdCopilot", text)
        self.assertIn("or saved anything", text)

    UNMARKED = "review-scheduled-unmarked"

    def test_a_case_runs_the_review_skill_in_a_task_without_the_marker(self):
        # The PR #22 review: the case #22 exists for, a scheduled task in
        # the customer's own words answered by adcopilot-review, had no eval;
        # only daily-scheduled-run, where adcopilot-daily answers, graded the
        # marker. This case's prompt is not AdCopilot's recipe and names no
        # source, so the marker can come only from the skill.
        self.assertTrue(os.path.isfile(os.path.join(
            ROOT, "evals", self.UNMARKED, "case.yaml")), "no %s case" % self.UNMARKED)
        text = read("evals/%s/case.yaml" % self.UNMARKED)
        self.assertIn("tags: [review]\n", text)
        self.assertIn("adcopilot-review", grader_block(text, "skill-fired"))
        m = re.search(r"^  prompt: \|\n((?:    .*\n)+)", text, re.M)
        self.assertIsNotNone(m)
        prompt = " ".join(m.group(1).split())
        self.assertIn("scheduled task", prompt)
        self.assertFalse(prompt.startswith("AdCopilot morning check"))
        for word in ("claude-scheduled", "claude-plugin", "source",
                     "get_org_context", "morning check"):
            with self.subTest(absent=word):
                self.assertNotIn(word, prompt)
        # The marker grader is daily-scheduled-run's, line for line.
        def rule(case):
            block = grader_block(read("evals/%s/case.yaml" % case),
                                 "marks-the-scheduled-run")
            return [l.strip() for l in block.splitlines()
                    if not l.strip().startswith("#")]
        self.assertEqual(rule(self.UNMARKED), rule(self.CASE))
        block = grader_block(text, "marks-the-scheduled-run")
        pattern = re.compile(re.search(r"^\s+input_match: '((?:[^']|'')*)'\s*$",
                                       block, re.M).group(1).replace("''", "'"))
        counted = ['{}', '{"source":"claude-plugin/%s"}' % manifest_version(),
                   '{"source": "claude-plugin"}', '{"source":"chatgpt"}', 'not json']
        passed = ['{"source":"claude-scheduled"}',
                  '{"tools":["full_audit"],"source": "claude-scheduled"}']
        for call in counted:
            with self.subTest(call=call):
                self.assertRegex(call, pattern)
        for call in passed:
            with self.subTest(call=call):
                self.assertNotRegex(call, pattern)
        # A run that never reads the server would pass the grader above on
        # zero calls; this one fails it.
        server, _ = grader(self.UNMARKED, "read-the-server-first")
        self.assertRegex('"tool": "mcp__plugin_adcopilot_adcopilot__get_org_context", '
                         '"input": "{}"', server)
        self.assertNotRegex('"tool": "mcp__plugin_adcopilot_adcopilot__full_audit", '
                            '"input": "{\\"source\\": \\"get_org_context\\"}"', server)
        # Nothing in Google Ads changes; a note is not graded here.
        writes, _ = grader(self.UNMARKED, "never-changes-google-ads")
        self.assertIn("match: not_contains",
                      grader_block(text, "never-changes-google-ads"))
        for tool in ("add_negative_keywords", "update_campaign",
                     "set_campaign_status", "gtm_create_tag",
                     "ga4_create_conversion_event"):
            with self.subTest(write=tool):
                self.assertRegex('"tool": "mcp__plugin_adcopilot_adcopilot__%s"' % tool,
                                 writes)
        for tool in ("get_org_context", "full_audit", "analyze_waste",
                     "analyze_search_terms", "budget_pacing", "search",
                     "conversion_setup_audit", "save_org_context"):
            with self.subTest(read=tool):
                self.assertNotRegex('"tool": "mcp__plugin_adcopilot_adcopilot__%s"' % tool,
                                    writes)

    def test_the_unmarked_case_is_served_the_scheduled_answer(self):
        # The answer v2.41.0 gives a call marked claude-scheduled: no plugin
        # block, so no skill named and the playbook's full branch; the same
        # data as review-follows-related-reads but the two sightings the call
        # stamps before the answer is read.
        ctx = mock(self.UNMARKED, "get_org_context")
        source = mock("review-follows-related-reads", "get_org_context")
        self.assertNotIn("plugin", ctx)
        self.assertNotIn("[PLUGIN]", ctx["playbook"])
        self.assertIn("[%s]" % ctx["situation"], ctx["playbook"])
        self.assertNotIn("installed in this assistant", ctx["next_step"])
        self.assertIsNone(ctx["overlays"]["schedule_offer"])
        self.assertNotIn("schedule", ctx["routine"])
        stamp = ctx["routine"]["scheduled_last_seen_at"]
        self.assertRegex(stamp, r"^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d$")
        self.assertEqual(ctx["routine"]["scheduled_first_seen_at"], stamp)
        differ = sorted(k for k in set(ctx) | set(source)
                        if ctx.get(k) != source.get(k))
        self.assertEqual(differ, ["next_step", "playbook", "plugin", "routine"])
        rest = dict(ctx["routine"], scheduled_first_seen_at=None,
                    scheduled_last_seen_at=None)
        was = dict(source["routine"], scheduled_first_seen_at=None,
                   scheduled_last_seen_at=None)
        self.assertEqual(rest, was)
        head = read("evals/%s/mocks/adcopilot/get_org_context.md" % self.UNMARKED)
        head = " ".join(re.match(r"^---\n(.*?)\n---\n", head, re.S).group(1)
                        .replace("#", " ").split())
        self.assertIn("Re-rendered with AdCopilot release/v2.41.0's own code "
                      "(967d743b", head)
        # The other mocks are the source case's, byte for byte.
        mocks = os.path.join(ROOT, "evals", self.UNMARKED, "mocks", "adcopilot")
        for name in sorted(os.listdir(mocks)):
            if name == "get_org_context.md":
                continue
            with self.subTest(mock=name):
                self.assertEqual(
                    read("evals/%s/mocks/adcopilot/%s" % (self.UNMARKED, name)),
                    read("evals/review-follows-related-reads/mocks/adcopilot/%s" % name))

    def test_the_readme_note_says_both(self):
        notes = section(read("README.md"), "## AdCopilot version") or ""
        start = notes.find("**%s (" % SCHEDULED_NOTE_VERSION)
        note = " ".join(notes[start:].split("\n\n", 1)[0].split())
        for part in ('`source: "claude-scheduled"`', "never `claude-plugin`",
                     "`save_org_context`", CONTEXT_TOOL_TITLE, SAVE_TOOL_TITLE,
                     CHECKIN_FIRST_CALL,
                     "AdCopilot v2.44.0, deployed 2026-10-22"):
            with self.subTest(part=part):
                self.assertIn(part, note)

    def test_the_readme_note_says_only_the_recipe_is_the_morning_check(self):
        # PR #22's second review: AdCopilot read any run marked
        # claude-scheduled as its morning check, so a customer's own weekly
        # task stopped the morning-check offer. C5 (AdCopilot v2.43,
        # `schedule_recipe.CHECKIN_TASK`, `is_morning_check_task`) counts only
        # a run whose first call also names the morning check's task; the
        # note says what the server does now, not what it did at d9bd20ae.
        notes = section(read("README.md"), "## AdCopilot version") or ""
        start = notes.find("**%s (" % SCHEDULED_NOTE_VERSION)
        note = " ".join(notes[start:].split("\n\n", 1)[0].split())
        for part in ("counts only a run whose first call also names that task "
                     "as its morning check",
                     "a customer's own scheduled task is a scheduled run, not "
                     "the morning check",
                     "even when an older saved copy of the recipe does not "
                     "name it"):
            with self.subTest(part=part):
                self.assertIn(part, note)
        self.assertNotIn("a customer's own scheduled task counts as one too", note)


class AlwaysAllowStep(unittest.TestCase):
    """0.2.14: every copy of the step that lets a scheduled run finish names
    both AdCopilot tools Claude lists under Write/delete tools.

    v2.42.3 annotates `get_org_context` as not read-only, so Claude lists it,
    titled "AdCopilot: what is connected and where you are", under
    Write/delete tools beside "AdCopilot: save business notes and progress".
    A copy of the set-up step that puts only the read-only tools on Always
    allow leaves the run's first call on Needs approval, and the run stops
    there with nobody to answer: 23 scheduling workspaces last ran between
    2026-10-16 and the v2.42.3 deploy, and 19 of them were not seen again.
    AdCopilot's own step (`schedule_recipe.ALWAYS_ALLOW_STEP`, v2.44.0) names
    both titles; every copy here must too, and the run's first call names the
    morning check's task (`CHECKIN_FIRST_CALL`)."""

    DAILY = "skills/adcopilot-daily/SKILL.md"
    # Words only a copy of the permissions step carries.
    STEP = re.compile(r"Always allow|Tool permissions|tool permissions")

    def copies(self):
        """(file, paragraph) for every paragraph or list item, in the files
        the model reads and in the README, that gives the permissions step."""
        found = []
        for rel in model_read_files() + ["README.md"]:
            for para in re.split(r"\n\s*\n|\n(?=\d+\. |- )", read(rel)):
                if self.STEP.search(para):
                    found.append((rel, " ".join(para.split())))
        return found

    def test_every_copy_names_both_tools(self):
        copies = self.copies()
        files = sorted({rel for rel, _ in copies})
        # The set-up step in the daily skill, and the README's account of it.
        self.assertIn(self.DAILY, files)
        self.assertIn("README.md", files)
        for rel, para in copies:
            with self.subTest(file=rel, para=para[:80]):
                self.assertIn(CONTEXT_TOOL_TITLE, para)
                self.assertIn(SAVE_TOOL_TITLE, para)
                self.assertIn("Needs approval", para)

    def test_the_old_step_is_gone_everywhere(self):
        for rel in model_read_files() + ["README.md"]:
            text = flat(rel)
            with self.subTest(file=rel):
                self.assertNotIn(SET_UP_WRITES_ASK, text)
                self.assertNotIn("set the read-only tools to **Always allow**", text)
        manifest = " ".join(read(".claude-plugin/plugin.json").split())
        self.assertNotIn("Always allow", manifest)

    def test_the_titles_are_the_servers(self):
        # schedule_recipe.CONTEXT_TOOL_TITLE and SAVE_TOOL_TITLE at v2.44.0,
        # quoted as AdCopilot's step quotes them.
        self.assertEqual(CONTEXT_TOOL_TITLE,
                         "AdCopilot: what is connected and where you are")
        self.assertEqual(SAVE_TOOL_TITLE,
                         "AdCopilot: save business notes and progress")
        self.assertIn("“%s” and “%s”" % (CONTEXT_TOOL_TITLE, SAVE_TOOL_TITLE),
                      SET_UP_ALWAYS_ALLOW)
        self.assertEqual(flat(self.DAILY).count(SET_UP_ALWAYS_ALLOW), 1)

    def test_the_run_names_the_morning_check_task(self):
        self.assertEqual(CHECKIN_FIRST_CALL,
                         'Call get_org_context first, with source '
                         '"claude-scheduled" and task "AdCopilot morning check".')
        self.assertIn('task "%s"' % CHECKIN_TASK, CHECKIN_FIRST_CALL)
        self.assertEqual(SCHEDULED_CHECKIN.count(CHECKIN_FIRST_CALL), 1)
        self.assertTrue(SCHEDULED_CHECKIN.startswith(
            CHECKIN_TASK + ", read-only. " + CHECKIN_FIRST_CALL + " "))
        setup = section(read(self.DAILY), "## The set-up") or ""
        self.assertEqual(fenced(setup).count(CHECKIN_FIRST_CALL), 1)
        run = section(read(self.DAILY), "## The run") or ""
        step1 = " ".join(run[run.find("\n1. "):run.find("\n2. ")].split())
        self.assertIn('`source: "claude-scheduled"` and `task: "%s"`'
                      % CHECKIN_TASK, step1)
        # The 0.2.14 review: only the morning check's own instructions send
        # its task. A customer's own scheduled task that lands here and sent
        # it would be counted as the morning check (`is_morning_check_task`),
        # which C5 set out to stop.
        self.assertNotIn("even when the instructions do not name it", step1)
        self.assertIn('Send that task whenever the instructions open with "%s", '
                      'even when their first call does not name it' % CHECKIN_TASK,
                      step1)
        self.assertIn("any other scheduled task, such as one in the customer's "
                      "own words, sends the `task` its own instructions give, or "
                      "none, never the morning check's", step1)
        # The case's prompt is the older recipe the condition is for.
        prompt = read("evals/daily-scheduled-run/case.yaml")
        self.assertIn("    %s, read-only. Call get_org_context first." % CHECKIN_TASK,
                      prompt)

    def test_the_scheduled_case_grades_the_task(self):
        text = read("evals/daily-scheduled-run/case.yaml")
        block = grader_block(text, "names-the-morning-check")
        self.assertIn("arm: with-only", block)
        pattern = re.compile(re.search(r"^\s+input_match: '((?:[^']|'')*)'\s*$",
                                       block, re.M).group(1).replace("''", "'"))
        for call in ('{"source":"claude-scheduled"}', '{}', 'not json',
                     '{"source":"claude-scheduled","task":"Weekly report"}'):
            with self.subTest(counted=call):
                self.assertRegex(call, pattern)
        for call in ('{"source":"claude-scheduled","task":"AdCopilot morning check"}',
                     '{"task": "AdCopilot morning check", "source": "claude-scheduled"}'):
            with self.subTest(passed=call):
                self.assertNotRegex(call, pattern)
        # The prompt is an older saved recipe: it names no task, so the task
        # comes from the skill alone.
        m = re.search(r"^  prompt: \|\n((?:    .*\n)+)", text, re.M)
        self.assertNotIn("task", " ".join(m.group(1).split()))


if __name__ == "__main__":
    unittest.main()
