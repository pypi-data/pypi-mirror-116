import abc
import pandas as pd
from nemuru_ml.common.database_client import DataBaseClient
from nemuru_ml.common.file_client import FileClient
from nemuru_ml.common.logger import Logger


class Etl(abc.ABC):

    def __init__(self, data: pd.DataFrame, logger: Logger):
        self._data = data
        self._logger = logger

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'transform') and
                callable(subclass.transform))

    @classmethod
    def from_query(cls, query: str, data_base: DataBaseClient, logger: Logger):
        """Load pandas dataframe from query"""
        return cls(data_base.execute_query(query), logger)

    @classmethod
    def from_file(cls, path: str, file_client: FileClient, logger: Logger):
        """Load from file source"""
        return cls(file_client.read_from_csv(path), logger)

    @abc.abstractmethod
    def transform(self) -> pd.DataFrame:
        """Load in the data set"""
        raise NotImplementedError

    def run(self) -> pd.DataFrame:
        etl_data = self.transform()
        self._logger.log_data(self._data, 'data')
        self._logger.log_data(etl_data, 'etl_data')
        return etl_data

    def data(self) -> pd.DataFrame:
        return self._data
