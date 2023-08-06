import mlflow
import os
from nemuru_ml.common.model_registry import ModelRegistry


class MlflowRegistry(ModelRegistry):

    def __init__(self):
        self._client = mlflow.tracking.MlflowClient(
            tracking_uri=os.getenv('TRACKING_SERVER_URI')
        )

    def update(self, model_uri: str, model_name: str):
        model = self.get_model_from_registry('{}'.format(model_uri))
        self._client.create_model_version(
            name='{}'.format(model_name),
            source='{}'.format(model_uri),
            run_id='{}'.format(model._model_meta.run_id),
        )

    def update_staging(self, model_uri: str, model_name: str):
        model = self.get_model_from_registry('{}'.format(model_uri))
        model_register = self._client.create_model_version(
            name='{}'.format(model_name),
            source='{}'.format(model_uri),
            run_id='{}'.format(model._model_meta.run_id),
        )
        self._client.transition_model_version_stage(
            name='{}'.format(model_name),
            version=model_register.version,
            stage="Staging"
        )

    def update_production(self, model_uri: str, model_name: str, model):
        model = ModelRegistry.get_model_from_registry('{}'.format(model_uri))
        model_register = self._client.create_model_version(
            name='{}'.format(model_name),
            source='{}'.format(model_uri),
            run_id='{}'.format(model.metadata.run_id),
        )
        self._client.transition_model_version_stage(
            name='{}'.format(model_name),
            version=model_register.version,
            stage="Production"
        )

    def client(self):
        return self._client

    def get_model_from_registry(self, model_uri: str):

        return mlflow.pyfunc.load_model(
            model_uri=f"{model_uri}"
        )
