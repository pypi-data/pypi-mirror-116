import pandas as pd

from nemuru_ml.common.file_client import FileClient


class BigQueryClient(FileClient):

    def read_from_csv(self, path: str) -> pd.DataFrame:
        return pd.read_csv(path)

    def write_to_csv(self, data: pd.DataFrame,path: str) -> None:
        data.to_csv(path)
