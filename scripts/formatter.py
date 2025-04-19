import sys
import re
import textwrap

def fix_indentation(code, spaces=4):
    return code.replace('\t', ' ' * spaces)

def limit_line_length(code, max_length=120):
    lines = code.split('\n')
    new_lines = []
    for line in lines:
        if len(line) > max_length:
            wrapped = textwrap.fill(line, width=max_length, subsequent_indent=' ' * 4)
            new_lines.append(wrapped)
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)

def remove_trailing_whitespace(code):
    lines = code.split('\n')
    new_lines = [line.rstrip() for line in lines]
    return '\n'.join(new_lines)

def sort_imports(code):
    import_lines = []
    other_lines = []
    for line in code.split('\n'):
        if line.startswith('import ') or line.startswith('from '):
            import_lines.append(line)
        else:
            other_lines.append(line)
    sorted_imports = sorted(import_lines)
    return '\n'.join(sorted_imports + [''] + other_lines)

def standardize_string_quotes(code, quote_style="'"):
    if quote_style not in ["'", '"']:
        quote_style = "'"
    pattern = r'\"([^\"]*)\"' if quote_style == "'" else r"\'([^\']*)\'"
    replacement = f"{quote_style}\\1{quote_style}"
    return re.sub(pattern, replacement, code)

def add_newline_at_eof(code):
    if not code.endswith('\n'):
        return code + '\n'
    return code

def format_code(code):
    code = fix_indentation(code)
    code = remove_trailing_whitespace(code)
    code = sort_imports(code)
    code = standardize_string_quotes(code, quote_style="'")
    code = limit_line_length(code)
    code = add_newline_at_eof(code)
    return code

def format_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        formatted_content = format_code(content)
        if content != formatted_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(formatted_content)
            print(f"Formatted: {file_path}")
            return 1  # Indicate that the file was modified
        else:
            print(f"Formatted: {file_path} (no changes)")
            return 0  # No changes
    except Exception as e:
        print(f"Error formatting {file_path}: {e}")
        return 1  # Treat as error

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python formatter.py <file1.py> [<file2.py> ...]")
        sys.exit(1)
    exit_code = 0
    for file_path in sys.argv[1:]:
        result = format_file(file_path)
        if result != 0:
            exit_code = result
    sys.exit(exit_code)
