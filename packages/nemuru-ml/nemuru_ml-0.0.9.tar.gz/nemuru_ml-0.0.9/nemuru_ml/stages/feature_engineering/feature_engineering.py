import abc
import pandas as pd
from nemuru_ml.common.logger import Logger
from typing import List


class FeatureEngineering(abc.ABC):

    def __init__(self, logger: Logger):
        self._logger = logger
        self._artifacts = []

    @classmethod
    def initialize(cls, logger: Logger):
        return cls(logger)

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'transform') and
                callable(subclass.transform))

    @abc.abstractmethod
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Load in the data set"""
        raise NotImplementedError

    def artifacts(self) -> List:
        return self._artifacts

    def run(self, data: pd.DataFrame) -> pd.DataFrame:
        transformed_data = self.transform(data)
        self.__log_artifact()
        return transformed_data

    def __log_artifact(self):
        for artifact in self._artifacts:
            self._logger.log_artifact(artifact)
