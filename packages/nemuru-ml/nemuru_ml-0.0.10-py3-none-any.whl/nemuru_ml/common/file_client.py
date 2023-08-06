import abc

import pandas as pd


class FileClient(abc.ABC):
    @classmethod
    def __subclasshook__(cls, subclass):
        return ((hasattr(subclass, 'read_from_csv') and
                callable(subclass.read_from_csv)) and
                (hasattr(subclass, 'write_to_csv') and
                 callable(subclass.write_to_csv)))

    @abc.abstractmethod
    def read_from_csv(self, path: str) -> pd.DataFrame:
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def write_to_csv(self, data: pd.DataFrame, path: str) -> None:
        """Write data to path"""
        raise NotImplementedError
