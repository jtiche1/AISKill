# The 8-trait hobby model

Every personality exam the skill accepts is translated into these eight traits. Each trait is a number from **-1 to +1**. 0 means neutral or unknown. The same eight traits score every hobby in `hobby-catalog.json`, which is what makes a person and a hobby comparable.

| Key | Trait (+) | Opposite (−) | What +1 looks like | What −1 looks like |
|---|---|---|---|---|
| `soc` | Social | Independent | Energized by groups, wants company | Recharges alone, prefers solo time |
| `act` | Active | Easygoing | Restless when still, wants to move | Prefers low-key, seated activities |
| `cre` | Creative | Structured | Wants to make and express things | Prefers clear rules and set methods |
| `out` | Outdoorsy | Homebody | Fresh air resets their mood | Happiest indoors |
| `ana` | Analytical | Intuitive | Loves puzzles and how things work | Goes by feel more than figuring out |
| `nov` | Adventurous | Steady | Chases new experiences and thrills | Enjoys familiar comforts |
| `com` | Competitive | Laid-back | Likes to win and keep score | Not interested in winning |
| `pat` | Patient | Spontaneous | Can focus on detail for hours | Wants quick payoffs |

Two **practical constraints** sit beside the traits:

| Key | 1 | 2 | 3 (default) |
|---|---|---|---|
| `budget` | Almost nothing | A little (a class or some gear) | Whatever it takes |
| `time` | A couple of hours a week | A few evenings a week | Whole weekends |

## How matching works

For each hobby, the script measures how far the person's eight scores are from the hobby's eight scores. Traits the hobby depends on heavily count more: weight = 0.35 + |hobby score|. The match is 1 minus the weighted average distance. Then:

- −0.07 for each budget level the hobby is above the person's budget
- −0.06 for each time level the hobby is above the person's time

The score is shown as a 1–99% match. Percentages are for **ranking only**. They are not probabilities, so don't present "83%" as "83% chance you'll enjoy it."

## How the hobby profiles were set

Each hobby was scored by asking what a typical beginner experiences in its first few months: who they do it with, how physical it is, whether it's indoors or out, whether there's a winner, and how much patient practice it needs before it's fun. Cost and time describe getting started, not mastery.

## Limits to tell people about

- The catalog has 44 hobbies. Someone's ideal hobby may not be in it. The skill may suggest a close cousin (see SKILL.md, step 6), but it never invents a match percentage for it.
- Personality explains part of hobby enjoyment. Access, health, culture, friends and plain chance matter too. The ranking is a list of good things to try, not a verdict.
