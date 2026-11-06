---
name: hobby-matcher
description: Recommends hobbies from a person's personality and returns all 44 hobbies in the catalog ranked from most to least likely to be enjoyed, each with a match %, the reason it fits, and a first step. Use when someone asks what hobby to pick up, wants hobby or free-time ideas "for my personality", shares personality-test results (Big Five/OCEAN, MBTI such as INFP, Enneagram such as 4w5) and asks what activities suit them, or wants to take a personality quiz to find a hobby. Not for career advice, clinical or mental-health assessment, or planning one specific event.
---

# Hobby Matcher

Turns personality-exam results into a ranked hobby list. The ranking is computed by a script, so the same answers always give the same list. Your job is to collect the right inputs, run the script, and explain the results clearly.

**Who this is for:** anyone deciding what to do with their free time. Typical users are students, people new to a city, people coming out of a busy period, and counselors or club leaders helping someone else choose.

**What a good result looks like:** a short profile summary, the top 3 hobbies explained in plain language with a concrete first step, and the full ranked table of all 44 hobbies. Every number comes from the script.

## Files in this skill

| File | Use it to |
|---|---|
| `scripts/rank_hobbies.py` | Print the quiz, convert any exam to the 8 traits, and rank the hobbies. Standard-library Python. |
| `scripts/selftest.py` | Check the script still works after any edit. |
| `references/quiz.json` | The 16-question exam: questions, answer options, scoring weights. |
| `references/hobby-catalog.json` | The 44 hobbies with trait profiles, cost, time and first steps. |
| `references/trait-model.md` | What the 8 traits mean and how matching works. Read it before explaining results. |
| `references/personality-frameworks.md` | How Big Five, MBTI and Enneagram convert, their limits, and follow-up questions. |
| `assets/report-template.md` | The required layout of the final answer. |
| `assets/example-session.md` | A complete worked example, from first message to final report. |
| `assets/free-time-fortune.html` | A clickable web version of the same quiz to give the person if they'd rather click than chat. |

Run scripts from this skill's folder. Use `python`, or `python3` / `py` if `python` isn't found.

## Steps

### 1. Find out what the person already has

Ask one question if it isn't already clear: "Do you have results from a personality test (Big Five, MBTI, Enneagram), or would you like to take a 3-minute quiz?"

- **Big Five, MBTI or Enneagram results** → go to step 3.
- **No results, a different test, or only a self-description** → go to step 2. Read `references/personality-frameworks.md` ("Which input to prefer") if you're unsure.
- **Results from two different tests** → use the built-in quiz if they're willing. Otherwise use the Big Five. Mention which one you used.

### 2. Give the built-in quiz

1. Run `python scripts/rank_hobbies.py print-quiz` to get the exact questions. Never reword or reorder them, because the scoring depends on them.
2. Ask the questions in four groups of four, numbered, so the person can answer quickly, e.g. `1: +1, 2: B, 3: -2, 4: C`.
   - For agree/disagree statements, show the scale once: −2 strongly disagree, −1 disagree, 0 neutral, +1 agree, +2 strongly agree.
   - For choice questions, label options A, B, C, D. Convert letters to 0-based numbers yourself (A=0, B=1…).
3. If an answer is unclear ("kind of?"), ask once about that item only. "Kind of agree" means +1.
4. Save the 16 answers to a temporary file such as `answers.json` with the content `{"answers": [ ... ]}`. Scale answers are −2..2; choice, budget and time answers are option indexes.
5. If they'd rather click, give them `assets/free-time-fortune.html` (it opens in any browser) and stop there: that page shows its own ranking. It doesn't export answers, so to get the full write-up from you they still need to answer here.

### 3. Collect constraints

If the quiz didn't already ask (questions 15–16), ask for:
- **Budget to start:** 1 almost nothing, 2 a little, 3 whatever it takes
- **Weekly time:** 1 a couple of hours, 2 a few evenings, 3 whole weekends
- **Anything to leave out:** hobbies they already do, or can't do because of health, access or location. Don't ask about health details. Only take what they choose to tell you.

### 4. Run the ranking

Pick the matching command:

```
python scripts/rank_hobbies.py from-quiz answers.json
python scripts/rank_hobbies.py from-bigfive --O 72 --C 40 --E 25 --A 66 --N 58 --budget 2 --time 1
python scripts/rank_hobbies.py from-mbti --type INFP --budget 1 --time 2
python scripts/rank_hobbies.py from-enneagram --type 4 --wing 5 --budget 2 --time 2
python scripts/rank_hobbies.py from-traits --soc 0.4 --act -0.2 ... --budget 3 --time 3
```

Add `--exclude "Chess,Yoga"` for hobbies to leave out. Use `--format json` if you need the data rather than the table.

### 5. Fill gaps, then re-run

If the output's profile table says a trait is **"not measured"** or a **"weak signal"** (common with MBTI, Big Five and Enneagram), ask the follow-up question for that trait from `references/personality-frameworks.md`. Re-run with `--set out=0.5` and/or `--set act=-0.5` (answer ÷ 2). Skip this only if the person declines, and then say the outdoor/active ranking is less certain.

### 6. Write the answer

Follow `assets/report-template.md` exactly:

1. **Profile in one or two sentences**, using the "Strongest signals" line.
2. **Top 3**, each with its match %, why it fits (from the script's "Why", reworded naturally), the first step, and cost/time.
3. **The full ranked table**, all hobbies most to least likely, copied from the script output. If the conversation is casual, show the top 10 and offer the rest.
4. **One line on limits**, from `references/trait-model.md`.

Rules:
- Never change the order or the percentages, and never add a hobby to the ranked table. If a hobby they'd clearly like isn't in the catalog, you may add it under "Also worth a look (not scored)" with a one-line reason.
- The percentages rank options. Don't call them probabilities.
- Don't diagnose, label or judge personality ("you're antisocial"). Describe preferences ("you recharge alone").
- When MBTI was the input, add one sentence noting that MBTI results can shift on a retest, and offer the quiz.
- Keep the person's answers in this conversation. Don't save them anywhere else.

### 7. Offer a next step

End with one short offer: re-rank with different budget or time, exclude something, or go deeper on one hobby.

## Checking the skill

After editing the script, quiz or catalog, run `python scripts/selftest.py`. Every check must pass. The first check confirms the script still gives the same ranking as the web quiz.
