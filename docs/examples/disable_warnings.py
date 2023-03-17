import logging
import warnings


def disable_warnings() -> None:
    """Disable output of warnings."""

    logging.root.setLevel(logging.ERROR)
    warnings.filterwarnings("ignore")
