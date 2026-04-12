import ast
import difflib
import os

# --- 1. THE INDIVIDUAL STRATEGIES (PLUGINS) ---

def handle_name_error(file_path: str, extracted_values: list) -> str:
    """Finds typos for missing variables."""
    missing_var = extracted_values[0]
    
    # ... (Imagine your previous AST parsing code is here) ...
    # For brevity, let's assume we found the match:
    closest_match = "maximum_user_connections" # Mocking the AST output
    
    if closest_match:
        return f"Did you mean to type '{closest_match}'?"
    return ""

def handle_attribute_error(file_path: str, extracted_values: list) -> str:
    """Finds typos for missing object methods (e.g., .appendd)"""
    obj_type = extracted_values[0]
    missing_attr = extracted_values[1]
    
    # ... (AST logic to find valid methods for this object) ...
    closest_match = "append" # Mocking the AST output
    
    if closest_match:
         return f"{obj_type} objects don't have '{missing_attr}'. Did you mean '{closest_match}'?"
    return ""

def handle_import_error(file_path: str, extracted_values: list) -> str:
    """ Find typos for missing imports """
    missing_module = extracted_values[0]
    
    # ... (Imagine your previous AST parsing code is here) ...
    # For brevity, let's assume we found the match:
    closest_match = "maximum_user_connections" # Mocking the AST output
    
    if closest_match:
        return f"Did you mean to type '{closest_match}'?"
    return ""
    
# --- 2. THE REGISTRY (THE MAGIC ROUTER) ---
# We map the string name of the error to the function that handles it.
AST_REGISTRY = {
    "NameError": handle_name_error,
    "AttributeError": handle_attribute_error,
    "ImportError": handle_import_error,
    # "SyntaxError": handle_syntax_error,
}