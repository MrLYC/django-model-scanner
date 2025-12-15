# Design: CLI Entrypoint

## Architecture

```
User Command
    ↓
main.py (CLI parser)
    ↓
pylint.lint.Run (with checker plugin)
    ↓
DjangoModelChecker (existing)
    ↓
YAML output
```

## Key Design Decisions

### 1. Argument Parsing

**Decision**: Use Python's built-in `argparse` module

**Rationale**:
- No additional dependencies
- Well-documented and standard
- Good error messages out of the box
- Sufficient for our simple use case

**Alternative considered**: Click library
- Rejected: Adds dependency, overkill for two simple arguments

### 2. Pylint Invocation

**Decision**: Use `pylint.lint.Run()` programmatically

**Rationale**:
- Direct integration with existing checker
- Consistent behavior with manual pylint usage
- Captures output and exit codes
- No subprocess overhead

**Implementation**:
```python
from pylint.lint import Run

Run([
    project_path,
    "--disable=all",
    "--load-plugins=django_model_scanner.checker",
    "--enable=django-model-scanner",
    f"--django-models-output={output_path}"
])
```

### 3. Output Handling

**Decision**: Default to `django_models.yaml` in current working directory

**Rationale**:
- Predictable behavior
- Easy to find output
- Can be overridden with `-o`

**Path resolution**:
- Relative paths resolved against CWD
- Absolute paths used as-is
- Parent directories must exist (fail fast with clear error)

### 4. Error Handling

**Decision**: Catch pylint exceptions and provide user-friendly messages

**Error scenarios**:
1. Project path doesn't exist → Error: "Project path not found: {path}"
2. Project path not readable → Error: "Cannot access project path: {path}"
3. Output path not writable → Error: "Cannot write to output path: {path}"
4. Pylint execution fails → Show pylint error + exit code

### 5. Script Entry Point

**Decision**: Add optional console script entry point `django-model-scanner`

**Rationale**:
- More convenient than `python -m django_model_scanner`
- Industry standard pattern
- Easy to remember

**Configuration** (in pyproject.toml):
```toml
[project.scripts]
django-model-scanner = "django_model_scanner.main:main"
```

## Module Structure

```
django_model_scanner/
├── __init__.py
├── main.py          # CLI entry point (NEW implementation)
├── checker.py       # Existing pylint checker (unchanged)
├── model_parser.py  # Existing (unchanged)
├── ast_utils.py     # Existing (unchanged)
└── export.py        # Existing (unchanged)
```

## Interface Contract

### Command-line Arguments

| Argument | Short | Required | Default | Description |
|----------|-------|----------|---------|-------------|
| `--project` | `-p` | Yes | - | Path to Django project to scan |
| `--output` | `-o` | No | `django_models.yaml` | Output YAML file path |
| `--help` | `-h` | No | - | Show help message |

### Exit Codes

- `0`: Success (models scanned and exported)
- `1`: Error (path not found, permission denied, etc.)
- `2`: Pylint execution error

### Standard Output

- Success: "Django models exported to {output_path}"
- Errors: Clear error message to stderr

## Example Usage

```bash
# Basic usage
python -m django_model_scanner -p /path/to/project

# Custom output
python -m django_model_scanner -p ./src -o models.yaml

# With script entry point (after install)
django-model-scanner -p src -o output/models.yaml

# Help
python -m django_model_scanner --help
```

## Testing Strategy

1. **Unit tests**: Test argument parsing in isolation
2. **Integration tests**: Test with sample Django project
3. **Error tests**: Test all error scenarios (missing paths, permission issues)
4. **Subprocess tests**: Verify `python -m django_model_scanner` works
5. **Entry point tests**: Verify `django-model-scanner` works after installation
