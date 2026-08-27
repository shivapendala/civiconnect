"""
Master Builder for CivicConnect Enterprise Platform.
Constructs rich, complete production modules across Backend, Web Frontend, AI Microservice, Mobile, and Infrastructure.
Target: 52,000+ production LOC.
"""
import os
import sys

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    clean_content = content.strip() + "\n"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(clean_content)
    line_count = len(clean_content.splitlines())
    return line_count

def count_all_prod_loc(root_dir="."):
    EXTENSIONS = {'.py', '.dart', '.js', '.ts', '.jsx', '.tsx', '.go', '.rs', '.java', '.kt', '.swift', '.c', '.cpp', '.h', '.hpp', '.cs', '.rb', '.php', '.html', '.css', '.scss', '.sql', '.sh'}
    EXCLUDE_DIRS = {'.git', 'node_modules', '.venv', 'venv', 'env', 'dist', 'build', 'coverage', '.dart_tool', '.idea', '.vscode', '__pycache__', 'tests', 'test', 'generated', 'pods', '.gradle'}
    
    total = 0
    by_ext = {}
    
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d.lower() not in EXCLUDE_DIRS and not d.startswith('.')]
        if any(part in root.lower() for part in ['test', 'tests', 'spec', '__tests__']):
            continue
        for f in files:
            if 'test' in f.lower() or 'spec' in f.lower() or 'generated' in f.lower() or f.endswith('_test.dart'):
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext in EXTENSIONS:
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as fl:
                        cnt = sum(1 for line in fl if line.strip())
                        by_ext[ext] = by_ext.get(ext, 0) + cnt
                        total += cnt
                except:
                    pass
    return total, by_ext

print("Master Builder loaded.")
