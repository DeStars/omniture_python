__author__ = 'DeStars'
import ConfigParser

from OmnitureReporting.ReportDefinition import DummyReportDefinition
from OmnitureReporting.omniture_wrapper import OmnitureWrapper

config_parser = ConfigParser.SafeConfigParser()
config_parser.read('omniture_python.cfg')
user = config_parser.get('authentication', 'user')
secret = config_parser.get('authentication', 'secret')
client = OmnitureWrapper(user, secret)

temp_builder = DummyReportDefinition().add_metrics(config_parser.get('report', 'metrics')).add_elements(
    config_parser.get('report', 'elements'),
    num_values=50000).with_date_granularity(config_parser.get('report', 'date_granularity'))
report_suite_id = [config_parser.get('report', 'reportsuiteid')]
dates = config_parser.get('report', 'dates')

builders = [temp_builder]
suite_id_builders = [x.with_report_suite_id(sid) for x in builders for sid in report_suite_id]
final_builders = [x.with_dates(date[0], date[1]) for x in suite_id_builders for date in dates]

for builder in final_builders:
    print builder.get_report_definition()
    report = client.retrieve_report(builder.get_report_definition())
    print report
