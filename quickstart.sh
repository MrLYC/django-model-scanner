#!/bin/bash
# Quick setup and usage script

echo "Django Model Scanner - Quick Start"
echo "===================================="
echo ""

# Install dependencies
echo "1. Installing dependencies..."
pip install -q pylint astroid pyyaml django

# Install package in development mode
echo "2. Installing django-model-scanner..."
pip install -q -e .

# Verify installation
echo "3. Verifying installation..."
python -c "from django_model_scanner import checker; print('✓ Package installed')" || {
    echo "✗ Package installation failed"
    exit 1
}

# Run scanner on example using python -m pylint
echo "4. Scanning example blog models..."
python -m pylint examples/blog/models.py \
  --load-plugins=django_model_scanner.checker \
  --disable=all \
  --django-models-output=example_output.yaml

# Show results
if [ -f example_output.yaml ]; then
    echo ""
    echo "✓ Scan complete! Output saved to example_output.yaml"
    echo ""
    echo "First few lines of output:"
    head -40 example_output.yaml
else
    echo ""
    echo "Trying alternative method with test script..."
    python test_scan.py
fi
