# Worked example: MBTI input with follow-ups

This is a real run of the skill. The numbers come from `rank_hobbies.py`. Use it as the model for tone, length and order.

---

**User:** I'm an INFJ and I have way too much free time since I moved. What hobby should I pick up?

**Agent (step 1, the input is clear, so go to step 3):**
Nice, an INFJ result works. Three quick things so the ranking fits your real life:
1. How much would you spend to get started? **1** almost nothing · **2** a little · **3** whatever it takes
2. How much time a week? **1** a couple of hours · **2** a few evenings · **3** whole weekends
3. Anything you already do or can't do?

**User:** 1, 2, nothing to leave out

**Agent runs:** `python scripts/rank_hobbies.py from-mbti --type INFJ --budget 1 --time 2`
The output shows Outdoorsy as "not measured" and Active as a "weak signal", so step 5 applies.

**Agent (step 5):**
MBTI doesn't say much about two things that matter for hobbies. On a scale of −2 (strongly disagree) to +2 (strongly agree):
- "Fresh air fixes almost any mood."
- "I get restless if I sit still for too long."

**User:** +2 and -1

**Agent runs:** `python scripts/rank_hobbies.py from-mbti --type INFJ --set out=1 --set act=-0.5 --budget 1 --time 2`

**Agent (step 6, final answer):**

## Your hobby fortune

You come across as outdoorsy, independent and easygoing: you recharge on your own, and you'd rather be outside than indoors, as long as the pace is calm. You'd spend almost nothing to start and have a few evenings a week.

### Your top 3

**1. Birdwatching: 86% match**
Being outside resets you, and you have the patience to wait and watch. It's quiet, solo-friendly, and free.
*First step:* Get a free bird ID app and log 5 species in a park. · *Cost:* $ · *Time:* light

**2. Gardening: 85% match**
Same outdoor reset, plus slow and steady progress you can see.
*First step:* Grow basil and mint on a sunny windowsill. · *Cost:* $ · *Time:* medium

**3. Watercolor painting: 82% match**
Your creative side, at a calm pace, on your own schedule.
*First step:* Get a student pan set and paint one lemon. · *Cost:* $ · *Time:* light

### Full ranking, most to least likely to be enjoyed

| # | Hobby | Match | Category | Cost | Time |
|---:|---|---:|---|---|---|
| 1 | Birdwatching | 86% | Outdoors | $ | light |
| 2 | Gardening | 85% | Outdoors | $ | medium |
| 3 | Watercolor painting | 82% | Creative | $ | light |
| 4 | Foraging | 78% | Outdoors | $ | medium |
| 5 | Hiking | 76% | Outdoors | $ | medium |
| 6 | Creative writing | 75% | Creative | $ | light |
| 7 | Journaling | 74% | Creative | $ | light |
| 8 | Calligraphy | 72% | Creative | $ | light |
| 9 | Photography | 67% | Creative | $$ | light |
| 10 | Baking bread | 67% | Making | $ | light |
| … | *(rows 11–41 continue in script order)* | | | | |
| 42 | Surfing | 25% | Outdoors | $$$ | heavy |
| 43 | Martial arts | 20% | Active | $$ | medium |
| 44 | Escape rooms | 16% | Mind | $$ | light |

*These matches compare your answers with how each hobby usually feels in its first few months. They rank good things to try; they don't predict for sure what you'll love.*

MBTI types can change when people retake the test. Want to take the 3-minute quiz to double-check?

**Next:** Want me to re-rank with a bigger budget, or go deeper on getting started with birdwatching?

---

## What made this answer good

- It asked only what was missing: constraints, plus the two traits MBTI doesn't cover.
- Every percentage and the order come straight from the script.
- The "why" lines describe preferences, not labels.
- It used the MBTI caveat once and briefly.
- In a real answer, all 44 rows are shown. They're shortened here only to keep the example readable.
