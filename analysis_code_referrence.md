{
// See https://go.microsoft.com/fwlink/?LinkId=733558
// for the documentation about the tasks.json format
"version": "2.0.0",
"tasks": [
{
"label": "Generate Dependency Graph",
"type": "shell",
"command": "uv run pydeps --show-deps --noshow apps/ > dependency_graph.json",
"problemMatcher": [],
"group": {
"kind": "build",
"isDefault": false
},
"presentation": {
"reveal": "silent",
"panel": "shared",
"focus": false,
"clear": true
}
},
{
"label": "Run Ruff Linter",
"type": "shell",
"command": "uv run ruff check .",
"problemMatcher": [],
"group": {
"kind": "test",
"isDefault": false
},
"presentation": {
"reveal": "always",
"panel": "shared",
"focus": true,
"clear": true
}
},
{
"label": "Run Radon Complexity Check",
"type": "shell",
"command": "uv run radon cc . -a -s",
"problemMatcher": [],
"group": {
"kind": "test",
"isDefault": false
},
"presentation": {
"reveal": "always",
"panel": "shared",
"focus": true,
"clear": true
}
},
{
"label": "Run Radon Maintainability Check",
"type": "shell",
"command": "uv run radon mi . -s",
"problemMatcher": [],
"group": {
"kind": "test",
"isDefault": false
},
"presentation": {
"reveal": "always",
"panel": "shared",
"focus": true,
"clear": true
}
},
{
"label": "Run Clonedigger Duplication Check",
"type": "shell",
"command": "uv run clonedigger . --output=clones.txt",
"problemMatcher": [],
"group": {
"kind": "test",
"isDefault": false
},
"presentation": {
"reveal": "always",
"panel": "shared",
"focus": true,
"clear": true
}
},
{
"label": "Ruff Check (JSON)",
"type": "shell",
"command": "mkdir -p analysis_results && uv run ruff check . --output-format=json > analysis_results/ruff_results.json",
"problemMatcher": []
},
{
"label": "Radon CC (JSON)",
"type": "shell",
"command": "mkdir -p analysis_results && uv run radon cc . -j > analysis_results/radon_cc_results.json",
"problemMatcher": []
},
{
"label": "Copydetect (JSON)",
"type": "shell",
"command": "mkdir -p analysis_results && uv run copydetect -t . -O analysis_results/copydetect_report.html",
"problemMatcher": []
},
{
"label": "Pydeps (JSON)",
"type": "shell",
"command": "mkdir -p analysis_results && uv run pydeps --json . > analysis_results/pydeps_results.json",
"problemMatcher": []
},
{
"label": "Run All Analyses (JSON)",
"dependsOn": [
"Ruff Check (JSON)",
"Radon CC (JSON)",
"Copydetect (JSON)",
"Pydeps (JSON)"
],
"group": {
"kind": "build",
"isDefault": true
},
"problemMatcher": []
}
]
}

---

# VSCode Code Analysis Tasks

This document explains how the VSCode tasks defined in `.vscode/tasks.json` perform code analysis on the project.

## Overview

The primary task for running all analyses is `"Run All Analyses (JSON)"`. This task serves as an orchestrator and does not execute any analysis command directly. Instead, it relies on the `dependsOn` property to trigger four individual analysis tasks.

When you run `"Run All Analyses (JSON)"`, VSCode executes the following dependent tasks:

1.  `"Ruff Check (JSON)"`
2.  `"Radon CC (JSON)"`
3.  `"Copydetect (JSON)"`
4.  `"Pydeps (JSON)"`

Each of these tasks is responsible for running a specific analysis tool and saving its output to the `analysis_results/` directory. The tasks automatically create this directory if it doesn't exist.

## Individual Analysis Tasks

Here's a breakdown of what each dependent task does:

### 1. Ruff Check (JSON)

- **Label:** `"Ruff Check (JSON)"`
- **Command:** `mkdir -p analysis_results && uv run ruff check src --output-format=json > analysis_results/ruff_results.json`
- **Tool:** [Ruff](https://beta.ruff.rs/docs/)
- **Purpose:** Runs the Ruff linter and formatter across the Python source code (`src`).
- **Output:** Generates a JSON file (`ruff_results.json`) containing the linting results in the `templates/python_uv/analysis_results/` directory.

### 2. Radon CC (JSON)

- **Label:** `"Radon CC (JSON)"`
- **Command:** `mkdir -p analysis_results && uv run radon cc src -j > analysis_results/radon_cc_results.json`
- **Tool:** [Radon](https://radon.readthedocs.io/en/latest/)
- **Purpose:** Calculates the cyclomatic complexity of the code in the Python source directory (`src`). The `-j` flag specifies JSON output.
- **Output:** Generates a JSON file (`radon_cc_results.json`) containing the complexity analysis results in the `templates/python_uv/analysis_results/` directory.

### 3. Copydetect (HTML)

- **Label:** `"Copydetect (JSON)"`
- **Command:** `mkdir -p analysis_results && uv run copydetect --noise-thresh 20 --guarantee-thresh 5 -s . -n 3 -O analysis_results/copydetect_report.html`
- **Tool:** [Copydetect](https://github.com/blingenf K/copydetect)
- **Purpose:** Detects duplicated code segments within the entire project (`.`). It analyzes all supported files with a noise threshold of 20 tokens (`--noise-thresh`) and a guarantee threshold of 5 tokens (`--guarantee-thresh`). The `-n 3` flag limits the number of matches per file to 3.
- **Output:** Generates an HTML report (`copydetect_report.html`) detailing the code duplication found. This report is saved in the `templates/python_uv/analysis_results/` directory.

### 4. Pydeps (JSON)

- **Label:** `"Pydeps (JSON)"`
- **Command:** `mkdir -p analysis_results && uv run python -m pydeps src/calculator.py --show-deps --pylib > analysis_results/pydeps_results.json`
- **Tool:** [Pydeps](https://github.com/thebjorn/pydeps)
- **Purpose:** Analyzes dependencies for the specific file `src/calculator.py` to understand module relationships, including standard library imports (`--pylib\`).
- **Output:** Generates a JSON file (`pydeps_results.json`) containing the dependency graph information for `src/calculator.py` in the `templates/python_uv/analysis_results/` directory.

## Running the Task

You can run this analysis suite from VSCode by:

1.  Opening the Command Palette (Ctrl+Shift+P or Cmd+Shift+P).
2.  Typing "Tasks: Run Task".
3.  Selecting `"Run All Analyses (JSON)"`.

The results of each analysis will be saved in the corresponding file within the `analysis_results/` directory.

## Setup in Another VSCode Environment

To replicate this analysis task setup in a different VSCode workspace for this project, follow these steps:

**Prerequisites:**

1.  **Project Files:** Ensure you have the complete project source code.
2.  **`uv` Installation:** This project uses `uv` for Python package management. Make sure `uv` is installed on your system. You can find installation instructions [here](https://github.com/astral-sh/uv#installation).
3.  **VSCode:** You need Visual Studio Code installed.

**Setup Steps:**

1.  **Navigate to Project Root:** Open your terminal and change the directory to the root of this project.
2.  **Install Dependencies:** Run the following command to install all required project dependencies, including the analysis tools (Ruff, Radon, Copydetect, Pydeps):

```bash
uv sync
```

This command reads the `pyproject.toml` and `uv.lock` files and installs the specified packages into a virtual environment managed by `uv`. 3. **Copy Task Configuration:**

- Create a directory named `.vscode` in the root of your project if it doesn't already exist.
- Copy the `tasks.json` file (which contains the analysis task definitions) into the `.vscode` directory.

4.  **Reload VSCode (Optional):** Sometimes, reloading the VSCode window helps ensure it picks up the new task configuration. (Use `Developer: Reload Window` from the Command Palette).
5.  **Verify:** Follow the steps in the "Running the Task" section above to ensure the \"Run All Analyses (JSON)\" task is available and runs correctly.
