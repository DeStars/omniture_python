import ConfigParser
import ast
import codecs
import csv
import os
import shutil
import uuid
import unicodecsv

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
        :param metrics: list of strings e.g. [visits, revenue]
        :param elements: e.g. searchEngineNaturalKeyword
        :param date_granularity: string e.g. day
        :param report_suite_id: string e.g. my report suite
        :param dates: list of start and end date strings e.g. [['2014-07-01', '2014-07-31']['2014-08-01', '2014-08-31']]
        :return: report generator
        """
        final_builders = self.__get_report_builders(dates, elements, metrics, date_granularity, report_suite_id)
        for builder in final_builders:
            report = self.client.retrieve_report(builder.get_report_definition())
            yield report['report']

    def __get_report_builders(self, dates, elements, metrics, date_granularity, report_suite_id):
        temp_builder = [ReportBuilder().add_elements(elements, num_values=50000).with_date_granularity(
            date_granularity).add_metrics(metrics)]
        suite_id_builders = [x.with_report_suite_id(sid) for x in temp_builder for sid in report_suite_id]
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

cf_date_granularity = config_parser.get('report', 'date_granularity')
cf_report_suite_id = ast.literal_eval(config_parser.get('report', 'reportsuiteid'))
cf_dates = ast.literal_eval(config_parser.get('report', 'dates'))

for report_type in ['paid', 'natural', 'referrer']:
    metrics = ast.literal_eval(config_parser.get(report_type, 'metrics'))
    elements = config_parser.get(report_type, 'elements')
    table = config_parser.get(report_type, 'table')

    service = OmniturePython(cf_user, cf_secret)
    for report in service.get_csv_reports(metrics, elements, cf_date_granularity, cf_report_suite_id, cf_dates):
        try:
            filename = "{0}.csv".format(uuid.uuid1())
            fullpath = os.path.join(config_parser.get('report', 'folder'), filename)
            with open(fullpath, 'w') as fh:
                csv_writer = unicodecsv.writer(fh, encoding='utf-8')
                for row in report:
                    csv_writer.writerow(row)
        finally:
            pass
            #os.remove(fullpath)