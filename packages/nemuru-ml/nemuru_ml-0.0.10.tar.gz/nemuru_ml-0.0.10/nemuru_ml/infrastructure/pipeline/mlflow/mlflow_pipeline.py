import mlflow
import os

from nemuru_ml.pipeline.pipeline import Pipeline as AbstractPipeline
from nemuru_ml.stages.etl.etl import Etl
from nemuru_ml.stages.evaluation.evaluation import Evaluation
from nemuru_ml.stages.feature_engineering.feature_engineering import FeatureEngineering
from nemuru_ml.stages.training.training import Training


class MlflowPipeline(AbstractPipeline):

    def __init__(
            self,
            etl: Etl,
            feature_engineering: FeatureEngineering,
            training: Training,
            evaluation: Evaluation
    ):
        self.experiment = os.environ['EXPERIMENT']
        self.tracking_server_uri = os.environ['TRACKING_SERVER_URI']

        super().__init__(
            etl,
            feature_engineering,
            training,
            evaluation
        )

    def _start_pipeline(self) -> str:
        mlflow.set_tracking_uri(self.tracking_server_uri)
        mlflow.set_experiment(self.experiment)
        run = mlflow.start_run()
        return run.info.run_id

    def _stop_pipeline(self) -> None:
        mlflow.end_run()
