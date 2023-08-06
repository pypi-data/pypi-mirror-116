import logging
from collections import Counter

from torch.nn.modules.module import _IncompatibleKeys

logger = logging.getLogger(__name__)


def print_incompatible_keys(incompatible_keys: _IncompatibleKeys):
    """
    Pretty print a summary of the incompatible keys returned by pytorch's load_state_dict.

    :param incompatible_keys: the _IncompatibleKeys returned by load_state_dict call.
    """

    missing_keys = [".".join(i.split(".")[:2]) for i in incompatible_keys.missing_keys]
    missing_keys_count = dict(Counter(missing_keys))
    unexpected_keys = [".".join(i.split(".")[:2]) for i in incompatible_keys.unexpected_keys]
    unexpected_keys_count = dict(Counter(unexpected_keys))

    logger.info("Missing keys:")
    for k, v in missing_keys_count.items():
        logger.info(f"    {k}: {v}")

    logger.info("Unexpected keys:")
    for k, v in unexpected_keys_count.items():
        logger.info(f"    {k}: {v}")
