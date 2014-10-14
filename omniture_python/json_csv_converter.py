from datetime import datetime

__author__ = 'DeStars'


class JsonToCsvConverter:
    def __init__(self):
        pass

    def convert_to_csv(self, data):
        csv_data = [self.__get_header_row(data)]
        csv_data.extend([row for row in self.__get_rows(data)])
        return csv_data

    @staticmethod
    def __get_header_row(data):
        header_row = ['Date', 'Report Suite']
        for element in data['elements']:
            header_row.append(element['name'])
        for metric in data['metrics']:
            header_row.append(metric['name'])
        return header_row

    def __get_rows(self, data):
        rows = []
        for breakdown in data['data']:
            date_string = datetime.strptime(breakdown['name'], '%a. %d %b. %Y').strftime('%Y-%m-%d')
            rows.extend([self.__get_row(breakdown_elements, data['reportSuite']['name'], date_string) for breakdown_elements
                        in breakdown['breakdown']])
        return rows

    @staticmethod
    def __get_row(row_data, report_suite, date):
        row_elements = [date, report_suite, row_data['name']]
        row_elements.extend([metric for metric in row_data['counts']])
        return row_elements
