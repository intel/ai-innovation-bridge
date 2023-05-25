from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict
from typing import Tuple

import numpy as np
import pandas as pd

class AbstractModel(ABC):
    @abstractmethod
    def __init__(self, backend: str, bucket: str, path: Path):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def validate(self) -> Dict:
        pass

