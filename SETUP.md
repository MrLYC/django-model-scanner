# Setup and Usage Guide

## Prerequisites

Django model scanner requires Django to be installed for astroid type inference to work correctly.

## Installation Steps

1. **Install Django** (required for astroid inference):
   ```bash
   pip install django>=3.2
   ```

2. **Install the scanner**:
   ```bash
   pip install -e .
   ```

   Or install with Django included:
   ```bash
   pip install -e ".[examples]"
   ```

3. **Verify installation**:
   ```bash
   python -c "import django; print(f'Django {django.get_version()}')"
   python -c "from django_model_scanner import checker; print('Scanner installed')"
   django-model-scanner --version
   ```

## Quick Test

### Using the CLI (Recommended)

Run the scanner with the simple CLI:

```bash
# Scan the example blog app
django-model-scanner -p examples/blog -o test_models.yaml

# Or using module invocation
python -m django_model_scanner -p examples/blog -o test_models.yaml
```

This should generate `test_models.yaml` with all 6 models from `examples/blog/models.py`.

### Using Direct Scanner (Alternative)

Run the test scanner (bypasses pylint):

```bash
python test_scan.py
```

This should generate `test_output.yaml` with all 6 models from `examples/blog/models.py`.

## CLI Usage

Once installed, use the scanner with simple commands:

```bash
# Basic usage - scan a project
django-model-scanner -p /path/to/project

# Scan with custom output
django-model-scanner -p ./myapp -o models.yaml

# Show help
django-model-scanner --help
```

### Module Invocation

If the `django-model-scanner` command is not in your PATH, use module invocation:

```bash
python -m django_model_scanner -p /path/to/project -o output.yaml
```

## Usage with Pylint (Advanced)

Once installed, scan your Django models:

```bash
# Scan a specific file
python -m pylint examples/blog/models.py \
  --load-plugins=django_model_scanner.checker \
  --disable=all

# Output saved to django_models.yaml by default
```

### Custom output path:

```bash
python -m pylint examples/blog/models.py \
  --load-plugins=django_model_scanner.checker \
  --disable=all \
  --django-models-output=my_models.yaml
```

## Troubleshooting

### "No files to lint: exiting"

This is a known issue with pylint. Try:

1. Use the test scanner instead:
   ```bash
   python test_scan.py
   ```

2. Or modify test_scan.py to scan your own files

### "No module named 'django'"

Install Django:
```bash
pip install django
```

### Astroid inference issues

The scanner uses fallback heuristics when astroid inference fails, so it should work even if Django imports can't be fully resolved. However, having Django installed improves detection accuracy.

## What Works

✅ Model detection (including abstract inheritance)
✅ Field parsing (all Django field types)
✅ Relationship detection (ForeignKey, M2M, O2O)
✅ Table name extraction
✅ YAML export with normalized values
✅ Direct scanning via test_scan.py

⚠️ Pylint integration has issues ("No files to lint")

## Next Steps

If pylint integration doesn't work, you can:
1. Use `test_scan.py` as a template for your own scanner
2. Import the scanner modules directly in your code
3. Help debug the pylint integration issue

