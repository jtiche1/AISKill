#!/usr/bin/env python3
"""Rank 44 hobbies for a person from personality-exam results.

Every input is converted to the same 8-trait profile (each trait -1..+1),
then compared against references/hobby-catalog.json. Standard library only.

Subcommands
  print-quiz                        Print the 16-question exam to administer.
  from-quiz     ANSWERS.json        Score the built-in exam ({"answers": [...]}).
  from-bigfive  --O --C --E --A --N Big Five / OCEAN percentiles 0-100.
  from-mbti     --type INFP         Myers-Briggs four-letter type.
  from-enneagram --type 4 [--wing 5]
  from-traits   --soc .. --pat      An 8-trait profile you already have.

Shared options
  --budget 1|2|3   1 almost nothing, 2 a little, 3 whatever it takes (default 3)
  --time   1|2|3   1 a couple of hours/week, 2 a few evenings, 3 whole weekends (default 3)
  --set trait=value   Override or fill one trait, e.g. --set out=0.5 (repeatable)
  --exclude "Chess,Surfing"   Hobbies to leave out (already does them, can't do them)
  --top N          Rows to show (default: all 44)
  --format md|json Output format (default md)
"""
import argparse
import json
import os
import sys

TRAITS = ["soc", "act", "cre", "out", "ana", "nov", "com", "pat"]
LABEL = {"soc": "Social", "act": "Active", "cre": "Creative", "out": "Outdoorsy",
         "ana": "Analytical", "nov": "Adventurous", "com": "Competitive", "pat": "Patient"}
OPPOSITE = {"soc": "Independent", "act": "Easygoing", "cre": "Structured", "out": "Homebody",
            "ana": "Intuitive", "nov": "Steady", "com": "Laid-back", "pat": "Spontaneous"}
PHRASE = {
    "soc": ("you light up around people", "you guard your solo time"),
    "act": ("you need to move", "you like to keep things low-key"),
    "cre": ("you want to make things", "you like a clear structure"),
    "out": ("fresh air resets you", "you're happiest indoors"),
    "ana": ("you love a good puzzle", "you'd rather feel it than figure it out"),
    "nov": ("you chase new experiences", "you enjoy familiar comforts"),
    "com": ("you like to win", "you're not here to keep score"),
    "pat": ("you can focus for hours", "you like a quick payoff"),
}
BUDGET = {1: "almost nothing", 2: "a little", 3: "whatever it takes"}
TIME = {1: "a couple of hours a week", 2: "a few evenings a week", 3: "whole weekends"}

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "references")


def load(name):
    with open(os.path.join(REF, name), encoding="utf-8") as f:
        return json.load(f)


def clamp(v):
    return max(-1.0, min(1.0, v))


# ---------- converters: each returns (traits, source-per-trait) ----------

def from_quiz(answers):
    qs = load("quiz.json")["questions"]
    if len(answers) != len(qs):
        sys.exit(f"Expected {len(qs)} answers, got {len(answers)}.")
    raw = {t: 0.0 for t in TRAITS}
    maxabs = {t: 0.0 for t in TRAITS}
    budget = time = 3
    for q, a in zip(qs, answers):
        if q["type"] == "scale":
            if a not in (-2, -1, 0, 1, 2):
                sys.exit(f"Scale answer must be -2..2, got {a!r} for: {q['q']}")
            for k, w in q["d"].items():
                raw[k] += a * w
                maxabs[k] += 2 * abs(w)
        elif q["type"] in ("budget", "time"):
            v = q["opts"][a]["v"]
            budget, time = (v, time) if q["type"] == "budget" else (budget, v)
        else:
            for k, w in q["opts"][a]["d"].items():
                raw[k] += w
            for k in TRAITS:
                maxabs[k] += max(abs(o["d"].get(k, 0)) for o in q["opts"])
    traits = {k: clamp(raw[k] / maxabs[k] * 1.6) if maxabs[k] else 0.0 for k in TRAITS}
    return traits, {k: "quiz" for k in TRAITS}, budget, time


def from_bigfive(O, C, E, A, N):
    z = {k: clamp((v - 50) / 50) for k, v in dict(O=O, C=C, E=E, A=A, N=N).items()}
    t = {
        "soc": 0.8 * z["E"] + 0.2 * z["A"],
        "act": 0.25 * z["E"] - 0.15 * z["N"],
        "cre": 0.8 * z["O"],
        "out": 0.0,
        "ana": 0.5 * z["O"] + 0.3 * z["C"],
        "nov": 0.5 * z["O"] + 0.3 * z["E"] - 0.3 * z["N"],
        "com": -0.5 * z["A"] + 0.2 * z["C"] + 0.2 * z["E"],
        "pat": 0.7 * z["C"] - 0.15 * z["E"],
    }
    src = {k: "Big Five" for k in TRAITS}
    src["act"] = "Big Five (weak signal)"
    src["out"] = "not measured"
    return {k: clamp(v) for k, v in t.items()}, src


MBTI_LETTERS = {
    "E": {"soc": .7, "act": .15, "nov": .2}, "I": {"soc": -.7, "act": -.15, "nov": -.2},
    "N": {"cre": .45, "nov": .4, "ana": .2}, "S": {"cre": -.2, "nov": -.3, "pat": .2},
    "T": {"ana": .4, "com": .4}, "F": {"ana": -.2, "com": -.3, "soc": .15},
    "J": {"pat": .4, "nov": -.2}, "P": {"pat": -.3, "nov": .2},
}


def from_mbti(code):
    code = code.strip().upper()[:4]
    if len(code) != 4 or any(c not in MBTI_LETTERS for c in code) \
            or code[0] not in "EI" or code[1] not in "NS" or code[2] not in "TF" or code[3] not in "JP":
        sys.exit(f"Not a valid MBTI type: {code!r} (expected e.g. INFP).")
    t = {k: 0.0 for k in TRAITS}
    for c in code:
        for k, w in MBTI_LETTERS[c].items():
            t[k] += w
    src = {k: "MBTI" for k in TRAITS}
    src["act"] = "MBTI (weak signal)"
    src["out"] = "not measured"
    return {k: clamp(v) for k, v in t.items()}, src


ENNEAGRAM = {
    1: {"pat": .6, "ana": .3, "com": .2, "nov": -.3, "cre": .1},
    2: {"soc": .8, "com": -.4, "cre": .2},
    3: {"com": .8, "soc": .4, "act": .3, "pat": .2},
    4: {"cre": .8, "soc": -.4, "nov": .3, "com": -.3},
    5: {"ana": .8, "soc": -.7, "pat": .5, "act": -.3},
    6: {"nov": -.5, "soc": .3, "pat": .3, "ana": .2},
    7: {"nov": .9, "soc": .5, "act": .4, "pat": -.5},
    8: {"com": .8, "act": .4, "soc": .2, "nov": .3},
    9: {"com": -.7, "nov": -.3, "out": .2, "soc": .1, "pat": .2},
}


def from_enneagram(kind, wing=None):
    if kind not in ENNEAGRAM or (wing is not None and wing not in ENNEAGRAM):
        sys.exit("Enneagram type and wing must be 1-9.")
    t = {k: ENNEAGRAM[kind].get(k, 0.0) for k in TRAITS}
    if wing:
        for k, w in ENNEAGRAM[wing].items():
            t[k] += 0.3 * w
    src = {k: "Enneagram" for k in TRAITS}
    src["act"] = "Enneagram (weak signal)"
    src["out"] = "not measured"
    return {k: clamp(v) for k, v in t.items()}, src


# ---------- matching (same formula as the web quiz) ----------

def why_for(h, traits, budget, time, pct=100):
    if pct < 45:
        k = max(TRAITS, key=lambda k: abs(h["profile"][k]) * abs(traits[k] - h["profile"][k]))
        need = (LABEL[k] if h["profile"][k] > 0 else OPPOSITE[k]).lower()
        need = "a homebody" if need == "homebody" else need
        return f"Weak fit: it rewards being {need}, and {PHRASE[k][0 if traits[k] > 0 else 1]}."
    fits = []
    for k in TRAITS:
        hv = h["profile"][k]
        s = hv * traits[k]
        if s > 0.08 and abs(hv) >= 0.4:
            fits.append((s, PHRASE[k][0 if traits[k] > 0 else 1]))
    fits = [p for _, p in sorted(fits, reverse=True)[:2]]
    notes = []
    if h["cost"] > budget:
        notes.append("it costs more to start than you'd like")
    if h["time"] > time:
        notes.append("it wants more time than you have")
    s = ("Fits because " + " and ".join(fits) + ".") if fits else \
        "A wildcard: it doesn't lean hard on your strongest traits."
    if notes:
        s += " Watch out: " + ", and ".join(notes) + "."
    return s


def rank(traits, budget, time, exclude=()):
    excl = {e.strip().lower() for e in exclude if e.strip()}
    out = []
    for h in load("hobby-catalog.json")["hobbies"]:
        if h["name"].lower() in excl:
            continue
        num = den = 0.0
        for k in TRAITS:
            hv = h["profile"][k]
            w = 0.35 + abs(hv)
            num += w * abs(traits[k] - hv)
            den += w * 2
        m = 1 - num / den
        if h["cost"] > budget:
            m -= 0.07 * (h["cost"] - budget)
        if h["time"] > time:
            m -= 0.06 * (h["time"] - time)
        pct = round(max(1, min(99, (m - 0.35) / 0.6 * 100)))
        out.append({**h, "match": pct, "score": round(m, 4), "why": why_for(h, traits, budget, time, pct)})
    return sorted(out, key=lambda r: -r["score"])


def top_traits(traits):
    ordered = sorted(TRAITS, key=lambda k: -abs(traits[k]))[:3]
    return [LABEL[k] if traits[k] >= 0 else OPPOSITE[k] for k in ordered]


# ---------- output ----------

def bar(v):
    n = round((v + 1) * 5)
    return "█" * n + "░" * (10 - n)


def render_md(traits, src, budget, time, ranked, top):
    lines = ["## Trait profile", "", "| Trait | Score | -1 ··· +1 | Source |", "|---|---:|---|---|"]
    for k in TRAITS:
        lines.append(f"| {LABEL[k]} | {traits[k]:+.2f} | `{bar(traits[k])}` | {src[k]} |")
    lines += ["", f"**Strongest signals:** {', '.join(top_traits(traits))}  ",
              f"**Budget:** {BUDGET[budget]} · **Time:** {TIME[time]}", ""]
    missing = [LABEL[k] for k in TRAITS if src[k] == "not measured"]
    if missing:
        lines += [f"> Not measured by this exam: {', '.join(missing)}. Treated as neutral (0). "
                  "Ask the follow-up questions in SKILL.md to fill them.", ""]
    lines += ["## Ranked hobbies (most to least likely to be enjoyed)", "",
              "| # | Hobby | Match | Category | Cost | Time | Why | First step |",
              "|---:|---|---:|---|---|---|---|---|"]
    for i, r in enumerate(ranked[:top], 1):
        lines.append(f"| {i} | {r['name']} | {r['match']}% | {r['category']} | {'$' * r['cost']} | "
                     f"{['', 'light', 'medium', 'heavy'][r['time']]} | {r['why']} | {r['first_step']} |")
    return "\n".join(lines)


def print_quiz():
    for i, q in enumerate(load("quiz.json")["questions"], 1):
        if q["type"] == "scale":
            print(f"{i}. {q['q']}  (answer -2 strongly disagree … +2 strongly agree)")
        else:
            opts = "  ".join(f"[{j}] {o['t']}" for j, o in enumerate(q["opts"]))
            print(f"{i}. {q['q']}  {opts}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("print-quiz")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--budget", type=int, choices=[1, 2, 3])
    common.add_argument("--time", type=int, choices=[1, 2, 3])
    common.add_argument("--set", action="append", default=[], metavar="TRAIT=VALUE")
    common.add_argument("--exclude", default="")
    common.add_argument("--top", type=int, default=44)
    common.add_argument("--format", choices=["md", "json"], default="md")
    p = sub.add_parser("from-quiz", parents=[common]); p.add_argument("answers")
    p = sub.add_parser("from-bigfive", parents=[common])
    for k in "OCEAN":
        p.add_argument(f"--{k}", type=float, required=True, help="percentile 0-100")
    p = sub.add_parser("from-mbti", parents=[common]); p.add_argument("--type", required=True)
    p = sub.add_parser("from-enneagram", parents=[common])
    p.add_argument("--type", type=int, required=True); p.add_argument("--wing", type=int)
    p = sub.add_parser("from-traits", parents=[common])
    for k in TRAITS:
        p.add_argument(f"--{k}", type=float, default=0.0)
    a = ap.parse_args()

    if a.cmd == "print-quiz":
        print_quiz(); return
    budget = time = 3
    if a.cmd == "from-quiz":
        with open(a.answers, encoding="utf-8-sig") as f:
            traits, src, budget, time = from_quiz(json.load(f)["answers"])
    elif a.cmd == "from-bigfive":
        traits, src = from_bigfive(a.O, a.C, a.E, a.A, a.N)
    elif a.cmd == "from-mbti":
        traits, src = from_mbti(a.type)
    elif a.cmd == "from-enneagram":
        traits, src = from_enneagram(a.type, a.wing)
    else:
        traits = {k: clamp(getattr(a, k)) for k in TRAITS}
        src = {k: "given" for k in TRAITS}
    for kv in a.set:
        k, _, v = kv.partition("=")
        if k not in TRAITS:
            sys.exit(f"Unknown trait {k!r}; use one of {', '.join(TRAITS)}.")
        traits[k], src[k] = clamp(float(v)), "follow-up answer"
    budget = a.budget or budget
    time = a.time or time

    ranked = rank(traits, budget, time, a.exclude.split(","))
    if a.format == "json":
        print(json.dumps({"traits": traits, "sources": src, "budget": budget, "time": time,
                          "top_traits": top_traits(traits), "ranking": ranked[:a.top]}, indent=1, ensure_ascii=False))
    else:
        print(render_md(traits, src, budget, time, ranked, a.top))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
