import json
import os

def load_rules():
    """Loads the error rules from the JSON file."""
    # Find the absolute path to the json file next to this script
    # current_dir = os.path.dirname(data\rules.json)
    current_dir = 'data/'
    json_path = os.path.join(current_dir, 'rules.json')
    
    with open(json_path, 'r') as file:
        return json.load(file)

def translate_error(traceback_text: str) -> dict:
    import re # Lazy import
    
    data = load_rules()
    rules = data["rules"]
    default_error = data["default"]

    lines = [line.strip() for line in traceback_text.strip().split('\n') if line.strip()]
    if not lines:
        return {"explanation": "No error text provided.", "fix": "Provide a valid Python error."}
    
    actual_error_line = lines[-1]

    # Flexible regex to catch single or double quotes, and handle missing ones
    location_match = re.search(r'File\s+[\'"]?(.*?)[\'"]?,\s+line\s+(\d+)', traceback_text)
    file_name = location_match.group(1) if location_match else "Unknown File"
    line_number = location_match.group(2) if location_match else "Unknown Line"

    for rule in rules:
        # Compile the regex pattern on the fly
        pattern = re.compile(rule["pattern"])
        match = pattern.search(actual_error_line)
        
        if match:
            extracted_values = match.groups()
            return {
                "explanation": rule["explanation"].format(*extracted_values),
                "fix": rule["fix"].format(*extracted_values),
                "matched_error": actual_error_line,
                "file": file_name,
                "line": line_number
            }

    return {
        "explanation": default_error["explanation"],
        "fix": default_error["fix"],
        "matched_error": actual_error_line,
        "file": file_name,
        "line": line_number
    }