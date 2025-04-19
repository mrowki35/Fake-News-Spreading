import sys
import os
import ast
import re


class Linter:
    def __init__(self):
        self.errors = []

    def check_line_length(self, file_path, code, max_length=80):
        lines = code.split('\n')
        for i, line in enumerate(lines, start=1):
            if len(line) > max_length:
                self.errors.append(f"{file_path}:{i}: Line exceeds {max_length} characters (currently {len(line)}).")

    def check_trailing_whitespace(self, file_path, code):
        lines = code.split('\n')
        for i, line in enumerate(lines, start=1):
            if line.rstrip() != line:
                self.errors.append(f"{file_path}:{i}: Trailing whitespace detected.")

    def check_unused_imports(self, file_path, code):
        try:
            tree = ast.parse(code, filename=file_path)
            imported = set()
            used = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imported.add(node.module.split('.')[0])
                elif isinstance(node, ast.Name):
                    used.add(node.id)

            unused = imported - used
            for imp in unused:
                self.errors.append(f"{file_path}: Unused import '{imp}'.")
        except SyntaxError as e:
            self.errors.append(f"{file_path}: Syntax error - {e}")

    def check_naming_conventions(self, file_path, tree):
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                    self.errors.append(
                        f"{file_path}:{node.lineno}: Function name '{node.name}' should be in snake_case.")
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if not re.match(r'^[a-z_][a-z0-9_]*$', target.id):
                            self.errors.append(
                                f"{file_path}:{target.lineno}: Variable name '{target.id}' should be in snake_case.")

    def lint_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        self.check_line_length(file_path, code)
        self.check_trailing_whitespace(file_path, code)
        self.check_unused_imports(file_path, code)

        try:
            tree = ast.parse(code, filename=file_path)
            self.check_naming_conventions(file_path, tree)
        except SyntaxError as e:
            self.errors.append(f"{file_path}: Syntax error - {e}")

    def lint_all_py_files(self, files):
        for file_path in files:
            if file_path.endswith('.py'):
                self.lint_file(file_path)

    def report(self):
        if not self.errors:
            print("No linting errors found.")
            return True
        else:
            print("Linting errors:")
            for error in self.errors:
                print(error)
            return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python linter.py <file1.py> [<file2.py> ...]")
        sys.exit(1)
    linter = Linter()
    linter.lint_all_py_files(sys.argv[1:])
    success = linter.report()
    if not success:
        sys.exit(1)
