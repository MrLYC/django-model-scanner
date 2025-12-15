# Implementation Tasks

## 1. CLI Argument Parser Setup

- [x] 1.1 Import `argparse` in `main.py`
- [x] 1.2 Create ArgumentParser with program description
- [x] 1.3 Add `-p/--project` argument (required, type=str, help text)
- [x] 1.4 Add `-o/--output` argument (optional, default="django_models.yaml", type=str, help text)
- [x] 1.5 Add version argument `--version` showing package version
- [x] 1.6 Configure help formatting for readable output

## 2. Path Validation Logic

- [x] 2.1 Implement `validate_project_path(path)` function
  - Check if path exists using `os.path.exists()`
  - Check if path is readable using `os.access(path, os.R_OK)`
  - Return validation result with error message if needed
- [x] 2.2 Implement `validate_output_path(path)` function
  - Check if parent directory exists
  - Check if parent directory is writable
  - Handle absolute and relative paths correctly
  - Return validation result with error message if needed
- [x] 2.3 Add error handling for path resolution edge cases

## 3. Pylint Integration

- [x] 3.1 Import `pylint.lint.Run` in main.py
- [x] 3.2 Implement `run_scanner(project_path, output_path)` function
  - Construct pylint arguments list
  - Call `Run()` with proper arguments
  - Handle SystemExit from pylint
  - Capture and return exit code
- [x] 3.3 Add try-except for ImportError if pylint not installed
- [x] 3.4 Test with various project structures

## 4. Main Entry Point Implementation

- [x] 4.1 Implement `main()` function with full flow:
  - Parse command-line arguments
  - Validate project path → exit on error
  - Validate output path → exit on error
  - Run scanner with validated paths
  - Print success message or error
  - Return appropriate exit code
- [x] 4.2 Add `if __name__ == "__main__":` block calling main()
- [x] 4.3 Ensure proper error handling and exit codes

## 5. Console Script Entry Point

- [x] 5.1 Update `pyproject.toml` to add `[project.scripts]` section
- [x] 5.2 Add entry point: `django-scan = "django_model_scanner.main:main"`
- [x] 5.3 Test installation with `pip install -e .`
- [x] 5.4 Verify `django-scan` command works after install

## 6. __main__.py for Module Invocation

- [x] 6.1 Create `django_model_scanner/__main__.py`
- [x] 6.2 Import and call main() from main.py
- [x] 6.3 Test `python -m django_model_scanner` invocation

## 7. Error Messages and User Feedback

- [x] 7.1 Create consistent error message format
- [x] 7.2 Write errors to stderr using `sys.stderr`
- [x] 7.3 Write success messages to stdout
- [x] 7.4 Add clear error messages for all failure scenarios:
  - Project path not found
  - Project path not readable
  - Output directory doesn't exist
  - Pylint execution failure
  - Missing required arguments

## 8. Documentation Updates

- [x] 8.1 Update README.md with CLI usage section
  - Add "CLI Usage" section before "Usage with Pylint"
  - Include examples with `-p` and `-o` arguments
  - Show both `python -m` and `django-scan` invocations
- [x] 8.2 Update README.md installation section
  - Mention console script installation
  - Add note about `django-scan` command availability
- [x] 8.3 Update SETUP.md with CLI quick start examples
- [x] 8.4 Add CLI examples to quickstart.sh

## 9. Testing

- [x] 9.1 Write unit tests for argument parser
  - Test with valid arguments
  - Test with missing project argument
  - Test with invalid arguments
  - Test default output path
- [x] 9.2 Write unit tests for path validation
  - Test existing vs non-existing paths
  - Test readable vs non-readable paths
  - Test output directory validation
- [x] 9.3 Write integration test with example project
  - Scan examples/blog/models.py
  - Verify output file created
  - Verify output contains expected models
- [x] 9.4 Write test for module invocation (`python -m`)
- [x] 9.5 Write test for console script (if installed)
- [x] 9.6 Test error scenarios return correct exit codes

## 10. Edge Cases and Refinements

- [x] 10.1 Handle relative vs absolute paths correctly
- [x] 10.2 Handle paths with spaces and special characters
- [x] 10.3 Handle symlinks properly
- [ ] 10.4 Add timeout handling for large projects (if needed)
- [ ] 10.5 Consider adding `--verbose` flag for debugging
- [ ] 10.6 Consider adding `--quiet` flag to suppress output

## Dependencies

- Tasks 1-2 can be done in parallel
- Task 3 depends on task 1 (needs args to be available)
- Task 4 depends on tasks 1-3
- Task 5-6 depend on task 4
- Task 8 depends on task 4 (needs working implementation to document)
- Task 9 depends on tasks 4-6 (needs complete implementation)
- Task 10 can be done incrementally after task 4

## Validation Checklist

- [x] All tests pass
- [x] `python -m django_model_scanner -p examples/blog -o test.yaml` works
- [x] `django-scan -p examples/blog` works (after install)
- [x] `python -m django_model_scanner --help` shows clear usage
- [x] Error messages are clear and actionable
- [x] Exit codes are appropriate (0 for success, non-zero for errors)
- [x] Documentation is updated and accurate
