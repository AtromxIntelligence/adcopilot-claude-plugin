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
- The stop condition is the server's own (`situations.schedule_offer` on
  feat/v2302-t3): `routine.daily.status` `user_set` or a date in
  `routine.scheduled_last_seen_at`, and nothing else. If AdCopilot renames a
  field the offer never stops; if the plugin stops on more than the server
  does, the plugin is silent while the server's next_step asks for the offer.
- The unattended run. `adcopilot-daily` passes `claude-scheduled`, never
  `claude-plugin`, and its instructions say read-only and ask-nothing — the
  two properties a scheduled run with nobody to answer depends on. With no
  account named it never falls back to a manager account, which Google
  refuses metrics for.
- Honesty about what keeps a run to reads (D71's family). Nothing on the
  server makes a scheduled run read-only; on Automatically approve, or in a
  Claude Code routine, the instructions are all that does. Neither the skill
  nor the README may call that a guarantee.
- Directory policy (plan D7). Nothing the model is told by the habit block or
  the run carries sales or upgrade wording.
- The instructions the set-up hands over are AdCopilot's own recipe, word for
  word (`ads_mcp_cloud/schedule_recipe.py`, SCHEDULED_CHECKIN, as of
  AdCopilot v2.30.2); its first sentence is what marks the run.
  The server's emails, docs and dashboard do not all carry it yet, so nothing
  here says they do.
- The eval graders and the offer agree: the regexes that look for the offer
  (or for its absence) match the two sentences the block prescribes, so a
  reword cannot silently turn a grader blind.
- The manifest is 0.2.4 and every command the README lists exists.
- The plugin marker says its version (#696): every interactive
  `get_org_context` call passes `source: "claude-plugin/<version>"` with
  the manifest's own version, so a release bump that misses one copy
  fails here; no bare `"claude-plugin"` is left; the version is the
  X.Y.Z the server reads; and every eval grader that checks the marker
  fails the bare value and passes the versioned one.
"""

import json
import os
import subprocess
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
# SCHEDULED_CHECKIN, AdCopilot v2.30.2). `{account}` is filled
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


def manifest_version():
    return json.loads(read(".claude-plugin/plugin.json"))["version"]


def plugin_marker():
    """The marker every interactive `get_org_context` call passes (#696):
    the plugin and its version, which the server reads from the slash on."""
    return 'source: "claude-plugin/%s"' % manifest_version()


BARE_MARKER = 'source: "claude-plugin"'


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
        # feat/v2302-t3: tenants.ROUTINE_STATUSES, and tools_adcopilot's
        # routine["scheduled_last_seen_at"]).
        block = self.blocks()[HABIT_CARRIERS[0]] or ""
        for field in ("`routine.daily.status` is `user_set`",
                      "`routine.scheduled_last_seen_at`", "`in_app`"):
            with self.subTest(field=field):
                self.assertIn(field, block)

    def test_stop_condition_is_no_wider_than_the_servers(self):
        # situations.schedule_offer stops on user_set or a scheduled run seen,
        # never on a row's surface: a row switched off keeps surface
        # claude_scheduled, and Recipe A writes a weekly-only one. Stopping on
        # surface leaves the plugin silent while next_step asks for the offer.
        block = self.blocks()[HABIT_CARRIERS[0]] or ""
        self.assertNotIn("claude_scheduled", block)
        self.assertNotIn("`surface`", block)

    def test_offered_only_for_a_running_account(self):
        # The server offers only in ADS_ACTIVE_* situations: a campaign that
        # is switched on. /launch ends on a campaign built paused.
        block = self.blocks()[HABIT_CARRIERS[0]] or ""
        self.assertIn("a campaign switched on", block)

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
        self.assertNotIn('source: "claude-plugin', run)

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

        `adcopilot-daily` is the one exception: its run is unattended, so it
        passes `source: "claude-scheduled"` instead.
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
                marker = ('source: "claude-scheduled"'
                          if "adcopilot-daily" in rel
                          else plugin_marker())
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
        morning = section(read("README.md"), "### Every morning, without asking") or ""
        self.assertNotIn("It changes nothing", morning)
        self.assertIn("Nothing on AdCopilot's side stops a change", morning)
        self.assertIn("**Automatically approve**", morning)
        self.assertIn("**Blocked**", morning)

    def test_no_claim_the_recipe_is_already_everywhere(self):
        readme = read("README.md")
        self.assertNotIn("same text", readme)
        self.assertNotIn("emails and docs give", readme)

    def test_the_emailed_check_in_is_the_morning_check_only_when_on(self):
        morning = section(read("README.md"), "### Every morning, without asking") or ""
        self.assertIn("emailed daily check-in, when it is on,", morning)


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
        for case in ("habit-offer-code", "habit-offer-untold"):
            with self.subTest(case=case):
                pattern, flags = grader(case, "offer-names-schedule-at-the-end")
                self.assertRegex(self.REPLY + OFFER_CODE, re.compile(pattern, flags))
                self.assertNotRegex(self.REPLY + OFFER_CHAT, re.compile(pattern, flags))

    def test_untold_case_refuses_the_chat_wording_and_not_the_code_offer(self):
        pattern, flags = grader("habit-offer-untold", "not-the-claude-chat-wording")
        self.assertNotRegex(OFFER_CODE, re.compile(pattern, flags))
        self.assertRegex(OFFER_CHAT, re.compile(pattern, flags))

    def test_untold_case_says_nothing_about_where_they_are(self):
        # Every other habit case tells the model where it is, and the block
        # believes them, so the tell itself (`claude mcp list`) was never
        # exercised. This one is the bare command a real user types; the
        # harness is Claude Code, so the Claude Code wording is owed.
        text = read("evals/habit-offer-untold/case.yaml")
        m = re.search(r"^  prompt: \|\n((?:    .*\n)+)", text, re.M)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1).strip(), "/adcopilot:daily")

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
        owed = ("habit-offer-chat", "habit-offer-code", "habit-offer-untold",
                "daily-scheduled-run")
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
        self.assertGreaterEqual(seen, 14, "expected the 14 marker sites, saw %d" % seen)

    def test_no_bare_marker_is_left(self):
        for rel in self.model_read():
            with self.subTest(file=rel):
                self.assertNotIn(BARE_MARKER, read(rel),
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


class AuditorToolList(unittest.TestCase):
    """The auditor subagent reaches the live connector with nobody watching
    its individual calls, so the founder's rule is that it calls NO write
    tool. Its own text says it changes nothing, but text is not a constraint —
    the frontmatter `tools:` list is, and nothing held it to reads. This bans
    write VERBS rather than listing the reads, so a new read tool added later
    passes and any write fails, however the server names it."""

    WRITE_VERBS = ("add", "create", "update", "set", "remove", "link",
                   "attach", "pause", "save", "submit", "request", "delete",
                   "enable", "apply", "upload")
    # Product prefixes that sit in front of the verb.
    PRODUCTS = ("ga4_", "gtm_", "gsc_")
    # Non-connector tools the agent is allowed. Read only; no Bash, no Write.
    HOST_TOOLS = {"Read"}
    MCP = "mcp__plugin_adcopilot_adcopilot__"

    def tools(self):
        fm = frontmatter(read("agents/adcopilot-auditor.md"))
        m = re.search(r"^tools:\s*\[(.*?)\]\s*$", fm, re.S | re.M)
        self.assertIsNotNone(m, "the auditor has no `tools:` list to check")
        return [t.strip().strip('"\'') for t in m.group(1).split(",") if t.strip()]

    def test_every_connector_tool_is_a_read(self):
        offenders = []
        for tool in self.tools():
            if not tool.startswith(self.MCP):
                continue
            name = tool[len(self.MCP):]
            for prefix in self.PRODUCTS:
                if name.startswith(prefix):
                    name = name[len(prefix):]
                    break
            if name.split("_", 1)[0] in self.WRITE_VERBS:
                offenders.append(tool)
        self.assertEqual(
            [], offenders,
            "the auditor runs unattended and must call no write tool; "
            "these look like writes: %s" % offenders)

    def test_no_wildcard_and_no_host_write_tools(self):
        for tool in self.tools():
            if tool.startswith(self.MCP):
                continue
            self.assertNotIn("*", tool, "a wildcard would admit every write tool")
            self.assertIn(
                tool, self.HOST_TOOLS,
                "%s is not an allowed host tool for the auditor (Write, Edit "
                "and Bash would each give it a way around the read-only "
                "tool list)" % tool)

    def test_it_can_attribute_a_change(self):
        # Cover item 7 asks who changed a budget; without this read the
        # answer is always "unknown". read-only on the server side.
        self.assertIn(self.MCP + "change_history", self.tools())


if __name__ == "__main__":
    unittest.main()
