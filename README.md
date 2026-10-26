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

**What the game is.** A number guessing game built with Streamlit. The computer picks a secret number, you guess, and it tells you to go higher or lower. Difficulty sets the range and the number of attempts: Easy is 1 to 20 with 6 attempts, Normal is 1 to 100 with 8, and Hard is 1 to 50 with 5. The starter code was AI-generated with bugs built in. The project was to find them, fix them and prove the fixes with tests.

**Bugs I found.**
- The hints were backwards. A guess above the secret said "Go HIGHER".
- The same guess could get different hints on different turns, because the game turned the secret into text on every other attempt and compared it alphabetically.
- Guesses like 0 and -100000 were accepted.
- A decimal like 100.1 was accepted and silently rounded down to 100.
- Clicking New Game after a win or loss changed the secret but left the game stuck on the game-over screen.
- The banner always said "between 1 and 100", even on Easy.

**Fixes I applied.**
- Swapped the hint messages back to output the correct directions.
- Removed the code that turned the secret number into text, so guesses are compared as numbers rather than words.
- Added a range check, and decimals are now rejected with "Enter a whole number."
- New Game now resets the status, score and history, and picks the secret from the selected difficulty.
- The banner now shows the real range for the chosen difficulty.
- Moved all four game-rule functions into `logic_utils.py`, so `app.py` only handles the screen and the game state. This lets the tests check the rules without starting the app.
- Added 15 pytest tests, including one that would have caught each bug above.

**Known issues I have not yet fixed.**
- Invalid guesses use up an attempt, and "Attempts left" can go below zero without ending the game. The counter also starts one attempt early, so a new Normal game shows 7 left instead of 8.
- The scoring is odd: a Too High guess adds 5 points on even attempts and subtracts 5 on odd ones, and winning on the first guess scores 70, not 100.
- The Submit button sometimes needs a second click right after typing.

The full bug log, replay trace and notes on working with AI are in [reflection.md](reflection.md).

## 📸 Demo Walkthrough


Sample game on Normal difficulty. 
The secret is 55, visible in "Developer Debug Info" 

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

- Challenge 1: edge-case tests for decimals, non-numeric text, empty input, `None` and out-of-range guesses are in `tests/test_game_logic.py`. The passing output is under Test Results above. Prompts and rationale are in `ai_interactions.md`.
