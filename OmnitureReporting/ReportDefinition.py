__author__ = 'DeStars'

from datetime import datetime


class DummyReportDefinition:
    def __init__(self):
        self.data = {}

    @classmethod
    def _elements(cls):
        return ("_suite_id", "_start_date", "_end_date",
                "_date_granularity", "_metrics_id", "_elements")

    def _convert_to_int(self, int_str):
        return int(int_str)

    def _convert_to_date(self, date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').strftime("%Y-%m-%d")

    def _copy(self):
        obj = DummyReportDefinition()
        for val in DummyReportDefinition._elements():
            if val in self.data:
                obj.data[val] = self.data[val]
        return obj

    def with_report_suite_id(self, suite_id):
        obj = self._copy()
        obj.data["_suite_id"] = suite_id
        return obj

    def with_dates(self, start_date, end_date):
        obj = self._with_start_date(start_date)._with_end_date(end_date)
        return obj

    def _with_start_date(self, date):
        obj = self._copy()
        obj.data["_start_date"] = self._convert_to_date(date)
        return obj

    def _with_end_date(self, date):
        obj = self._copy()
        obj.data["_end_date"] = self._convert_to_date(date)
        return obj

    def with_date_granularity(self, granularity):
        obj = self._copy()
        obj.data["_date_granularity"] = granularity
        return obj

    def add_metrics(self, metrics_id):
        obj = self._copy()
        if "_metrics_id" not in obj.data:
            obj.data["_metrics_id"] = []
        obj.data["_metrics_id"] = metrics_id
        return obj

    def add_elements(self, element_id, num_values):
        obj = self._copy()
        if "_elements" not in obj.data:
            obj.data["_elements"] = []
        obj.data["_elements"].append([element_id, str(num_values)])
        return obj

    def get_report_definition(self):
        # check all required elements are available
        # return object
        metrics = [{"id": mid} for mid in [self.data["_metrics_id"]]]
        elements = [{"id": eid, "top": top} for eid, top in self.data["_elements"]]
        return {
            "reportDescription":{
                "reportSuiteID": self.data["_suite_id"],
                "dateFrom": self.data["_start_date"],
                "dateTo": self.data["_end_date"],
                "dateGranularity": self.data["_date_granularity"],
                "metrics": metrics,
                "elements": elements
            }
        }