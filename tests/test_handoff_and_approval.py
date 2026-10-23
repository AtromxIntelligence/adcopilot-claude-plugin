"""The hand-off to AdCopilot v2.41.0's steps, the approval wording and the Cursor path.

One of the structural test files that `tests/test_structure.py` was split
into in 0.2.15. At 273 KB that file was over the plugin directory's 256 KiB
limit for a file that is not an image or a font. The tests moved verbatim, by
topic (same classes, same names, same assertions), and the helpers they share
live in `structure_helpers.py`; `tests/test_plugin_size.py` keeps any file
from growing past the limit again.

Run with `python3 -m unittest discover -s tests -v` from the repository root
(stdlib only; CI runs it in checks.yml).

What it pins, and why each one is here:
- Cursor (0.2.12's Cursor round): wherever the plugin works out which client
  it is in, Cursor is checked first, `claude mcp` is never run there, and the
  connector may be named `server`; the daily-habit offer is made only when
  get_org_context hands over `routine.schedule` (AdCopilot's own decision for
  the client) and a no is recorded only from Claude, and in Cursor the plugin
  makes the check-in offer next_step asks for instead of one of its own;
  every command says what to do without its skill, and the four that send
  the versioned marker send the bare one there, so the server never hands
  the turn to a skill that is not installed; /adcopilot:audit gives Cursor's
  refresh for a stale tool list first; and one approval sentence serves every
  client, its Cursor half naming the Allowlist run mode.

- AdCopilot v2.41.0 alignment (0.2.12): the plugin's text and its newest eval
  fixtures say what that release does, including the hand-off to the skill
  that owns the turn.
- No surface promises that a change waits for a yes without the condition
  that makes it true (0.2.12), and one approval sentence serves every AI
  client.
"""

import os
import sys
import json
import re
import unittest

# The helpers sit beside this file; the path is set so this file also runs
# on its own (`python3 tests/test_handoff_and_approval.py`).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from structure_helpers import (  # noqa: E402
    COMMANDS,
    DELEGATING_COMMANDS,
    HABIT_CARRIERS,
    HABIT_HEADING,
    NO_SKILLS,
    SERVER_MEASURE_STEP,
    SERVER_RETURNING,
    SERVER_REVIEW_STEP,
    flat,
    frontmatter,
    grader,
    grader_block,
    mock,
    model_read_files,
    never_grader,
    read,
    section,
)


class ApprovalCondition(unittest.TestCase):
    """0.2.12, the approval rule's family: no surface promises that a change
    waits for a yes without the condition that makes it true.

    The approval is the AI client's, and it holds while AdCopilot's write
    tools stay on Needs approval. The docs skill said so, and its first list
    did too; then a second list in the same reply said "every change waits for
    your yes" with nothing after it, and the README promised "made only on
    your yes" in three places. Every sentence that makes the promise must
    carry its condition ("as long as" or "while") in the same sentence; a
    related read's own sentence says a change is still only proposed, which
    is a promise of nothing.

    Fix round 1: the promise is also made in the third person, where the
    customer reads it: `/adcopilot:negatives`' description in the command
    picker ("added only after the customer's yes") and the auditor's report
    line ("happens only after the customer says yes"). The wider pattern runs
    over what the customer is shown: the README, the manifests, every
    frontmatter description, and the auditor's report section. A rule the
    model is given in a body ("Apply it only on their yes") is the model's
    own and holds whatever the client's approval setting, so it carries no
    condition and the wider pattern leaves it alone."""

    PROMISE = re.compile(r"waits? for (?:your|the customer's|their|the) "
                         r"(?:yes|approval)|"
                         r"only (?:on|after|with) your (?:yes|approval)|"
                         r"only after you (?:say yes|approve)", re.I)
    THIRD_PERSON_PROMISE = re.compile(
        r"only (?:on|after|with) (?:the customer's|their) (?:yes|approval)|"
        r"only (?:after|once|when) (?:the customer|they) (?:says?|gives?) "
        r"(?:yes|their yes|approval)|"
        r"only after (?:the customer|they) approves?", re.I)
    CONDITION = re.compile(r"\b(?:as long as|while)\b", re.I)
    RELATED = "They are reads only: a change is still only proposed"
    AUDITOR = "agents/adcopilot-auditor.md"

    @staticmethod
    def sentences(text):
        out = []
        for block in re.split(r"\n\s*\n|\n(?=\s*(?:[-*]|\d+\.)\s)", text):
            joined = " ".join(block.split())
            out += [s for s in re.split(r"(?<=[.!?])\s+(?=[^a-z])", joined) if s]
        return out

    def offenders(self, text, promise=None):
        promise = promise or self.PROMISE
        return [s for s in self.sentences(text)
                if promise.search(s) and not self.CONDITION.search(s)]

    def surfaces(self):
        return (["README.md", ".claude-plugin/plugin.json",
                 ".claude-plugin/marketplace.json"] + model_read_files())

    def customer_visible(self):
        """(label, text) for everything a customer is shown in AdCopilot's
        own words: the README and manifests whole, each skill's, command's
        and agent's frontmatter description, and the auditor's report
        section, which is what its report says."""
        out = [(rel, read(rel)) for rel in
               ("README.md", ".claude-plugin/plugin.json",
                ".claude-plugin/marketplace.json")]
        for rel in model_read_files():
            m = re.search(r"^description: (.+)$", frontmatter(read(rel)), re.M)
            if m:
                out.append((rel + " (description)", m.group(1)))
        out.append((self.AUDITOR + " (## The report)",
                    section(read(self.AUDITOR), "## The report") or ""))
        return out

    def test_the_wider_guard_catches_the_third_person_promise(self):
        for bad in ("Propose never-show-for words for them — added only after "
                    "the customer's yes, then read back.",
                    "Nothing above has been applied, and any of these changes "
                    "happens only after the customer says yes in their own "
                    "conversation — the one that asked for this audit — never "
                    "here."):
            with self.subTest(bad=bad):
                self.assertEqual(self.offenders(bad, self.THIRD_PERSON_PROMISE), [bad])
        for good in ("Propose never-show-for words for them — added only after "
                     "the customer's yes, while the write tools stay on Needs "
                     "approval, then read back.",
                     "Any of these changes happens only after the customer says "
                     "yes in their own conversation, while AdCopilot's write "
                     "tools stay on Needs approval there, and never here."):
            with self.subTest(good=good):
                self.assertEqual(self.offenders(good, self.THIRD_PERSON_PROMISE), [])

    def test_nothing_the_customer_is_shown_promises_it_in_the_third_person(self):
        labels = [label for label, _text in self.customer_visible()]
        self.assertIn("commands/negatives.md (description)", labels)
        self.assertIn(self.AUDITOR + " (## The report)", labels)
        for label, text in self.customer_visible():
            with self.subTest(surface=label):
                self.assertEqual(self.offenders(text, self.THIRD_PERSON_PROMISE), [])

    def test_the_two_third_person_sentences_carry_it(self):
        # The Cursor round: the two sentences now promise nothing, so they
        # need no condition, and they name no Claude-only setting.
        desc = re.search(r"^description: (.+)$",
                         frontmatter(read("commands/negatives.md")), re.M).group(1)
        self.assertIn("and propose never-show-for words (negative keywords) for "
                      "them; the ones added are read back.", desc)
        self.assertIn("nothing above has been applied; each change is a "
                      "proposal, to be put to the customer in their own "
                      "conversation — the one that asked for this audit — and "
                      "never made here.", flat(self.AUDITOR))
        for text in (desc, section(read(self.AUDITOR), "## The report") or ""):
            self.assertNotIn("Needs approval", text)

    def test_the_guard_catches_the_words_it_is_for(self):
        for bad in ("They are reads only: a change still waits for the customer's yes.",
                    "They are reads only: a change still waits for the yes.",
                    "Fix and improve your campaigns (every change waits for your yes): Block wasted searches.",
                    "The first fix is proposed; made only on your yes, read back, then the next one proposed.",
                    "Never-show-for words are added only after your yes, then read back."):
            with self.subTest(bad=bad):
                self.assertEqual(self.offenders(bad), [bad])
        for good in ("Every change waits for your yes, as long as AdCopilot's write tools stay on Needs approval.",
                     "It is made only on your yes while the write tools stay on **Needs approval**, then read back.",
                     "They are reads only: a change is still only proposed."):
            with self.subTest(good=good):
                self.assertEqual(self.offenders(good), [])

    def test_no_surface_promises_approval_without_its_condition(self):
        for rel in self.surfaces():
            with self.subTest(file=rel):
                self.assertEqual(self.offenders(read(rel)), [])

    def test_a_related_read_leaves_a_change_proposed(self):
        carriers = [rel for rel in model_read_files()
                    if "They are reads only" in flat(rel)]
        self.assertGreaterEqual(len(carriers), 9)
        for rel in carriers:
            with self.subTest(file=rel):
                self.assertIn(self.RELATED, flat(rel))
        # The review's own wording, which the others follow.
        self.assertIn(self.RELATED + ".", flat("skills/adcopilot-review/SKILL.md"))


class V241Alignment(unittest.TestCase):
    """0.2.12 aligned with AdCopilot v2.41.0 (release/v2.41.0, PR #843): the
    plugin's text and its newest eval fixtures say what that release does.

    - #831: `set_campaign_status` is served with
      `_meta["anthropic/requiresUserInteraction"]`, so Claude Code (2.1.214 or
      later) asks before every use of that tool whatever its settings, and a
      run with nobody to answer cannot use it. PRODUCT-FACTS: say it of
      Claude Code with its version and of that tool alone; of the desktop app
      no more than that it "may also ask every time for this tool". It is
      that tool alone (`toolsurface.NEEDS_A_PERSON`): `update_campaign` takes
      a status too (ENABLED or PAUSED) and is not flagged, so no surface says
      every pause or switch-on is asked about, and none says a cloud routine
      refuses one (Claude on the web is not verified).
    - #827: a first call that skipped get_org_context can carry a note (once
      its switch is on), so every surface opens with get_org_context.
    - #821: the assistant reports no limit no call returned: no surface calls
      the answer's size a read cap.
    - #829, #832, #820: the cases that grade a question answered first on a
      roomy day with eight reads, one set of dates on the account's own
      yesterday (this month's pacing and the change log run to its today),
      and the costliest searches named.
    - #839: nothing here offers a developer token of the customer's own."""

    DOCS = "skills/adcopilot-docs/SKILL.md"
    QUESTION = "review-question-first-roomy"
    DATES = "review-account-day-named-searches"
    UNCAPPED = "review-uncapped-no-limit-words"
    # The audit and the analysis lenses end on the account's yesterday; this
    # month's pacing and the change log run through its today (v2.41.0's
    # `account_month_bounds` and `change_event_window`).
    LENSES = ("full_audit", "analyze_search_terms", "analyze_waste",
              "conversion_setup_audit")
    TODAY_LENSES = ("budget_pacing", "change_history")
    FIVE = ("review-uncapped-no-limit-words", "review-question-first-roomy",
            "docs-capabilities-untracked", "docs-capabilities-routed",
            "review-account-day-named-searches")
    # What the alignment first said, of every pause or switch-on (only
    # set_campaign_status is flagged) and of a cloud routine (not verified).
    OVERCLAIM = re.compile(r"pausing or switching on a campaign: Claude Code|"
                           r"every pause or switch-on|"
                           r"marks pausing or switching on a campaign|"
                           r"will not do it with nobody there|"
                           r"Only pausing or switching on a campaign is refused|"
                           r"runs its other tools without asking")

    def test_the_one_tool_claude_code_always_asks_about(self):
        # The Cursor round: the exception is named by the tool, and the
        # plugin routes every pause and switch-on through it, so what it says
        # stays true on v2.41.0 (where `update_campaign` also takes a status,
        # unflagged) and after the server refuses a status there.
        exception = ("`set_campaign_status`, the tool that pauses a campaign or "
                     "switches one on")
        routed = {"README.md": "The plugin's skills pause or switch on a "
                               "campaign only with that tool, never with a "
                               "status in a change to the campaign's settings "
                               "(`update_campaign`)",
                  self.DOCS: "This plugin pauses or switches on a campaign only "
                             "with that tool, never with a status in a change to "
                             "the campaign's settings (`update_campaign`)"}
        for rel in ("README.md", self.DOCS):
            with self.subTest(file=rel):
                text = flat(rel)
                self.assertIn(exception, text)
                self.assertIn("Claude Code (version 2.1.214 or later) asks before "
                              "every use of it", text)
                self.assertIn("a run with nobody there to answer cannot use it", text)
                self.assertIn("the Claude desktop app may also ask every time", text)
                self.assertIn(routed[rel], text)
                # How far it goes, in words that stay true on v2.41.0 (where
                # `update_campaign` also takes a status, unflagged) and once
                # the server refuses a status there (adcopilot#852): the
                # plugin never sends one, and a settings change follows the
                # client's settings. No evergreen sentence pins v2.41.0's
                # update_campaign behaviour.
                self.assertNotIn("v2.41.0 also lets", text)
        morning = " ".join((section(read("README.md"),
                                    "### Every morning, without asking") or "").split())
        self.assertIn("AdCopilot marks `set_campaign_status`, the tool that pauses "
                      "a campaign or switches one on, as needing a person, so "
                      "Claude Code (version 2.1.214 or later) will not use it in a "
                      "run on your computer with nobody there to answer", morning)
        self.assertIn("the mark does not hold that change", morning)
        self.assertIn("A Claude Code routine runs its tools without asking", morning)
        for rel in ["README.md", ".claude-plugin/plugin.json"] + model_read_files():
            with self.subTest(overclaim=rel):
                found = self.OVERCLAIM.search(flat(rel))
                self.assertIsNone(found, found and found.group(0))
        # The daily skill's routine step says nothing of the flag: whether a
        # cloud routine honours it is not verified.
        self.assertNotIn("2.1.214", flat("skills/adcopilot-daily/SKILL.md"))
        rubric = grader_block(read("evals/docs-safe-to-let-loose/case.yaml"),
                              "the-approval-answer-names-its-condition")
        self.assertIn("except `set_campaign_status`, the tool that pauses a "
                      "campaign or switches one on", " ".join(rubric.split()))

    def test_every_pause_or_switch_on_goes_through_set_campaign_status(self):
        # (5) of the Cursor round: the surfaces that pause a campaign or
        # switch one on name `set_campaign_status`, and no surface sends a
        # status through `update_campaign` (v2.41.0 takes one there, without
        # the flag; a server change is making it refuse one).
        for rel, words in (("skills/adcopilot-review/SKILL.md",
                            "Pause a campaign, or switch one on, only with "
                            "`set_campaign_status`, never with a status in "
                            "`update_campaign`"),
                           ("commands/audit.md",
                            "a pause or a switch-on with `set_campaign_status`, "
                            "never a status in `update_campaign`"),
                           ("skills/adcopilot-launch/SKILL.md",
                            "Pausing a campaign or switching one on is "
                            "`set_campaign_status`'s alone, never a status in "
                            "`update_campaign`.")):
            with self.subTest(file=rel):
                self.assertIn(words, flat(rel))
        status = re.compile(r"\bstatus\b", re.I)
        for rel in model_read_files():
            for sentence in ApprovalCondition.sentences(read(rel)):
                if "`update_campaign`" in sentence and status.search(sentence):
                    with self.subTest(file=rel, sentence=sentence[:80]):
                        self.assertRegex(sentence, r"\bnever\b")

    def test_a_request_to_get_started_follows_the_installed_skill(self):
        # v2.41.0's next_step and [PLUGIN]: "on a greeting alone, a request to
        # get started or ..., follow" the installed steps. adcopilot-connect
        # fires on "asks to get started", so it alone carries the exception
        # to the hand-off sentence every marked surface shares.
        exception = ("A greeting alone or a request to get started is the one "
                     "exception: then `next_step` is describing this request "
                     "too, so follow that skill's steps, as `next_step` says.")
        for rel in model_read_files():
            with self.subTest(file=rel):
                self.assertEqual(flat(rel).count(exception),
                                 1 if rel == "skills/adcopilot-connect/SKILL.md" else 0)
        self.assertIn("asks to get started",
                      frontmatter(read("skills/adcopilot-connect/SKILL.md")))

    def test_the_readme_dates_and_cases(self):
        notes = section(read("README.md"), "## AdCopilot version") or ""
        note = " ".join(notes[notes.find("**0.2.12 ("):].split("\n\n", 1)[0].split())
        self.assertIn("This month's pacing (`budget_pacing`) and the change log "
                      "(`change_history`) run through the account's today", note)
        self.assertNotIn("ends every report window", note)
        evals = " ".join((section(read("README.md"),
                                  "## Evals, and how a skill earns its place") or "").split())
        self.assertIn("The four cases added in 0.2.5 (`docs-safe-to-let-loose`", evals)
        self.assertNotIn("The four newest cases", evals)
        # What the six newest cases have and have not run on (the Cursor
        # round's review): four ran on 2026-10-17 against an earlier text.
        self.assertNotIn("written but not yet run", evals)
        self.assertIn("ran on 2026-10-17 against an earlier 0.2.12 text, where "
                      "`meta-connector-absent` scored 0.778, under the 0.8 line "
                      "on all three of its runs, and the other two have never "
                      "run", evals)
        self.assertNotIn("Five new cases are written and have not been run.", note)
        self.assertIn("three of them ran once, on 2026-10-17, against an earlier "
                      "0.2.12 text, and two never have", note)
        # The 0.2.5 cases' baseline arm, after the re-render.
        self.assertIn("the baseline arm is the plugin present with its skill "
                      "bodies empty", evals)

    def test_the_readme_says_which_campaign_it_will_not_switch_on(self):
        # The server refuses a switch-on only for the campaign AdCopilot built
        # (toolfilter.FIRST_CAMPAIGN_REFUSAL), and the plugin pauses or
        # switches on others with set_campaign_status on a yes.
        will_not = section(read("README.md"), "## What it will not do") or ""
        self.assertIn("- **Switch on a campaign it built.**", will_not)
        self.assertNotIn("**Switch a campaign on.**", will_not)

    def test_the_v241_fixtures_hold_what_classify_derives(self):
        # release/v2.41.0's situations.classify, run on each fixture's own
        # data, gives exactly its overlays (no `focus`, #423), and
        # tools_adcopilot._hints gives no hint for these states.
        for case in self.FIVE:
            with self.subTest(case=case):
                ctx = mock(case, "get_org_context")
                self.assertNotIn("focus", ctx["overlays"])
                self.assertEqual(ctx["hints"], [])
                self.assertFalse(ctx["overlays"]["draft_waiting"])
                self.assertFalse(ctx["overlays"]["routine_pending"])
                self.assertIsNone(ctx["overlays"]["plugin_offer"])
                first = ctx["profile"].get("first_campaign") or {}
                if first.get("campaign_id"):
                    self.assertTrue(first.get("enabled_seen_at"))
                self.assertNotEqual(ctx["routine"]["weekly"]["status"], "off")

    def test_every_surface_opens_with_get_org_context(self):
        self.assertIn("`get_org_context` first, then `full_audit` at `depth: "
                      "deep`, then `budget_pacing`.", flat("commands/audit.md"))

    def test_no_surface_calls_the_answers_size_a_cap(self):
        for rel in model_read_files():
            with self.subTest(file=rel):
                self.assertNotIn("read cap", flat(rel))
        desc = re.search(r"^description: (.+)$",
                         frontmatter(read("commands/daily.md")), re.M).group(1)
        self.assertIn("as far as the reads AdCopilot sizes for one answer allow",
                      desc)

    def test_no_developer_token_of_their_own_is_offered(self):
        own = re.compile(r"developer token|bring[- ]your[- ]own|own (?:API )?token|"
                         r"\bBYO\b", re.I)
        for rel in (["README.md", ".claude-plugin/plugin.json",
                     ".claude-plugin/marketplace.json"] + model_read_files()):
            with self.subTest(file=rel):
                found = own.search(read(rel))
                self.assertIsNone(found, found and found.group(0))

    def test_the_release_note_puts_the_server_first(self):
        notes = section(read("README.md"), "## AdCopilot version") or ""
        note = " ".join(notes[notes.find("**0.2.12 ("):].split("\n\n", 1)[0].split())
        self.assertIn("true against AdCopilot v2.41.0, which must be live before "
                      "this version is published", note)
        self.assertIn("so that release goes out first", note)
        self.assertNotIn("no server release has to come first", note)
        # 0.2.14 adds fix-checks-three-checks (#24) and review-scheduled-unmarked (#22).
        self.assertIn("thirty cases across the suite", flat("README.md"))

    def test_the_question_first_case(self):
        ctx = mock(self.QUESTION, "get_org_context")
        self.assertEqual(ctx, mock(self.UNCAPPED, "get_org_context"))
        self.assertEqual(ctx["situation"], "ADS_ACTIVE_UNTRACKED")
        self.assertEqual(ctx["plugin"]["skill"], "adcopilot-measure")
        self.assertIsNone(ctx["org"]["ops_today_cap"])
        self.assertEqual(ctx["cross_reads"]["ads_reads_max"], 8)
        self.assertEqual(ctx["next_step"], SERVER_MEASURE_STEP + " " + SERVER_RETURNING)
        text = read("evals/%s/case.yaml" % self.QUESTION)
        self.assertIn("tags: [review]\n", text)
        self.assertTrue(never_grader(text, "Skill", "adcopilot-measure"))
        self.assertIn("adcopilot-review", grader_block(text, "skill-fired"))
        pattern, flags = grader(self.QUESTION, "makes-more-than-five-google-ads-reads")
        rx = re.compile(pattern, flags)
        mcp = "mcp__plugin_adcopilot_adcopilot__"

        def log(tools):
            return json.dumps([{"tool": mcp + name, "input": {}} for name in tools])

        five = ["get_org_context", "full_audit", "search", "analyze_search_terms",
                "budget_pacing", "conversion_setup_audit", "gsc_search_analytics"]
        self.assertIsNone(rx.search(log(five)))
        self.assertIsNotNone(rx.search(log(five + ["analyze_waste"])))
        self.assertEqual(grader(self.QUESTION, "no-limit-words"),
                         grader(self.UNCAPPED, "no-limit-words"))
        top = mock(self.QUESTION, "analyze_search_terms")["findings"][0]
        self.assertEqual(top["title"], "Costliest search terms with no conversion")
        self.assertIn("not proven waste", top["detail"])
        self.assertEqual(top["recommended_actions"], [])

    def test_the_account_day_case(self):
        ctx = mock(self.DATES, "get_org_context")
        self.assertEqual(ctx["situation"], "ADS_ACTIVE_TRACKED")
        self.assertEqual(ctx["plugin"]["skill"], "adcopilot-review")
        self.assertEqual(ctx["next_step"], SERVER_REVIEW_STEP + " " + SERVER_RETURNING)
        probe = next(v for k, v in ctx["ads_probe"].items() if k.isdigit())
        self.assertEqual(probe["time_zone"], "Asia/Kolkata")
        self.assertEqual(probe["last_30d"]["end_date"], "2026-10-13")
        # Asked at 20:55 UTC on 13 Oct: UTC's yesterday is 12 Oct, the
        # account's is 13 Oct, and v2.41.0 ends every window on the latter.
        self.assertTrue(ctx["ads_probe"]["computed_at"].startswith("2026-10-13 20:55"))
        for tool in self.LENSES:
            with self.subTest(tool=tool):
                result = mock(self.DATES, tool)
                self.assertEqual(result["date_range"]["end"], "2026-10-13")
                self.assertEqual(result["time_zone"], "Asia/Kolkata")
        # v2.41.0 at 20:55 UTC on 13 Oct, Asia/Kolkata: change_event_window(14)
        # is 1 Oct..14 Oct, account_month_bounds 1 Oct..14 Oct, 14 days elapsed.
        for tool in self.TODAY_LENSES:
            with self.subTest(today=tool):
                result = mock(self.DATES, tool)
                self.assertEqual(result["date_range"],
                                 {"start": "2026-10-01", "end": "2026-10-14", "days": 14})
                self.assertEqual(result["time_zone"], "Asia/Kolkata")
        self.assertEqual(mock(self.DATES, "budget_pacing")["month_to_date"]["days_elapsed"], 14)
        # At 08:40 UTC on 6 Oct, America/New_York: 7 Sep..6 Oct over 30 days,
        # and the month so far 1 Oct..6 Oct, 6 days elapsed.
        for case in (self.QUESTION, self.UNCAPPED):
            with self.subTest(case=case):
                self.assertEqual(mock(case, "change_history")["date_range"],
                                 {"start": "2026-09-07", "end": "2026-10-06", "days": 30})
                pacing = mock(case, "budget_pacing")
                self.assertEqual(pacing["date_range"],
                                 {"start": "2026-10-01", "end": "2026-10-06", "days": 6})
                self.assertEqual(pacing["month_to_date"]["days_elapsed"], 6)
        days = sorted({row["segments.date"] for row in mock(self.DATES, "search")["result"]
                       if "segments.date" in row})
        self.assertEqual(days[-1], "2026-10-13")
        audit = mock(self.DATES, "full_audit")
        self.assertIn("from 56 of the 62 checks that apply to this account", audit["narrative"])
        self.assertIn("in the 7 days from 7 Oct to 13 Oct",
                      next(f["detail"] for f in audit["findings"] if f["check_id"] == "G-CT3"))
        self.assertTrue(any(c.get("reason_code") == "NO_MARKET_BENCHMARK"
                            for c in audit["coverage"]))
        # G16 as v2.41.0's evaluator words it: 40% of spend is a fail, and its
        # window is a length, which review step 1 dates from date_range.end.
        g16 = next(f for f in audit["findings"] if f["check_id"] == "G16")
        self.assertEqual((g16["status"], g16["title"]),
                         ("fail", "Wasted spend on irrelevant terms"))
        self.assertIn("in the last 14 days", g16["detail"])
        self.assertNotIn("Oct", g16["detail"])
        self.assertEqual(g16, next(f for f in mock(self.DATES, "analyze_waste")["findings"]
                                   if f["check_id"] == "G16"))
        self.assertEqual(audit["counts"]["fail"],
                         sum(1 for f in audit["findings"] if f["status"] == "fail"))
        # No related read promises the searches' names (v2.41.0's
        # related_reads.from_envelope names the two failing areas).
        self.assertEqual([r["tool"] for r in audit["related_reads"]],
                         ["analyze_waste", "conversion_setup_audit"])
        terms = mock(self.DATES, "analyze_search_terms")["findings"]
        self.assertEqual([f["check_id"] for f in terms],
                         ["O-NEG-TOP", "O-NEG-FREE", "O-NEG-INFO", "O-NEG-JOB"])
        self.assertEqual(terms[-1]["title"], "Job-seeker search terms")
        names = [r[0] for r in mock(self.DATES, "analyze_search_terms")["findings"][0]
                 ["evidence"]["rows"]]
        self.assertEqual(names[:2], ["dentist jobs bangalore", "free dental camp"])
        text = read("evals/%s/case.yaml" % self.DATES)
        for name in ("search-ends-on-the-accounts-yesterday",
                     "no-search-ends-on-another-day",
                     "names-the-two-costliest-searches",
                     "coverage-is-a-count-not-a-percentage",
                     "one-set-of-dates-and-named-searches", "marks-plugin-use",
                     "skill-fired", "no-change-without-a-yes"):
            with self.subTest(grader=name):
                self.assertIn("  - name: %s\n" % name, text)
        ends, flags = grader(self.DATES, "search-ends-on-the-accounts-yesterday")
        other, _ = grader(self.DATES, "no-search-ends-on-another-day")
        call = json.dumps([{"tool": "mcp__plugin_adcopilot_adcopilot__search",
                            "input": {"start_date": "2026-09-30",
                                      "end_date": "%s"}}])
        self.assertRegex(call % "2026-10-13", re.compile(ends, flags))
        self.assertNotRegex(call % "2026-10-13", re.compile(other))
        for day in ("2026-10-12", "2026-10-14", "2026-10-25", "2026-11-02",
                    "2027-01-04"):
            with self.subTest(day=day):
                self.assertRegex(call % day, re.compile(other))
        # An earlier comparison window is not a wrong day.
        for day in ("2026-09-29", "2026-10-06"):
            with self.subTest(earlier=day):
                self.assertNotRegex(call % day, re.compile(other))
        # The same day written into the conditions, as an object or as an
        # escaped JSON string: a BETWEEN range, or a <= bound.
        mcp = "mcp__plugin_adcopilot_adcopilot__search"
        for cond in ("segments.date BETWEEN '2026-09-30' AND '%s'",
                     "segments.date between '2026-09-30' and '%s'",
                     "segments.date >= '2026-09-30' AND segments.date <= '%s'"):
            for as_string in (False, True):
                def log(day):
                    inp = {"resource": "campaign", "conditions": [cond % day]}
                    return json.dumps([{"tool": mcp, "input": json.dumps(inp)
                                        if as_string else inp}])
                with self.subTest(cond=cond, as_string=as_string):
                    self.assertRegex(log("2026-10-13"), re.compile(ends, flags))
                    self.assertNotRegex(log("2026-10-13"), re.compile(other))
                    self.assertNotRegex(log("2026-10-14"), re.compile(ends, flags))
                    self.assertRegex(log("2026-10-14"), re.compile(other))
                    self.assertRegex(log("2026-10-12"), re.compile(other))
                    self.assertNotRegex(log("2026-09-29"), re.compile(other))
        # The Cursor round closes the graders' blind spot: the same days in
        # double quotes, a `<` bound on the day after, a single day, and a
        # DURING range that takes in the account's unfinished today.
        def logged(cond, as_string):
            inp = {"resource": "campaign", "conditions": [cond]}
            return json.dumps([{"tool": mcp, "input": json.dumps(inp)
                                if as_string else inp}])
        for as_string in (False, True):
            for cond, right in (
                    ('segments.date BETWEEN "2026-09-30" AND "2026-10-13"', True),
                    ('segments.date <= "2026-10-13"', True),
                    ("segments.date < '2026-10-14'", True),
                    ('segments.date < "2026-10-14"', True),
                    ("segments.date = '2026-10-13'", True),
                    ('segments.date BETWEEN "2026-09-30" AND "2026-10-14"', False),
                    ('segments.date <= "2026-10-12"', False),
                    ("segments.date < '2026-10-15'", False),
                    ("segments.date < '2026-10-13'", False),
                    ("segments.date = '2026-10-14'", False),
                    ("segments.date DURING TODAY", False),
                    ("segments.date DURING THIS_MONTH", False),
                    ("segments.date during this_week_mon_today", False)):
                with self.subTest(cond=cond, as_string=as_string):
                    if right:
                        self.assertRegex(logged(cond, as_string), re.compile(ends, flags))
                        self.assertNotRegex(logged(cond, as_string), re.compile(other))
                    else:
                        self.assertNotRegex(logged(cond, as_string), re.compile(ends, flags))
                        self.assertRegex(logged(cond, as_string), re.compile(other))
            for cond in ("segments.date < '2026-09-30'",
                         'segments.date BETWEEN "2026-09-16" AND "2026-09-29"',
                         "segments.date DURING LAST_14_DAYS",
                         "segments.date IN ('2026-10-06', '2026-10-13')"):
                with self.subTest(earlier=cond, as_string=as_string):
                    self.assertNotRegex(logged(cond, as_string), re.compile(other))
            # The review's closing of the remaining gaps: an open range (a `>`
            # or `>=` bound with no upper bound runs to the account's today,
            # whatever its first day) and an IN list holding a wrong day.
            for cond in ("segments.date >= '2026-10-14'",
                         'segments.date > "2026-10-13"',
                         "segments.date >= '2026-10-13'",
                         "segments.date >= '2026-09-30'",
                         "segments.date>='2026-09-30'",
                         "segments.date IN ('2026-10-14')",
                         'segments.date in ("2026-10-13", "2026-10-14")',
                         "segments.date IN ('2026-10-12')"):
                with self.subTest(wrong=cond, as_string=as_string):
                    self.assertRegex(logged(cond, as_string), re.compile(other))
                    self.assertNotRegex(logged(cond, as_string), re.compile(ends, flags))
            # A lower bound with an upper one, in either order or in two
            # conditions, is a finite range and is judged by its end.
            def two(conds):
                inp = {"resource": "campaign", "conditions": conds}
                return json.dumps([{"tool": mcp, "input": json.dumps(inp)
                                    if as_string else inp}])
            for conds, right in (
                    (["segments.date <= '2026-10-13' AND segments.date >= '2026-09-30'"], True),
                    (["segments.date >= '2026-09-30'", "segments.date <= '2026-10-13'"], True),
                    (["segments.date > '2026-09-29'", 'segments.date < "2026-10-14"'], True),
                    (["segments.date >= '2026-09-30'", "segments.date <= '2026-10-14'"], False)):
                with self.subTest(conds=conds, as_string=as_string):
                    if right:
                        self.assertRegex(two(conds), re.compile(ends, flags))
                        self.assertNotRegex(two(conds), re.compile(other))
                    else:
                        self.assertRegex(two(conds), re.compile(other))
            # A lower bound beside end_date is bounded by end_date.
            for end, wrong in (("2026-10-13", False), ("2026-10-14", True)):
                inp = {"resource": "campaign", "start_date": "2026-09-30",
                       "end_date": end, "conditions": ["segments.date >= '2026-09-30'"]}
                log = json.dumps([{"tool": mcp, "input": json.dumps(inp)
                                   if as_string else inp}])
                with self.subTest(end_date=end, as_string=as_string):
                    if wrong:
                        self.assertRegex(log, re.compile(other))
                    else:
                        self.assertNotRegex(log, re.compile(other))
                        self.assertRegex(log, re.compile(ends, flags))
            # Neither grader is decided by a `tools` refresh or a lens call.
            refresh = json.dumps([{"tool": "mcp__plugin_adcopilot_adcopilot__get_org_context",
                                   "input": {"tools": ["search"], "source": "x"}},
                                  {"tool": "mcp__plugin_adcopilot_adcopilot__budget_pacing",
                                   "input": {"customer_id": "1"},
                                   "output": "segments.date >= '2026-10-01'"}])
            self.assertNotRegex(refresh, re.compile(other))
        cov, cflags = grader(self.DATES, "coverage-is-a-count-not-a-percentage")
        self.assertRegex("Coverage was 73% of its 73 checks.", re.compile(cov, cflags))
        self.assertRegex("Coverage was 90% of its 70 checks.", re.compile(cov, cflags))
        self.assertNotRegex("The audit's score comes from the 58 of 73 checks "
                            "that gave a result.", re.compile(cov, cflags))
        self.assertNotRegex("The audit's score comes from 56 of the 62 checks "
                            "that apply to this account.", re.compile(cov, cflags))


# The Cursor round of 0.2.12. AdCopilot is listed on cursor.directory, whose
# "Add to Cursor" installs the connector under the name `server`, and Cursor
# reads skills from .cursor/skills or .claude/skills. Cursor has no "Needs
# approval" setting: its run modes decide (Auto-review, the recommended
# default, can let an MCP call through; Allowlist; Run Everything), and a
# cloud agent never asks. v2.41.0 reports a Cursor connection as `surface`
# `cursor` (tools_adcopilot._SURFACE_MAP) and offers it no schedule
# (schedule_recipe.offer_for gives None for a named client that is not Claude).
APPROVAL_SENTENCE = ("AdCopilot proposes each change first. For a hard stop, "
                     "set your AI client to ask before AdCopilot's write tools: "
                     "Needs approval in Claude; in Cursor, use the Allowlist "
                     "run mode and keep them off the allowlist (Cursor's cloud "
                     "agents never ask).")


CURSOR_CONFIG = ("eyJ0eXBlIjoiaHR0cCIsInVybCI6Imh0dHBzOi8vbWNwLmFkY29waWxvdC5jbG91"
                 "ZC9tY3AifQ%3D%3D")


CURSOR_TELL = ("`get_org_context`'s top-level `surface` is `cursor`, or Cursor's "
               "own instructions or the person say so")


GOOGLE_ACCESS_DISCLOSURE = (
    "AdCopilot connects to Google Ads through its own Google Cloud project, "
    "with your Google sign-in. If you want programmatic access to Google Ads "
    "for your own software, get your own Google Cloud account and apply for "
    "Google Ads API access there.")


class ClientNeutralApproval(unittest.TestCase):
    """One approval sentence for every AI client. The earlier 0.2.12 text
    made "while the write tools stay on Needs approval" the condition of every
    promise: a Claude setting, which the plugin directory, the README and
    cursor.directory's copy of the description all showed to Cursor users."""

    CLAUDE_ONLY = re.compile(r"while (?:the|AdCopilot's) write tools (?:stay|need)|"
                             r"Your AI client asks before each change", re.I)

    def surfaces(self):
        return (["README.md", ".claude-plugin/plugin.json",
                 ".claude-plugin/marketplace.json"] + model_read_files())

    def test_the_manifest_and_the_readme_carry_the_sentence(self):
        desc = json.loads(read(".claude-plugin/plugin.json"))["description"]
        self.assertIn(APPROVAL_SENTENCE, desc)
        self.assertIn("AdCopilot never deletes anything but a negative keyword.", desc)
        self.assertLessEqual(len(desc), 1024)
        intro = " ".join(read("README.md").split("\n## ", 1)[0].split())
        self.assertIn(APPROVAL_SENTENCE, intro)

    def test_no_surface_keeps_the_claude_only_condition(self):
        for rel in self.surfaces():
            with self.subTest(file=rel):
                found = self.CLAUDE_ONLY.search(flat(rel))
                self.assertIsNone(found, found and found.group(0))

    def test_needs_approval_is_named_beside_cursor(self):
        # Wherever the customer reads "Needs approval", Cursor's way is in the
        # same sentence. The one exception is adcopilot-daily's set-up step
        # for the Claude app, which is Claude's own screen.
        visible = [(rel, read(rel)) for rel in
                   ("README.md", ".claude-plugin/plugin.json",
                    ".claude-plugin/marketplace.json")]
        visible.append(("skills/adcopilot-docs/SKILL.md",
                        read("skills/adcopilot-docs/SKILL.md")))
        for rel, text in visible:
            for sentence in ApprovalCondition.sentences(text):
                if "Needs approval" in sentence:
                    with self.subTest(file=rel, sentence=sentence[:80]):
                        self.assertIn("Cursor", sentence)

    def test_cursors_hard_stop_names_the_allowlist_run_mode(self):
        # Keeping the write tools off the allowlist is a hard stop only in
        # Cursor's Allowlist run mode: in Auto-review, its recommended default,
        # a classifier can let a tool that is not allowlisted through.
        for rel in (["README.md", ".claude-plugin/plugin.json"]
                    + model_read_files()):
            text = flat(rel)
            for sentence in ApprovalCondition.sentences(text):
                if "Cursor" in sentence and "off the allowlist" in sentence:
                    with self.subTest(file=rel, sentence=sentence[:90]):
                        self.assertIn("Allowlist", sentence.replace(
                            "off the allowlist", ""))

    def test_the_docs_skill_names_each_clients_hard_stop(self):
        docs = flat("skills/adcopilot-docs/SKILL.md")
        for words in ("AdCopilot proposes each change first.",
                      "**Needs approval** in claude.ai, Cowork and the desktop app",
                      "in Cursor, the write tools kept off the allowlist",
                      "Cursor has no **Needs approval** setting",
                      "a Cursor cloud agent never asks",
                      "never promise a yes before every change without the hard "
                      "stop beside it."):
            with self.subTest(words=words):
                self.assertIn(words, docs)


class CursorPath(unittest.TestCase):
    """Wherever the plugin works out which client it is in, Cursor is checked
    first: there it never runs `claude mcp` (Cursor's agent can reach a shell
    where Claude Code is installed, and that command lists Claude Code's
    connectors), the connector may be named `server`, and it gives Cursor's
    sign-in step instead of the plugin's Connectors tab."""

    def test_setup_checks_for_cursor_before_claude_code(self):
        text = flat("commands/setup.md")
        cursor = text.index("If this is Cursor (" + CURSOR_TELL + ")")
        self.assertLess(cursor, text.index("`claude mcp list`"))
        for words in ("never run `claude mcp`, not even to check",
                      "may be named `server` rather than `adcopilot`; it is the "
                      "same connector",
                      "**Let Cursor use your AdCopilot?**",
                      "config=" + CURSOR_CONFIG,
                      "Nothing in the next three paragraphs applies in Cursor."):
            with self.subTest(words=words):
                self.assertIn(words, text)

    def test_connect_signs_in_cursor_first(self):
        step = " ".join((section(read("skills/adcopilot-connect/SKILL.md"),
                                 "### 1. Signed in") or "").split())
        self.assertLess(step.index("**Cursor** (" + CURSOR_TELL + ")"),
                        step.index("**Claude Code**"))
        for words in ("never run `claude mcp` here",
                      "may be named `server` rather than `adcopilot`",
                      "**Let Cursor use your AdCopilot?**",
                      "config=" + CURSOR_CONFIG):
            with self.subTest(words=words):
                self.assertIn(words, step)
        # The plugin's Connectors tab is the web branch's, not Cursor's.
        cursor = step.split("**Claude Code**")[0]
        self.assertNotIn("Connectors", cursor)

    def test_the_habit_block_checks_for_cursor_first(self):
        block = " ".join((section(read(HABIT_CARRIERS[0]), HABIT_HEADING) or "").split())
        first = block.index("First, Cursor. If this is Cursor (" + CURSOR_TELL + ")")
        self.assertLess(first, block.index("make one offer"))
        self.assertLess(first, block.index("`claude mcp list`"))
        self.assertIn("make no schedule offer of your own, never run `claude mcp` "
                      "to work out where you are, and never call "
                      "`save_org_context` with `routine.own_schedule`", block)
        self.assertNotIn("make no offer,", block)
        self.assertNotIn("record nothing about a schedule", block)
        self.assertIn("never Cursor, ChatGPT or another client", block)

    def test_in_cursor_the_servers_check_in_offer_is_made(self):
        # v2.41.0 gives a Cursor connection no schedule_offer, but while the
        # routine is pending its next_step still ends "Before you finish,
        # offer to set up a daily check-in and a Monday summary." and the
        # playbook carries THE CLOSE (plugin_drops_schedule applies only when
        # schedule_offer is set). "Make no offer" would have cut the one
        # daily loop Cursor has.
        offer = ("If `next_step` asks you to offer a check-in or a summary, "
                 "make that offer as it says, with the playbook's close (THE "
                 "CLOSE) for the steps on a yes.")
        for rel in HABIT_CARRIERS:
            block = " ".join((section(read(rel), HABIT_HEADING) or "").split())
            cursor = block.split("Everywhere else,")[0]
            with self.subTest(file=rel):
                self.assertEqual(cursor.count(offer), 1)
        review = flat("skills/adcopilot-review/SKILL.md")
        self.assertIn("In Cursor (" + CURSOR_TELL + ") there is none of the "
                      "plugin's own: make no schedule offer, never run "
                      "`claude mcp` to work out where you are, and never call "
                      "`save_org_context` with `routine.own_schedule`; if "
                      "`next_step` asks you to offer a check-in or a summary, "
                      "make that offer as it says, with the playbook's close "
                      "(THE CLOSE) for the steps on a yes.", review)
        readme = flat("README.md")
        self.assertIn("there the plugin makes no schedule offer of its own; in "
                      "Cursor, when AdCopilot's answer asks for an offer of a "
                      "check-in or a summary, the plugin makes that one as "
                      "AdCopilot words it.", readme)
        self.assertNotIn("and there the plugin makes no offer.", readme)

    def test_audit_refreshes_a_stale_tool_list_cursor_first(self):
        text = flat("commands/audit.md")
        cursor = text.index("If the tool is still missing, Cursor first: in "
                            "Cursor (" + CURSOR_TELL + ") there is no `/mcp`")
        self.assertLess(cursor, text.index("`/mcp`, choose `adcopilot`"))
        for words in ("you never run `claude mcp` there",
                      "turning AdCopilot off and on again in Cursor's MCP "
                      "settings, where it may be named `server`, refetches the "
                      "tool list",
                      "removing it and adding it again is the last resort.",
                      "Everywhere else, `/mcp`, choose `adcopilot`, then "
                      "Reconnect refetches the tool list",
                      "The first fix is then that refresh, with its last resort"):
            with self.subTest(words=words):
                self.assertIn(words, text)
        self.assertNotIn("that reconnect", text)

    def test_own_schedule_is_recorded_only_from_claude(self):
        block = " ".join((section(read(HABIT_CARRIERS[0]), HABIT_HEADING) or "").split())
        self.assertIn("Record it only from Claude: AdCopilot keeps "
                      "`routine.own_schedule` for the whole workspace", block)
        review = flat("skills/adcopilot-review/SKILL.md")
        self.assertIn("else `declined` — only from Claude", review)
        self.assertIn("In Cursor (" + CURSOR_TELL + ") there is none", review)
        self.assertIn("and `get_org_context` hands you its recipe, "
                      "`routine.schedule`, which AdCopilot sends only when its "
                      "`overlays.schedule_offer` is set", review)
        self.assertIn("when a scheduled run has checked in on two different "
                      "days (`routine.scheduled_first_seen_at` and "
                      "`routine.scheduled_last_seen_at`)", review)
        daily = flat("skills/adcopilot-daily/SKILL.md")
        self.assertIn("Never call `save_org_context` with `routine.own_schedule` "
                      "from Cursor", daily)
        self.assertLess(daily.index("Cursor first."),
                        daily.index("First, the instructions they will save."))

    def test_every_command_says_what_to_do_without_its_skill(self):
        for name in COMMANDS:
            rel = "commands/%s.md" % name
            text = flat(rel)
            with self.subTest(file=rel):
                if rel in DELEGATING_COMMANDS:
                    self.assertIn("If that skill is not installed here (Cursor can "
                                  "add this command without it), follow "
                                  "`get_org_context`'s `next_step` and `playbook` "
                                  "instead.", text)
                else:
                    # The versioned marker hands the turn to a skill, so a
                    # fallback to next_step and the playbook would point back
                    # at the skill that is missing: these send the bare one.
                    self.assertIn(NO_SKILLS, text)
                    self.assertNotIn("If that skill is not installed here", text)
                    keep = text.index("Send `source` exactly as written, the "
                                      "version included")
                    self.assertLess(keep, text.index(NO_SKILLS))
                    self.assertLess(text.index(NO_SKILLS),
                                    text.index("When the answer's `plugin.skill`"))

    def test_the_auditor_is_readonly_where_cursor_reads_it(self):
        text = read("agents/adcopilot-auditor.md")
        self.assertRegex(frontmatter(text), r"(?m)^readonly: true$")
        comment = " ".join(text.split("<!--", 1)[1].split("-->", 1)[0].split())
        self.assertIn("The list is enforced only in Claude Code.", comment)
        self.assertIn("its subagents have no tool list", comment)
        self.assertIn("does not say it holds back an MCP write", comment)

    def test_the_readme_has_a_cursor_section(self):
        install = " ".join((section(read("README.md"), "## Install") or "").split())
        cursor = " ".join((section(read("README.md"), "### Cursor") or "").split())
        self.assertTrue(cursor)
        self.assertIn(cursor[:200], install)
        self.assertIn("(https://cursor.com/en/install-mcp?name=adcopilot&config="
                      + CURSOR_CONFIG + ")", cursor)
        self.assertIn("`cursor://anysphere.cursor-deeplink/mcp/install?name="
                      "adcopilot&config=" + CURSOR_CONFIG + "`", cursor)
        self.assertNotIn("name=server", cursor)
        for words in ("**Let Cursor use your AdCopilot?**",
                      "can name the connector `server` instead of `adcopilot`",
                      "Cursor has no **Needs approval** setting",
                      "Settings, then Agents, then Approvals & Execution",
                      "keep AdCopilot's write tools off the allowlist",
                      "**Auto-review**, Cursor's recommended default",
                      "**Run Everything** asks before nothing",
                      "a Cursor cloud agent never asks you to approve an action"):
            with self.subTest(words=words):
                self.assertIn(words, cursor)

    def test_the_config_is_the_connectors_own(self):
        import base64
        from urllib.parse import unquote
        self.assertEqual(json.loads(base64.b64decode(unquote(CURSOR_CONFIG))),
                         json.loads(read(".mcp.json"))["mcpServers"]["adcopilot"])

    def test_googles_disclosure_is_under_install_word_for_word(self):
        install = section(read("README.md"), "## Install") or ""
        before_surfaces = install.split("\n### ", 1)[0]
        self.assertIn("\n" + GOOGLE_ACCESS_DISCLOSURE + "\n", before_surfaces)
        self.assertEqual(flat("README.md").count(GOOGLE_ACCESS_DISCLOSURE), 1)


if __name__ == "__main__":
    unittest.main()
