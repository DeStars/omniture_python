omniture_python
===============

Python wrapper for Omniture API 1.4

Will only work with Omniture Reporting API version 1.4 or higher.
Reports can be saved in CSV format compatible with multiple analytics tools.

Instructions
--------------
Service can be initialised by one line
    service = OmniturePython(<user>, <secret>)

To retrieve report as JSON call get_reports method, or get_csv_reports to get reports as CSV compatible list.
Note that those methods return generator object, so you can iterate through that, e.g.
    for report in service.get_csv_reports(metrics, elements, date_granularity, report_suite_id, dates):
        # do stuff

Refer to Omniture API documentation to find list of available metrics and elements.

Project stage
--------------
Currently under development, use at you own risk.