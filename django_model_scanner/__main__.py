"""Entry point for python -m django_model_scanner invocation."""

import sys
from pathlib import Path

# Add parent directory to path to import main.py from root
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from main import main

if __name__ == "__main__":
    sys.exit(main())
