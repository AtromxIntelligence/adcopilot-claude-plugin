"""The eval cases, their graders and their fixtures.

One of the structural test files that `tests/test_structure.py` was split
into in 0.2.15. At 273 KB that file was over the plugin directory's 256 KiB
limit for a file that is not an image or a font. The tests moved verbatim, by
topic (same classes, same names, same assertions), and the helpers they share
live in `structure_helpers.py`; `tests/test_plugin_size.py` keeps any file
from growing past the limit again.

Run with `python3 -m unittest discover -s tests -v` from the repository root
(stdlib only; CI runs it in checks.yml).

What it pins, and why each one is here:
- The eval graders and the offer agree: the regexes that look for the offer
  (or for its absence) match the two sentences the block prescribes, so a
  reword cannot silently turn a grader blind.

- The eval cases hold what the transcript did and the fixtures the server
  would really send: the docs cases, the judge's replay, the 0.2.12 cases, and
  the older fixtures re-rendered with release/v2.41.0's own code.
"""

import os
import sys
import json
import re
import unittest

# The helpers sit beside this file; the path is set so this file also runs
# on its own (`python3 tests/test_eval_cases.py`).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from structure_helpers import (  # noqa: E402
    CHECKIN_FIRST_CALL,
    OFFER_CHAT,
    OFFER_CODE,
    ROOT,
    SCHEDULED_CHECKIN,
    SERVER_MEASURE_STEP,
    SERVER_RETURNING,
    SERVER_REVIEW_STEP,
    grader,
    grader_block,
    manifest_version,
    mock,
    never_grader,
    read,
    section,
)


# The same recipe as v2.41.0 rendered it, before C5 gave its first call a
# `task`: the frozen eval fixtures re-rendered with that release's code
# (OlderFixturesOnV241) still carry it, and a recipe saved then opens with it.
SCHEDULED_CHECKIN_V241 = SCHEDULED_CHECKIN.replace(
    CHECKIN_FIRST_CALL,
    "Call get_org_context first, with source \"claude-scheduled\".", 1)


class EvalGraders(unittest.TestCase):
    """The deterministic graders and the offer they look for agree."""

    # The wasted searches are the first finding that puts a cost on
    # something; the offer follows them and the reply ends on its question.
    COST = "Needs a look: four searches took $24.50 in clicks and sold nothing.\n\n"
    ASK = "\n\nShall I add the four negatives?\n\n"

    def test_chat_case_finds_the_chat_offer_with_its_value_line(self):
        pattern, flags = grader("habit-offer-chat", "offer-is-a-scheduled-task-with-the-value-line")
        self.assertRegex(self.COST + OFFER_CHAT + self.ASK, re.compile(pattern, flags))
        # No offer, or one with no value line, is not it.
        self.assertNotRegex(self.COST + self.ASK, re.compile(pattern, flags))
        self.assertNotRegex(self.COST + "Want a daily check? Say \"schedule it\" and "
                            "I'll set it up as a Claude scheduled task." + self.ASK,
                            re.compile(pattern, flags))

    def test_the_offer_is_not_required_to_be_the_last_thing(self):
        # 0.2.11 moved it: after the costly finding, before the question the
        # reply ends on. The old graders demanded it within 300 characters of
        # the end, which the new reply fails by design.
        for case, name in (("habit-offer-chat", "offer-is-a-scheduled-task-with-the-value-line"),
                           ("habit-offer-code", "offer-names-schedule-with-the-value-line"),
                           ("habit-offer-untold", "offer-names-schedule-with-the-value-line")):
            text = read("evals/%s/case.yaml" % case)
            self.assertNotIn("$'", grader_block(text, name), case)
            self.assertNotIn("at-the-end", text, case)

    def test_chat_case_refuses_the_code_wording_and_not_the_chat_offer(self):
        pattern, flags = grader("habit-offer-chat", "not-the-claude-code-wording")
        self.assertNotRegex(OFFER_CHAT, re.compile(pattern, flags))
        self.assertRegex(OFFER_CODE, re.compile(pattern, flags))

    def test_code_case_finds_the_code_offer_with_its_value_line(self):
        for case in ("habit-offer-code", "habit-offer-untold"):
            with self.subTest(case=case):
                pattern, flags = grader(case, "offer-names-schedule-with-the-value-line")
                self.assertRegex(self.COST + OFFER_CODE + self.ASK, re.compile(pattern, flags))
                self.assertNotRegex(self.COST + OFFER_CHAT + self.ASK, re.compile(pattern, flags))
                self.assertNotRegex(self.COST + self.ASK, re.compile(pattern, flags))

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


# The playbook section an installed skill gets (onboarding_skill
# ._PLUGIN_SECTION, release/v2.41.0), with the skill named.
SERVER_PLUGIN_SECTION = ("## [PLUGIN] The installed skill\n\n"
                         "The AdCopilot skill {skill}, installed here, carries "
                         "this situation's steps. On a greeting alone, a request "
                         "to get started or the request it is for, follow it, "
                         "inside the rails, with the reads `cross_reads` names. "
                         "Asked anything else, answer that first with only the "
                         "reads it needs, then offer it.")


class RealTurnDocsCase(unittest.TestCase):
    """Fix round 1: docs-capabilities-routed hands a counted account to the
    review, but the real turn (audit rows, 2026-10-13 20:55 UTC) was
    ADS_ACTIVE_UNTRACKED handed to adcopilot-measure, with situational
    cross_reads that made no read and offered Analytics. This case is that
    state, graded on the same docs rule, and also on starting neither the
    review nor the measurement steps and on no budget read, which the real
    turn made."""

    CASE = "docs-capabilities-untracked"
    MCP = "mcp__plugin_adcopilot_adcopilot__"

    def test_the_fixture_is_the_real_turns_server_state(self):
        ctx = mock(self.CASE, "get_org_context")
        self.assertEqual(ctx["situation"], "ADS_ACTIVE_UNTRACKED")
        self.assertEqual(ctx["plugin"]["skill"], "adcopilot-measure")
        self.assertEqual(ctx["next_step"], SERVER_MEASURE_STEP + " " + SERVER_RETURNING)
        for part in ("[RAILS]", "[RECAP]", "[PLUGIN]", "adcopilot-measure"):
            with self.subTest(part=part):
                self.assertIn(part, ctx["playbook"])
        cross = ctx["cross_reads"]
        self.assertEqual(cross["mode"], "situational")
        self.assertEqual(cross["reads"], [])
        self.assertEqual([c["product"] for c in cross["connect"]], ["ga4"])
        # v2.41.0: an untracked account on a day with no daily limit is sized
        # at eight (situations.ads_reads_max, roomy_day).
        self.assertEqual(cross["ads_reads_max"], 8)
        self.assertNotIn("reads_left_today", cross)
        self.assertIn(SERVER_PLUGIN_SECTION.format(skill="adcopilot-measure"),
                      ctx["playbook"])
        self.assertEqual(ctx["org"]["plan"], "pro")
        self.assertIsNone(ctx["org"]["ops_today_cap"])
        products = ctx["products"]
        self.assertTrue(products["google_ads"]["connected"])
        self.assertTrue(products["search_console"]["connected"])
        self.assertFalse(products["ga4"]["connected"])
        self.assertFalse(products["gtm"]["connected"])
        probe = next(v for k, v in ctx["ads_probe"].items() if k.isdigit())
        self.assertGreater(probe["last_30d"]["cost_micros"], 0)
        self.assertEqual(probe["last_30d"]["conversions"], 0)
        # Untracked, not the routed case's tracked sub-case: 50 clicks or more.
        self.assertGreaterEqual(probe["last_30d"]["clicks"], 50)
        self.assertGreaterEqual(probe["conversion_actions"]["primary"], 1)

    def test_it_reads_nothing_and_starts_neither_skill(self):
        text = read("evals/%s/case.yaml" % self.CASE)
        for tool in ("full_audit", "analyze_waste", "analyze_search_terms",
                     "search", "conversion_setup_audit", "budget_pacing",
                     "gsc_search_analytics"):
            with self.subTest(tool=tool):
                self.assertTrue(never_grader(text, self.MCP + tool), tool)
        for skill in ("adcopilot-review", "adcopilot-measure"):
            with self.subTest(skill=skill):
                self.assertTrue(never_grader(text, "Skill", skill), skill)
        self.assertIn("adcopilot-docs", grader_block(text, "skill-fired"))
        self.assertIn('  prompt: "I have the AdCopilot plugin. Please walk me '
                      'through what it can do."\n', text)
        self.assertIn("tags: [docs]\n", text)

    def test_its_rubric_and_approval_grader(self):
        text = read("evals/%s/case.yaml" % self.CASE)
        for name in DocsJudgeReplay.ITEMS[self.CASE]:
            with self.subTest(grader=name):
                llm = grader_block(text, name)
                self.assertIn("type: llm", llm)
                self.assertIn("$1,865 on 607 clicks", llm)
        self.assertIn("Exactly one question",
                      grader_block(text, "one-closing-question"))
        self.assertIn("Tracking without Analytics",
                      grader_block(text, "tracking-without-analytics"))
        self.assertEqual(grader(self.CASE, "no-approval-promise-without-its-condition"),
                         grader("docs-capabilities-routed",
                                "no-approval-promise-without-its-condition"))
        self.assertIn("marks-plugin-use", text)

    def test_the_routed_case_no_longer_claims_the_real_turns_hand_off(self):
        routed = read("evals/docs-capabilities-routed/case.yaml")
        description = routed[:routed.index("tags:")]
        self.assertIn("docs-capabilities-untracked reproduces it", description)
        self.assertNotIn("because the server's next_step said", description)

    def test_every_mock_it_needs_is_there(self):
        for tool in ("get_org_context", "full_audit", "search",
                     "analyze_search_terms", "analyze_waste",
                     "conversion_setup_audit", "budget_pacing",
                     "gsc_search_analytics"):
            with self.subTest(tool=tool):
                self.assertIsInstance(mock(self.CASE, tool), dict)


class DocsJudgeReplay(unittest.TestCase):
    """Fix round 2 (2026-10-17), committed locally as 9d60b3c, d90ca35 and
    467c2a8 and never pushed: the v2.41 alignment was built on the branch as
    pushed, so it left them out, and the Cursor round's review found them
    missing. They come back here on the current text, with the approval
    item in its client-neutral form.

    From the first run of the two docs cases (claudeVersion 2.1.302, judge
    sonnet, plugin d478dba): every deterministic grader passed on all six
    runs, and the one rubric grader failed five of them. Each saved reply
    was put back in front of the suite's own judge, one rubric item at a
    time. Item 2 failed every reply on 3 of 3 votes, because it allowed
    nothing about the account "beyond facts from that 30-day summary" while
    item 1 asks for what is connected, the routines and the look-ups, which
    the same workspace answer carries. With item 2 allowing what that answer
    says, all six replies pass it on 3 of 3 votes, and four replies that
    each review the account (one of them the real 2026-10-14 turn) still
    fail it on 3 of 3.

    One routed reply failed the approval item on its own text: a routine's
    line said "Nothing is added until you say yes." with no condition. The
    docs skill now keeps approval out of the routine lines and says it once,
    with its condition.

    A strict one-word judge given four or five conditions at once failed a
    reply it passed on each, so each item is its own llm grader with the
    same words, and a run's report says which item failed. Written as
    "PASS only if this holds:" and then the numbered item on its own line,
    the approval item passed 7 of 8 saved replies it had failed in the
    unnumbered form, and still failed a reply whose approval line had no
    condition. The run on 467c2a8 (2026-10-17T15:21Z) passed both docs
    cases."""

    CASES = ("docs-capabilities-untracked", "docs-capabilities-routed")
    ITEMS = {
        "docs-capabilities-untracked": [
            "one-list", "no-review-no-set-up", "one-closing-question",
            "approval-with-its-condition", "tracking-without-analytics"],
        "docs-capabilities-routed": [
            "one-list", "no-review", "one-closing-question",
            "approval-with-its-condition"],
    }
    REVIEW = {"docs-capabilities-untracked": "no-review-no-set-up",
              "docs-capabilities-routed": "no-review"}
    OLD = ("The reply reports nothing about the account beyond facts from "
           "that 30-day summary")
    ALLOWED = ("Apart from what the workspace answer itself says (what is "
               "connected and to which account or site, how many campaigns "
               "there are and how many are on, which routines are already "
               "scheduled, the plan and the look-ups used today) and the "
               "facts in that 30-day summary, with at most a sentence on what "
               "the 30-day fact could mean as the reason for the closing "
               "offer, the reply reports nothing about the account: no health "
               "score, no audit findings, no search terms, no "
               "week-against-week comparison, no budget pacing figures, no "
               "setting to change")

    def test_item_two_allows_what_the_workspace_answer_says(self):
        for case in self.CASES:
            llm = grader_block(read("evals/%s/case.yaml" % case),
                               self.REVIEW[case])
            with self.subTest(case=case):
                self.assertNotIn(self.OLD, llm)
                self.assertEqual(llm.count(self.ALLOWED), 1)
                self.assertIn("Saying what a routine does is not reporting on "
                              "the account.", llm)
                self.assertIn("FAIL if it delivers a performance review", llm)

    def test_the_untracked_case_still_fails_a_started_set_up(self):
        llm = grader_block(read("evals/docs-capabilities-untracked/case.yaml"),
                           "no-review-no-set-up")
        self.assertIn("and it does not start setting up conversion tracking.",
                      llm)
        self.assertIn("or begins the tracking set-up.", llm)

    def test_each_item_is_its_own_llm_grader(self):
        for case in self.CASES:
            text = read("evals/%s/case.yaml" % case)
            with self.subTest(case=case):
                self.assertNotIn("one-list-one-question", text)
                self.assertNotIn("PASS only if all", text)
                llm = [b for b in re.split(r"\n  - name: ", text)[1:]
                       if re.search(r"^    type: llm$", b, re.M)]
                self.assertEqual([b.split("\n", 1)[0] for b in llm],
                                 self.ITEMS[case])
                for n, block in enumerate(llm, 1):
                    # The item keeps its number after a colon and a new line:
                    # as "PASS only if this holds. Approval with its
                    # condition. ..." the suite's judge failed the approval
                    # item on 7 of 8 saved replies; in this form it passes 7
                    # of the same 8 (fix round 2's replay).
                    self.assertEqual(block.count(
                        "      PASS only if this holds:\n      %d. " % n), 1)
                    self.assertIn("The customer asked only what the AdCopilot "
                                  "plugin can do.", block)
                    self.assertIn("focus: last_message", block)
                    self.assertNotRegex(block, r"^    weight:")

    def test_the_approval_item_keeps_the_client_neutral_condition(self):
        for case in self.CASES:
            llm = " ".join(grader_block(read("evals/%s/case.yaml" % case),
                                        "approval-with-its-condition").split())
            with self.subTest(case=case):
                self.assertIn("4. Approval with its condition.", llm)
                self.assertIn("in Cursor, the Allowlist run mode with the "
                              "write tools kept off the allowlist", llm)
                self.assertNotIn("while the write tools stay on Needs "
                                 "approval", llm)

    def test_a_routine_line_carries_no_approval(self):
        can = " ".join((section(read("skills/adcopilot-docs/SKILL.md"),
                                "## What AdCopilot can do") or "").split())
        self.assertIn("Say what each routine reads and proposes, and leave "
                      "approval to the part on what AdCopilot may change, "
                      "where it is said once with its condition: no routine's "
                      "line adds that nothing happens until they say yes.",
                      can)


class NewEvalCases(unittest.TestCase):
    """0.2.12's two cases, held to what the transcript did and to the
    fixtures the server would really send."""

    UNCAPPED = "review-uncapped-no-limit-words"
    ROUTED = "docs-capabilities-routed"
    MCP = "mcp__plugin_adcopilot_adcopilot__"
    TRANSCRIPT_LIMIT = ("I hit today's read limit for this review before listing "
                        "those searches, so that's one more look-up.")

    def test_the_uncapped_fixture_is_pro_with_no_day_to_spend(self):
        ctx = mock(self.UNCAPPED, "get_org_context")
        self.assertEqual(ctx["org"]["plan"], "pro")
        self.assertIsNone(ctx["org"]["ops_today_cap"])
        self.assertEqual(ctx["situation"], "ADS_ACTIVE_UNTRACKED")
        # v2.41.0 sizes this answer at eight on a day with no daily limit.
        self.assertEqual(ctx["cross_reads"]["ads_reads_max"], 8)
        self.assertNotIn("reads_left_today", ctx["cross_reads"])
        self.assertEqual(ctx["next_step"], SERVER_MEASURE_STEP + " " + SERVER_RETURNING)
        audit = mock(self.UNCAPPED, "full_audit")
        self.assertIn("analyze_waste", [r["tool"] for r in audit["related_reads"]])

    def test_the_uncapped_grader_catches_the_transcript(self):
        pattern, flags = grader(self.UNCAPPED, "no-limit-words")
        rx = re.compile(pattern, flags)
        for said in self.CLAIMS_A_LIMIT:
            with self.subTest(said=said):
                self.assertRegex(said, rx)
        for said in self.TRUE_ON_AN_UNCAPPED_PLAN:
            with self.subTest(said=said):
                self.assertNotRegex(said, rx)

    # Fix round 1: 0.2.12's first pattern failed the three true sentences
    # below that begin "Your Pro plan has no look-up limit", "There is no read
    # limit" and "Today's look-ups are unlimited", and missed "used up
    # today's quota" and "reached the cap", although the review's What breaks
    # rule names quota.
    CLAIMS_A_LIMIT = (
        "I hit today's read limit for this review before listing those "
        "searches, so that's one more look-up.",
        "I hit today’s read limit for this review before listing those "
        "searches, so that’s one more look-up.",
        "That used up today's look-ups.",
        "I've hit the review's limit, so I stopped there.",
        "That used up today's quota.",
        "I've reached the cap for this review.",
        "There's no daily limit, but I hit the review's cap.",
        "Today's read limit stopped this review before the searches.",
        # The re-run plan (2026-10-18): a negation earlier in the clause that
        # governs another verb leaves the claim a claim. The first pattern let
        # a "didn't" or "can't" anywhere before the verb pass the clause.
        "I wasn't able to read the rest because I hit today's read limit.",
        "I wasn't able to list them all before hitting the read limit.",
        "The list isn't complete because I hit the read limit.",
        "I haven't listed the rest because I hit today's read limit.",
        "I hadn't finished the searches when I hit the read limit.",
        "That wasn't everything because I ran out of today's look-ups.",
        "It isn't possible to read more today since I've reached the look-up limit.",
        "I didn't finish because I hit the read limit.",
        "I can't read more because I hit today's read limit.",
        "Nothing more is listed because I hit the read limit.",
        # The re-run plan's adversarial check: a clause that opens on a
        # negated subject still claims a limit after a joining word, and "ran
        # out of reads" and the passive claim one without a limit verb.
        "None of the remaining searches could be read after I hit the limit.",
        "Nothing else could be checked once I reached my daily cap.",
        "No more reads were possible once I hit the daily limit.",
        "I've run out of reads for today.",
        "I'm out of reads for today, so the searches will have to wait.",
        "I didn't get to the searches because the daily limit was reached.",
        "Today's quota has been used up, so I stopped there.",
        "That wasn't everything — I ran out of today's look-ups.",
        # Plan v3: the passive with "the", ran out of look-ups with no limit
        # word, and a negation ended by "because" or "as".
        "The limit was reached before I got to the searches.",
        "I ran out of look-ups before the searches.",
        "It hasn't got to the searches yet because the review reached its cap.",
        "We aren't done, as I used up today's look-ups.",
    )
    TRUE_ON_AN_UNCAPPED_PLAN = (
        "Your Pro plan has no look-up limit, so ask for as many reads as you like.",
        "There is no read limit on your plan.",
        "Today's look-ups are unlimited on Pro.",
        "Your workspace is on the Pro plan, which has no daily limit on look-ups.",
        "On your Pro plan you won't hit a daily limit.",
        "The next read would show how each campaign bids; say the word and I "
        "will run it.",
        # A campaign's budget or per-click cap is a finding, not a read limit.
        "Your campaign hit its daily budget cap on 9 of the 14 days.",
        "The campaign hit the limit of its budget by 3pm most days.",
        "Switch to Maximize Clicks with a per-click cap of ₹40.",
        # A negation that governs the verb, and a campaign as its subject
        # (review-question-first-roomy run 2 and review-account-day-named-
        # searches, 2026-10-18).
        "As of 6 October the campaign was on pace for about $1,586 this "
        "month and hadn't hit its daily limit on any day.",
        "Both campaigns are on pace and neither has hit its daily cap.",
        "Both campaigns are on pace and haven't hit their daily cap.",
        "The campaign hasn’t yet hit its cap.",
        "No campaign hit its daily limit.",
        "The campaign hit its daily limit on 3 days.",
        "It hit its $130 daily cap on 12 of the 14 days.",
        "There isn't a read limit on Pro.",
        # The re-run plan's adversarial check: a negation that governs the
        # whole clause, not only the word right before the verb.
        "Your plan has no read or look-up limit.",
        "You won't run into a read limit on Pro.",
        "You don't need to worry about a look-up limit on your plan.",
        "You never hit a read limit on Pro.",
        "You haven't hit a read limit, because Pro has none.",
        "The campaign didn't come close to hitting its cap.",
        "It never came near reaching its daily limit.",
        "It wasn't close to reaching its cap on any day.",
        # Plan v3: reassurances the v2 pattern failed (its negation had to sit
        # right before the verb or noun) and negated subjects the old one failed.
        "Nothing here was cut short by a read limit.",
        "There's no need to worry about a read limit on Pro.",
        "You won't be stopped by a read limit on Pro.",
        "Spend didn't get anywhere near hitting the daily cap.",
        "It's not at risk of hitting its daily limit this month.",
        "None of your campaigns hit their caps this month.",
        "Neither campaign reached its cap.",
    )

    def test_the_uncapped_case_keeps_the_shared_graders(self):
        text = read("evals/%s/case.yaml" % self.UNCAPPED)
        for name in ("no-change-without-a-yes", "marks-plugin-use", "skill-fired"):
            with self.subTest(grader=name):
                self.assertIn("  - name: %s\n" % name, text)
        self.assertIn("adcopilot-review", grader_block(text, "skill-fired"))
        self.assertIn("match: not_contains", grader_block(text, "no-limit-words"))
        self.assertIn("target: last_message", grader_block(text, "no-limit-words"))

    def test_the_routed_fixture_is_what_the_server_sends(self):
        ctx = mock(self.ROUTED, "get_org_context")
        self.assertEqual(ctx["plugin"]["skill"], "adcopilot-review")
        self.assertEqual(ctx["situation"], "ADS_ACTIVE_TRACKED")
        self.assertEqual(ctx["next_step"], SERVER_REVIEW_STEP + " " + SERVER_RETURNING)
        for part in ("[RAILS]", "[RECAP]", "[PLUGIN]", "adcopilot-review"):
            with self.subTest(part=part):
                self.assertIn(part, ctx["playbook"])
        say = ctx["cross_reads"]["say"]
        self.assertIn("make every read below", say)
        # v2.41.0 (#829): the demonstration is for a greeting or a request to
        # get started; anything else is answered first.
        self.assertTrue(say.startswith("On a greeting alone or a request to get "
                                       "started, "), say[:80])
        self.assertIn("Asked anything else, answer that first with only the "
                      "reads it needs, then offer the rest.", say)
        self.assertIn(SERVER_PLUGIN_SECTION.format(skill="adcopilot-review"),
                      ctx["playbook"])
        probe = next(v for k, v in ctx["ads_probe"].items() if k.isdigit())
        self.assertGreater(probe["last_30d"]["cost_micros"], 0)
        self.assertEqual(probe["last_30d"]["conversions"], 0)
        # Under the server's 50-click line an account with no result stays
        # ADS_ACTIVE_TRACKED (situations._untracked_subcase).
        self.assertLess(probe["last_30d"]["clicks"], 50)

    def test_the_routed_prompt(self):
        text = read("evals/%s/case.yaml" % self.ROUTED)
        self.assertIn('  prompt: "I have the AdCopilot plugin. Please walk me '
                      'through what it can do."\n', text)

    def test_the_routed_case_reads_nothing_and_starts_nothing(self):
        text = read("evals/%s/case.yaml" % self.ROUTED)
        blocks = re.split(r"\n  - name: ", text)[1:]

        def never(tool, needle=None):
            for block in blocks:
                if (re.search(r"^\s+type: tool_used\s*$", block, re.M)
                        and re.search(r"^\s+tool: %s\s*$" % re.escape(tool), block, re.M)
                        and (needle is None or needle in block)
                        and re.search(r"^\s+max: 0\s*$", block, re.M)
                        and re.search(r"^\s+min: 0\s*$", block, re.M)):
                    return True
            return False

        for tool in ("full_audit", "analyze_waste", "analyze_search_terms",
                     "search", "conversion_setup_audit"):
            with self.subTest(tool=tool):
                self.assertTrue(never(self.MCP + tool), tool)
        self.assertTrue(never("Skill", "adcopilot-review"))
        fired = grader_block(text, "skill-fired")
        self.assertIn("adcopilot-docs", fired)
        for name in DocsJudgeReplay.ITEMS[self.ROUTED]:
            with self.subTest(grader=name):
                self.assertIn("type: llm", grader_block(text, name))
        self.assertIn("Exactly one question",
                      grader_block(text, "one-closing-question"))

    def test_the_routed_approval_grader(self):
        pattern, flags = grader(self.ROUTED, "no-approval-promise-without-its-condition")
        rx = re.compile(pattern, flags)
        for said in ("Fix and improve your campaigns (every change waits for "
                     "your yes): block wasted searches.",
                     "Through it I can read your accounts freely, and I can make "
                     "changes only after you approve each one.",
                     "Nothing changes without your approval: every change waits "
                     "for your yes. It is on claude.ai, too."):
            with self.subTest(said=said):
                self.assertRegex(said, rx)
        for said in ("Every change waits for your yes, as long as AdCopilot's "
                     "write tools stay on 'Needs approval' in your Claude settings.",
                     "Your AI client asks before each change while the write tools "
                     "stay on Needs approval in claude.ai, and every change waits "
                     "for your yes.",
                     "Nothing can be deleted except a negative keyword."):
            with self.subTest(said=said):
                self.assertNotRegex(said, rx)


class OlderFixturesOnV241(unittest.TestCase):
    """The Cursor round re-renders the older cases' get_org_context answers
    with release/v2.41.0's own code (967d743b), as the five 0.2.12 fixtures
    were: situations.classify on each fixture's own data, plugin_skill,
    next_step, render_playbook, cross_reads, question_map,
    schedule_recipe.as_data and tools_adcopilot._hints. setup-signed-out's
    answer is the client's sign-in error, not a server answer, and the
    suite-wide evals/mocks fixture is left as it is."""

    CASES = ("audit-stale-tools", "daily-scheduled-run", "habit-offer-chat",
             "habit-offer-code", "habit-offer-untold",
             "habit-recorded-stays-quiet", "launch-manual-settings",
             "launch-unserved-campaign", "measure-import-trap",
             "measure-teaches", "review-follows-related-reads",
             "review-spends-the-depth", "seo-discovered-is-not-a-verdict",
             "seo-two-numbers-that-lie")
    OFFER = {"habit-offer-chat": "claude", "habit-offer-code": "claude_code",
             "habit-offer-untold": "both", "audit-stale-tools": "claude_code",
             "measure-import-trap": "claude_code"}

    def ctx(self, case):
        text = read("evals/%s/mocks/adcopilot/get_org_context.md" % case)
        if case == "audit-stale-tools":
            return json.loads(re.search(r"\n\n(\{\"org\".*?\})\n\n", text, re.S).group(1))
        return mock(case, "get_org_context")

    def test_each_is_v241s_rendering(self):
        for case in self.CASES:
            with self.subTest(case=case):
                text = read("evals/%s/mocks/adcopilot/get_org_context.md" % case)
                head = re.match(r"^---\n(.*?)\n---\n", text, re.S).group(1)
                self.assertIn("Re-rendered with AdCopilot release/v2.41.0's own "
                              "code (967d743b", " ".join(head.replace("#", " ").split()))
                ctx = self.ctx(case)
                self.assertNotIn("focus", ctx["overlays"])
                for key in ("schedule_offer", "quota_sized", "plugin_offer",
                            "checkin_later", "site_health"):
                    self.assertIn(key, ctx["overlays"])
                if case == "daily-scheduled-run":
                    self.assertNotIn("plugin", ctx)
                else:
                    self.assertEqual(ctx["plugin"]["version"], manifest_version())
                for acct in (k for k in ctx["ads_probe"] if k.isdigit()):
                    last = ctx["ads_probe"][acct]["last_30d"]
                    self.assertRegex(last["start_date"], r"^\d{4}-\d\d-\d\d$")
                    self.assertRegex(last["end_date"], r"^\d{4}-\d\d-\d\d$")
                    self.assertIn("cost_micros", last)
                routine = ctx["routine"]
                for key in ("scheduled_first_seen_at", "scheduled_last_seen_at",
                            "own_schedule", "own_schedule_at"):
                    self.assertIn(key, routine)

    def test_each_header_names_the_values_changed(self):
        # The re-render set routine.weekly.status from off to skipped in five
        # fixtures and added a first scheduled sighting to one; each header
        # says so, and the others change nothing in their data.
        weekly = ("habit-recorded-stays-quiet", "review-follows-related-reads",
                  "review-spends-the-depth", "seo-discovered-is-not-a-verdict",
                  "seo-two-numbers-that-lie")
        for case in self.CASES:
            text = read("evals/%s/mocks/adcopilot/get_org_context.md" % case)
            head = re.match(r"^---\n(.*?)\n---\n", text, re.S).group(1)
            head = " ".join(head.replace("#", " ").split())
            with self.subTest(case=case):
                said = ("routine.weekly.status is skipped (it was off), so that "
                        "next_step asks for no routine offer")
                self.assertEqual(said in head, case in weekly)
                if case in weekly:
                    self.assertEqual(self.ctx(case)["routine"]["weekly"]["status"],
                                     "skipped")
                first = ("routine.scheduled_first_seen_at is 2026-09-22 12:07:40 "
                         "(it was absent), a day before scheduled_last_seen_at")
                self.assertEqual(first in head,
                                 case == "habit-recorded-stays-quiet")
                self.assertEqual("changed rather than carried over" in head,
                                 case in weekly)

    def test_routine_schedule_is_there_exactly_when_the_offer_is(self):
        for case in self.CASES:
            with self.subTest(case=case):
                ctx = self.ctx(case)
                offer = ctx["overlays"]["schedule_offer"]
                self.assertEqual(offer, self.OFFER.get(case))
                if offer:
                    self.assertEqual(ctx["routine"]["schedule"]["offer"], offer)
                    self.assertEqual(ctx["routine"]["schedule"]["instructions"],
                                     SCHEDULED_CHECKIN_V241.format(
                                         account="Google Ads account 123-456-7890"))
                else:
                    self.assertNotIn("schedule", ctx["routine"])

    def test_the_habit_cases_say_where_they_are_as_v241_does(self):
        self.assertEqual(self.ctx("habit-offer-untold")["surface"], "other")
        for case in ("habit-offer-chat", "habit-offer-code"):
            self.assertEqual(self.ctx(case)["surface"], "claude")
        quiet = self.ctx("habit-recorded-stays-quiet")["routine"]
        self.assertNotEqual(quiet["scheduled_first_seen_at"][:10],
                            quiet["scheduled_last_seen_at"][:10])
        # On a turn a skill owns, v2.41.0 leaves the offer to the skill.
        for case in ("habit-offer-chat", "habit-offer-code", "habit-offer-untold"):
            self.assertNotIn("Before you finish, offer", self.ctx(case)["next_step"])

    def test_no_call_log_grader_is_decided_by_the_fixture_alone(self):
        # mock_calls carries every mocked call's output too, so a grader that
        # matches a tool's NAME would be decided by the playbook's or
        # question_map's text. The call-log graders are anchored on the
        # call's own "tool".
        for case in self.CASES + ("review-uncapped-no-limit-words",
                                  "review-question-first-roomy",
                                  "docs-capabilities-untracked",
                                  "docs-capabilities-routed",
                                  "review-account-day-named-searches"):
            text = read("evals/%s/mocks/adcopilot/get_org_context.md" % case)
            output = re.match(r"^---\n.*?\n---\n(.*)$", text, re.S).group(1)
            record = json.dumps({"tool": "mcp__plugin_adcopilot_adcopilot__get_org_context",
                                 "input": {"source": "claude-plugin/%s" % manifest_version()},
                                 "output": output}, separators=(",", ":"),
                                ensure_ascii=False)
            case_text = read("evals/%s/case.yaml" % case)
            for block in re.split(r"\n  - name: ", case_text)[1:]:
                name = block.split("\n", 1)[0]
                if not (re.search(r"^\s+type: regex\s*$", block, re.M)
                        and re.search(r"^\s+target: mock_calls\s*$", block, re.M)):
                    continue
                if name == "read-the-server-first":
                    continue
                plain = re.search(r"^\s+pattern: ([^'\s][^\n]*?)\s*$", block, re.M)
                if plain:
                    pattern = plain.group(1)
                    flags = re.I if re.search(r"^\s+flags: i\s*$", block, re.M) else 0
                else:
                    pattern, flags = grader(case, name)
                with self.subTest(case=case, grader=name):
                    self.assertIsNone(re.search(pattern, record, flags))


if __name__ == "__main__":
    unittest.main()
