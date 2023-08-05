import abc
import pandas as pd
from typing import Tuple
from nemuru_ml.common.logger import Logger


class Training(abc.ABC):

    def __init__(self, label: str, logger: Logger):

        self._label = label
        self._logger = logger
        self._data = None
        self._train_data = None
        self._test_data = None
        self._model = None
        self._artifacts = []

    @classmethod
    def initialize(cls, label: str, logger: Logger):
        return cls(label, logger)

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'split_data') and
                callable(subclass.split_data) and
                hasattr(subclass, 'fit') and
                callable(subclass.fit) and
                hasattr(subclass, 'model_uri') and
                callable(subclass.model_uri) and
                hasattr(subclass, 'model_name') and
                callable(subclass.model_name) and
                hasattr(subclass, '_log_model') and
                callable(subclass._log_model) and
                hasattr(subclass, '_auto_log') and
                callable(subclass._auto_log))

    def data(self) -> pd.DataFrame:
        return self._data

    def label(self) -> str:
        return self._label

    def train_data(self) -> pd.DataFrame:
        return self._train_data

    def test_data(self) -> pd.DataFrame:
        return self._test_data

    def model(self):
        return self._model

    @abc.abstractmethod
    def split_data(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def fit(self, train_data: pd.DataFrame, test_data: pd.DataFrame, label: str):
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def model_uri(self) -> str:
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def model_name(self) -> str:
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def _log_model(self, model) -> None:
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def _auto_log(self) -> None:
        """Load in the data set"""
        raise NotImplementedError

    def run(self, data: pd.DataFrame):
        self._data = data
        print('Training is starting...')
        self._train_data, self._test_data = self.split_data(data)
        self._auto_log()
        self._model = self.fit(self._train_data, self._test_data, self._label)
        self.__log_artifact()
        print('Training is done')
        return self.model_uri(), self.model_name()

    def __log_artifact(self):
        if self.train_data is not None:
            self._logger.log_data(self._train_data, 'train_data')
        if self.test_data is not None:
            self._logger.log_data(self._test_data, 'test_data')
        for artifact in self._artifacts:
            self._logger.log_artifact(artifact)
        self._log_model(self._model)
