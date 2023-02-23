from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict
from typing import Tuple

import numpy as np
import pandas as pd

class AbstractModel(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_train_test_loaders(self):
        pass

    @abstractmethod
    def train(self):
        pass
    
    @abstractmethod
    def evaluate(self):
        pass
    
    @abstractmethod
    def predict_localize(self):
        pass
    
    @abstractmethod
    def save_model(self):
        pass


