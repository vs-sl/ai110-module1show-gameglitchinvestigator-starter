# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7)

I asked the AI for tests in three rounds. I wrote the prompts below. The AI chose the specific edge cases, and I read each test and ran the suite before keeping it.

Prompts used:
1. "Add a test for each fix in tests/test_game_logic.py. Use these two: guess 60 vs secret 50 returns 'Too High'. Guesses 0 and -100000 are rejected."
2. The AI offered to fix decimal handling and add a test for it, I gave it the go ahead and verified results.
3. "add the test" (for `get_range_for_difficulty`, after I moved it into logic_utils.py)

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Decimal above the range ("100.1") | Prompt 2 | `test_parse_guess_rejects_decimal_above_high` | Yes. It fails if the old rounding code is put back (checked on a copy) | The old code turned 100.1 into 100, which slipped past the range check. This was a real bug I saw in the game. |
| Decimal inside the range ("7.9") | Prompt 2 | `test_parse_guess_rejects_decimal_in_range` | Yes. It also fails with the old rounding code | The first test only proves the range edge. This one proves any decimal is rejected, with the message "Enter a whole number." |
| Non-numeric text ("abc") | Prompt 2 | `test_parse_guess_rejects_non_numeric` | Yes. I did not break the code to check this one | Text is the most common bad input. It checks that the message stays "That is not a number." and the game does not crash. |
| Empty input ("") and `None` | Prompt 2 | `test_parse_guess_rejects_empty_and_none` | Yes. I did not break the code to check this one | Clicking Submit with an empty box is easy to do by accident. The check keeps the "Enter a guess." path from raising an error. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
