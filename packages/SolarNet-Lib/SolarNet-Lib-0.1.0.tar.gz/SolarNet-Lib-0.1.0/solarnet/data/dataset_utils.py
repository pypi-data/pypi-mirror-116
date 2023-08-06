from abc import ABC, abstractmethod
from typing import Optional, Sequence, Tuple

import torch
from torch.utils.data import Dataset


class BaseDataset(Dataset, ABC):
    @abstractmethod
    def y(self, indices: Optional[Sequence[int]] = None) -> list:
        pass
