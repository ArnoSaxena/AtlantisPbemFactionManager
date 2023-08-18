from month import Month
from staticHelper import StaticHelper


class Region:
    def __init__(
            self,
            coord_x: int,
            coord_y: int,
            coord_z: int,
            region_type: str):
        self.coords = (coord_x, coord_y, coord_z)
        self.region_type = region_type
        self.reports = {}
        self.province_hexagon = None

    def get_key(self):
        return self.get_key_from_coordinates(self.coords[0], self.coords[1], self.coords[2])

    @staticmethod
    def get_key_from_coordinates(x: int, y: int, z: int):
        return f'{x}_{y}_{z}'

    def add_region_report(self, faction_number, time_key, report_data):
        report_dict_key = f'{faction_number}_{time_key}'
        self.reports[report_dict_key] = report_data

    def merge_reports(self, region):
        for new_report_key in region.reports.keys():
            if new_report_key not in self.reports.keys():
                self.reports[new_report_key] = region.reports[new_report_key]

    def get_report_keys(self, faction_number=-1):
        report_keys = {}
        for key in self.reports.keys():
            if -1 != faction_number:
                current_faction_number = int(self.reports[key]['faction']['number'])
                if faction_number != current_faction_number:
                    continue
            report_keys.add(key)
        return

    def get_latest_report(self, faction_number=-1):
        time_key = None
        latest_report = None
        for report_key in self.reports.keys():
            key_data = report_key.split('_')
            current_faction_number = int(key_data[0])
            current_report_month = int(key_data[1])
            current_report_year = int(key_data[2])
            if -1 != faction_number:
                if faction_number != current_faction_number:
                    continue
            current_time_key = f'{current_report_month}_{current_report_year}'
            if Month.left_time_key_younger(current_time_key, time_key):
                time_key = current_time_key
                latest_report = self.reports[report_key]
        return latest_report
