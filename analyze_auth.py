#!/usr/bin/env python3
import ast
import sys

FILE_PATH = r'D:\dev\Dia-D\backend\routes\auth.py'

try:
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        source = f.read()
    
    # Parse the Python source
    tree = ast.parse(source)
    print("File parsed successfully!")
    print(f"Total nodes walked: {len(list(ast.walk(tree)))}")
    
    # Find all function definitions
    print("\nFunction definitions:")
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            print(f"  Function: {node.name}")
            print(f"    Line: {node.lineno}, End line: {node.end_lineno}")
            # Get the decorator names
            for dec in node.decorator_list:
                if isinstance(dec, ast.Call):
                    func_name = ast.unparse(dec.func) if hasattr(ast, 'unparse') else str(dec.func)
                    print(f"    Decorator: {func_name}")
                else:
                    print(f"    Decorator: {ast.unparse(dec) if hasattr(ast, 'unparse') else str(dec)}")
    
    # Find all try nodes
    print("\nTry blocks:")
    for node in ast.walk(tree):
        if isinstance(node, ast.Try):
            print(f"  Try block at line {node.lineno}")
            for handler in node.handlers:
                print(f"    Handler: {handler.type}")
    
except SyntaxError as e:
    print(f"Syntax error in file: {e}")
    print(f"Error at line {e.lineno}")
    sys.exit(1)