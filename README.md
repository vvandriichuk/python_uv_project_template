# Install uv
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```sh
uv python list
```

```sh
uv python install 3.13.2
uv python uninstall 3.13.2
```

## if I want to use any version of Python while run the code
```sh
uv python pin 3.13.2
```

If I want to change the version of Python for current running the code I can change the verion in the file .python-version

## Init the project
```sh
uv init
```
## Create venv

```sh
# Create virtual env
uv venv ./.venv

# Activate venv
source ./.venv/bin/activate
```

## Installing Dependencies with uv

### Option 1: Install all project dependencies including dev dependencies

Install the main project dependencies and all development dependencies:

```bash
# Install project dependencies
uv pip install -r requirements.txt  # If you have a requirements.txt file
# OR
uv pip install .  # Install from pyproject.toml

# Then install development dependencies
uv pip install ".[dev]"
```

### Option 2: Install only project dependencies without dev tools

If you only want to install the main project dependencies without development tools:

```bash
# From requirements.txt
uv pip install -r requirements.txt

# OR from pyproject.toml
uv pip install .
```

### Option 3: Install only specific dev tools

If you only need specific package:

```sh
uv add requests
uv add --dev pytest
```

## Run the code
```sh
uv run my_package/main.py
```

```sh
uv tree
```

# Run tests
```sh
uv run pytest tests/
```

# Docker
### Build the image
```sh
docker build -t python-uv-project .
```

### Run the container
```sh
docker run python-uv-project
```

# Setting Up pre-commit with uv and Git

This guide explains how to set up pre-commit hooks for your Python project using uv package manager and integrate them with Git.

```bash
# Install only pre-commit
uv pip install pre-commit

# OR install multiple specific tools
uv pip install pre-commit mypy ruff pytest
```

## Setting Up pre-commit

### 1. Install pre-commit hooks

Once you have the pre-commit package installed and the configuration file created, install the Git hooks:

```bash
pre-commit install
```

This command sets up pre-commit to run before each commit.

### 2. Add pre-push hooks (optional)

If you want to run checks before pushing to your repository:

```bash
pre-commit install --hook-type pre-push
```

### 3. Test your setup

To verify that everything is set up correctly, you can run pre-commit on all files:

```bash
pre-commit run --all-files
```

## Using pre-commit with Git

After installation, pre-commit will automatically:

1. Run before each commit when you execute `git commit`
2. If you installed the pre-push hook, it will also run before each `git push`
3. If any checks fail, the commit/push will be prevented until you fix the issues

## Additional Commands

- To update your hooks to the latest versions:
  ```bash
  pre-commit autoupdate
  ```

- To temporarily bypass the hooks (not recommended for normal workflow):
  ```bash
  git commit -m "Your message" --no-verify
  ```

- To manually run a specific hook:
  ```bash
  pre-commit run hook-id
  ```

# Installing and Configuring Pyright for a Python Project with uv

### What is Pyright and Why Use It

Pyright is a static type checker for Python, developed by Microsoft. It checks types and identifies potential errors in your code without executing it.

**Benefits of using Pyright:**
- Detects type errors before code execution
- Operates faster than other analyzers thanks to its TypeScript implementation
- Provides incremental analysis (only checks modified files)
- Improves code completion in modern editors
- Helps document code through type annotations
- Makes refactoring safer

### Installing Pyright for a uv Project

#### Step 1: Install Pyright using npm

```bash
npm install -g pyright
```

#### Step 2: Create a configuration file

Create a `pyrightconfig.json` file in your project root with the following content:

```json
{
  "include": ["my_package"],
  "exclude": ["**/__pycache__", ".venv"],
  "reportMissingImports": true,
  "pythonVersion": "3.13",
  "pythonPlatform": "Darwin",
  "typeCheckingMode": "basic",
  "venvPath": ".",
  "venv": ".venv"
}
```

#### Step 3: Verify it works

Run a check on your project:

```bash
pyright
```

### Editor Integration

#### Visual Studio Code

1. Install the **Pylance** extension
2. It will automatically use your `pyrightconfig.json`

#### PyCharm

1. Install the **Pyright** plugin from the plugin marketplace
2. Configure it to use your `pyrightconfig.json`

### Adding Types to Your Code

For maximum effectiveness with Pyright, add type annotations to your code:

```python
def calculate_total(items: list[float]) -> float:
    """Calculate the sum of all items."""
    return sum(items)
```

### Explanation of pyrightconfig.json Settings

- `include`: Directories to check
- `exclude`: Directories to exclude
- `reportMissingImports`: Warn about imports that cannot be found
- `pythonVersion`: Specifies your Python version (3.13)
- `pythonPlatform`: Specifies the OS (Darwin for macOS)
- `typeCheckingMode`: Type checking mode (basic, standard, strict)
- `venvPath`: Path to the directory containing the virtual environment
- `venv`: Name of the virtual environment directory

### Integration with uv Workflow

Pyright complements uv exceptionally well:
- uv provides fast dependency management and virtual environments
- Pyright provides static type analysis
- Together they form a powerful and fast Python development environment

### Recommended Workflow

1. Initialize your project with `uv init`
2. Create and activate an environment with the required Python version using `uv venv`
3. Install dependencies with `uv pip install`
4. Configure Pyright via `pyrightconfig.json`
5. Develop with real-time type checking
6. Run `pyright` before committing changes

## Using bat instead cat:

The `bat` command is a modern alternative to the standard `cat` command in Unix systems, providing an enhanced file display in the terminal.

`bat` is not a standard Unix command but a separate utility written in Rust. Here are its key features:

- **Syntax highlighting** – Supports highlighting for multiple programming languages and file formats.
- **Line numbering** – Automatically displays line numbers.
- **Git integration** – Shows Git changes in files.
- **Automatic file type detection**.
- **Support for viewing non-text files (in hexadecimal format)**.
- **Automatic pagination (like `less`)**.

### Viewing a file with syntax highlighting
```sh
bat filename.py
```

### Viewing multiple files
```sh
bat file1.txt file2.txt
```

### Viewing a file without line numbering
```sh
bat -p filename.txt
```

### Outputting only specific lines (from 10 to 20)
```sh
bat -r 10:20 filename.txt
```

### Viewing a file as plain output (without decorations)
```sh
bat --plain filename.txt
```

### Using `bat` as a replacement for `cat` in pipelines
```sh
command | bat
```
