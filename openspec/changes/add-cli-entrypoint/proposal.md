# Add CLI Entrypoint

## Why

Currently, users must invoke the scanner through pylint with verbose command-line arguments:
```bash
python -m pylint /path/to/project --disable=all --load-plugins=django_model_scanner.checker --enable=django-model-scanner --django-models-output=/output/path.yaml
```

This is cumbersome and error-prone. Users need a simpler, more intuitive CLI interface that:
- Reduces typing and cognitive load
- Provides clear, self-documenting options
- Works as a standalone tool without understanding pylint internals
- Enables easier integration into build scripts and CI/CD pipelines

## What Changes

Transform `main.py` into a command-line interface that wraps the pylint integration, providing:
- **Simple invocation**: `python -m django_model_scanner -p /path/to/project -o output.yaml`
- **Clear options**: `-p/--project` for input path, `-o/--output` for output file
- **Sensible defaults**: Default output to `django_models.yaml` in current directory
- **Proper exit codes**: Return 0 for success, non-zero for errors
- **Help documentation**: Built-in `--help` with usage examples

## Impact

### New Capabilities
- `cli-interface`: Command-line interface for easy invocation

### Affected Code
- **Modified**: `main.py` - transform from placeholder to full CLI
- **Modified**: `pyproject.toml` - add console script entry point (optional)
- **Modified**: `README.md` - update with CLI usage examples

### Breaking Changes
None. The existing pylint plugin interface remains unchanged. This adds a convenience layer.

### User Experience
**Before:**
```bash
python -m pylint /Users/user/project/src --disable=all --load-plugins=django_model_scanner.checker --enable=django-model-scanner --django-models-output=/tmp/models.yaml
```

**After:**
```bash
python -m django_model_scanner -p /Users/user/project/src -o /tmp/models.yaml
# or even simpler:
django-scan -p src -o models.yaml  # if installed with script entry point
```

## Implementation Notes

The CLI will internally use `pylint.lint.Run` with the appropriate arguments, exactly as shown in the reference example. This ensures consistency with the existing checker while providing a more user-friendly interface.
