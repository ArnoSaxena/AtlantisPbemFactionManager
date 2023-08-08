import re
from enum import Enum


class Month(Enum):
    Unknown = 0
    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
    July = 7
    August = 8
    September = 9
    October = 10
    November = 11
    December = 12

    @staticmethod
    def get_report_time(report_lines):
        for i in range(len(report_lines)):
            report_line = report_lines[i]
            if "Atlantis Report For:" in report_line and len(report_lines) > i:
                # June, Year 1
                time_split = report_lines[i + 2].strip().split(',')
                report_month = Month[time_split[0].strip()]
                report_year = int(time_split[1].strip().split(' ')[1])
                return report_month, report_year
        else:
            return None, None

    @staticmethod
    def get_time_key(month, year):
        return f'{month.value}_{year}'

    @staticmethod
    def get_month_and_year(time_key):
        time_key_regex = r"^(\d*)_(\d*)$"
        result = re.search(time_key_regex, time_key)
        if result is not None:
            return Month(int(result.group(1))), int(result.group(2))

    @staticmethod
    def left_time_key_larger(left_time_key, right_time_key):
        time_key_regex = r"^(\d*)_(\d*)$"
        left_result = re.search(time_key_regex, left_time_key)
        right_result = re.search(time_key_regex, right_time_key)
        if left_result is not None and right_result is not None:
            left_month = int(left_result.group(1))
            left_year = int(left_result.group(2))
            right_month = int(right_result.group(1))
            right_year = int(right_result.group(2))
            if left_year == right_year:
                if left_month > right_month:
                    return True
                else:
                    return False
            elif left_year > right_year:
                return True
            else:
                return False
