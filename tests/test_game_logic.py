from logic_utils import check_guess, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_too_high_hint_says_go_lower():
    # Regression: the hint messages were swapped
    _, message = check_guess(60, 50)
    assert "LOWER" in message

def test_too_low_hint_says_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message

def test_parse_guess_rejects_zero():
    # Regression: out-of-range guesses were accepted
    ok, value, err = parse_guess("0", 1, 100)
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_rejects_large_negative():
    ok, value, err = parse_guess("-100000", 1, 100)
    assert ok is False

def test_parse_guess_rejects_above_high():
    ok, value, err = parse_guess("101", 1, 100)
    assert ok is False

def test_parse_guess_accepts_bounds():
    assert parse_guess("1", 1, 100)[:2] == (True, 1)
    assert parse_guess("100", 1, 100)[:2] == (True, 100)
