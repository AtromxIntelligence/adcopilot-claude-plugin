"""Structural invariants of the plugin's own text — the half of 0.2.4's
contract a model is not needed to check.

Run with `python3 -m unittest discover -s tests -v` from the repository root
(stdlib only; CI runs it in checks.yml).

What it pins, and why each one is here:

- The daily-habit block. Every interactive flow — the three teaching skills
  and the four commands that have no skill of their own — ends with the same
  offer to make the check a daily habit. It is repeated verbatim, like the
  teaching contract, because a skill cannot include another file in every
  surface the plugin runs on (an eval run has no Read tool at all). A copy
  that drifts is a flow that offers differently, or stops offering, so the
  copies are compared byte for byte.
- The stop condition names the three fields the server reports a schedule
  with. If AdCopilot renames one, the offer never stops; this is where that
  shows first.
- The unattended run. `adcopilot-daily` passes `claude-scheduled`, never
  `claude-plugin`, and its instructions say read-only and ask-nothing — the
  two properties a scheduled run with nobody to answer depends on.
- Directory policy (plan D7). Nothing the model is told by the habit block or
  the run carries sales or upgrade wording.
- The instructions the set-up hands over are AdCopilot's own recipe, word for
  word (`ads_mcp_cloud/schedule_recipe.py`, SCHEDULED_CHECKIN, as of server
  commit 11cc4469 on feat/v2302-t3): the server's emails, docs and dashboard
  give people the same text, and its first sentence is what marks the run.
- The eval graders and the offer agree: the regexes that look for the offer
  (or for its absence) match the two sentences the block prescribes, so a
  reword cannot silently turn a grader blind.
- The manifest is 0.2.4 and every command the README lists exists.
"""

import json
import os
import re
import unittest

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

HABIT_HEADING = "## The daily habit"
# The files that carry the block themselves. /setup, /launch and /measure
# delegate to a skill that carries it.
HABIT_CARRIERS = [
    "skills/adcopilot-connect/SKILL.md",
    "skills/adcopilot-launch/SKILL.md",
    "skills/adcopilot-measure/SKILL.md",
    "commands/audit.md",
    "commands/daily.md",
    "commands/weekly.md",
    "commands/negatives.md",
]
DELEGATING_COMMANDS = {
    "commands/setup.md": "adcopilot-connect",
    "commands/launch.md": "adcopilot-launch",
    "commands/measure.md": "adcopilot-measure",
}
COMMANDS = ["setup", "audit", "daily", "weekly", "negatives", "launch", "measure"]

# The two sentences the offer is made in, one per surface. The eval graders
# look for their substance, so a reword is a deliberate act, made here too.
OFFER_CHAT = ("If you'd like a check of this account every weekday morning "
              "without having to ask, say \"schedule it\" and I'll walk you "
              "through saving it as a Claude scheduled task — about two minutes.")
OFFER_CODE = ("If you'd like a check of this account every weekday morning "
              "without having to ask, say \"schedule it\" and I'll set it up "
              "as a Claude Code routine with /schedule.")

# AdCopilot's own recipe (server: ads_mcp_cloud/schedule_recipe.py,
# SCHEDULED_CHECKIN, commit 11cc4469 on feat/v2302-t3). `{account}` is filled
# in by the set-up. Change it there first, then here and in the skill.
SCHEDULED_CHECKIN = (
    "AdCopilot morning check, read-only. Call get_org_context first, with "
    "source \"claude-scheduled\". Do not use any tool that changes my "
    "account, and do not ask me questions; if something is unknown, say so "
    "and carry on. For {account}:\n"
    "1. Yesterday's spend, clicks, conversions and cost per conversion "
    "against my 7-day average.\n"
    "2. This month's budget pacing: on track, over or under, and any campaign "
    "limited by budget.\n"
    "3. The 5 search terms from the last 7 days that cost the most with no "
    "conversions, with their cost.\n"
    "4. Any ad that is disapproved or limited, with Google's stated reason.\n"
    "5. Any change made in the account in the last 24 hours, and by whom.\n"
    "Start with one line: \"All clear\" or \"Needs a look\". End with the "
    "single most valuable fix, written as a yes/no question I can answer when "
    "I open this."
)

# Sales or upgrade wording, which the directory policy keeps out of anything
# the model is told (plan D7), and the three words the copy rules ban.
SALES = re.compile(r"\b(upgrade|pricing|subscribe|subscription|trial|discount|"
                   r"buy|purchase|paid plan|starter|plus plan)\b|\$\d", re.I)
BANNED = re.compile(r"\b(seamless(ly)?|effortless(ly)?|magic(al)?)\b", re.I)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def section(text, heading):
    """The text from `heading` to the next heading of the same or a higher
    level, or to the end."""
    level = len(heading) - len(heading.lstrip("#"))
    start = text.find(heading + "\n")
    if start < 0:
        return None
    rest = text[start + len(heading) + 1:]
    m = re.search(r"^#{1,%d} " % level, rest, re.M)
    return heading + "\n" + (rest[:m.start()] if m else rest)


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else ""


def fenced(text, lang="text"):
    """The body of the first ```lang fenced block in `text`, or None."""
    m = re.search(r"^```%s\n(.*?)\n```$" % lang, text or "", re.S | re.M)
    return m.group(1) if m else None


def grader(case, name):
    """(pattern, flags) of a regex grader in evals/<case>/case.yaml. The
    patterns are single-quoted YAML scalars (a quote doubled inside), which is
    all this reads, so it needs no YAML library — CI's python3 is bare."""
    text = read("evals/%s/case.yaml" % case)
    start = text.index("  - name: %s\n" % name)
    end = text.find("\n  - name: ", start + 1)
    block = text[start:end if end > 0 else len(text)]
    m = re.search(r"^\s+pattern: '((?:[^']|'')*)'\s*$", block, re.M)
    if m is None:
        raise AssertionError("%s/%s has no single-quoted pattern" % (case, name))
    flags = re.I if re.search(r"^\s+flags: i\s*$", block, re.M) else 0
    return m.group(1).replace("''", "'"), flags


def mock(case, tool):
    """The JSON a `type: fixed` mock answers with, parsed."""
    text = read("evals/%s/mocks/adcopilot/%s.md" % (case, tool))
    return json.loads(re.match(r"^---\n.*?\n---\n(.*)$", text, re.S).group(1))


class DailyHabitBlock(unittest.TestCase):

    def blocks(self):
        return {rel: section(read(rel), HABIT_HEADING) for rel in HABIT_CARRIERS}

    def test_every_interactive_flow_carries_the_block(self):
        for rel, block in self.blocks().items():
            with self.subTest(file=rel):
                self.assertIsNotNone(block, "%s has no %r section" % (rel, HABIT_HEADING))

    def test_the_copies_are_identical(self):
        blocks = self.blocks()
        first_rel = HABIT_CARRIERS[0]
        first = (blocks[first_rel] or "").rstrip()
        for rel, block in blocks.items():
            with self.subTest(file=rel):
                self.assertEqual((block or "").rstrip(), first,
                                 "%s's daily-habit block differs from %s's — change all of them together"
                                 % (rel, first_rel))

    def test_it_is_the_last_section(self):
        # The offer closes the reply, so its instructions close the file:
        # nothing after it can be read as a later step.
        for rel in HABIT_CARRIERS:
            with self.subTest(file=rel):
                text = read(rel)
                after = text[text.find(HABIT_HEADING):]
                self.assertEqual(len(re.findall(r"^#{1,2} ", after, re.M)), 1,
                                 "%s has a section after the daily-habit block" % rel)

    def test_both_offer_sentences_verbatim(self):
        block = self.blocks()[HABIT_CARRIERS[0]] or ""
        self.assertIn(OFFER_CHAT, block)
        self.assertIn(OFFER_CODE, block)

    def test_stop_condition_names_the_servers_fields(self):
        # The names get_org_context reports a schedule by (server
        # feat/v2302-t3: tenants.ROUTINE_STATUSES / ROUTINE_SURFACES, and
        # tools_adcopilot's routine["scheduled_last_seen_at"]).
        block = self.blocks()[HABIT_CARRIERS[0]] or ""
        for field in ("`routine.daily.status` is `user_set`", "`claude_scheduled`",
                      "`routine.scheduled_last_seen_at`", "`in_app`"):
            with self.subTest(field=field):
                self.assertIn(field, block)

    def test_the_offer_is_not_a_second_question(self):
        # Every flow already ends on at most one question; the offer is a
        # statement, so a reply never ends on two.
        for offer in (OFFER_CHAT, OFFER_CODE):
            with self.subTest(offer=offer[-40:]):
                self.assertNotIn("?", offer)
        self.assertIn("not a second question", self.blocks()[HABIT_CARRIERS[0]] or "")

    def test_one_offer_even_when_the_server_asks_for_one(self):
        # The server's next_step can carry its own routine offer (a daily
        # check-in and a Monday summary); the reply makes one, not two.
        block = self.blocks()[HABIT_CARRIERS[0]] or ""
        self.assertIn("`next_step`", block)
        self.assertIn("never two", block)

    def test_never_in_a_run_nobody_reads(self):
        block = self.blocks()[HABIT_CARRIERS[0]] or ""
        self.assertIn("nobody is reading", block)

    def test_surface_tell_is_the_one_setup_uses(self):
        # /setup and adcopilot-connect tell Claude Code apart by
        # `claude mcp list`; the offer must not use a different tell.
        block = self.blocks()[HABIT_CARRIERS[0]] or ""
        self.assertIn("`claude mcp list`", block)
        self.assertIn("claude.ai, Cowork", block)

    def test_it_hands_a_yes_to_the_daily_skill(self):
        block = self.blocks()[HABIT_CARRIERS[0]] or ""
        self.assertIn("adcopilot-daily", block)

    def test_no_sales_wording(self):
        block = self.blocks()[HABIT_CARRIERS[0]] or ""
        self.assertIsNone(SALES.search(block), SALES.search(block) and SALES.search(block).group(0))

    def test_delegating_commands_point_at_a_carrier(self):
        for rel, skill in DELEGATING_COMMANDS.items():
            with self.subTest(file=rel):
                text = read(rel)
                self.assertIn("`%s` skill" % skill, text)
                self.assertIn("skills/%s/SKILL.md" % skill, HABIT_CARRIERS)


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
        self.assertNotIn('source: "claude-plugin"', run)

    def test_read_only_and_asks_nothing(self):
        run = section(self.skill(), "## The run") or ""
        self.assertRegex(run, r"Read only\.")
        self.assertRegex(run, r"Ask nothing\.")
        self.assertIn("save_org_context", run)  # named as a tool the run does not call
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

    def test_the_account_without_one_named(self):
        # The account AdCopilot's own check-in reads (plan B6/B11 fields).
        run = section(self.skill(), "## The run") or ""
        self.assertIn("`latest_check_in.account`", run)
        self.assertIn("`routine.daily.customer_id`", run)

    def test_no_sales_wording_in_the_run(self):
        run = section(self.skill(), "## The run") or ""
        self.assertIsNone(SALES.search(run))


class Commands(unittest.TestCase):

    def test_each_command_exists_with_frontmatter(self):
        for name in COMMANDS:
            with self.subTest(command=name):
                fm = frontmatter(read("commands/%s.md" % name))
                self.assertRegex(fm, r"(?m)^name: %s$" % name)
                self.assertRegex(fm, r"(?m)^description: \S")

    def test_interactive_reads_carry_the_plugin_marker(self):
        for name in ("audit", "daily", "weekly", "negatives"):
            with self.subTest(command=name):
                self.assertIn('source: "claude-plugin"', read("commands/%s.md" % name))

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


class EvalGraders(unittest.TestCase):
    """The deterministic graders and the offer they look for agree."""

    REPLY = "Needs a look: one ad is disapproved.\n\nShall I add the four negatives?\n\n"

    def test_chat_case_finds_the_chat_offer_at_the_end(self):
        pattern, flags = grader("habit-offer-chat", "offer-is-a-scheduled-task-at-the-end")
        self.assertRegex(self.REPLY + OFFER_CHAT, re.compile(pattern, flags))
        self.assertNotRegex(self.REPLY + OFFER_CHAT + "\n\n" + "x" * 400, re.compile(pattern, flags))

    def test_chat_case_refuses_the_code_wording_and_not_the_chat_offer(self):
        pattern, flags = grader("habit-offer-chat", "not-the-claude-code-wording")
        self.assertNotRegex(OFFER_CHAT, re.compile(pattern, flags))
        self.assertRegex(OFFER_CODE, re.compile(pattern, flags))

    def test_code_case_finds_the_code_offer_at_the_end(self):
        pattern, flags = grader("habit-offer-code", "offer-names-schedule-at-the-end")
        self.assertRegex(self.REPLY + OFFER_CODE, re.compile(pattern, flags))

    def test_quiet_cases_would_catch_either_offer(self):
        for case, name in (("habit-recorded-stays-quiet", "no-offer-wording"),
                           ("daily-scheduled-run", "never-offers-a-schedule")):
            pattern, flags = grader(case, name)
            for offer in (OFFER_CHAT, OFFER_CODE):
                with self.subTest(case=case, offer=offer[-30:]):
                    self.assertRegex(offer, re.compile(pattern, flags))

    def test_quiet_case_lets_a_report_mention_the_running_schedule(self):
        pattern, flags = grader("habit-recorded-stays-quiet", "no-offer-wording")
        self.assertNotRegex("Your scheduled morning check ran today, and the email "
                            "check-in comes every weekday morning.", re.compile(pattern, flags))

    def test_a_never_grader_allows_zero_calls(self):
        # `tool_used` counts from min 1 unless told otherwise, so `max: 0`
        # alone reads "expected 1..0" and fails every run, the clean ones
        # included (found on the first 0.2.4 run, 2026-10-04).
        cases = os.path.join(ROOT, "evals")
        for case in sorted(os.listdir(cases)):
            path = os.path.join(cases, case, "case.yaml")
            if not os.path.isfile(path):
                continue
            for block in re.split(r"\n  - name: ", read("evals/%s/case.yaml" % case))[1:]:
                if re.search(r"^\s+type: tool_used\s*$", block, re.M) and \
                        re.search(r"^\s+max: 0\s*$", block, re.M):
                    with self.subTest(case=case, grader=block.split("\n", 1)[0]):
                        self.assertRegex(block, r"(?m)^\s+min: 0\s*$")

    def test_mocks_carry_the_servers_schedule_fields(self):
        # The shape get_org_context answers with from the release that reads
        # "claude-scheduled": routine.scheduled_last_seen_at, latest_check_in.
        owed = ("habit-offer-chat", "habit-offer-code", "daily-scheduled-run")
        for case in owed + ("habit-recorded-stays-quiet",):
            ctx = mock(case, "get_org_context")
            with self.subTest(case=case):
                self.assertIn("scheduled_last_seen_at", ctx["routine"])
                self.assertIn("latest_check_in", ctx)
                self.assertEqual(ctx["routine"]["daily"]["status"], "in_app")
                if case in owed:
                    self.assertIsNone(ctx["routine"]["scheduled_last_seen_at"])
                else:
                    self.assertRegex(ctx["routine"]["scheduled_last_seen_at"] or "", r"^\d{4}-\d\d-\d\d")


class Copy(unittest.TestCase):

    def test_no_banned_words_anywhere_the_model_reads(self):
        files = ["README.md"] + ["commands/%s" % f for f in os.listdir(os.path.join(ROOT, "commands"))]
        files += ["skills/%s/SKILL.md" % d for d in os.listdir(os.path.join(ROOT, "skills"))]
        for rel in files:
            with self.subTest(file=rel):
                self.assertIsNone(BANNED.search(read(rel)))


class Manifest(unittest.TestCase):

    def test_version(self):
        self.assertEqual(json.loads(read(".claude-plugin/plugin.json"))["version"], "0.2.4")


if __name__ == "__main__":
    unittest.main()
