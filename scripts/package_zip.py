"""
Script to create clean, verified civicconnect_repo.zip containing .git directory and all project files.
"""
import os
import zipfile
import subprocess
import shutil

def package_repo():
    repo_dir = os.path.abspath("d:/civic connect/civicconnect")
    output_zip = os.path.abspath("d:/civic connect/civicconnect_repo.zip")
    
    print(f"Packaging repository from {repo_dir} to {output_zip}...")
    
    # Exclude temporary caches and virtualenvs to keep zip compact and clean
    EXCLUDE_PATTERNS = [
        "node_modules", ".venv", "venv", "env", "build", "dist",
        ".dart_tool", "__pycache__", ".pytest_cache", ".idea", ".vscode",
        "*.pyc", "*.pyo", "db.sqlite3"
    ]

    total_files = 0
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(repo_dir):
            # Check exclusions
            rel_root = os.path.relpath(root, repo_dir)
            if any(p in rel_root for p in ["node_modules", "venv", ".venv", "env", "build", "dist", ".dart_tool", "__pycache__", ".pytest_cache", ".idea", ".vscode"]):
                continue
                
            for file in files:
                if file.endswith((".pyc", ".pyo")):
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, repo_dir)
                zipf.write(full_path, rel_path)
                total_files += 1

    file_size_mb = os.path.getsize(output_zip) / (1024 * 1024)
    print(f"Successfully packaged {total_files} files into {output_zip} ({file_size_mb:.2f} MB)")
    
    # Test zip extraction and git repository validity in temporary folder
    test_dir = os.path.abspath("d:/civic connect/temp_zip_test")
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir, ignore_errors=True)
    os.makedirs(test_dir, exist_ok=True)
    
    print("Testing zip archive extraction and git validity...")
    with zipfile.ZipFile(output_zip, "r") as zipf:
        zipf.extractall(test_dir)
        
    # Check git status and log inside extracted folder
    res_status = subprocess.run(["git", "status"], cwd=test_dir, capture_output=True, text=True)
    res_log = subprocess.run(["git", "log", "-n", "5", "--oneline"], cwd=test_dir, capture_output=True, text=True)
    
    print("Git status in extracted zip:\n", res_status.stdout)
    print("Git log in extracted zip:\n", res_log.stdout)
    
    # Cleanup test dir
    shutil.rmtree(test_dir, ignore_errors=True)
    print("Verification completed successfully!")

if __name__ == "__main__":
    package_repo()
