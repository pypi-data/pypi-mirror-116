import abc
import pandas as pd
from typing import Optional, Dict


class Logger(abc.ABC):
    @classmethod
    def __subclasshook__(cls, subclass):
        return ((hasattr(subclass, 'log_artifact') and
                callable(subclass.log_artifact)) and
                (hasattr(subclass, 'log_data') and
                 callable(subclass.log_data)))

    @abc.abstractmethod
    def log_artifact(self, artifact: Dict, artifact_path: Optional[str] = None) -> None:
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def log_data(self, data: pd.DataFrame, artifact_path: Optional[str] = None) -> None:
        """Load in the data set"""
        raise NotImplementedError
