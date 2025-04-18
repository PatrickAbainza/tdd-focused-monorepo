#!/usr/bin/env python3
"""Python Dependency Analysis Tool.

This script analyzes Python dependencies across a project by:
1. Discovering source directories based on provided patterns
2. Analyzing imports in each Python file
3. Generating a structured JSON report of dependencies

Usage:
    python analyze_deps.py [options]

Options:
    --search-pattern PATTERN   Directory search pattern (default: **/src)
    --output-file PATH        Output JSON file path (default: analysis_results/pydeps_results.json)
    --exclude PATTERN         Exclude directories matching pattern (can be used multiple times)

Examples:
    # Default analysis of all src directories
    python analyze_deps.py

    # Custom search pattern and output location
    python analyze_deps.py --search-pattern "**/python" --output-file "deps.json"

    # Exclude test directories
    python analyze_deps.py --exclude "**/tests" --exclude "**/fixtures"
"""
import json
import ast
import argparse
from datetime import datetime, timezone
from pathlib import Path
import fnmatch
import json
from collections import defaultdict


# Default patterns to exclude from analysis
DEFAULT_EXCLUDES = [
    "node_modules",        # Exclude node_modules directory
    ".venv",              # Exclude Python virtual environment
    "venv",               # Exclude alternate virtual environment name
    "__pycache__",        # Exclude Python cache directories
    ".git",               # Exclude git directory
    ".pytest_cache",      # Exclude pytest cache
    ".coverage",          # Exclude coverage data
    "*.egg-info",         # Exclude Python package metadata
    "dist",               # Exclude distribution builds
    "build",              # Exclude build artifacts
    ".idea",             # IDE files
    ".vscode",           # VSCode files
    ".DS_Store",         # macOS files
    "*.pyc",             # Compiled Python
    "*.pyo",             # Optimized Python
    "*.pyd",             # Python DLL
    ".mypy_cache",       # MyPy cache
    ".ruff_cache",       # Ruff cache
    "htmlcov",           # Coverage reports
    ".env",              # Environment files
    "*.log"              # Log files
]

# Define patterns for important files to include
IMPORTANT_FILE_PATTERNS = [
    "*.py",              # Python source files
    "*.ini",             # Configuration files
    "*.toml",            # Project configuration (e.g. pyproject.toml)
    "*.yaml", "*.yml",   # YAML config files
    "*.json",            # JSON config/data files
    "*.md",              # Documentation
    "Dockerfile",        # Docker configuration
    "requirements.txt",   # Python dependencies
    "setup.py",          # Package setup
    "*.lock"             # Lock files (e.g. poetry.lock, uv.lock)
]

def is_important_file(path):
    """Check if a file is considered important for troubleshooting."""
    return any(fnmatch.fnmatch(str(path), pattern) for pattern in IMPORTANT_FILE_PATTERNS)

def find_imports(file_path):
    """Find all imports in a Python file using AST."""
    try:
        with open(file_path) as f:
            tree = ast.parse(f.read())
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.append(name.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for name in node.names:
                    if module:
                        imports.append(f"{module}.{name.name}")
                    else:
                        imports.append(name.name)
        return imports
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return []


def analyze_directory(directory):
    """Analyze all Python files in a directory for dependencies."""
    try:
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"Directory not found: {directory}")
            return None

        all_imports = []
        # Find all Python files recursively
        for python_file in dir_path.rglob("*.py"):
            imports = find_imports(python_file)
            if imports:
                relative_path = python_file.relative_to(dir_path)
                module_path = str(relative_path).replace("/", ".").replace(".py", "")
                module_info = {
                    "file": str(relative_path),
                    "module": module_path,
                    "imports": imports
                }
                all_imports.append(module_info)

        if all_imports:
            return {
                "name": directory.replace("/", "."),
                "modules": all_imports
            }
        return None

    except Exception as e:
        print(f"Exception analyzing {directory}: {e}")
        return None


def should_skip_directory(path_str, exclude_patterns):
    """Check if directory should be skipped based on exclude patterns."""
    path = Path(path_str)
    for pattern in exclude_patterns:
        # Check if any parent directory matches the exclusion pattern
        for parent in path.parents:
            if fnmatch.fnmatch(str(parent), pattern) or fnmatch.fnmatch(str(parent.name), pattern):
                return True
        # Check the directory itself
        if fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(path.name, pattern):
            return True
    return False


def find_source_directories(search_pattern="**/src", exclude_patterns=None):
    """Find all directories matching the search patterns.
    
    Args:
        search_pattern (str): Space-separated patterns to search for (glob or direct paths)
        exclude_patterns (list): Patterns to exclude
    """
    if exclude_patterns is None:
        exclude_patterns = []
        
    # Add default exclusions
    all_excludes = exclude_patterns + DEFAULT_EXCLUDES
    
    # Split search pattern into individual patterns
    patterns = search_pattern.split()
    
    root_path = Path(".")
    matching_dirs = set()  # Use set to avoid duplicates
    
    for pattern in patterns:
        # First try direct path match
        direct_path = root_path / pattern
        if direct_path.is_dir() and not should_skip_directory(str(direct_path), exclude_patterns):
            matching_dirs.add(str(direct_path))
            continue
            
        # If not a direct path, try glob pattern
        try:
            for path in root_path.glob(pattern):
                if not path.is_dir():
                    continue
                    
                path_str = str(path)
                if not should_skip_directory(path_str, exclude_patterns):
                    matching_dirs.add(path_str)
        except Exception as e:
            print(f"Warning: Error processing pattern '{pattern}': {e}")
            
    if not matching_dirs:
        print(f"Warning: No directories found for patterns: {patterns}")
            
    return sorted(list(matching_dirs))  # Convert back to sorted list for consistent output


def generate_project_structure(root_path='.', exclude_patterns=None, max_depth=3):
    """Generate a tree structure of the project directory.
    
    Args:
        root_path (str): Root directory to start from
        exclude_patterns (list): Patterns to exclude
        max_depth (int): Maximum depth to traverse (default: 3)
        
    Returns:
        dict: Nested dictionary representing the directory structure
    """
    if exclude_patterns is None:
        exclude_patterns = []
        
    def should_exclude(path):
        return any(fnmatch.fnmatch(str(path), pattern) for pattern in exclude_patterns)
    
    def build_tree(path, current_depth=0):
        if should_exclude(path):
            return None
            
        if path.is_file():
            if is_important_file(path):
                return str(path.name)
            return None
            
        # If we've reached max depth, just return an empty dict to indicate a directory
        if current_depth >= max_depth:
            return {}
            
        tree = {}
        try:
            for child in sorted(path.iterdir()):
                child_tree = build_tree(child, current_depth + 1)
                if child_tree is not None:
                    if child.is_dir():
                        tree[str(child.name)] = child_tree
                    else:
                        if 'files' not in tree:
                            tree['files'] = []
                        tree['files'].append(child_tree)
        except PermissionError:
            print(f"Warning: Permission denied for {path}")
            return None
            
        return tree if tree else None
    
    root = Path(root_path)
    structure = {str(root.name): build_tree(root, 0)}
    return structure

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('--search-pattern',
                        default='**/src',
                        help='Directory search pattern (default: **/src)')
                        
    parser.add_argument('--output-file',
                        default='analysis_results/pydeps_results.json',
                        help='Output JSON file path')
                        
    parser.add_argument('--structure-file',
                        default='analysis_results/project_structure.json',
                        help='Output file for project structure')
                        
    parser.add_argument('--exclude',
                        action='append',
                        default=[],
                        help='Exclude directories matching pattern (can be used multiple times)')
                        
    return parser.parse_args()


def main():
    """Analyze source directories and combine results."""
    args = parse_args()
    
    # Find source directories
    src_dirs = find_source_directories(args.search_pattern, args.exclude)
    if not src_dirs:
        print(f"No directories found matching pattern: {args.search_pattern}")
        return

    # Create output directory if needed
    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    all_results = []
    for directory in src_dirs:
        print(f"Analyzing {directory}...")
        result = analyze_directory(directory)
        if result:
            all_results.append(result)
            print(f"Found dependencies in {directory}")

    final_results = {
        "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
        "project_root": str(Path.cwd().absolute()),
        "modules": all_results
    }

    # Write combined results
    with open(output_path, "w") as f:
        json.dump(final_results, f, indent=2)
    
    # Generate and write project structure
    structure_path = Path(args.structure_file)
    structure_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Use the same exclude patterns for structure generation
    project_structure = generate_project_structure(
        root_path=".",
        exclude_patterns=args.exclude + DEFAULT_EXCLUDES
    )
    
    with open(structure_path, "w") as f:
        json.dump(project_structure, f, indent=2)
    
    print(f"\nAnalysis complete. Results written to {output_path}")
    print(f"Project structure written to {structure_path}")
    print(f"Analyzed {len(all_results)} source directories")


if __name__ == "__main__":
    main()
