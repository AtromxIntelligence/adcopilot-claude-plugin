"""The daily-habit block, identical wherever it appears, and the server's own stop condition.

One of the structural test files that `tests/test_structure.py` was split
into in 0.2.15. At 273 KB that file was over the plugin directory's 256 KiB
limit for a file that is not an image or a font. The tests moved verbatim, by
topic (same classes, same names, same assertions), and the helpers they share
live in `structure_helpers.py`; `tests/test_plugin_size.py` keeps any file
from growing past the limit again.

Run with `python3 -m unittest discover -s tests -v` from the repository root
(stdlib only; CI runs it in checks.yml).

What it pins, and why each one is here:
- The daily-habit block. Every interactive flow — the three teaching skills,
  the fix-checks skill and the four commands that have no skill of their
  own — ends with the same
  offer to make the check a daily habit. It is repeated verbatim, like the
  teaching contract, because a skill cannot include another file in every
  surface the plugin runs on (an eval run has no Read tool at all). A copy
  that drifts is a flow that offers differently, or stops offering, so the
  copies are compared byte for byte.
- The stop condition is the server's own (`situations.schedule_offer`):
  `routine.daily.status` `user_set`, a scheduled run seen on two different
  days (`routine.scheduled_first_seen_at` and
  `routine.scheduled_last_seen_at`), or `routine.own_schedule` `saved`,
  `unavailable` or `declined` (plan B9, D160), and nothing else. If AdCopilot renames a field the
  offer never stops; if the plugin stops on more than the server does, the
  plugin is silent while the server's next_step asks for the offer; if it
  stops on less, a Claude with no scheduled tasks is offered one every
  conversation after AdCopilot has recorded that it cannot.
- Directory policy (plan D7). Nothing the model is told by the habit block or
  the run carries sales or upgrade wording.

- The offer at the first value (0.2.11): right after the first finding the
  morning check also reads, tied to it, with the value line; for any other
  finding, or none, the reply closes without claiming the check would have
  caught anything. A no is asked about once, and a not-now is recorded too.
"""

import os
import sys
import re
import unittest

# The helpers sit beside this file; the path is set so this file also runs
# on its own (`python3 tests/test_daily_habit.py`).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from structure_helpers import (  # noqa: E402
    DELEGATING_COMMANDS,
    HABIT_CARRIERS,
    HABIT_HEADING,
    OFFER_CHAT,
    OFFER_CODE,
    ROOT,
    SALES,
    SCHEDULED_CHECKIN,
    read,
    section,
)


# The first sentence of an offer made at the close, for a finding the morning
# check does not read or none: it does not say the check would have caught
# anything.
OFFER_CLOSE_FIRST = ("A read-only check that runs by itself every weekday at 8:07 "
                     "can look over this account for you each morning, opening "
                     "with \"All clear\" or \"Needs a look\" plus one yes/no fix.")


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
                      "`routine.scheduled_first_seen_at`",
                      "`routine.scheduled_last_seen_at`", "`in_app`",
                      "`routine.own_schedule` is `saved`, `unavailable` or "
                      "`declined`"):
            with self.subTest(field=field):
                self.assertIn(field, block)

    def test_stop_condition_is_no_wider_than_the_servers(self):
        # situations.schedule_offer stops on user_set or a scheduled run seen,
        # never on a row's surface: a row switched off keeps surface
        # claude_scheduled, and Recipe A writes a weekly-only one. Stopping on
        # surface leaves the plugin silent while next_step asks for the offer.
        # (The answer's TOP-LEVEL `surface`, `cursor` for a Cursor connection,
        # is the Cursor tell, not a stop condition.)
        block = self.blocks()[HABIT_CARRIERS[0]] or ""
        self.assertNotIn("claude_scheduled", block)
        self.assertNotIn("routine.daily.surface", block)
        self.assertNotIn("`surface` `", block)
        self.assertIn("`get_org_context`'s top-level `surface` is `cursor`", block)

    def test_the_offer_follows_the_servers_decision_for_the_client(self):
        # 0.2.12 Cursor round: the offer is made only when get_org_context
        # hands over `routine.schedule`, which v2.41.0 sets exactly when
        # classify's `overlays.schedule_offer` is set
        # (tools_adcopilot.get_org_context; schedule_recipe.offer_for gives
        # None for any named client that is not Claude, Cursor included).
        # The plugin no longer decides from the routine fields alone.
        block = " ".join((self.blocks()[HABIT_CARRIERS[0]] or "").split())
        self.assertIn("and only when both hold: Google Ads is connected and "
                      "readable with a campaign switched on, and "
                      "`get_org_context` hands you its recipe, "
                      "`routine.schedule`.", block)
        self.assertIn("AdCopilot sends `routine.schedule` only when its "
                      "`overlays.schedule_offer` is set, which is its own "
                      "decision for this workspace and this AI client: no "
                      "schedule is reported, the call is not a scheduled run",
                      block)
        # situations.schedule_offer believes a scheduled run only once it has
        # been seen on two separate UTC days (_seen_on_two_days); one sighting
        # can be a chat that ran the pasted request instead of saving it.
        self.assertIn("when a scheduled run has checked in on two different "
                      "days (`routine.scheduled_first_seen_at` and "
                      "`routine.scheduled_last_seen_at` hold dates on different "
                      "days)", block)
        self.assertNotIn("`routine.scheduled_last_seen_at` holds a date", block)
        self.assertNotIn("sends it exactly when", block)
        self.assertIn("Never make the offer without it, and never work it out "
                      "from the other fields.", block)
        self.assertIn("Word it for where they are, by `routine.schedule.offer`: "
                      "`claude_code` is Claude Code, and `claude` is the Claude "
                      "app. `both` means AdCopilot could not tell which Claude "
                      "this is", block)
        # The values the block names are the server's own
        # (schedule_recipe.OFFERS).
        for value in ("claude", "claude_code", "both"):
            self.assertIn("`%s`" % value, block)

    def test_offered_only_for_a_running_account(self):
        # The server offers only in ADS_ACTIVE_* situations: a campaign that
        # is switched on. /launch ends on a campaign built paused.
        block = self.blocks()[HABIT_CARRIERS[0]] or ""
        self.assertIn("a campaign switched on", block)

    def test_each_offer_is_two_sentences_and_no_steps(self):
        # habit-offer-code/-untold, 2026-10-18 (plan v4): every judge vote failed
        # "one or two sentences" on the old wording, which the model wrote as
        # three ("...fix. Say \"schedule it\" and I'll...") or as two joined by
        # a semicolon, 57 to 60 words in all. Two plain sentences: the value
        # line, then the offer; with "read-only" for "only reads the account and
        # never changes anything" the value line is 32 words and the whole
        # offer 48 (Claude Code) or 51 (the Claude app). On plan v5's run
        # (2026-10-18 22:44Z) that offer passed item 4 where it stood as its own
        # paragraph, by 2 votes of 3 on each run, and failed it where it was
        # added to the end of the searches' paragraph. Plan v6 changes where it
        # stands, not its length: these limits hold the length that passed.
        for offer in (OFFER_CHAT, OFFER_CODE):
            with self.subTest(offer=offer[-40:]):
                self.assertNotIn(";", offer)
                self.assertEqual(len(re.findall(r"[.!?](?=\s|$)", offer.replace("8:07", "8h07"))), 2)
                self.assertTrue(offer.split(". ")[-1].startswith("If you say \"schedule it\", I'll "))
                self.assertLessEqual(len(offer.split(". ")[0].split()), 32)
                self.assertLessEqual(len(offer.split()), 51)
        self.assertNotIn(";", OFFER_CLOSE_FIRST)
        self.assertLessEqual(len(OFFER_CLOSE_FIRST.split()), 32)
        self.assertIn("two sentences, never split into more, and no set-up step before a yes",
                      " ".join((self.blocks()[HABIT_CARRIERS[0]] or "").split()))

    def test_the_offer_is_its_own_paragraph(self):
        # habit-offer-untold, 2026-10-18 22:44Z (plan v5): both runs added the
        # offer to the end of the searches' paragraph ("That's people looking
        # for work, freebies and how-to guides. A read-only check ...") and
        # failed "one or two sentences"; habit-offer-code's runs gave the same
        # offer a paragraph of its own and passed it. The block, the review
        # skill and the README say it is always its own paragraph.
        block = " ".join((self.blocks()[HABIT_CARRIERS[0]] or "").split())
        # 0.2.14: it follows the read-back of an applied fix, not a finding.
        self.assertIn("The offer is always its own paragraph, with a blank line "
                      "before and after it: it goes right after the read-back "
                      "(and any line that sums the fixes up), never on the end of "
                      "one of its sentences and never inside one of its "
                      "bullets.", block)
        self.assertIn("nothing else changed: a paragraph of its own, two "
                      "sentences, never split into more", block)
        # It sits between where the offer goes and what the close does, so it
        # covers both.
        self.assertLess(block.index("would have caught it on its first morning. "
                                    "The offer is always its own paragraph"),
                        block.index("For any other finding"))
        nxt = " ".join((section(read("skills/adcopilot-review/SKILL.md"),
                                "## What is next") or "").split())
        self.assertIn("Either way the offer is its own paragraph, with a blank "
                      "line before and after it, never on the end of a finding's "
                      "sentences and never inside a bullet.", nxt)
        readme = " ".join(read("README.md").split())
        self.assertIn("The offer comes, as a paragraph of its own, only in a "
                      "reply that asks you no yes/no on a fix", readme)

    def test_a_declined_first_fix_still_gets_the_offer_at_the_close(self):
        # 0.2.17 (AdCopilot's trial-return plan, #1): a first session whose
        # first fix for a finding the morning check reads was declined or
        # left for later ended with no next appointment. The same sentence
        # in every carrier and in the review skill's own paragraph, after
        # the paragraph rule and before the other-finding close.
        clause = ("If they decline the first fix for a finding the morning "
                  "check also reads, or put it off, make the offer at the "
                  "close of that reply instead, tied to that finding the same "
                  "way (before any question the reply ends on).")
        block = " ".join((self.blocks()[HABIT_CARRIERS[0]] or "").split())
        self.assertIn(clause, block)
        self.assertLess(block.index("never inside one of its bullets."),
                        block.index(clause))
        self.assertLess(block.index(clause), block.index("For any other finding"))
        review = " ".join((section(read("skills/adcopilot-review/SKILL.md"),
                                   "## What is next") or "").split())
        self.assertIn(clause, review)
        self.assertIsNone(SALES.search(clause))

    def test_the_finding_in_the_braces_is_kept_short(self):
        # The value line is 32 words before the finding; a long finding would
        # make the offer the long paragraph the judges fail.
        block = " ".join((self.blocks()[HABIT_CARRIERS[0]] or "").split())
        self.assertIn("with the finding in the braces kept short (a figure and a "
                      "noun) and nothing else changed", block)

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


class DailyHabitAtTheFirstValue(unittest.TestCase):
    """0.2.11: the offer comes right after the first finding the morning check
    ALSO READS, tied to it, with the value line; for any other finding, even a
    costly one, or none, it closes the reply without claiming the check would
    have caught anything. A no is asked about once, so that a Claude with no
    scheduled tasks is recorded, and a not-now is recorded too."""

    # The founder's rule for anything the model is told: no plan, price or
    # limit word. Stricter than SALES, which only the habit block and the run
    # were held to before.
    PLAN_PRICE_LIMIT = re.compile(
        r"\b(plans?|pric\w+|limits?|caps?|free|upgrade[sd]?|subscri\w+|trial|"
        r"discount\w*|buy|purchase\w*|starter|tier)\b|[$\u20ac\u00a3\u20b9]\s?\d", re.I)

    # What the morning check reads (SCHEDULED_CHECKIN above), and the findings
    # the offer may be tied to: each is a line of the check, so "would have
    # caught it" is true of every one.
    CHECK_READS = (
        ("searches that spent with no sale", "search terms from the last 7 days that cost the most with no conversions"),
        ("a campaign out of budget or off its budget pace", "budget pacing"),
        ("a disapproved ad", "Any ad that is disapproved or limited"),
        ("a drop against the 7-day average", "against my 7-day average"),
        ("a change nobody asked for", "Any change made in the account in the last 24 hours"),
    )
    # Costly, and not read by the check: the offer is made at the close.
    NOT_READ = ("a tracking fault", "a Quality Score problem", "a targeting problem")

    def block(self):
        return " ".join((section(read(HABIT_CARRIERS[0]), HABIT_HEADING) or "").split())

    def test_the_offer_waits_for_a_fix_applied_and_read_back(self):
        # 0.2.14 (the 2026-10-20 "Fix all three" chat): the offer came after
        # the first of three checks, beside its yes/no, and the day ran out
        # before any fix. It is made only in a reply that asks no yes/no on a
        # fix: after a fix applied and read back with no next fix proposed,
        # or at the close of a reply that proposes none.
        block = self.block()
        # Review of AdCopilot #942 (item 4): "only once no next fix is
        # proposed" was reached only with nothing left to fix, and on Free the
        # limit comes first. The first fix's read-back makes the offer in
        # place of the next fix's yes/no, and that yes/no waits a reply.
        self.assertIn("Make it in a reply that asks them no yes/no on a fix: "
                      "the reply that reads back the first fix they approved, "
                      "where the offer stands in for the next fix's yes/no "
                      "(name the next fix in one line without asking, and "
                      "propose it in the reply after), or the close of a reply "
                      "that proposes no fix at all.", block)
        self.assertNotIn("the reply proposes no next fix", block)
        # AdCopilot D254 (founder 2026-10-28): the morning check makes all
        # five reads on Free too, so no finding is left for the chat.
        self.assertIn("without saying the check would have caught it.", block)
        self.assertNotIn("leaves what changed for the chat", block)
        self.assertIn("Never make it beside a fix that waits for their answer: "
                      "the yes/no comes first, and the offer waits.", block)
        self.assertIn("When a fix applied in this conversation was for a "
                      "finding the morning check also reads", block)
        self.assertIn("tie it to that finding, with the figure you read "
                      "and never one you did not", block)
        # The 0.2.11 moment, right after the first finding, is gone.
        self.assertNotIn("Make it right after the first finding", block)
        # The old rule promised the check would catch ANY finding with a cost.
        self.assertNotIn("puts a cost or a loss on", block)
        # The old rules put it at the end of every reply.
        self.assertNotIn("the last line of the reply, at most once", block)
        self.assertNotIn("After the value is delivered", block)

    def test_every_finding_it_names_is_one_the_morning_check_reads(self):
        block = self.block()
        for finding, line in self.CHECK_READS:
            with self.subTest(finding=finding):
                self.assertIn(finding, block)
                self.assertIn(line, " ".join(SCHEDULED_CHECKIN.split()))
        named = block.split("the morning check also reads \u2014 ")[1].split(" \u2014 tie it")[0]
        self.assertEqual([p.strip() for p in named.split(",")],
                         [f for f, _l in self.CHECK_READS])

    def test_a_finding_the_check_does_not_read_gets_the_close_without_the_claim(self):
        block = self.block()
        self.assertIn("For any other finding, even one that costs money (%s), or "
                      "none, close the reply with the offer instead" % ", ".join(self.NOT_READ), block)
        self.assertIn("without saying the check would have caught it", block)
        # The three are not among the findings the offer is tied to.
        head = block.split("For any other finding")[0]
        for unread in self.NOT_READ:
            self.assertNotIn(unread, head)
        # The closing words carry no claim; the others do.
        self.assertIn(OFFER_CLOSE_FIRST, block)
        self.assertNotIn("caught", OFFER_CLOSE_FIRST)
        self.assertIn("the third line is for the close", block)
        for offer in (OFFER_CHAT, OFFER_CODE):
            self.assertIn("would have caught {the finding}", offer)

    def test_the_two_rules_for_a_reply_that_ends_on_a_question_agree(self):
        # D160 review: "close the reply with the offer, as its last line" and
        # "any question the reply ends on stays the last thing in it, and the
        # offer comes before that question" could not both hold. The offer
        # comes before the question, whichever way it is made.
        block = self.block()
        self.assertIn("close the reply with the offer instead (before any "
                      "question the reply ends on)", block)
        self.assertNotIn("as its last line", block)
        self.assertNotIn("the last line", block)

    def test_both_offers_carry_the_value_line(self):
        for offer in (OFFER_CHAT, OFFER_CODE):
            with self.subTest(offer=offer[-50:]):
                for piece in ("A read-only check that runs by itself every weekday "
                              "at 8:07 would have caught {the finding} on its first "
                              "morning,",
                              "opening with \"All clear\" or \"Needs a look\" "
                              "plus one yes/no fix."):
                    self.assertIn(piece, offer)
        self.assertIn("with the finding in the braces", self.block())

    def test_the_public_files_carry_no_internal_decision_tag(self):
        # The README, the skills, the commands, the agent and the manifests are
        # a public repository's text. AdCopilot's decision numbers and the
        # founder's say-so are its own records (the test comments may keep
        # them); the 0.2.11 note named both and was reworded (D160 review).
        public = ["README.md", ".claude-plugin/plugin.json",
                  ".claude-plugin/marketplace.json"]
        for sub in ("skills", "commands", "agents"):
            base = os.path.join(ROOT, sub)
            for dirpath, _dirs, names in os.walk(base):
                for name in sorted(names):
                    if name.endswith(".md"):
                        public.append(os.path.relpath(
                            os.path.join(dirpath, name), ROOT))
        tag = re.compile(r"\bD\d{2,3}\b|\b[Dd]ecisions? D\d+|the founder approved")
        for rel in public:
            with self.subTest(file=rel):
                found = tag.search(read(rel))
                self.assertIsNone(found, found and found.group(0))

    def test_the_readme_says_the_same_trigger_and_the_release_order(self):
        readme = " ".join(read("README.md").split())
        # 0.2.14: the moment is after a fix applied and read back.
        morning = " ".join((section(read("README.md"),
                                    "### Every morning, without asking") or "").split())
        # Review of AdCopilot #942 (item 4): the first fix's read-back.
        self.assertIn("only in a reply that asks you no yes/no on a fix: the "
                      "reply that reads back the first fix you approved, where "
                      "it stands in for the next fix's yes/no (the next fix is "
                      "named, and proposed in the reply after), or at the close "
                      "of a reply that proposes none. When that fix was for a "
                      "finding the morning check also reads", morning)
        self.assertNotIn("no next fix is proposed", morning)
        # AdCopilot D254: the morning check makes its five reads on every
        # plan, so no plan's check leaves what changed for the chat.
        self.assertNotIn("leaves what changed for the chat", morning)
        self.assertNotIn("except on Free's 10 a day", morning)
        self.assertNotIn("right after the first finding", morning)
        self.assertIn("With any other finding, or none, the offer closes the "
                      "reply instead, without that claim.", readme)
        self.assertNotIn("puts a cost or a loss on", readme)
        self.assertNotIn("is still the reply's last line", readme)
        self.assertIn("**Release order:** this version is written against the "
                      "AdCopilot build that accepts `declined`; on an older "
                      "server that call is rejected by name, so the server is "
                      "released first.", readme)

    def test_a_no_asks_once_and_records_the_answer(self):
        block = self.block()
        self.assertIn("A no ends it for this conversation: ask once whether "
                      "their Claude can create scheduled tasks, and call "
                      "`save_org_context` with `routine.own_schedule` "
                      "`unavailable` if it cannot, else `declined`.", block)

    def test_a_decline_stops_the_offer_for_the_servers_week(self):
        block = self.block()
        self.assertIn("once they said not now, which holds the offer for a week "
                      "and then lets it come back", block)
        # The server shows `declined` for that week only, so the plugin does
        # no date arithmetic.
        self.assertNotIn("own_schedule_at", block)

    def test_the_question_the_reply_ends_on_stays_last(self):
        # The offer is a statement ("say \"schedule it\""), so a reply
        # never carries two questions, and it sits before the one it ends on.
        self.assertIn("any question the reply ends on stays the last thing in "
                      "it, and the offer comes before that question", self.block())

    def test_nothing_the_model_is_told_names_a_plan_a_price_or_a_limit(self):
        for rel in HABIT_CARRIERS:
            with self.subTest(file=rel):
                blk = " ".join((section(read(rel), HABIT_HEADING) or "").split())
                found = self.PLAN_PRICE_LIMIT.search(blk)
                self.assertIsNone(found, found and found.group(0))
        daily = " ".join(read("skills/adcopilot-daily/SKILL.md").split())
        cost = re.search(r"Say what it costs before they save it:[^.]*\.", daily)
        self.assertIsNotNone(cost)
        self.assertIsNone(self.PLAN_PRICE_LIMIT.search(cost.group(0)), cost.group(0))

    def test_the_review_skill_words_it_the_same_way(self):
        nxt = " ".join((section(read("skills/adcopilot-review/SKILL.md"),
                                "## What is next") or "").split())
        self.assertIn("Its moment is a reply that asks them no yes/no on a fix: "
                      "the reply that reads back the first fix they approved, "
                      "where it stands in for the next fix's yes/no (name the "
                      "next fix in one line without asking, and propose it in "
                      "the reply after), or the close of a reply that proposes "
                      "none. Never beside a fix that waits for their answer. "
                      "When a fix applied in this conversation was for a "
                      "finding the morning check also reads", nxt)
        self.assertNotIn("leaves what changed for the chat", nxt)   # D254
        self.assertIn("for any other finding, even one that costs money (a "
                      "tracking fault, a Quality Score problem, a targeting "
                      "problem), or none, the close, before any question the "
                      "reply ends on, without saying the check would have "
                      "caught it", nxt)
        self.assertNotIn("puts a cost or a loss on", nxt)
        self.assertIn("ask once whether their Claude can create scheduled "
                      "tasks, and record `routine.own_schedule` `unavailable` "
                      "if it cannot, else `declined`", nxt)
        self.assertNotIn("the last line of the reply", nxt)
        self.assertIsNone(self.PLAN_PRICE_LIMIT.search(nxt))

    def test_a_run_costs_about_six_or_seven_reads_not_five(self):
        daily = " ".join(read("skills/adcopilot-daily/SKILL.md").split())
        self.assertIn("A run is about six or seven reads, each counted toward "
                      "the workspace's daily operations", daily)
        # AdCopilot D254: what a run counts, and nothing about whether the
        # day can hold it.
        self.assertIn("Say what it costs before they save it: about six or seven "
                      "reads a run, each counted toward the workspace's daily "
                      "operations.", daily)
        self.assertNotIn("can use the whole day's", daily)
        readme = " ".join(read("README.md").split())
        self.assertIn("A run reads about six or seven times, and each read "
                      "counts toward your workspace's daily operations.",
                      readme)
        self.assertNotIn("can use all of a Free workspace's 10", readme)

    def test_free_counts_in_weighted_operations(self):
        # AdCopilot v2.43.1 (D164, "Back for Free"): on Free a full audit or
        # an account health score counts 4 operations, an analysis 2 and a
        # single read 1; a paid plan and a running trial count every call 1.
        daily = " ".join(read("skills/adcopilot-daily/SKILL.md").split())
        # The run's own section names no plan to buy (`SALES`), so it says
        # "otherwise" where the set-up and the README name who counts 1.
        # AdCopilot D254 (founder 2026-10-28): every read on Free too; a run
        # that meets the limit passes the refusal's plan line on.
        # AdCopilot D254: what a run counts, never set against the day's
        # total (the server's run cost dropped "can use them all").
        self.assertIn("so the five reads would count 7 and a run about 8 to 10; "
                      "otherwise every read counts 1. If they "
                      "run out, say which reads were not reached, then the "
                      "plan line the refusal gives, word for word.", daily)
        self.assertNotIn("of Free's 10", daily)
        self.assertNotIn("make the first four reads only", daily)
        self.assertNotIn("the four count 6 of the 10", daily)
        # A trial held to Free's 10 a day (paused for its card, or waiting
        # for its first charge) is weighted while its `plan` still reads
        # `pro`, so the skill keys the cost on the server's own answer,
        # `org.ops_weighted` (AdCopilot v2.43.1), never on `plan`.
        self.assertIn("Where its `org.ops_weighted` is true (a workspace on "
                      "Free's 10 a day), an analysis counts 2 operations", daily)
        self.assertIn("Where `get_org_context`'s `org.ops_weighted` is true "
                      "(Free, and a trial held to Free's 10 a day, whose "
                      "`plan` still reads `pro`), say it in operations "
                      "instead: an analysis counts 2 there, so a run is about "
                      "8 to 10 operations.", daily)
        self.assertNotIn("`plan` is `free`", daily)
        readme = " ".join(read("README.md").split())
        self.assertIn("On Free, and on a trial held to Free's 10 a day, an "
                      "analysis such as budget pacing counts 2 operations and "
                      "a single read 1, so a run comes to about 8 to 10 "
                      "operations. On a paid plan or a running trial "
                      "every read counts 1.", readme)
        # The version notes keep what 0.2.14 shipped; everything above them
        # is what 0.2.17 says now.
        notes = " ".join((section(read("README.md"), "## AdCopilot version")
                          or "").split())
        self.assertIn("first four reads only", notes)
        self.assertNotIn("first four reads only", readme.replace(notes, ""))
        audit = " ".join(read("commands/audit.md").split())
        # AdCopilot D254 (founder 2026-10-28): no arithmetic of the day to
        # economise against; a refusal's own words and plan line instead.
        self.assertNotIn("6 of Free's 10", audit)
        self.assertIn("When a call is refused because it counts more than is "
                      "left today, say what the refusal says, the lighter "
                      "reads it names included, and the plan line it gives, "
                      "word for word", audit)
        # AdCopilot D254: the command never sizes a read itself; it runs
        # budget pacing and lets a refusal say whether it fits.
        self.assertNotIn("if it fits", audit)
        self.assertIn("then run `budget_pacing`; if it is refused too, pass "
                      "on that refusal's line instead.", audit)
        weekly = " ".join(read("commands/weekly.md").split())
        self.assertNotIn("5 or 6 of Free's 10", weekly)
        self.assertIn("Each read counts toward the workspace's daily "
                      "operations. When a call is refused at the daily limit, "
                      "say what it found first, then the plan line the "
                      "refusal gives, word for word, with the reset.", weekly)
        for rel, text in (("skills/adcopilot-daily/SKILL.md", daily),
                          ("README.md", readme), ("commands/audit.md", audit),
                          ("commands/weekly.md", weekly)):
            # Never the everyone switch's words: paid plans count 1 per call.
            self.assertNotIn("on every plan a full audit counts", text, rel)
        for rel in ("skills/adcopilot-daily/SKILL.md", "README.md"):
            text = " ".join(read(rel).split())
            self.assertNotIn("about five reads", text, rel)
            self.assertNotIn("reads about five times", text, rel)

    def test_the_five_numbered_reads_are_still_five(self):
        # The recipe has five lines; it is their COST that is six or seven.
        daily = read("skills/adcopilot-daily/SKILL.md")
        self.assertIn("Five reads, in this order", daily)


if __name__ == "__main__":
    unittest.main()
