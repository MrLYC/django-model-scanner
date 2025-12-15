#!/usr/bin/env python3
"""Simple validation script to check the implementation."""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from django_model_scanner.export import normalize_value, format_field_options


def test_normalize_value():
    """Test value normalization."""
    tests = [
        ("True", True),
        ("False", False),
        ("None", None),
        ("100", 100),
        ('"hello"', "hello"),
        ("'world'", "world"),
        ("models.CASCADE", "models.CASCADE"),
    ]

    for input_val, expected in tests:
        result = normalize_value(input_val)
        assert result == expected, f"normalize_value({input_val!r}) = {result!r}, expected {expected!r}"

    print("✓ normalize_value tests passed")


def test_format_field_options():
    """Test field options formatting."""
    options = {
        "max_length": "100",
        "null": "False",
        "blank": "True",
        "default": '"test"',
    }
    formatted = format_field_options(options)

    assert formatted["max_length"] == 100
    assert formatted["null"] is False
    assert formatted["blank"] is True
    assert formatted["default"] == "test"

    print("✓ format_field_options tests passed")


def check_file_structure():
    """Check that all required files exist."""
    required_files = [
        "django_model_scanner/__init__.py",
        "django_model_scanner/ast_utils.py",
        "django_model_scanner/model_parser.py",
        "django_model_scanner/export.py",
        "django_model_scanner/checker.py",
        "examples/blog/models.py",
        "README.md",
        "pyproject.toml",
    ]

    missing = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing.append(file_path)

    if missing:
        print(f"✗ Missing files: {', '.join(missing)}")
        return False

    print("✓ All required files exist")
    return True


def check_imports():
    """Check that modules can be imported."""
    try:
        from django_model_scanner import ast_utils
        from django_model_scanner import model_parser
        from django_model_scanner import export
        from django_model_scanner import checker

        print("✓ All modules can be imported")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def main():
    """Run all validation checks."""
    print("Django Model Scanner - Validation\n")
    print("=" * 50)

    all_passed = True

    # Check file structure
    if not check_file_structure():
        all_passed = False

    # Check imports
    if not check_imports():
        all_passed = False

    # Run unit tests
    try:
        test_normalize_value()
        test_format_field_options()
    except AssertionError as e:
        print(f"✗ Test failed: {e}")
        all_passed = False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All validation checks passed!")
        print("\nTo use the scanner:")
        print("  1. Install dependencies: pip install -e .")
        print("  2. Run scanner: pylint examples/blog --load-plugins=django_model_scanner.checker --disable=all")
        return 0
    else:
        print("✗ Some validation checks failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
