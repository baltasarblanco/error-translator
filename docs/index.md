# Welcome to Error Translator

Error Translator is a local, rule-based Python error translator. It converts raw tracebacks into plain English, keeps the original file and line context when available, and returns a structured fix suggestion you can read in the terminal or consume from code.

## Why it exists

Python tracebacks are precise, but they are not always beginner-friendly. This project narrows the gap by matching the final error line against a curated rule set, then combining that match with traceback metadata and optional AST-backed insight.

!!! tip "Local by default"
    Translation is deterministic and runs inside your Python process. No external service is required for normal CLI or library usage.

## Highlights

- Clear explanations written for humans, not compiler output.
- Structured results that include the matched error, file, line, and code context when available.
- Three entry points: import hook, CLI, and FastAPI service.
- Extensible rule table stored in `error_translator/rules.json`.

## Installation

```bash
pip install error-translator-cli-v2
```

For local development, install the repository requirements instead:

```bash
pip install -r requirements.txt
```

## Quick Start

### Automatic interception

```python title="script.py"
import error_translator.auto

maximum_user_connections = 100
print(maximum_user_connectons)
```

This is the magic import. Importing `error_translator.auto` installs the project's `sys.excepthook` handler, so unhandled exceptions in that process are translated automatically instead of showing only the raw traceback.

Use it when you want the error translation to happen with a single import and no extra wrapper code.

### CLI translation

Run a script and translate any crash that appears on `stderr`:

```bash
explain-error run script.py
```

Translate a raw error string directly:

```bash
explain-error "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
```

Pipe saved traceback text into the CLI:

```bash
Get-Content error.log | explain-error
```

```bash
cat error.log | explain-error
```

## API surface

The FastAPI service exposes a lightweight HTTP interface for integrations and demos.

```bash
uvicorn error_translator.server:app --reload
```

`POST /translate` accepts JSON with a `traceback_setting` field containing the traceback text.

## Returned fields

The translation result may include:

- `explanation`
- `fix`
- `matched_error`
- `file`
- `line`
- `code`
- `ast_insight`

## Learn more

- Read the architecture overview in `ARCHITECTURE.md`.
- See contribution guidance in `CONTRIBUTING.md`.

## For contributors

If you are here to improve the project, start with a small change. Good first contributions include fixing a doc typo, improving one rule explanation, or adding a test for an existing traceback example.

Before you open a pull request, run `pytest` and check that the docs still describe the code accurately.
