from caddie.core import Bag, Situation, commit_card, pick_club, reframe, effective_distance

CARRIES = {"9i": 130, "8i": 140, "7i": 150, "6i": 160}


def test_flat_150_picks_7i():
    club, warn = pick_club(150, CARRIES, None)
    assert club == "7i" and warn is None


def test_headwind_adds_club():
    s = Situation(distance_to_pin=150, wind_mph=10, wind_dir="head")
    assert effective_distance(s) > 150
    assert pick_club(effective_distance(s), CARRIES, None)[0] == "6i"


def test_hazard_short_takes_more_club():
    assert pick_club(150, CARRIES, "short")[0] == "6i"


def test_hazard_long_does_not_overclub():
    assert pick_club(145, CARRIES, None)[0] == "7i"
    assert pick_club(145, CARRIES, "long")[0] == "8i"


def test_out_of_range_warns():
    club, warn = pick_club(220, CARRIES, None)
    assert club == "6i" and warn


def test_card_states_safe_miss_opposite_hazard():
    card = commit_card(Situation(150, hazard="right"), Bag(CARRIES))
    assert "Miss left and you're fine." in card


def test_card_targets_center_not_pin():
    card = commit_card(Situation(150, pin="back"), Bag(CARRIES))
    assert "Center of the green" in card


def test_crosswind_line():
    card = commit_card(Situation(150, wind_mph=10, wind_dir="cross"), Bag(CARRIES))
    assert "Crosswind" in card


# --- the honesty rules -----------------------------------------------------

def test_no_praise_unless_confirmed():
    assert "start line" not in reframe("chunk")
    assert "start line" not in reframe("chunk", start_line_ok=None)
    assert "start line" not in reframe("chunk", start_line_ok=False)
    assert "start line was on target" in reframe("chunk", start_line_ok=True)


def test_direction_miss_praises_contact_only_if_confirmed():
    assert "Contact was solid" not in reframe("push")
    assert "Contact was solid" in reframe("push", contact_ok=True)


def test_shank_never_gets_automatic_praise():
    out = reframe("shank", start_line_ok=True, contact_ok=True)
    assert "on target" not in out and "solid" not in out


def test_every_reframe_has_a_next_shot_cue():
    from caddie.core import MISSES
    for key in MISSES:
        assert "Next shot:" in reframe(key)


def test_tilt_guard_after_two_misses():
    assert "Two in a row" in reframe("thin", consecutive_misses=2)
    assert "Two in a row" not in reframe("thin", consecutive_misses=1)


def test_pure_shot_praises_process_not_luck():
    assert "routine" in reframe("pure")
