import abc

from nemuru_ml.stages.etl.etl import Etl
from nemuru_ml.stages.evaluation.evaluation import Evaluation
from nemuru_ml.stages.feature_engineering.feature_engineering import FeatureEngineering
from nemuru_ml.stages.training.training import Training


class Pipeline(abc.ABC):

    def __init__(
            self,
            etl: Etl,
            feature_engineering: FeatureEngineering,
            training: Training,
            evaluation: Evaluation
    ):
        self.etl = etl
        self.feature_engineering = feature_engineering
        self.training = training
        self.evaluation = evaluation

    @classmethod
    def configure(
            cls,
            etl: Etl,
            feature_engineering: FeatureEngineering,
            training: Training,
            evaluation: Evaluation,
    ):
        return cls(etl, feature_engineering, training, evaluation)

    @abc.abstractmethod
    def _start_pipeline(self) -> None:
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def _stop_pipeline(self) -> None:
        """Load in the data set"""
        raise NotImplementedError

    def run(self):
        self._start_pipeline()
        try:
            data = self.etl.run()
            data = self.feature_engineering.run(data)
            model_uri, model_name = self.training.run(data)
            self.evaluation.update_model(model_uri, model_name)
        finally:
            self._stop_pipeline()
