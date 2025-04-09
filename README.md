# Enhanced TDD Project Setup & Templates

## Introduction

This repository serves a dual purpose:

1.  **Setup Scripts:** Provides scripts (`scripts/setup-prereqs.sh`) to quickly install essential development tools (Homebrew, Git, Python, Node.js, uv, VS Code) on macOS.
2.  **Enhanced TDD Templates:** Offers robust, pre-configured project templates for Python and Node.js, designed specifically for Test-Driven Development (TDD) and incorporating best practices like static analysis, security scanning, pre-commit hooks, CI, and Dockerization.

The overall goal is to significantly streamline the initial setup process for a modern, efficient, and quality-focused development environment, allowing developers to focus on writing code and tests sooner.

## Project Philosophy & Goals

- **Purpose:** Provide high-quality, TDD-focused project templates for Python (using `uv` and `pytest`) and Node.js (using Vite, React, TypeScript, and `vitest`).
- **Philosophy:** Test-Driven Development (TDD) is the standard approach. All contributions and usage should adhere to TDD principles.
- **Key Tools:** Leverage modern, efficient tools like `uv` for Python and `vitest` for Node.js, alongside a comprehensive suite for linting, formatting, analysis, and security.
- **Structure:** Project templates are organized within the `templates/` directory. Each template is self-contained but benefits from the root-level configurations (Makefile, VS Code settings).
- **Details:** For detailed setup and usage instructions specific to each template, please refer to their READMEs:
  - [Python Template README](templates/python-uv/README.md)
  - [Node.js Template README](templates/nodejs-vitest/README.md)
- **Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Prerequisites

- **macOS:** This setup is specifically designed and tested for macOS.
- **Xcode Command Line Tools:** Required by Homebrew and Git. If not installed, Homebrew installation will likely prompt you. You can also install them manually: `xcode-select --install`.

## Setup Steps

1.  **Clone the Repository:**

    ```bash
    git clone <repository-url> # Replace <repository-url> with the actual URL
    cd <repository-directory> # e.g., cd tdd-project-templates
    ```

2.  **Open in VS Code & Install Recommended Extensions:**

    - Open the cloned repository folder in Visual Studio Code.
    - VS Code should prompt you to install recommended extensions listed in `.vscode/extensions.json`. Click **"Install All"**. This is crucial for the integrated tooling (linters, formatters, debuggers) to work correctly.

    **Important:** Before running this task, ensure you are inside a Git repository. If you didn't clone the project, run `git init` in the root directory first. The task needs this to install pre-commit hooks.

3.  **Run the Automated Setup Task (Recommended):**

    - Once the project is open in VS Code, use the Command Palette (`Cmd+Shift+P` or `Ctrl+Shift+P`) and search for **"Tasks: Run Task"**.
    - Select the **"Run Initial Project Setup"** task.
    - This task automates several key steps:
      - Makes the prerequisites script executable (`chmod +x scripts/setup-prereqs.sh`).
      - Runs the prerequisites script (`./scripts/setup-prereqs.sh`) to install tools like Homebrew, Python, Node, uv, etc.
      - Runs `make setup` to install Python and Node.js dependencies for the templates.
      - Installs root pre-commit hooks (`uv run pre-commit install`).
      - Installs Node.js template pre-commit hooks (`cd templates/nodejs-vitest && npx husky install`).
    - Monitor the integrated terminal where the task runs for any errors.

4.  **Reload VS Code Window (IMPORTANT):**

    - **After the "Run Initial Project Setup" task completes**, it's highly recommended to reload the VS Code window. Use the Command Palette (`Cmd+Shift+P` or `Ctrl+Shift+P`) and search for **"Developer: Reload Window"**.
    - This ensures that any PATH changes made by the setup script (e.g., installing `uv` or `node`) are recognized by VS Code and its integrated terminal.

5.  **Manual Setup (Alternative):**
    If you prefer not to use the VS Code task, you can perform the steps manually:
    - **Make the Prerequisites Script Executable:**
      ```bash
      chmod +x scripts/setup-prereqs.sh
      ```
    - **Run the Prerequisites Script:**
      ```bash
      ./scripts/setup-prereqs.sh
      ```
      > **Note:** Review output for errors. If warned about the `code` command, install it via Command Palette (`Shell Command: Install 'code' command in PATH`) and restart your terminal.
    - **Reload VS Code Window:** As mentioned above, reload after the script.
    - **Install Dependencies & Hooks:**
      ```bash
      make setup # Installs template dependencies
      uv run pre-commit install # Installs root pre-commit hooks
      (cd templates/nodejs-vitest && npx husky install) # Installs Node.js pre-commit hooks
      ```

**Summary of Manual Steps Still Required (Even with Task):**

- **Cloning the repository.**
- **Opening the project in VS Code.**
- **Installing Recommended Extensions** when prompted by VS Code.
- **Reloading the VS Code Window** after the setup task finishes.

## Technology Stack / Tooling

This repository utilizes a range of modern tools within its templates:

**Python (`templates/python-uv/`)**

- **Package Management:** `uv` (Fast, Rust-based installer and resolver)
- **Testing:** `pytest` (Feature-rich testing framework)
- **Test Coverage:** `pytest-cov` (Coverage reporting for pytest)
- **Linting/Formatting:** `ruff` (Extremely fast linter and formatter)
- **Static Analysis:**
  - `radon` (Code complexity metrics)
  - `pydeps` (Dependency graph generation)
  - `copydetect` (Code duplication detection)
- **Security:** `pip-audit` (Checks for known vulnerabilities in dependencies)
- **Pre-commit Hooks:** `pre-commit` (Framework for managing git hooks)
- **Containerization:** `Docker`

**Node.js (`templates/nodejs-vitest/`)**

- **Package Management:** `npm`
- **Testing:** `vitest` (Vite-native testing framework)
- **Test Coverage:** `@vitest/coverage-v8` (Built-in coverage using V8)
- **Linting:** `eslint` (Pluggable linting utility)
- **Formatting:** `prettier` (Opinionated code formatter)
- **Pre-commit Hooks:**
  - `husky` (Git hooks manager)
  - `lint-staged` (Run linters on staged files)
- **Static Analysis:**
  - `jscpd` (Code duplication detection)
  - `eslint-plugin-complexity` (Cyclomatic complexity checks via ESLint)
  - `dependency-cruiser` (Dependency graph analysis and validation)
- **Security:** `npm audit` (Checks for known vulnerabilities in dependencies)
- **Containerization:** `Docker`

## VS Code Integration

The `.vscode/` directory provides workspace-level configurations to enhance the development experience:

- **`.vscode/extensions.json`:** Recommends essential VS Code extensions for Python/Node.js development, TDD, linting, formatting, debugging, Docker, etc. VS Code prompts installation on opening the project.
- **`.vscode/settings.json`:** Configures workspace settings like format-on-save (using Ruff for Python, Prettier for JS/TS), Python testing discovery (`pytest`), and default formatters.
- **`.vscode/tasks.json`:** Defines tasks runnable via the Command Palette (`Cmd+Shift+P` -> `Tasks: Run Task`). Includes tasks for running tests, coverage reports, linters, and static analysis tools for both Python and Node.js templates.
- **`.vscode/launch.json`:** Provides launch configurations for debugging tests (`pytest` for Python, `vitest` for Node.js) and application code directly within VS Code's debugger.

## Makefile Usage

A root-level `Makefile` simplifies common development tasks across both templates. It acts as a convenient wrapper around individual tool commands.

**Purpose:** Provide consistent, easy-to-remember commands for setup, testing, analysis, building, and cleaning.

**Key Combined Targets:**

- `make setup`: Installs dependencies for both Python and Node.js templates.
- `make test`: Runs test suites for both templates.
- `make coverage`: Generates test coverage reports for both templates.
- `make lint`: Runs linters (Ruff, ESLint) for both templates.
- `make analyze`: Runs static analysis tools (Radon, CopyDetect, Pydeps, JSCPD, Dependency Cruiser) for both templates.
- `make security`: Runs security vulnerability scanners (pip-audit, npm audit) for both templates.
- `make docker-build`: Builds Docker images for both templates.
- `make clean`: Removes generated files (caches, build artifacts, coverage reports, etc.).
- `make help`: Displays a list of all available targets and their descriptions.

**Note:** The Makefile also contains targets specific to individual templates (e.g., `make test-python`, `make lint-node`). Refer to the `Makefile` or run `make help` for the full list.

## Project Templates

### Python (`templates/python-uv/`)

- **Location:** `templates/python-uv/`
- **Core:** Uses `uv` for package management and `pytest` for testing.
- **Example:** Includes a simple `calculator.py` module with corresponding tests in `tests/test_calculator.py`.
- **Features:**
  - Pre-configured `pyproject.toml` for `uv`, `pytest`, `ruff`, `pytest-cov`.
  - Testing setup with `pytest`.
  - Coverage configuration via `pytest-cov`.
  - Static Analysis integration (Ruff, Radon, CopyDetect, Pydeps) via Makefile/tasks.
  - Security scanning (`pip-audit`) via Makefile/tasks.
  - Pre-commit hooks configured in root `.pre-commit-config.yaml`.
  - `Dockerfile` for containerization.
- **Details:** See [Python Template README](templates/python-uv/README.md).

### Node.js (`templates/nodejs-vitest/`)

- **Location:** `templates/nodejs-vitest/`
- **Core:** Uses Vite (with React and TypeScript) and `vitest` for testing.
- **Example:** Includes a simple `Greeting.tsx` React component with tests in `src/components/Greeting.test.tsx`.
- **Features:**
  - Configured `package.json` with scripts for dev, build, test, lint, analyze, security.
  - Testing setup with `vitest`, React Testing Library, and `jsdom`.
  - Coverage configuration via `@vitest/coverage-v8`.
  - Static Analysis integration (ESLint, Prettier, JSCPD, Complexity, Dependency Cruiser) via npm scripts/Makefile/tasks.
  - Security scanning (`npm audit`) via npm scripts/Makefile/tasks.
  - Pre-commit hooks via `husky` and `lint-staged`.
  - `Dockerfile` for containerization.
- **Details:** See [Node.js Template README](templates/nodejs-vitest/README.md).

## Pre-commit Hooks

Automated checks are configured to run before each commit to maintain code quality and consistency.

- **Python:** Uses the `pre-commit` framework. Configuration is in the root `.pre-commit-config.yaml`. Hooks include checks like `ruff` (linting/formatting), end-of-file fixing, trailing whitespace, etc.
  - **Setup:** Run `uv run pre-commit install` once in the root directory after cloning.
- **Node.js:** Uses `husky` and `lint-staged`. Configuration is in `templates/nodejs-vitest/package.json` (`lint-staged` section) and `.husky/`. Hooks typically run ESLint and Prettier on staged files.
  - **Setup:** Run `cd templates/nodejs-vitest && npx husky install` once after cloning and running `npm install`. The `make setup` target handles this.

## Continuous Integration (CI)

GitHub Actions workflows are defined in `.github/workflows/`:

- `python-ci.yml`: Automatically runs on pushes/pull requests to check the Python template. Executes setup, linting, testing, coverage checks, and security audit (`pip-audit`).
- `nodejs-ci.yml`: Automatically runs on pushes/pull requests to check the Node.js template. Executes setup, linting, testing, coverage checks, and security audit (`npm audit`).

These workflows help ensure that changes integrate correctly and maintain project standards.

## Troubleshooting

- **`code` Command Not Found:** If the `code` command isn't found after running setup and installing via VS Code Command Palette, restart your terminal or source your shell profile (`source ~/.zshrc`, `source ~/.bash_profile`, etc.). See [VS Code docs](https://code.visualstudio.com/docs/setup/mac#_launching-from-the-command-line).
- **Docker Issues:** Ensure you have Docker Desktop installed and running on your macOS to use any `docker` related Makefile targets or build/run containers.
- **Dependency Graphs (`pydeps`):** To visualize the `.dot` files generated by `pydeps` (Python dependency analysis), you may need to install Graphviz: `brew install graphviz`. Then use a command like `dot -Tpng graph.dot -o graph.png`.

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute.

## License

```text
MIT License

Copyright (c) 2025 <Your Name or Organization>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
