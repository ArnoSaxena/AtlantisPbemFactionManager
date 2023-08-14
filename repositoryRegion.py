from AtlantisManagerApp import REPORT_REGIONS_TOKEN, REPORT_REGION_TERRAIN_TOKEN
from data.region import Region


class RepositoryRegion:
    def __init__(self):
        self.regions = {}

    def add_region(self, region: Region) -> bool:
        if region.get_key() not in self.regions.keys():
            self.regions[region.get_key()] = region
            return True
        return False

    def get_region(self, x, y, z) -> Region:
        region_key = Region.get_key(x, y, z)
        if region_key in self.regions.keys():
            return self.regions[region_key]
        else:
            return None

    def load_regions_from_report_data(self, report_data):
        if REPORT_REGIONS_TOKEN in report_data.keys():
            province_reports = report_data[REPORT_REGIONS_TOKEN]
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
                region.add_report(province_report)
                self.add_region(region)
                stored_region = self.get_region(coord_x, coord_y, coord_z)
                stored_region.merge_reports(region)
