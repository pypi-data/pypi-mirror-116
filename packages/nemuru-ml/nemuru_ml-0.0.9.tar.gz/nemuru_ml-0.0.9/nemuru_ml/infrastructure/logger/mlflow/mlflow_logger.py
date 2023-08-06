import pandas as pd
import mlflow
import pickle
import os

from typing import Optional, Dict
from nemuru_ml.common.logger import Logger


class MlflowLogger(Logger):

    def __init__(self):
        super().__init__()

    def log_artifact(self, artifact: Dict, artifact_path: Optional[str] = None) -> None:
        """
            Log a local file or directory as an artifact of the currently active run. If no run is
            active, this method will create a new active run.

            :param artifact: Path to the file to write.
            :param artifact_path: If provided, the directory in ``artifact_uri`` to write to.
        """
        local_path = f"/tmp/{artifact['name']}.pickel"
        with open(local_path, 'wb') as handle:
            pickle.dump(artifact['value'], handle, protocol=pickle.HIGHEST_PROTOCOL)
        mlflow.log_artifact(local_path, artifact_path)
        os.remove(local_path)

    def log_data(self, data: pd.DataFrame, artifact_path: Optional[str] = None) -> None:
        """
            Log a local file or directory as an artifact of the currently active run. If no run is
            active, this method will create a new active run.

            :param data: Path to the file to write.
            :param artifact_path: If provided, the directory in ``artifact_uri`` to write to.
        """
        local_path = '/tmp/temp.csv'
        data.iloc[0:1].to_csv(local_path)
        mlflow.log_artifact(local_path, artifact_path)
        os.remove(local_path)






