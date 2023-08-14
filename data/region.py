from month import Month


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

    def get_key(self):
        return self.get_key_from_coordinates(self.coords[0], self.coords[1], self.coords[2])

    @staticmethod
    def get_key_from_coordinates(x: int, y: int, z: int):
        return f'{x}_{y}_{z}'

    def add_report(self, report_data):
        faction_number = int(report_data['faction']['number'])
        report_month_name = report_data['date']['month']
        report_month_enum = Month[report_month_name.strip()]
        report_year = int(report_data['date']['year'])
        time_key = Month.get_time_key(report_month_enum, report_year)
        report_dict_key = f'{faction_number}_{time_key}'
        self.reports[report_dict_key] = report_data

    def merge_reports(self, region):
        for new_report_key in region.reports.keys():
            if new_report_key not in self.reports.keys():
                self.reports[new_report_key] = region.reports[new_report_key]
