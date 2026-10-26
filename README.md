# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

Sample game on Normal difficulty. The secret is 55, visible in "Developer Debug Info".

1. The game opens on Normal. The sidebar shows "Range: 1 to 100" and "Attempts allowed: 8". The banner says "Guess a number between 1 and 100."
2. The player enters 40 and clicks Submit Guess. The hint says "Go HIGHER!" and the score drops to -5.
3. The player enters 70. The hint says "Go LOWER!" and the score drops to -10.
4. The player enters 0. The game shows "Guess must be between 1 and 100." The guess is rejected, the score stays at -10, and the guess still uses up an attempt.
5. The player enters 55.5. The game shows "Enter a whole number."
6. The player enters abc. The game shows "That is not a number."
7. The player enters 55. Balloons appear and the game shows "You won! The secret was 55. Final score: 10."
8. Submitting again shows "You already won. Start a new game to play again."
9. The player clicks New Game. The score returns to 0, the history clears, and a new secret is picked from the current difficulty's range.

note: Submit button sometimes needs a second click right after typing to actually process the entry. 

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ============= test session starts ==============
collected 15 items                             

tests/test_game_logic.py::test_winning_guess PASSED [  6%]
tests/test_game_logic.py::test_guess_too_high PASSED [ 13%]
tests/test_game_logic.py::test_guess_too_low PASSED [ 20%]
tests/test_game_logic.py::test_too_high_hint_says_go_lower PASSED [ 26%]
tests/test_game_logic.py::test_too_low_hint_says_go_higher PASSED [ 33%]
tests/test_game_logic.py::test_parse_guess_rejects_zero PASSED [ 40%]
tests/test_game_logic.py::test_parse_guess_rejects_large_negative PASSED [ 46%]
tests/test_game_logic.py::test_parse_guess_rejects_above_high PASSED [ 53%]
tests/test_game_logic.py::test_parse_guess_accepts_bounds PASSED [ 60%]
tests/test_game_logic.py::test_parse_guess_rejects_decimal_above_high PASSED [ 66%]
tests/test_game_logic.py::test_parse_guess_rejects_decimal_in_range PASSED [ 73%]
tests/test_game_logic.py::test_parse_guess_rejects_non_numeric PASSED [ 80%]
tests/test_game_logic.py::test_parse_guess_rejects_empty_and_none PASSED [ 86%]
tests/test_game_logic.py::test_get_range_for_difficulty PASSED [ 93%]
tests/test_game_logic.py::test_get_range_for_difficulty_unknown_defaults_to_normal PASSED [100%]

============== 15 passed in 0.02s ==============
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
