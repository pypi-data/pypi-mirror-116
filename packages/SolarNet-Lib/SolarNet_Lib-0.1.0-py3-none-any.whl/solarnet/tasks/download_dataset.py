import logging
from pathlib import Path

from solarnet.utils.filesystem import unzip
from solarnet.utils.s3 import BUCKET_DATA_REGISTRY, s3_download_file

logger = logging.getLogger(__name__)

datasets = ["sdo-benchmark"]


def download_dataset(dataset: str, destination: Path):
    if dataset not in datasets:
        raise ValueError("Dataset unknown")
    bucket_name = BUCKET_DATA_REGISTRY

    logger.info(f"Downloading {dataset} from {bucket_name} to {destination} ...")
    s3_download_file(bucket_name, s3_file=f"{dataset}.zip", local_dir=destination)

    logger.info(f"Unzipping archive...")
    unzip(destination / f"{dataset}.zip", destination / dataset, delete_file=True)
