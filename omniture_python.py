__author__ = 'DeStars'
import ConfigParser
import ast
import json

from omniture_python.report_definition import ReportBuilder
from omniture_python.omniture_wrapper import OmnitureWrapper


class OmniturePython:
    def __init__(self, user=cf_user, secret=cf_secret):
        self.client = OmnitureWrapper(user, secret)

    def get_reports(self, metrics, elements, date_granularity, report_suite_id, dates):
        """
        Sends report definitions to retrieve reports
        :param metrics: e.g. visits
        :param elements: e.g. searchEngineNaturalKeyword
        :param date_granularity: e.g. day
        :param report_suite_id: e.g. my report suite
        :param dates: e.g. [['2014-07-01', '2014-07-31']['2014-08-01', '2014-08-31']]
        :return: report object
        """
        temp_builder = ReportBuilder().add_metrics(metrics).add_elements(elements, num_values=50000).with_date_granularity(date_granularity)
        builders = [temp_builder]
        suite_id_builders = [x.with_report_suite_id(sid) for x in builders for sid in report_suite_id]
        final_builders = [x.with_dates(date[0], date[1]) for x in suite_id_builders for date in dates]
        for builder in final_builders:
            report = self.client.retrieve_report(builder.get_report_definition())
            return report['report']
            # TODO use generator to produce multiple reports

    def get_reports_csv(self, metrics, elements, date_granularity, report_suite_id, dates):
        report = self.get_reports(metrics, elements, date_granularity, report_suite_id, dates)
        return convert_to_csv(report)

# For development purposes use configuration file
config_parser = ConfigParser.SafeConfigParser()
config_parser.read('omniture_choice.cfg')
cf_user = config_parser.get('authentication', 'user')
cf_secret = config_parser.get('authentication', 'secret')

cf_metrics = config_parser.get('report', 'metrics')
cf_elements = config_parser.get('report', 'elements')
cf_date_granularity = config_parser.get('report', 'date_granularity')
cf_report_suite_id = ast.literal_eval(config_parser.get('report', 'reportsuiteid'))
cf_dates = ast.literal_eval(config_parser.get('report', 'dates'))

service = OmniturePython(cf_user, cf_secret)
report = service.get_reports(cf_metrics, cf_elements, cf_date_granularity, cf_report_suite_id, cf_dates)
with open('C:\\temp\omniture\\natural.json', 'wb') as fh:
    fh.write(json.dumps(report))
print
