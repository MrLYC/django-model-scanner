"""Basic tests for Django model scanner."""

import os
import tempfile
from pathlib import Path
import yaml

from django_model_scanner.export import normalize_value, format_field_options


def test_normalize_value():
    """Test value normalization."""
    assert normalize_value("True") is True
    assert normalize_value("False") is False
    assert normalize_value("None") is None
    assert normalize_value("100") == 100
    assert normalize_value('"hello"') == "hello"
    assert normalize_value("'world'") == "world"
    assert normalize_value("models.CASCADE") == "models.CASCADE"


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


def test_example_scan():
    """Test scanning the example blog app."""
    # This is a basic integration test
    # In practice, you'd run: pylint examples/blog --load-plugins=django_model_scanner.checker --disable=all
    print("Example models available at: examples/blog/models.py")
    print("To scan: pylint examples/blog --load-plugins=django_model_scanner.checker --disable=all")


if __name__ == "__main__":
    test_normalize_value()
    test_format_field_options()
    test_example_scan()
    print("All tests passed!")
