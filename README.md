# Safe Miss

A pre-shot **commit card** and an honest post-shot **reframe** for golfers who lose
confidence over the ball.

> Encourage the process, never fake the outcome.

## What it does
1. **Commit card:** given distance, lie, wind, hazard and pin position, it returns a
   club, a conservative target (center of the green), the *safe miss*, and one cue.
2. **Reframe:** after a miss, it names what actually happened and gives one next-shot fix.
   Praise ("your start line was on target") appears **only if you confirm it**, so the
   app can't flatter a bad swing.
3. **Tilt guard:** after two misses in a row it drops the swing thoughts and falls back
   to the routine.

## What it deliberately does not do
- No win probabilities or "you have a 71% chance" claims. Range data doesn't predict
  course results, and a precise number on biased data is a well-formatted lie.
- No LLM in the club/target logic. It's rule-based so it's predictable and testable.

## Example
```
CLUB:   6i  (plays like 156 yds)
TARGET: Center of the green, favoring the left side.
SAFE:   Miss left and you're fine.
CUE:    Weight slightly forward, brush the grass AFTER the ball.
```

## Run it
```bash
python -m caddie.core        # demo
pip install pytest && pytest # tests
```

## Roadmap
- [x] Rule-based commit card + reframe engine, with tests
- [ ] FastAPI: `POST /card`, `POST /reframe`
- [ ] Phone-first input screen (under 10 seconds)
- [ ] One home course mapped by hand (hazards per hole)
- [ ] Pilot with 5 golfers, see `docs/VALIDATION.md`
- [ ] Optional LLM layer for *wording only*

## Status
Early prototype. Cue text and distance multipliers are starter values and need review
by a qualified coach.

## License
MIT
