# Hobby Matcher: an agent skill

Recommends hobbies from a person's personality. It accepts a built-in 16-question quiz, Big Five (OCEAN) percentiles, an MBTI type, or an Enneagram type, and returns all 44 hobbies in its catalog ranked from most to least likely to be enjoyed. Each hobby gets a match %, the reason it fits, and a concrete first step.

## Install

Copy this `hobby-matcher` folder into either:
- `~/.claude/skills/` to use it in every project, or
- `<project>/.claude/skills/` to use it in one project.

Then start a **new** Claude Code session, because skills load when a session starts.

## Try it

- **Self-triggering:** ask "I'm an INFJ and I have too much free time. What hobby should I pick up?" or "Can you give me a personality quiz to find a hobby?"
- **On demand:** type `/hobby-matcher`.
- **Script only:** `python scripts/rank_hobbies.py from-mbti --type INFJ --budget 1 --time 2`
- **Self-test:** `python scripts/selftest.py` (10 checks; all should pass)

Requires Python 3.8+, standard library only.

## How it meets the project criteria

| Criterion | How |
|---|---|
| **Repeatable** | A script does all scoring, so the same answers always give the same ranking. The agent never makes up percentages. `selftest.py` checks this. |
| **Useful to a defined user** | For anyone choosing a free-time activity, such as students or people new to a city, and for counselors helping them. Output always follows `assets/report-template.md`. |
| **Appropriately scoped** | The description says when to trigger (hobby ideas, personality results, wanting a quiz) and when not to (career advice, clinical assessment). Unsupported tests fall back to the built-in quiz. |
| **Reusable / Packaged** | Everything the agent needs ships in this folder: exam, hobby dataset, conversion rules, template, worked example, and a clickable web version of the quiz. |

## Folder contents

| Path | Purpose |
|---|---|
| `SKILL.md` | Trigger description and step-by-step instructions for the agent |
| `references/quiz.json` | The 16-question exam and scoring weights |
| `references/hobby-catalog.json` | Dataset: 44 hobbies scored on 8 traits, plus cost, time and first step |
| `references/trait-model.md` | The 8 traits and the matching formula |
| `references/personality-frameworks.md` | Big Five / MBTI / Enneagram conversion rules, limits, follow-up questions |
| `scripts/rank_hobbies.py` | Prints the quiz, converts exams, ranks hobbies |
| `scripts/selftest.py` | Automated checks |
| `assets/report-template.md` | Required layout of the agent's final answer |
| `assets/example-session.md` | A complete worked example conversation |
| `assets/free-time-fortune.html` | Interactive web version of the quiz (open in any browser) |

Live web version: https://jtiche.shop/AISKill/
