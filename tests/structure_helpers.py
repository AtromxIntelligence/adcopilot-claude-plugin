"""Helpers the structural tests share.

Split out of `tests/test_structure.py` in 0.2.15 (see `tests/test_plugin_size.py`
for why): the root of the repository, the readers (`read`, `flat`, `section`,
`frontmatter`, `fenced`, `fenced_quote`, `grader`, `grader_block`, `mock`,
`model_read_files`), and the constants and sentences more than one test file
checks. A name used by one test file stays in that file, beside its tests.

This module's name does not start with `test`, so `unittest discover` does not
collect it, and it defines no `TestCase`.
"""

import json
import os
import re


ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


HABIT_HEADING = "## The daily habit"


# The files that carry the block themselves. /setup, /launch and /measure
# delegate to a skill that carries it.
HABIT_CARRIERS = [
    "skills/adcopilot-connect/SKILL.md",
    "skills/adcopilot-launch/SKILL.md",
    "skills/adcopilot-measure/SKILL.md",
    # 0.2.14 (review of AdCopilot #942, item 5): a skill cannot include
    # another file, and from 0.2.7 the server leaves the offer to the skill
    # that owns the turn, so fix-checks carries the block itself.
    "skills/adcopilot-fix-checks/SKILL.md",
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


# The sentences the offer is made in, one per surface, with the finding in the
# braces (0.2.11: right after the first finding the morning check also reads,
# tied to it, with the value line). The eval graders look for their substance,
# so a reword is a deliberate act, made here too.
OFFER_CHAT = ("A read-only check that runs by itself every weekday at 8:07 "
              "would have caught {the finding} on its first morning, opening "
              "with \"All clear\" or \"Needs a look\" plus one yes/no fix. If "
              "you say \"schedule it\", I'll walk you through saving it as a "
              "Claude scheduled task, about two minutes.")


OFFER_CODE = ("A read-only check that runs by itself every weekday at 8:07 "
              "would have caught {the finding} on its first morning, opening "
              "with \"All clear\" or \"Needs a look\" plus one yes/no fix. If "
              "you say \"schedule it\", I'll set it up as a Claude Code routine "
              "with /schedule.")


CHECKIN_FIRST_CALL = ("Call get_org_context first, with source "
                      "\"claude-scheduled\" and task \"AdCopilot morning "
                      "check\".")


SCHEDULED_CHECKIN = (
    "AdCopilot morning check, read-only. " + CHECKIN_FIRST_CALL + " Do not "
    "use any tool that changes my account, and do not ask me questions; if "
    "something is unknown, say so and carry on. For {account}:\n"
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


# The one place the bare marker is written (the Cursor round's review): the
# four commands that send the versioned marker send the bare one where the
# AdCopilot skills are not installed. On a versioned marker v2.41.0's
# situations.plugin_skill names the skill that owns the account's situation,
# next_step hands it the steps ("follow the AdCopilot review steps installed
# in this assistant") and the playbook's branch becomes `[PLUGIN]`; on the bare
# one plugin_version is None, so plugin_skill is None and the full branch
# comes back. It was "The one exception" until 0.2.14 (#22), when a scheduled
# run became the other (SCHEDULED_SOURCE_RULE).
NO_SKILLS = ("One exception is where the AdCopilot skills are not "
             "installed: Cursor can add this command without them, and then "
             "`adcopilot-review` is not among your skills. There, send "
             "`source: \"claude-plugin\"`, with no version, so AdCopilot hands "
             "no step to a skill that is not here, and `get_org_context`'s "
             "`next_step` and `playbook` carry those steps themselves.")


VERSIONED_COMMANDS = ("commands/audit.md", "commands/daily.md",
                      "commands/negatives.md", "commands/weekly.md")


# The sentence every file that sends the versioned marker carries, once, the
# same in each: a scheduled run sends the scheduled marker instead. Without it
# a scheduled task whose own words carry no marker (any task but AdCopilot's
# recipe) reaches the server through the review skill with the plugin marker,
# and the server never sees a scheduled run.
SCHEDULED_SOURCE_RULE = ("In a scheduled run, started by a Claude scheduled "
                         "task or a Claude Code routine with nobody there to "
                         "answer, send `source: \"claude-scheduled\"` instead, "
                         "never `claude-plugin`: `claude-scheduled` is how "
                         "AdCopilot knows the run is unattended.")


def flat(rel):
    """A file's text with every run of whitespace as one space, so a sentence
    is found wherever the file wraps it."""
    return " ".join(read(rel).split())


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


def grader_block(text, name):
    """The text of one grader in a case.yaml, from its `- name:` line to the
    next grader's."""
    start = text.index("  - name: %s\n" % name)
    end = text.find("\n  - name: ", start + 1)
    return text[start:end if end > 0 else len(text)]


def mock(case, tool):
    """The JSON a `type: fixed` mock answers with, parsed."""
    text = read("evals/%s/mocks/adcopilot/%s.md" % (case, tool))
    return json.loads(re.match(r"^---\n.*?\n---\n(.*)$", text, re.S).group(1))


def model_read_files():
    """Every skill, command and agent file the model reads, from disk."""
    found = []
    for sub in ("skills", "commands", "agents"):
        for dirpath, _dirs, names in os.walk(os.path.join(ROOT, sub)):
            for name in sorted(names):
                if name.endswith(".md"):
                    found.append(os.path.relpath(os.path.join(dirpath, name), ROOT))
    return sorted(found)


# The server's own hand-off text for a running, counted account (AdCopilot
# situations._PLUGIN_STEP["adcopilot-review"]) and its returning-customer
# sentence (_RETURNING_SENTENCE), as release/v2.41.0 words them (#829: the
# steps are followed on a greeting, a request to get started or the request
# they are for, and anything else is answered first, then the steps offered).
SERVER_REVIEW_STEP = ("The account is running and results are being counted; "
                      "on a greeting alone, a request to get started or a "
                      "question about how the ads are doing, follow the "
                      "AdCopilot review steps installed in this assistant, "
                      "answer anything else they asked first and then offer "
                      "those steps, and suggest no bidding change in the two "
                      "to three weeks after anything went live.")


SERVER_RETURNING = ("They have been here before, so open with one line on what "
                    "happened last time.")


# The hand-off for an account spending with nothing counted
# (situations._PLUGIN_STEP["adcopilot-measure"], release/v2.41.0): the real
# turn's get_org_context carried skill=adcopilot-measure, and v2.41.0 words
# that hand-off so a question is answered first.
SERVER_MEASURE_STEP = ("Money is going out and results are not being counted; "
                       "on a greeting alone, a request to get started or a "
                       "question about counting results, follow the AdCopilot "
                       "measurement steps installed in this assistant, answer "
                       "anything else they asked first and then offer those "
                       "steps, and suggest no change to how they bid until "
                       "results are counted.")


def never_grader(case_text, tool, needle=None):
    """True when the case carries a tool_used grader that allows `tool`
    (optionally only calls whose grader block contains `needle`) zero times."""
    for block in re.split(r"\n  - name: ", case_text)[1:]:
        if (re.search(r"^\s+type: tool_used\s*$", block, re.M)
                and re.search(r"^\s+tool: %s\s*$" % re.escape(tool), block, re.M)
                and (needle is None or needle in block)
                and re.search(r"^\s+max: 0\s*$", block, re.M)
                and re.search(r"^\s+min: 0\s*$", block, re.M)):
            return True
    return False
