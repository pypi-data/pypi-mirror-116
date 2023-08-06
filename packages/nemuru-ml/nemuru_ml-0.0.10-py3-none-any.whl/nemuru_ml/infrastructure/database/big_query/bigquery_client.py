import pandas as pd
from nemuru_ml.common.database_client import DataBaseClient

from google.cloud import bigquery


class BigQueryClient(DataBaseClient):

    def __init__(self):
        self.client = bigquery.Client()

    def execute_query(self, query: str) -> pd.DataFrame:
        return self.client.query(query).to_dataframe()
