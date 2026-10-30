# Validation plan

This project makes one claim: a pre-shot commit card and an honest post-shot reframe
make golfers feel more committed over the ball. It does not predict shot outcomes.
Until the tests below pass, treat it as unproven.

## Test 1: hand-run pilot (before building any UI)
Text 5 golfers the commit card before each shot for one round (copy it from the CLI).
After the round ask: did it help you commit? Would you use it again?

**Kill signal:** fewer than 3 of 5 would use it again.

## Test 2: friction
Median time from opening the app to a usable card must be under 10 seconds.

**Kill signal:** golfers skip it on the course because it slows them down.

## Test 3: novelty decay
Same golfers, 4 rounds. Does usage hold?

**Kill signal:** usage drops below 50% by round 4.

## Known risks
- Cue and fix text is a starter set. It must be reviewed by a qualified coach.
- Wind/lie multipliers are rules of thumb and need tuning.
- Phone use on course affects pace of play.
