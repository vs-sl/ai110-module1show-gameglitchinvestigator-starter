# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The hints seemed to give guidance opposite of the solution. Ie: guessed 20, 10, 1 against a secret of 35 and was told to go lower. I found three bugs: swapped hint messages, a secret that became a string on even attempts so guesses were compared alphabetically, and no range check, so 0 and -100000 were accepted.
Additional errors were as follows: Clicking New Game after a win or loss changed the secret in the debug panel but left me on the game-over screen until I reloaded the page. The game incorrectly accepted 100.1 as valid. Invalid inputs used up attempts but never ended the game, so "Attempts left" went negative. 
The score changes were not intuitive. The cause is `update_score`: a Too High guess adds 5 on even attempts and subtracts 5 on odd ones, and the win formula uses `attempt_number + 1`, so a win on attempt 2 scores 70 and a win on attempt 8 scores 10.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output | Suspected Code Location |
|---|---|---|---|---|
| 20, then 10, then 1 (secret 35) | "Go HIGHER" each time | "Go LOWER" each time | none | `check_guess`: hint messages swapped (original app.py lines 38 and 40) |
| 9 entered as the first two guesses of a new game (secret 50) | "Go HIGHER" both times | 1st: "Go HIGHER". 2nd: "Go LOWER" | none | app.py submit block: `secret = str(...)` on even attempts |
| 0, then -100000 (Normal, 1 to 100) | Error: out of range | Accepted as valid guesses | `parse_guess` returned `(True, 0, None)` and `(True, -100000, None)` | `parse_guess` had no range check |
| 100.1 (Normal, 1 to 100) | Rejected: above 100 and not a whole number | Accepted as 100 | `(True, 100, None)` | `parse_guess`: `int(float(raw))` truncates the decimal |
| "abc" submitted 8 times (Normal) | Game over after the 8th attempt | Game continues. "Attempts left" goes 7, 6, ... 0, -1, -2 | none | app.py submit block: `attempts += 1` runs for invalid input, but the limit check sits only in the valid-guess branch (`else:`) |
| Win a game, click New Game, enter a number, click Submit | A fresh game starts | Debug panel shows a new secret, but the page still says "You already won" or "Game over" | none | app.py `if new_game:` block resets `attempts` and `secret` but not `status`, `score` or `history`. The `status != "playing"` check then calls `st.stop()` |
| 60 entered as the first two guesses of a new game (secret 50) | Same guess changes the score the same way both times | Score goes to 5, then to 0 | none | app.py `update_score`: Too High scores +5 on even attempts and -5 on odd ones |
| Easy difficulty selected | Banner says "between 1 and 20" | Banner says "between 1 and 100" | none | app.py `st.info(...)`: range hardcoded in the f-string |

**Replay trace.** This is a replay of the original starter code (commit `f651d72`), run outside Streamlit with the same attempt counter and the same `str(secret)` rule on even attempts as the original submit block.

```
# Hints, secret 35 (Normal, attempts start at 1)
attempt 2: guess  20 -> Too Low, "Go LOWER!", score -5
attempt 3: guess  10 -> Too Low, "Go LOWER!", score -10
attempt 4: guess   1 -> Too Low, "Go LOWER!", score -15

# Same guess twice (secret 50)
attempt 2: guess   9 -> Too High, "Go HIGHER!", score 5
attempt 3: guess   9 -> Too Low, "Go LOWER!", score 0

# Score on the same guess twice (secret 50)
attempt 2: guess  60 -> Too High, "Go HIGHER!", score 5
attempt 3: guess  60 -> Too High, "Go HIGHER!", score 0

# Out-of-range and decimal input, starter parse_guess
parse_guess('0') -> (True, 0, None)
parse_guess('-100000') -> (True, -100000, None)
parse_guess('100.1') -> (True, 100, None)

# Invalid input, limit 8 (Normal), excerpt
invalid #7: attempts left 0
invalid #8: attempts left -1
invalid #9: attempts left -2
```

Notes:
- Rows 2 and 7 reproduce only as the first two guesses of a new game. `attempts` starts at 1 and increments before each guess, so the first guess is attempt 2 (even) and the second is attempt 3 (odd).
- Row 5: after 8 invalid inputs the next valid guess ends the game as a loss immediately, because the limit check finally runs with `attempts >= limit`.
- Rows 4 to 8 were reconstructed from symptoms I saw while testing. I did not record the exact inputs at the time. I verified rows 4, 5 and 7 by replaying them against the starter code, and rows 6 and 8 by reading the starter code.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

Used Claude. 

AI explanation of a bug: After winning a game, I clicked New Game and the debug panel showed a new secret, but the page stayed on the game-over screen. Claude explained that the New Game block reset attempts and secret but never reset status. Because status stayed "won" or "lost", the check status != "playing" ran on the next rerun and called st.stop(), so the submit logic below it never executed. It also pointed out that New Game ignored the difficulty (randint(1, 100)) and left score and history unchanged. I confirmed the explanation by reading that block, then fixed it by resetting status, score and history and picking the secret from the current difficulty range. I tested by winning, clicking New Game and submitting a guess, and repeated it after a loss.


Accepted: Claude explained that the app converted the secret to a string on even attempts, so guesses were compared alphabetically instead of numerically, and suggested removing that conversion. It was correct because both values are integers and need no conversion. I verified it by replaying the original code, where the same guess got different hints on attempts 2 and 3, and by checking that the hint stays consistent after the fix, in both pytest and the live game.


Did not accept as written: my first bug table (drafted by Claude) said that guess 9 against a secret of 50 shows a wrong hint on an even attempt. I didn't accept it without checking. I replayed the original code, and on even attempts the hint was "Go HIGHER", which is correct by accident, because the string comparison and the swapped messages cancel out. The real symptom was inconsistency: the same guess got "Go HIGHER" on attempt 2 and "Go LOWER" on attempt 3. I changed the table row to enter 9 twice, and the replay trace in section 1 shows the output.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed when a test that failed on the old behavior passed on the new, and when the live game matched. For the hint bug, I tested that a guess of 60 against a secret of 50 returns "Too High" and that the message says "Go LOWER". The message tests matter because the old code returned the right outcome with the wrong text, so an outcome-only test would have passed on broken code. 
For the range bug I tested 0, -100000, 101 (which are rejected), and 1 and 100 (which are accepted). I also added tests for decimals ("100.1", "7.9"), non-numeric text, empty input, None, and the difficulty ranges. 
In total, 15 pytest tests pass, run with .venv/bin/python -m pytest.



---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit is a framework that turns Python scripts into interactive web apps without requiring front-end development. So when you click something on the app the entire underlying Python script re-runs, loading an updated app. Though the entire script re-runs, the app is able to be  updated, as opposed to reset, becuase of streamlit session states, which acts as the memory vault that stores all the important info across re-runs.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

Reviewing my understanding of a codebase with claude and asking it to identify gaps or inconsistencies in my understanding. I made a few errors and hasty assumptions when reading through the code base, Claude was helpful in identifying the inconsistency. 

- What is one thing you would do differently next time you work with AI on a coding task?
I would be more careful to make sure I am developing a complete or adequate understanding of what im working on rather than relying on AI to be the driver...or rather than assuming that AI would know how to do a task properly. I learned that even if AI did something properly, my lack of knowledge wouldn't allow me to verify the output properly. 

- In one or two sentences, describe how this project changed the way you think about AI generated code.
Previously, I thought that as long as the driver in a development process gave AI specific enough requirements and expectations, it would be okay for the driver to trust that AI covers all the bases the driver is unknowledgable about, but I understand now that if the driver doesnt know how o do something, they wont be able to guide or verify the AI's work.