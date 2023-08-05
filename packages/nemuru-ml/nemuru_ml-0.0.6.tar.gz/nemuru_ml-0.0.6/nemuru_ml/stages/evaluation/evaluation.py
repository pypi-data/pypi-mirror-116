import abc
from nemuru_ml.common.model_registry import ModelRegistry


class Evaluation(abc.ABC):

    def __init__(self, model_registry: ModelRegistry):
        self._model_registry = model_registry

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'is_better_than_staging') and
                callable(subclass.is_better_than_staging))

    @classmethod
    def initialize(cls, model_registry: ModelRegistry):
        return cls(model_registry)

    @abc.abstractmethod
    def is_better_than_staging(self, model_uri: str, model_name: str) -> bool:
        """Load in the data set"""
        raise NotImplementedError

    def update_model(self, model_uri: str, model_name: str):
        if self.is_better_than_staging(model_uri, model_name):
            self._model_registry.update_staging(model_uri, model_name)
