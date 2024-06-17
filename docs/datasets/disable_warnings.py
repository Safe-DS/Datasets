"""Disable output of warnings."""

from __future__ import annotations

import logging
import warnings


def disable_warnings() -> None:
    """Disable output of warnings."""
    logging.root.setLevel(logging.ERROR)
    warnings.filterwarnings("ignore")
