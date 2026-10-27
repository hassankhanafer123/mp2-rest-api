import logging
from pathlib import Path

logger = logging.getLogger(__name__)

## Verbosity = how much information is printed to the console. The higher the level, the more information is printed.
def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        datefmt="%H:%M:%S",
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s")
    pass  # TODO: implement


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    if not Path(filepath).is_file():
        logger.error(f"Input file not found: {filepath}")
        return False

    logger.info(f"Input file validated: {filepath}")
    return True
    pass  # TODO: implement