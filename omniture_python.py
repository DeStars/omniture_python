import ConfigParser
import ast
import csv

from omniture_python.report_definition import ReportBuilder
from omniture_python.omniture_wrapper import OmnitureWrapper
from omniture_python.json_csv_converter import JsonToCsvConverter


__author__ = 'DeStars'


class OmniturePython:
    def __init__(self, user, secret):
        self.client = OmnitureWrapper(user, secret)

    def get_reports(self, metrics, elements, date_granularity, report_suite_id, dates):
        """
        Sends report definitions to retrieve reports
        :param metrics: e.g. visits
        :param elements: e.g. searchEngineNaturalKeyword
        :param date_granularity: e.g. day
        :param report_suite_id: e.g. my report suite
        :param dates: e.g. [['2014-07-01', '2014-07-31']['2014-08-01', '2014-08-31']]
        :return: report generator
        """
        final_builders = self.__get_report_builders(dates, elements, metrics, date_granularity, report_suite_id)
        for builder in final_builders:
            report = self.client.retrieve_report(builder.get_report_definition())
            yield report['report']

    def __get_report_builders(self, dates, elements, metrics, date_granularity, report_suite_id):
        temp_builder = ReportBuilder().add_elements(elements, num_values=50000).with_date_granularity(date_granularity)
        builders = [temp_builder]
        metrics_builder = [x.add_metrics(metric) for x in builders for metric in metrics]
        suite_id_builders = [x.with_report_suite_id(sid) for x in metrics_builder for sid in report_suite_id]
        final_builders = [x.with_dates(date[0], date[1]) for x in suite_id_builders for date in dates]
        return final_builders

    def get_csv_reports(self, metrics, elements, date_granularity, report_suite_id, dates):
        final_builders = self.__get_report_builders(dates, elements, metrics, date_granularity, report_suite_id)
        for builder in final_builders:
            report = self.client.retrieve_report(builder.get_report_definition())
            yield JsonToCsvConverter().convert_to_csv(report['report'])


# For development purposes use configuration file
config_parser = ConfigParser.SafeConfigParser()
config_parser.read('omniture_choice.cfg')
cf_user = config_parser.get('authentication', 'user')
cf_secret = config_parser.get('authentication', 'secret')

cf_metrics = ast.literal_eval(config_parser.get('report', 'metrics'))
cf_elements = config_parser.get('report', 'elements')
cf_date_granularity = config_parser.get('report', 'date_granularity')
cf_report_suite_id = ast.literal_eval(config_parser.get('report', 'reportsuiteid'))
cf_dates = ast.literal_eval(config_parser.get('report', 'dates'))

service = OmniturePython(cf_user, cf_secret)
for report in service.get_csv_reports(cf_metrics, cf_elements, cf_date_granularity, cf_report_suite_id, cf_dates):
    with open('C:\\temp\omniture\\natural.csv', 'wb') as fh:
        csv_writer = csv.writer(fh)
        for row in report:
            csv_writer.writerow(row)
# TODO data layer to load csv to database