"""
caddie.core: commit card + honest miss reframe.
Rule-based on purpose: no probabilities, no LLM in the decision path.
Python 3.10+
"""
from dataclasses import dataclass

# ---------------------------------------------------------------- inputs
@dataclass
class Situation:
    distance_to_pin: int              # yards
    lie: str = "fairway"              # fairway | rough | uphill | downhill | bunker
    wind_mph: int = 0
    wind_dir: str = "none"            # head | tail | cross | none
    hazard: str | None = None         # left | right | short | long
    pin: str = "middle"               # front | middle | back

@dataclass
class Bag:
    carries: dict                     # self-reported carry, e.g. {"9i": 130, "8i": 142}
    common_miss: str = "none"         # chunk | thin | push | pull | slice | hook | shank | none

# ---------------------------------------------------------------- tables
LIE_FACTOR = {"fairway": 1.00, "rough": 1.08, "uphill": 1.05, "downhill": 0.95, "bunker": 1.10}
PIN_TO_CENTER = {"front": +4, "middle": 0, "back": -4}   # we aim at green center, not the pin
OPPOSITE = {"left": "right", "right": "left", "short": "long", "long": "short"}

CUES = {  # starter cues; have a coach sanity-check these
    "chunk": "Weight slightly forward, brush the grass AFTER the ball.",
    "thin": "Keep your chest over the ball through impact.",
    "push": "Feel the clubface finish pointing at the target.",
    "pull": "Swing out to the right field, finish balanced.",
    "slice": "Light grip, rotate your forearms through the ball.",
    "hook": "Quiet hands, finish tall.",
    "shank": "Weight on the middle of your feet, ball slightly further away.",
    "none": "Pick a spot, exhale, commit.",
}

# kind: "contact" -> praise start line if user says it was on target
#       "direction" -> praise contact if user says it was solid
#       "none" -> no automatic praise
MISSES = {
    "chunk": dict(kind="contact", cause="Low point landed behind the ball.",
                  fix="Weight a touch forward, ball position center, brush the turf after the ball."),
    "thin": dict(kind="contact", cause="Club met the ball on the way up.",
                 fix="Stay in your posture, chest over the ball through impact."),
    "push": dict(kind="direction", cause="Face or path started right.",
                 fix="Finish with the face pointing at the target."),
    "pull": dict(kind="direction", cause="Face or path started left.",
                 fix="Hold your finish and check your aim before you start."),
    "slice": dict(kind="direction", cause="Face was open to the path.",
                  fix="Lighter grip pressure, rotate through."),
    "hook": dict(kind="direction", cause="Face was closed to the path.",
                 fix="Quieter hands, aim a touch right."),
    "shank": dict(kind="none", cause="Contact came off the hosel, usually from standing too close or the weight moving toward your toes.",
                  fix="Set up a little further from the ball, weight mid-foot. One swing, not a verdict."),
}

# ---------------------------------------------------------------- commit card
def effective_distance(s: Situation) -> float:
    d = s.distance_to_pin + PIN_TO_CENTER[s.pin]
    if s.wind_dir == "head":
        d *= 1 + 0.01 * s.wind_mph
    elif s.wind_dir == "tail":
        d *= 1 - 0.005 * s.wind_mph
    return d * LIE_FACTOR[s.lie]

def pick_club(eff: float, carries: dict, hazard: str | None) -> tuple[str, str | None]:
    ordered = sorted(carries.items(), key=lambda kv: kv[1])   # short -> long
    if hazard == "short":
        eff += 5                      # guard the trouble: take more club
    enough = [c for c, y in ordered if y >= eff]
    if hazard == "long":              # trouble behind: prefer the club that tops out near the target
        under = [c for c, y in ordered if y <= eff + 2]
        if under:
            return under[-1], None
    if enough:
        return enough[0], None
    return ordered[-1][0], "Green is out of range for your longest club. Play to your favorite layup number."

def commit_card(s: Situation, bag: Bag) -> str:
    eff = effective_distance(s)
    club, warn = pick_club(eff, bag.carries, s.hazard)
    if s.hazard in ("left", "right"):
        target = f"Center of the green, favoring the {OPPOSITE[s.hazard]} side."
        safe = f"Miss {OPPOSITE[s.hazard]} and you're fine."
    elif s.hazard in ("short", "long"):
        target = "Center of the green."
        safe = f"Miss {OPPOSITE[s.hazard]} and you're fine."
    else:
        target = "Center of the green."
        safe = "Anywhere on the green side is a good result."
    lines = [
        f"CLUB:   {club}  (plays like {round(eff)} yds)",
        f"TARGET: {target}",
        f"SAFE:   {safe}",
        f"CUE:    {CUES.get(bag.common_miss, CUES['none'])}",
    ]
    if s.wind_dir == "cross":
        lines.insert(2, "WIND:   Crosswind. Aim slightly into it, don't try to steer.")
    if warn:
        lines.append(f"NOTE:   {warn}")
    return "\n".join(lines)

# ---------------------------------------------------------------- reframe
def reframe(result: str, start_line_ok: bool | None = None,
            contact_ok: bool | None = None, consecutive_misses: int = 0) -> str:
    """
    result: 'pure' or a key of MISSES.
    Praise lines are only emitted when the USER confirmed them (True).
    None/False never produces praise, so the app can't flatter a bad swing.
    """
    if result == "pure":
        return "Committed swing, clean result. Same routine next shot."
    m = MISSES[result]
    parts = []
    if m["kind"] == "contact" and start_line_ok is True:
        parts.append("Your start line was on target. The miss was contact, not direction.")
    if m["kind"] == "direction" and contact_ok is True:
        parts.append("Contact was solid. The miss was face/path, not strike.")
    parts.append(m["cause"])
    parts.append("Next shot: " + m["fix"])
    if consecutive_misses >= 2:  # anti death-spiral
        parts.append("Two in a row happens to everyone. Drop the swing thought: target, exhale, commit.")
    return " ".join(parts)

# ---------------------------------------------------------------- demo
if __name__ == "__main__":
    bag = Bag(carries={"9i": 130, "8i": 140, "7i": 150, "6i": 160}, common_miss="chunk")
    s = Situation(distance_to_pin=148, wind_mph=8, wind_dir="head", hazard="right", pin="back")
    print(commit_card(s, bag), "\n")
    print(reframe("chunk", start_line_ok=True), "\n")
    print(reframe("chunk", start_line_ok=None, consecutive_misses=2), "\n")
    print(reframe("push", contact_ok=True))
