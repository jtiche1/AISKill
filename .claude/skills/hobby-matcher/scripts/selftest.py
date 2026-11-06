#!/usr/bin/env python3
"""Sanity checks for rank_hobbies.py. Run: python scripts/selftest.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rank_hobbies as rh  # noqa: E402

failures = 0


def check(name, ok, detail=""):
    global failures
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  -> {detail}"))
    failures += not ok


# 1. Same answers as a recorded web-quiz run must give the same top 3.
traits, _, b, t = rh.from_quiz([1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1])
top = [r["name"] for r in rh.rank(traits, b, t)[:3]]
check("quiz matches web version", top == ["Upcycling thrifted clothes", "Swimming", "Martial arts"], top)

# 2. Ranking is complete, sorted and deterministic.
r1 = rh.rank(traits, b, t)
r2 = rh.rank(traits, b, t)
check("all 44 hobbies ranked", len(r1) == 44, len(r1))
check("sorted best to worst", all(r1[i]["score"] >= r1[i + 1]["score"] for i in range(43)))
check("deterministic", [x["name"] for x in r1] == [x["name"] for x in r2])

# 3. Every converter stays inside -1..1.
for label, (tr, _) in {
    "bigfive extremes": rh.from_bigfive(100, 0, 100, 0, 100),
    "mbti ENTP": rh.from_mbti("ENTP"),
    "enneagram 7w8": rh.from_enneagram(7, 8),
}.items():
    check(f"{label} in range", all(-1 <= v <= 1 for v in tr.values()), tr)

# 4. Face validity: a strong introvert should not get group hobbies first.
intro, _ = rh.from_mbti("INTJ")
top5 = [r["category"] for r in rh.rank(intro, 3, 3)[:5]]
check("INTJ top 5 has no Social hobbies", "Social" not in top5, top5)

# 5. Constraints push expensive / time-hungry hobbies down.
tr = {k: 0.0 for k in rh.TRAITS}
rich = {r["name"]: i for i, r in enumerate(rh.rank(tr, 3, 3))}
broke = {r["name"]: i for i, r in enumerate(rh.rank(tr, 1, 1))}
check("Scuba drops with low budget/time", broke["Scuba diving"] > rich["Scuba diving"])

# 6. Exclusions remove hobbies.
names = [r["name"] for r in rh.rank(tr, 3, 3, ["Chess", " surfing "])]
check("exclude works", "Chess" not in names and "Surfing" not in names and len(names) == 42)

print("\nAll checks passed." if not failures else f"\n{failures} check(s) failed.")
sys.exit(1 if failures else 0)
