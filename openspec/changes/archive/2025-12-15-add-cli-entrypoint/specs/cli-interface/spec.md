# CLI Interface Specification

## ADDED Requirements

### REQ-CLI-001: Command-line Argument Parsing

The CLI must accept project path and output path as command-line arguments.

#### Scenario: User scans project with custom output
```bash
python -m django_model_scanner -p /Users/user/project/src -o /tmp/models.yaml
```
**Expected**: Scanner analyzes `/Users/user/project/src` and writes output to `/tmp/models.yaml`

#### Scenario: User scans project with default output
```bash
python -m django_model_scanner -p ./myapp
```
**Expected**: Scanner analyzes `./myapp` and writes output to `./django_models.yaml` in current directory

#### Scenario: User requests help
```bash
python -m django_model_scanner --help
```
**Expected**: Display usage information showing `-p/--project` and `-o/--output` options with examples

### REQ-CLI-002: Path Validation

The CLI must validate input paths before invoking pylint.

#### Scenario: Project path does not exist
```bash
python -m django_model_scanner -p /nonexistent/path
```
**Expected**: Exit with error message "Error: Project path not found: /nonexistent/path" and exit code 1

#### Scenario: Project path is not readable
```bash
python -m django_model_scanner -p /restricted/path
```
**Expected**: Exit with error message "Error: Cannot access project path: /restricted/path" and exit code 1

#### Scenario: Output directory does not exist
```bash
python -m django_model_scanner -p ./src -o /nonexistent/dir/output.yaml
```
**Expected**: Exit with error message "Error: Output directory does not exist: /nonexistent/dir" and exit code 1

### REQ-CLI-003: Pylint Integration

The CLI must invoke pylint programmatically with correct arguments.

#### Scenario: Successful scan
```bash
python -m django_model_scanner -p ./examples/blog -o test.yaml
```
**Expected**: 
- Invokes `pylint.lint.Run([path, "--disable=all", "--load-plugins=django_model_scanner.checker", "--enable=django-model-scanner", "--django-models-output=test.yaml"])`
- Prints "Django models exported to test.yaml"
- Exit code 0

#### Scenario: Pylint execution fails
```bash
python -m django_model_scanner -p ./invalid_python_code
```
**Expected**: 
- Display pylint error output
- Exit with non-zero code

### REQ-CLI-004: Module Invocation

The CLI must work when invoked as a Python module.

#### Scenario: Module invocation
```bash
python -m django_model_scanner -p ./src -o models.yaml
```
**Expected**: CLI executes successfully (requires `__main__.py` or main.py with `if __name__ == "__main__"`)

### REQ-CLI-005: Console Script Entry Point

The package should provide a console script entry point for convenient invocation.

#### Scenario: Script invocation (after pip install)
```bash
django-model-scanner -p ./src -o models.yaml
```
**Expected**: Same behavior as `python -m django_model_scanner -p ./src -o models.yaml`

#### Scenario: Script in PATH
```bash
which django-model-scanner
# /path/to/venv/bin/django-model-scanner

django-model-scanner --help
```
**Expected**: Script is available in PATH and displays help

### REQ-CLI-006: Error Messages

The CLI must provide clear, actionable error messages.

#### Scenario: Missing required argument
```bash
python -m django_model_scanner
```
**Expected**: Error message "Error: the following arguments are required: -p/--project" and exit code 2

#### Scenario: Invalid argument
```bash
python -m django_model_scanner --invalid-arg value
```
**Expected**: Error message showing "unrecognized arguments: --invalid-arg" with usage hint

### REQ-CLI-007: Output Feedback

The CLI must provide clear success feedback.

#### Scenario: Successful export with model count
```bash
python -m django_model_scanner -p ./examples/blog
```
**Expected Output**:
```
Django models exported to django_models.yaml
```

#### Scenario: No models found
```bash
python -m django_model_scanner -p ./empty_project
```
**Expected**: Should still create YAML (empty or with zero models) and show success message
