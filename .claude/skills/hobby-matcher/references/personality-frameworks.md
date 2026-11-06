# Translating personality exams into the 8 traits

`scripts/rank_hobbies.py` does every conversion below in code, so results are the same every time. This file explains what the code does, what each exam can and cannot tell us, and which follow-up questions fill the gaps.

## Which input to prefer

1. **Built-in quiz** (`references/quiz.json`). It measures all 8 traits plus budget and time directly. Use it when the person has no results, or has results from an exam that leaves several traits unmeasured.
2. **Big Five / OCEAN** (IPIP-NEO, BFI-2, Truity, 16Personalities' underlying scores, etc.). The best-researched framework. Use percentiles 0–100.
3. **Enneagram** (type + optional wing).
4. **MBTI** four-letter type. It's popular but less reliable: about half of people get a different letter on a retest. Say so briefly when you use it, and offer the quiz as a cross-check.
5. **Free description** ("I'm a quiet bookworm who loves puzzles"). Don't convert this yourself. Ask them to take the built-in quiz, which takes about 3 minutes.

Other exams (DISC, StrengthsFinder, Holland codes, HEXACO, a test without a known framework) aren't converted automatically. Run the built-in quiz instead, and use their result only to add color to the write-up.

## Big Five → traits

Each percentile p becomes z = (p − 50) / 50, so 50 → 0 and 100 → +1.

| Trait | Formula | Reasoning |
|---|---|---|
| Social | 0.8·E + 0.2·A | Extraversion is sociability. Agreeableness adds warmth toward group activities. |
| Active | 0.25·E − 0.15·N | Weak signal: extraverts are somewhat more physically active. **Ask a follow-up.** |
| Creative | 0.8·O | Openness includes aesthetic and creative interests. |
| Outdoorsy | not measured | No Big Five factor predicts this. **Ask a follow-up.** |
| Analytical | 0.5·O + 0.3·C | Openness to ideas plus the persistence of conscientiousness. |
| Adventurous | 0.5·O + 0.3·E − 0.3·N | Novelty-seeking rises with openness and extraversion and falls with anxiety. |
| Competitive | −0.5·A + 0.2·C + 0.2·E | Low agreeableness is the strongest predictor of liking to win. |
| Patient | 0.7·C − 0.15·E | Conscientiousness is sustained, detailed effort. |

If they give scores on another scale, convert to percentiles first: 1–5 → (score − 1) × 25, and "low/medium/high" → 20 / 50 / 80.

## MBTI → traits

Each letter adds weights. The total is clamped to −1..+1.

| Letter | Adds |
|---|---|
| E / I | Social ±0.7, Active ±0.15, Adventurous ±0.2 |
| N | Creative +0.45, Adventurous +0.4, Analytical +0.2 |
| S | Creative −0.2, Adventurous −0.3, Patient +0.2 |
| T | Analytical +0.4, Competitive +0.4 |
| F | Analytical −0.2, Competitive −0.3, Social +0.15 |
| J | Patient +0.4, Adventurous −0.2 |
| P | Patient −0.3, Adventurous +0.2 |

The "−A/−T" suffix (assertive/turbulent) is ignored. Outdoorsy is not measured, and Active is weak.

## Enneagram → traits

Base profile by type. A wing adds 30% of the wing type's profile.

| Type | Profile |
|---|---|
| 1 Reformer | Patient +.6, Analytical +.3, Competitive +.2, Adventurous −.3, Creative +.1 |
| 2 Helper | Social +.8, Competitive −.4, Creative +.2 |
| 3 Achiever | Competitive +.8, Social +.4, Active +.3, Patient +.2 |
| 4 Individualist | Creative +.8, Social −.4, Adventurous +.3, Competitive −.3 |
| 5 Investigator | Analytical +.8, Social −.7, Patient +.5, Active −.3 |
| 6 Loyalist | Adventurous −.5, Social +.3, Patient +.3, Analytical +.2 |
| 7 Enthusiast | Adventurous +.9, Social +.5, Active +.4, Patient −.5 |
| 8 Challenger | Competitive +.8, Active +.4, Social +.2, Adventurous +.3 |
| 9 Peacemaker | Competitive −.7, Adventurous −.3, Outdoorsy +.2, Social +.1, Patient +.2 |

Outdoorsy is mostly unmeasured, and Active is weak.

## Follow-up questions for unmeasured traits

When the script's output says a trait is "not measured" or a "weak signal", ask the matching question and pass the answer with `--set`. Answers use the 5-point scale: strongly disagree −2, disagree −1, neutral 0, agree +1, strongly agree +2. Divide by 2 to get the trait value.

| Trait | Ask | Pass |
|---|---|---|
| Outdoorsy | "Fresh air fixes almost any mood." | `--set out=<answer/2>` |
| Active | "I get restless if I sit still for too long." | `--set act=<answer/2>` |

Always ask for budget and time as well (see quiz questions 15–16). If they skip them, the defaults (3 and 3) apply no penalty.
