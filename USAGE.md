# Quick Usage Guide

## TL;DR

```bash
# Install
pip install -e .

# Scan a models file
python -m pylint examples/blog/models.py \
  --load-plugins=django_model_scanner.checker \
  --disable=all
```

## Common Patterns

### Scan a single models.py file
```bash
python -m pylint myapp/models.py \
  --load-plugins=django_model_scanner.checker \
  --disable=all
```

### Scan all models in a directory
```bash
python -m pylint myapp/models/*.py \
  --load-plugins=django_model_scanner.checker \
  --disable=all
```

### Scan entire Django project
```bash
python -m pylint . \
  --load-plugins=django_model_scanner.checker \
  --disable=all
```

### Custom output location
```bash
python -m pylint myapp/models.py \
  --load-plugins=django_model_scanner.checker \
  --disable=all \
  --django-models-output=output/schema.yaml
```

### With verbose output
```bash
python -m pylint myapp/models.py \
  --load-plugins=django_model_scanner.checker \
  --disable=all \
  --django-models-verbose=y
```

## Important Notes

⚠️ **Use `python -m pylint` for better compatibility**

✅ **Correct:**
- `python -m pylint myapp/models.py`
- `python -m pylint myapp/*.py`
- `python -m pylint .` (scans all .py recursively)

❌ **May not work:**
- `pylint myapp/` (command not found or PATH issues)

## Troubleshooting

### "No files to lint: exiting"

This means pylint didn't find any Python files to analyze.

**Solution:** Specify .py files explicitly:
```bash
# Instead of:
python -m pylint examples/blog

# Use:
python -m pylint examples/blog/models.py
# or
python -m pylint examples/blog/*.py
```

### "command not found: pylint"

Use `python -m pylint` instead of just `pylint`:
```bash
python -m pylint myapp/models.py --load-plugins=django_model_scanner.checker --disable=all
```

Or ensure pylint is in your PATH:
```bash
pip install --user pylint
# or
pip install pylint
```

### Output file not generated

Check that:
1. The scanner found Django models (use `--django-models-verbose=y`)
2. The output directory exists (create it first if needed)
3. You have write permissions

### No models detected

Verify that:
1. Your models inherit from `django.db.models.Model`
2. The files contain valid Python syntax
3. The models are defined as classes (not dynamically generated)
