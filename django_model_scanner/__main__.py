"""Entry point for python -m django_model_scanner invocation."""

import sys
from .main import main

if __name__ == "__main__":
    sys.exit(main())
