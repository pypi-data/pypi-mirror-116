import abc

import pandas as pd


class DataBaseClient(abc.ABC):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'execute_query') and
                callable(subclass.execute_query))

    @abc.abstractmethod
    def execute_query(self, query: str) -> pd.DataFrame:
        """Load in the data set"""
        raise NotImplementedError
