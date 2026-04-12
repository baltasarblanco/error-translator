# Error Translator CLI

Error Translator CLI turns Python tracebacks into clear, actionable explanations. It is a local, rule-based tool that reads the final error line, matches it against a curated regex rule set, and returns a structured translation with the original file, line number, code context, and a suggested fix.

## Highlights

- Runs locally with no model inference or external API calls during normal translation.
- Supports three entry points: automatic crash interception, CLI execution, and direct traceback translation.
- Extracts file and line information from standard Python tracebacks when available.
- Includes optional AST-based insight hooks for a few error families.
- Provides both machine-readable results and colorized terminal output.

## Installation

Install the published package with pip:

```bash
pip install error-translator-cli-v2
```

For local development or running the project from source, install the repository dependencies instead:

```bash
pip install -r requirements.txt
```

## Usage

### 1. Automatic crash interception

Import `error_translator.auto` at the top of a script to replace Python's default exception hook with the translated output.

This is the project's magic import: once imported, any unhandled exception in that process is intercepted and formatted by the translator before Python prints the default traceback.

```python
import error_translator.auto

maximum_user_connections = 100
print(maximum_user_connectons)
```

Use this when you want the translation to happen automatically without wrapping your code in a custom try/except block.

### 2. CLI execution

Run a script through the CLI and let the tool translate crashes from `stderr`.

```bash
explain-error run script.py
```

You can also translate a raw traceback or error string directly:

```bash
explain-error "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
```

If you want to pipe a saved traceback into the tool, use the shell syntax for your terminal:

```bash
Get-Content error.log | explain-error
```

```bash
cat error.log | explain-error
```

### 3. Programmatic use

```python
from error_translator.core import translate_error

result = translate_error(traceback_text)
print(result["explanation"])
```

### 4. HTTP API

Start the FastAPI app with Uvicorn:

```bash
uvicorn error_translator.server:app --reload
```

`POST /translate` expects JSON in the form:

```json
{
	"traceback_setting": "Traceback (most recent call last): ..."
}
```

## What the translator returns

The translation engine returns a dictionary with these fields when available:

- `explanation`
- `fix`
- `matched_error`
- `file`
- `line`
- `code`
- `ast_insight`

## Supported errors

The bundled rule set covers many common Python runtime, syntax, indentation, import, OS, encoding, and networking errors. The full list lives in `error_translator/rules.json` and can be expanded over time without changing the runtime engine.

## Project layout

- `error_translator/core.py` loads the rule set and performs the translation.
- `error_translator/cli.py` provides the `explain-error` command.
- `error_translator/auto.py` installs the automatic exception hook.
- `error_translator/server.py` exposes the HTTP API.
- `error_translator/ast_handlers.py` contains contextual suggestion hooks.
- `error_translator/rules.json` stores the rule database.

## Development notes

- `builder.py` can generate new rule drafts with Gemini when `GEMINI_API_KEY` is set.
- `scraper.py` refreshes the scraped exception dataset from the official Python documentation.
- `tests/test_core.py` contains the current regression coverage for the translation engine.

Built by Gourabananda Datta.