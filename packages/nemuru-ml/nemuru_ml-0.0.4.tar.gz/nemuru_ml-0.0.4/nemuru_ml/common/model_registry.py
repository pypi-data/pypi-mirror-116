import abc


class ModelRegistry(abc.ABC):
    @classmethod
    def __subclasshook__(cls, subclass):
        return ((hasattr(subclass, 'update_staging') and
                callable(subclass.update_staging)) and
                (hasattr(subclass, 'update_production') and
                 callable(subclass.update_production)) and
                (hasattr(subclass, 'get_model_from_registry') and
                 callable(subclass.update_production)))

    @abc.abstractmethod
    def update_staging(self, model_uri: str, model_name: str):
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def update_production(self, model_uri: str, model_name: str, model):
        """Load in the data set """
        raise NotImplementedError

    def get_model_from_registry(self, model_uri: str):
        """Load model from Registry"""
        raise NotImplementedError
