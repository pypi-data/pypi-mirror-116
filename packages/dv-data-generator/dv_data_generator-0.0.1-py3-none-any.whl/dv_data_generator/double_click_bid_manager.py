from __future__ import annotations

import os
import uuid
import requests
from pandas import pandas, DataFrame
from dv_data_generator.utils import get_report_url, try_run, write_csv
from dv_data_generator.google_api import GoogleApi


class DoubleClickBidManager(GoogleApi):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self._dataframe = DataFrame()
        self._service = self.get_service("DBM")

    def __create_report(self, body: dict) -> dict:
        return self._service.queries().createquery(body=body).execute()

    def __run_report(self, queryId: str) -> dict:
        return self._service.queries().runquery(queryId=queryId, body={}).execute()

    def __delete_report(self, queryId: str) -> dict:
        return self._service.queries().deletequery(queryId=queryId).execute()

    def execute_query(self, query: dict) -> DoubleClickBidManager:
        """
        Runs a DBM API report query by creating the report, executing and deleting the report.
        To access the data, use the `data` property after running the query

        Args:
            query (dict): DBM Report Create Query
        """

        assert "metadata" in query, "The query must have metadata"
        assert "type" in query["metadata"], "The query must have a type"
        assert query["metadata"]["type"] == "CSV", "The query type must be CSV"

        result = try_run(method=self.__create_report, value=query)

        assert "queryId" in result, "The report was not created"

        query_id = result["queryId"]
        unique_id = uuid.uuid4()
        file_location = f"dv360_{query_id}_{unique_id}.csv"

        try_run(
            method=self.__run_report, value=query_id, fail_method=self.__delete_report
        )

        report_url = get_report_url(self._service, query_id)

        dataset = requests.get(report_url)
        csv_text = dataset.text
        write_csv(file_location, csv_text)

        dataframe = pandas.read_csv(
            file_location, sep=",", dtype=str, skipinitialspace=True
        )

        self._dataframe = dataframe

        os.remove(file_location)

        try_run(self.__delete_report, query_id)

        return self

    @property
    def data(self) -> DataFrame:
        """A dataframe containing the report data

        Returns:
            DataFrame: Report data in a dataframe
        """
        return self._dataframe
