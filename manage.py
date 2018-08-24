#!/usr/bin/env python
import os
import sys
import re
from eflooring.import_env import read_env
## reference https://gist.github.com/bennylope/2999704

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eflooring.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    read_env("eflooring/.env")
    execute_from_command_line(sys.argv)
