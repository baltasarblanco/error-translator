import sys
import argparse
from .core import translate_error

# ANSI Color Codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    MAGENTA = '\033[95m'

def print_result(result: dict):
    """Prints the translated error to the terminal with colors."""
    print(f"\n{Colors.RED}{Colors.BOLD} Error Detected:{Colors.RESET}")
    print(f"{result.get('matched_error', 'N/A')}")
    
    if "file" in result:
        print(f"{Colors.YELLOW} Location: {result['file']} (Line {result['line']}){Colors.RESET}\n")
        if result.get("code"):
            print(f"{Colors.RESET}   |")
            print(f"{Colors.RESET}   |  {Colors.RED}{result['code']}{Colors.RESET}")
            print(f"{Colors.RESET}   |\n")
        else:
            print("\n")

    else:
        print()
    
    print(f"{Colors.CYAN}{Colors.BOLD} Explanation:{Colors.RESET}")
    print(f"{result['explanation']}\n")
    
    print(f"{Colors.GREEN}{Colors.BOLD} Suggested Fix:{Colors.RESET}")
    print(f"{result['fix']}\n")

    if result.get("ast_insight"):
        print(f"{Colors.MAGENTA}{Colors.BOLD} AST Insight:{Colors.RESET}")
        print(f"{result['ast_insight']}\n")

def run_script(script_name: str):
    """Runs a python script in the background and catches its errors."""
    import subprocess
    try:
        # Run the script using the current Python environment
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True
        )
        
        # If the script ran perfectly (Return Code 0), print standard output
        if result.returncode == 0:
            print(result.stdout, end="")
        
        # If the script crashed, print whatever succeeded, THEN translate the error
        else:
            if result.stdout:
                print(result.stdout, end="")
            
            translation = translate_error(result.stderr)
            print_result(translation)
            
    except FileNotFoundError:
        print(f"{Colors.RED}Error: Could not find script '{script_name}'{Colors.RESET}")

# Entry point of the program
def main():
    parser = argparse.ArgumentParser(
        description="🔍 Error Translator — Turn cryptic Python tracebacks into clear, actionable advice.",
        epilog="""
Examples:
  # Run a Python script and translate any unhandled errors
  explain-error run my_script.py

  # Translate a raw error string directly
  explain-error "NameError: name 'usr_count' is not defined"

  # Pipe a traceback from a log file or another command
  cat error.log | explain-error

For more information, visit: https://github.com/gourabanandad/error-translator
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "args",
        nargs="*",
        help=(
            "Positional arguments. Use 'run <script.py>' to execute a Python file, "
            "or provide an error string to translate. If no arguments are given and "
            "stdin is not piped, this help message is displayed."
        )
    )

    parsed_args = parser.parse_args()

    # 1. Handle Piped Input (e.g., cat error.log | explain-error)
    if not sys.stdin.isatty():
        error_input = sys.stdin.read()
        if error_input.strip():
            print_result(translate_error(error_input))
            return

    # 2. Print help if no arguments and no piped input
    if not parsed_args.args:
        parser.print_help()
        sys.exit(1)

    # 3. Check if the user used the "run" command
    if parsed_args.args[0] == "run" and len(parsed_args.args) > 1:
        script_name = parsed_args.args[1]
        run_script(script_name)

    # 4. Fallback: Treat the input as a raw error string
    else:
        error_input = " ".join(parsed_args.args)
        print_result(translate_error(error_input))

if __name__ == "__main__":
    main()