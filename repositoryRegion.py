import json

from data.region import Region
from data.regionExit import RegionExit
from month import Month
from staticHelper import StaticHelper


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

    def get_all_known_provinces(self):
        all_known_provinces = []
        for region in self.regions:
            if region.province not in all_known_provinces:
                all_known_provinces.append(region.province)
        return all_known_provinces

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

        if StaticHelper.REPORT_REGIONS_TOKEN in report_data.keys():
            region_reports = report_data[StaticHelper.REPORT_REGIONS_TOKEN]
            any_region_added = False
            for region_report_data in region_reports:
                region = Region.create_region_from_report_data(faction_number, time_key, region_report_data)
                if region is None:
                    continue

                self.add_region(region)
                stored_region = self.get_region(region.coords[0], region.coords[1], region.coords[2])
                stored_region.merge(region)
                any_region_added = True

            return True if any_region_added else False
        else:
            return False

    def get_json_dump(self):
        json_regions = json.dumps({key: obj.__dict__ for (key, obj) in self.regions.items()}, indent=2)
        return json_regions

    def initialise_from_json(self, json_regions):
        self.initialise_from_regions_dicts(json.loads(json_regions))

    def initialise_from_regions_dicts(self, regions_dicts):
        self.regions = {}
        for region_key, regions_dict in regions_dicts.items():
            region = Region(
                int(regions_dict['coords'][0]),
                int(regions_dict['coords'][1]),
                int(regions_dict['coords'][2]),
                regions_dict['region_type'])
            if len(regions_dict['reports']) > 0:
                for report_id, report in regions_dict['reports'].items():
                    region.reports[report_id] = report
            self.regions[region_key] = region
