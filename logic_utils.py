# FIX: Moved from app.py into logic_utils.py unchanged. Done with Claude Code.
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100

# FIX: Moved from app.py and added a proper low/high range check so 0 and negatives are rejected. Done with Claude Code in a separate session.

def parse_guess(raw: str, low: int, high: int):
    """
    Parse user input into an int guess within [low, high].

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    # FIX: Decimals are rejected. int(float("100.1")) used to truncate to 100
    # and slip past the range check.
    try:
        value = int(raw)
    except ValueError:
        if "." in raw:
            return False, None, "Enter a whole number."
        return False, None, "That is not a number."

    if value < low or value > high:
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None

# FIX: Moved from app.py, swapped the hint messages and removed the str-compare fallback. Done with Claude Code in its own chat session.

def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"

    return "Too Low", "📈 Go HIGHER!"


# FIX: Moved from app.py into logic_utils.py unchanged. Scoring rules are
# still the original ones. Done with Claude Code.
def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
