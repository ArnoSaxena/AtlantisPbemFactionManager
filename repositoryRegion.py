from data.region import Region
from month import Month

REPORT_REGIONS_TOKEN = 'regions'
REPORT_REGION_TERRAIN_TOKEN = 'terrain'


class RepositoryRegion:
    def __init__(self):
        self.regions = {}

    def add_region(self, region: Region) -> bool:
        if region.get_key() not in self.regions.keys():
            self.regions[region.get_key()] = region
            return True
        return False

    def get_region(self, x, y, z) -> Region:
        return self.get_region_by_key(Region.get_key_from_coordinates(x, y, z))

    def get_region_by_key(self, region_key):
        if region_key in self.regions.keys():
            return self.regions[region_key]
        else:
            return None

    def load_regions_from_report_data(self, report_data):
        try:
            faction_number = int(report_data['faction']['number'])
        except KeyError:
            return False

        try:
            report_month_name = report_data['date']['month']
            report_month_enum = Month[report_month_name.strip()]
            report_year = int(report_data['date']['year'])
            time_key = Month.get_time_key(report_month_enum, report_year)
        except KeyError:
            return False

        if REPORT_REGIONS_TOKEN in report_data.keys():
            province_reports = report_data[REPORT_REGIONS_TOKEN]
            province_added = False
            for province_report in province_reports:
                if 'location' in province_report.keys():
                    coords = province_report['location']
                    if len(coords) == 2:
                        coord_z = 1
                    else:
                        coord_z = int(coords[2])
                    coord_x = int(coords[0])
                    coord_y = int(coords[1])
                else:
                    # TODO: log error can not create region
                    continue
                if REPORT_REGION_TERRAIN_TOKEN in province_report.keys():
                    terrain = province_report[REPORT_REGION_TERRAIN_TOKEN]
                else:
                    # TODO: log error can not create region
                    continue
                region = Region(coord_x, coord_y, coord_z, terrain)
                region.add_region_report(faction_number, time_key, province_report)
                self.add_region(region)
                stored_region = self.get_region(coord_x, coord_y, coord_z)
                stored_region.merge_reports(region)
                province_added = True

            return True if province_added else False
        else:
            return False
