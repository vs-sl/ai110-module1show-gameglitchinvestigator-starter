# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 20 | go higher | go lower (but target is 35)| believe error is in check guess |
| 0 | "out of range" | "go lower" | believe error is in check guess.  |
| -100000 | "out of range" | "go lower" | check guess  |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
Used Claude. 

Accepted: the range check in parse_guess. It was correct because the bound check sits after parsing and returns the same (ok, value, err) shape, so app.py needed only the extra low, high arguments. I verified it with the 0, -100000 and 101 tests and in the live game.

Changed: the starter tests compared check_guess to a bare string, but it returns a tuple. I kept the tuple, unpacked it in the tests, and verified it with pytest.


---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?
Made tests with AI aiming to be mutually exclusive, collecetively exhaustive solutions to bugs. (still a wip)
9 pytest tests passed, using .venv/bin/python -m pytest.

I played the live game: guessed above and below the secret, and tried 0, -100000 and 101.
AI helped me design the tests, for example helped suggest boundary cases.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
