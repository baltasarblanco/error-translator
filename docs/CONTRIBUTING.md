# Contributing to Error Translator

Thank you for considering a contribution. This project is intentionally small, so even a modest improvement to a rule, test, or page can make the experience better for the next person who opens the repository.

If you are new here, start with a tiny change. A good first PR might fix a typo in the docs, improve one error explanation, or add a regression test for an existing rule.

## Quick start

Set up the project and verify the test suite before you change anything:

```bash
pip install -r requirements.txt
pytest
```

If that passes, you are ready to edit.

## What to edit

- Use `error_translator/rules.json` when you want to improve an explanation or fix for a specific Python error.
- Use `error_translator/core.py` only when the translation flow itself needs to change.
- Use `error_translator/ast_handlers.py` when the fix needs source-file context.
- Use `tests/test_core.py` whenever you add or adjust behavior so the change stays covered.
- Use `README.md` or the files in `docs/` when the user-facing instructions need to be clearer.

## Recommended workflow

1. Pick one small problem and focus on that only.
2. Find the exact traceback line or behavior you want to improve.
3. Update the rule, doc, or handler with the smallest change that solves it.
4. Add or update a test that proves the behavior.
5. Run `pytest` again before you open a pull request.

If you want help drafting a new rule, you can run `python builder.py` after setting `GEMINI_API_KEY`. The builder reads `scraped_errors_database.json`, proposes a draft, and asks for approval before writing to `error_translator/rules.json`.

If you want to refresh the source dataset used by the builder, run `python scraper.py`.

## Rule-writing tips

- Match the final traceback line as narrowly as possible.
- Avoid patterns that are so broad they could describe several different errors.
- Keep explanations short and beginner-friendly.
- Make fixes concrete and actionable.
- Prefer plain language over technical jargon unless the error itself requires it.

## Good first contributions

- Fix a typo or unclear sentence in the docs.
- Add a test for an existing traceback example.
- Improve one rule's explanation or fix.
- Expand a missing example in the README.

## Before opening a pull request

- The docs still read naturally and do not promise behavior the code does not have.
- The test suite passes locally.
- The change is small enough to review quickly.
- Any new rule or behavior has at least one test.
