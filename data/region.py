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
        self.exits = []
        self.province = ""
        self.race = ""
        self.population = -1
        self.tax = -1
        self.wages = -1
        self.total_wages = -1
        self.entertainment = -1

        # TODO: forSale, products and units.
        #      forSale and products need itemRepository
        #      units need unitRepository

    def get_key(self):
        return self.get_key_from_coordinates(self.coords[0], self.coords[1], self.coords[2])

    @staticmethod
    def get_key_from_coordinates(x: int, y: int, z: int):
        return f'{x}_{y}_{z}'

    def add_region_report(self, faction_number, time_key, report_data):
        report_dict_key = f'{faction_number}_{time_key}'
        self.reports[report_dict_key] = report_data

    def merge(self, region, overwrite=True):
        if self.coords != region.coords:
            return False

        if self.region_type != region.region_type and overwrite:
            self.region_type = region.region_type

        if (len(self.exits) > 0 and overwrite) or len(self.exits) == 0:
            if len(region.exits) > 0:
                self.exits = region.exits

        if (self.province != "" and overwrite) or self.province == "":
            if region.province != "":
                self.province = region.province

        if (self.race != "" and overwrite) or self.race == "":
            if region.race != "":
                self.race = region.race

        if (self.population != -1 and overwrite) or self.population == -1:
            if region.population != -1:
                self.population = region.population

        if (self.tax != -1 and overwrite) or self.tax == -1:
            if region.tax != -1:
                self.tax = region.tax

        if (self.wages != -1 and overwrite) or self.wages == -1:
            if region.wages != -1:
                self.wages = region.wages

        if (self.total_wages != -1 and overwrite) or self.total_wages == -1:
            if region.total_wages != -1:
                self.total_wages = region.total_wages

        if (self.entertainment != -1 and overwrite) or self.entertainment == -1:
            if region.entertainment != -1:
                self.entertainment = region.entertainment

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

    @staticmethod
    def create_region_from_report_data(faction_number, time_key, region_report_data):
        if 'location' in region_report_data.keys():
            coords = region_report_data['location']
            if len(coords) == 2:
                coord_z = 1
            else:
                coord_z = int(coords[2])
            coord_x = int(coords[0])
            coord_y = int(coords[1])
        else:
            # TODO: log error can not create region
            return None
        if StaticHelper.REPORT_REGION_TERRAIN_TOKEN in region_report_data.keys():
            terrain = region_report_data[StaticHelper.REPORT_REGION_TERRAIN_TOKEN]
        else:
            # TODO: log error can not create region
            return None
        region = Region(coord_x, coord_y, coord_z, terrain)
        region.add_region_report(faction_number, time_key, region_report_data)

        if 'exits' in region_report_data.keys():
            for region_exit in region_report_data['exits'].keys():
                if region_exit not in region.exits:
                    region.exits.append(region_exit)

        if 'province' in region_report_data.keys():
            region.province = region_report_data['province']

        if 'race' in region_report_data.keys():
            region.race = region_report_data['race']

        if 'population' in region_report_data.keys():
            region.population = int(region_report_data['population'])

        if 'tax' in region_report_data.keys():
            region.tax = int(region_report_data['tax'])

        if 'wages' in region_report_data.keys():
            region.wages = int(region_report_data['wages'])

        if 'totalWages' in region_report_data.keys():
            region.total_wages = int(region_report_data['totalWages'])

        if 'entertainment' in region_report_data.keys():
            region.entertainment = int(region_report_data['entertainment'])

        return region
